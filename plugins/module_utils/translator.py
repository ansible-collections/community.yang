# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import glob
import os
import re
import sys
import shutil
import time
import json
import uuid

from copy import deepcopy

from ansible.module_utils.basic import missing_required_lib
from ansible.module_utils._text import to_text
from ansible.module_utils.six import StringIO

from ansible_collections.community.yang.plugins.module_utils.common import (
    load_from_source,
    find_file_in_path,
    find_share_path,
    to_list,
)

try:
    import pyang  # noqa

    HAS_PYANG = True
except ImportError:
    HAS_PYANG = False

try:
    from lxml import etree

    HAS_LXML = True
except ImportError:
    HAS_LXML = False


class Translator(object):
    def __init__(
        self,
        yang_files,
        search_path=None,
        doctype="config",
        keep_tmp_files=False,
        debug=None,
    ):
        yang_files = to_list(yang_files) if yang_files else []
        self._yang_files = []
        self._doctype = doctype
        self._keep_tmp_files = keep_tmp_files
        self._debug = debug
        self._handle_yang_file_path(yang_files)
        self._handle_search_path(search_path)
        self._set_pyang_executables()

    def _handle_yang_file_path(self, yang_files):
        for yang_file in yang_files:
            yang_file = os.path.realpath(os.path.expanduser(yang_file))
            if not os.path.isfile(yang_file):
                # Maybe we are passing a glob?
                _yang_files = glob.glob(yang_file)
                if not _yang_files:
                    # Glob returned no files
                    raise ValueError("%s invalid file path" % yang_file)
                self._yang_files.extend(_yang_files)
            else:
                self._yang_files.append(yang_file)

        # glob.glob returns the files unordered when doing wildcard
        # sort to fix some dependency issues
        self._yang_files.sort()

        # ensure file path entry is unique
        self._yang_files = list(set(self._yang_files))

    def _handle_search_path(self, search_path):
        if search_path is None:
            search_path = os.path.dirname(self._yang_files[0])

        abs_search_path = None
        for path in search_path.split(":"):
            path = os.path.realpath(os.path.expanduser(path))
            if abs_search_path is None:
                abs_search_path = path
            else:
                abs_search_path += ":" + path
            if path != "" and not os.path.isdir(path):
                raise ValueError("%s is invalid directory path" % path)

        self._search_path = abs_search_path

    def _set_pyang_executables(self):
        if not HAS_PYANG:
            raise ValueError(missing_required_lib("pyang"))
        if not HAS_LXML:
            raise ValueError(missing_required_lib("lxml"))
        base_pyang_path = sys.modules["pyang"].__file__
        self._pyang_exec_path = find_file_in_path("pyang")
        self._pyang_module = load_from_source(self._pyang_exec_path, "pyang")
        sys.modules["pyang"].__file__ = base_pyang_path

    def json_to_xml(self, json_data, tmp_dir_path):
        """
        The method translates JSON data encoded as per YANG model (RFC 7951)
        to XML payload
        :param json_data: JSON data that should to translated to XML
        :param tmp_dir_path: Temporary directory path to copy intermediate files
        :return: XML data in string format.
        """
        saved_arg = deepcopy(sys.argv)
        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        sys.stdout = sys.stderr = StringIO()

        if isinstance(json_data, dict):
            # input is in json format, copy it to file in temporary location
            json_file_path = os.path.join(
                tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "json")
            )
            json_file_path = os.path.realpath(
                os.path.expanduser(json_file_path)
            )
            with open(json_file_path, "w") as f:
                f.write(json.dumps(json_data))
            json_file_path = os.path.realpath(
                os.path.expanduser(json_file_path)
            )

        elif os.path.isfile(json_data):
            json_file_path = json_data
        else:
            raise ValueError(
                "unable to create/find temporary json file %s" % json_data
            )

        try:
            # validate json
            with open(json_file_path) as fp:
                json.load(fp)
        except Exception as exc:
            raise ValueError(
                "Failed to load json configuration: %s"
                % (to_text(exc, errors="surrogate_or_strict"))
            )
        jtox_file_path = os.path.join(
            tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "jtox")
        )
        xml_file_path = os.path.join(
            tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "xml")
        )
        jtox_file_path = os.path.realpath(os.path.expanduser(jtox_file_path))
        xml_file_path = os.path.realpath(os.path.expanduser(xml_file_path))

        yang_metada_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "files/yang"
        )
        yang_metadata_path = os.path.join(yang_metada_dir, "nc-op.yang")
        self._search_path += ":%s" % yang_metada_dir

        # fill in the sys args before invoking pyang
        sys.argv = (
            [
                self._pyang_exec_path,
                "-f",
                "jtox",
                "-o",
                jtox_file_path,
                "-p",
                self._search_path,
                "--lax-quote-checks",
            ]
            + self._yang_files
            + [yang_metadata_path]
        )
        if self._debug:
            self._debug(
                "Generating jtox file '%s' by executing command '%s'"
                % (jtox_file_path, " ".join(sys.argv))
            )
        try:
            self._pyang_module.run()
        except SystemExit:
            pass
        except Exception as e:
            shutil.rmtree(
                os.path.realpath(os.path.expanduser(tmp_dir_path)),
                ignore_errors=True,
            )
            raise ValueError(
                "Error while generating intermediate (jtox) file: %s" % e
            )
        finally:
            err = sys.stderr.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(os.path.expanduser(tmp_dir_path)),
                        ignore_errors=True,
                    )
                raise ValueError(
                    "Error while generating intermediate (jtox) file: %s" % err
                )

        json2xml_exec_path = find_file_in_path("json2xml")
        json2xml_module = load_from_source(json2xml_exec_path, "json2xml")

        # fill in the sys args before invoking json2xml
        sys.argv = [
            json2xml_exec_path,
            "-t",
            self._doctype,
            "-o",
            xml_file_path,
            jtox_file_path,
            json_file_path,
        ]

        if self._debug:
            self._debug(
                "Generating xml file '%s' by executing command '%s'"
                % (xml_file_path, " ".join(sys.argv))
            )
        try:
            json2xml_module.main()
            with open(xml_file_path, "r+") as fp:
                b_content = fp.read()
                content = to_text(b_content, errors="surrogate_or_strict")
        except UnicodeError as uni_error:
            raise ValueError(
                "Error while translating to text: %s" % str(uni_error)
            )
        except SystemExit:
            pass
        finally:
            err = sys.stderr.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(os.path.expanduser(tmp_dir_path)),
                        ignore_errors=True,
                    )
                raise ValueError("Error while translating to xml: %s" % err)
            sys.argv = saved_arg
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

        try:
            content = re.sub(r"<\? ?xml .*\? ?>", "", content)
            root = etree.fromstring(content)
        except Exception as e:
            raise ValueError("Error while reading xml document: %s" % e)
        finally:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(tmp_dir_path)),
                    ignore_errors=True,
                )

        return etree.tostring(root).decode("utf-8")

    def xml_to_json(self, xml_data, tmp_dir_path):
        """
        The method translates XML data to JSON data encoded as per YANG model (RFC 7951)
        :param xml_data: XML data or file path containing xml data that should to translated to JSON
        :param tmp_dir_path: Temporary directory path to copy intermediate files
        :return: data in JSON format.
    """

        try:
            etree.fromstring(xml_data)
            # input is xml string, copy it to file in temporary location
            xml_file_path = os.path.join(
                tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "xml")
            )
            xml_file_path = os.path.realpath(os.path.expanduser(xml_file_path))
            with open(xml_file_path, "w") as f:
                if not xml_data.startswith("<?xml version"):
                    xml_data = (
                        '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_data
                    )
                data = xml_data
                f.write(data)
        except etree.XMLSyntaxError:
            if os.path.isfile(xml_data):
                # input is xml file path
                xml_file_path = os.path.realpath(os.path.expanduser(xml_data))
            else:
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(os.path.expanduser(tmp_dir_path)),
                        ignore_errors=True,
                    )
                raise ValueError(
                    "Unable to create file or read XML data %s" % xml_data
                )

        xml_file_path = os.path.realpath(os.path.expanduser(xml_file_path))

        if os.path.isfile(xml_data):
            try:
                # validate xml
                etree.parse(xml_file_path)
                if self._debug:
                    self._debug(
                        "Parsing xml data from temporary file: %s"
                        % xml_file_path
                    )
            except Exception as exc:
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(os.path.expanduser(tmp_dir_path)),
                        ignore_errors=True,
                    )
                raise ValueError(
                    "Failed to load xml data: %s"
                    % (to_text(exc, errors="surrogate_or_strict"))
                )

        base_pyang_path = sys.modules["pyang"].__file__
        pyang_exec_path = find_file_in_path("pyang")

        saved_arg = deepcopy(sys.argv)
        sys.modules["pyang"].__file__ = base_pyang_path

        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        sys.stdout = sys.stderr = StringIO()

        jsonxsl_relative_dirpath = os.path.join("yang", "xslt")
        jsonxsl_dir_path = find_share_path(
            os.path.join(jsonxsl_relative_dirpath, "jsonxsl-templates.xsl")
        )
        if jsonxsl_dir_path is None:
            raise ValueError(
                "Could not find jsonxsl-templates.xsl in environment path"
            )
        os.environ["PYANG_XSLT_DIR"] = os.path.join(
            jsonxsl_dir_path, jsonxsl_relative_dirpath
        )

        xsl_file_path = os.path.join(
            tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "xsl")
        )
        json_file_path = os.path.join(
            tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "json")
        )
        xls_file_path = os.path.realpath(os.path.expanduser(xsl_file_path))
        json_file_path = os.path.realpath(os.path.expanduser(json_file_path))

        # fill in the sys args before invoking pyang
        sys.argv = [
            pyang_exec_path,
            "-f",
            "jsonxsl",
            "-o",
            xls_file_path,
            "-p",
            self._search_path,
            "--lax-quote-checks",
        ] + self._yang_files

        if self._debug:
            self._debug(
                "Generating xsl file '%s' by executing command '%s'"
                % (xls_file_path, " ".join(sys.argv))
            )
        try:
            self._pyang_module.run()
        except SystemExit:
            pass
        except Exception as e:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(tmp_dir_path)),
                    ignore_errors=True,
                )
            raise ValueError(
                "Error while generating intermediate (xsl) file: %s" % e
            )
        finally:
            err = sys.stderr.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(os.path.expanduser(tmp_dir_path)),
                        ignore_errors=True,
                    )
                raise ValueError(
                    "Error while generating (xsl) intermediate file: %s" % err
                )

        xsltproc_exec_path = find_file_in_path("xsltproc")
        if not xsltproc_exec_path:
            raise ValueError(
                "xsltproc executable not found."
                " Install 'libxml2-dev' and 'libxslt-dev' packages"
            )

        # fill in the sys args before invoking xsltproc
        sys.argv = [
            xsltproc_exec_path,
            "-o",
            json_file_path,
            xsl_file_path,
            xml_file_path,
        ]

        if self._debug:
            self._debug(
                "Generating json data in temp file '%s' by executing command '%s'"
                % (json_file_path, " ".join(sys.argv))
            )
        time.sleep(5)

        try:
            os.system(" ".join(sys.argv))
        except SystemExit:
            pass
        finally:
            err = sys.stderr.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(os.path.expanduser(tmp_dir_path)),
                        ignore_errors=True,
                    )
                raise ValueError("Error while translating to json: %s" % err)
            sys.argv = saved_arg
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

        try:
            if self._debug:
                self._debug(
                    "Reading output json data from temporary file: %s"
                    % json_file_path
                )
            with open(json_file_path, "r") as fp:
                raw_content = fp.read()
                content = json.loads(raw_content)
        except Exception as e:
            raise ValueError(
                "Error while reading json document %s from path %s"
                % (e, json_file_path)
            )
        finally:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(tmp_dir_path)),
                    ignore_errors=True,
                )
        return content
