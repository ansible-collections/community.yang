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
import imp
import uuid

from copy import deepcopy

from ansible.module_utils._text import to_text
from ansible.module_utils.six import StringIO
from ansible.utils.path import unfrackpath, makedirs_safe
from ansible.errors import AnsibleError
from ansible.utils.display import Display

from ansible_collections.community.yang.plugins.module_utils.common import (
    find_file_in_path,
)

display = Display()

try:
    import pyang  # noqa
except ImportError:
    raise AnsibleError("pyang is not installed")

try:
    from lxml import etree
except ImportError:
    raise AnsibleError("lxml is not installed")

JSON2XML_DIR_PATH = "~/.ansible/tmp/yang/json2xml"
XM2JSONL_DIR_PATH = "~/.ansible/tmp/xml2json"


class Translator(object):
    def __init__(
        self,
        yang_file,
        search_path=None,
        doctype="config",
        keep_tmp_files=False,
    ):
        self._doctype = doctype
        self._keep_tmp_files = keep_tmp_files
        self._handle_yang_file_path(yang_file)
        self._handle_search_path(search_path)
        self._set_pyang_executables()

    def _handle_yang_file_path(self, yang_file):
        yang_file = os.path.realpath(os.path.expanduser(yang_file))
        if not os.path.isfile(yang_file):
            # Maybe we are passing a glob?
            self._yang_files = glob.glob(yang_file)
            if not self._yang_files:
                # Glob returned no files
                raise AnsibleError("%s invalid file path" % yang_file)
        else:
            self._yang_files = [yang_file]

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
                raise AnsibleError("%s is invalid directory path" % path)

        self._search_path = abs_search_path

    def _set_pyang_executables(self):
        base_pyang_path = sys.modules["pyang"].__file__
        self._pyang_exec_path = find_file_in_path("pyang")
        self._pyang_exec = imp.load_source("pyang", self._pyang_exec_path)
        sys.modules["pyang"].__file__ = base_pyang_path

    def json_to_xml(self, json_data):
        """
        The method translates JSON data encoded as per YANG model (RFC 7951)
        to XML payload
        :param json_data: JSON data that should to translated to XML
        :return: XML data in string format.
        """
        saved_arg = deepcopy(sys.argv)
        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        sys.stdout = sys.stderr = StringIO()

        plugin_instance = str(uuid.uuid4())

        plugindir = unfrackpath(JSON2XML_DIR_PATH)
        makedirs_safe(plugindir)
        makedirs_safe(os.path.join(plugindir, plugin_instance))

        jtox_file_path = os.path.join(
            JSON2XML_DIR_PATH,
            plugin_instance,
            "%s.%s" % (str(uuid.uuid4()), "jtox"),
        )
        xml_file_path = os.path.join(
            JSON2XML_DIR_PATH,
            plugin_instance,
            "%s.%s" % (str(uuid.uuid4()), "xml"),
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

        try:
            self._pyang_exec.run()
        except SystemExit:
            pass
        except Exception as e:
            temp_dir = os.path.join(JSON2XML_DIR_PATH, plugin_instance)
            shutil.rmtree(
                os.path.realpath(os.path.expanduser(temp_dir)),
                ignore_errors=True,
            )
            raise AnsibleError(
                "Error while generating intermediate (jtox) file: %s" % e
            )
        finally:
            err = sys.stderr.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    temp_dir = os.path.join(JSON2XML_DIR_PATH, plugin_instance)
                    shutil.rmtree(
                        os.path.realpath(os.path.expanduser(temp_dir)),
                        ignore_errors=True,
                    )
                raise AnsibleError(
                    "Error while generating intermediate (jtox) file: %s" % err
                )

        json2xml_exec_path = find_file_in_path("json2xml")
        json2xml_exec = imp.load_source("json2xml", json2xml_exec_path)

        # fill in the sys args before invoking json2xml
        sys.argv = [
            json2xml_exec_path,
            "-t",
            self._doctype,
            "-o",
            xml_file_path,
            jtox_file_path,
            json_data,
        ]

        try:
            json2xml_exec.main()
            with open(xml_file_path, "r+") as fp:
                content = fp.read()

        except SystemExit:
            pass
        finally:
            err = sys.stderr.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    temp_dir = os.path.join(JSON2XML_DIR_PATH, plugin_instance)
                    shutil.rmtree(
                        os.path.realpath(os.path.expanduser(temp_dir)),
                        ignore_errors=True,
                    )
                raise AnsibleError("Error while translating to xml: %s" % err)
            sys.argv = saved_arg
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

        try:
            content = re.sub(r"<\? ?xml .*\? ?>", "", content)
            root = etree.fromstring(content)
        except Exception as e:
            raise AnsibleError("Error while reading xml document: %s" % e)
        finally:
            if not self._keep_tmp_files:
                temp_dir = os.path.join(JSON2XML_DIR_PATH, plugin_instance)
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(temp_dir)),
                    ignore_errors=True,
                )

        return etree.tostring(root)

    def xml_to_json(self, xml_data):
        """
        The method translates XML data to JSON data encoded as per YANG model (RFC 7951)
        :param xml_data: XML data or file path containing xml data that should to translated to JSON
        :return: data in JSON format.
    """
        plugindir = unfrackpath(XM2JSONL_DIR_PATH)
        makedirs_safe(plugindir)

        if os.path.isfile(xml_data):
            # input is xml file path
            xml_file_path = os.path.realpath(os.path.expanduser(xml_data))
        else:
            # input is xml string, copy it to file in temporary location
            xml_file_path = os.path.join(
                XM2JSONL_DIR_PATH, "%s.%s" % (str(uuid.uuid4()), "xml")
            )
            xml_file_path = os.path.realpath(os.path.expanduser(xml_file_path))
            with open(xml_file_path, "w") as f:
                if not xml_data.startswith("<?xml version"):
                    xml_data = (
                        '<?xml version="1.0" encoding="UTF-8"?>\n' + xml_data
                    )
                data = xml_data
                f.write(data)

        xml_file_path = os.path.realpath(os.path.expanduser(xml_file_path))

        try:
            # validate xml
            etree.parse(xml_file_path)
            display.vvvv(
                "Parsing xml data from temporary file: %s" % xml_file_path
            )
        except Exception as exc:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(XM2JSONL_DIR_PATH)),
                    ignore_errors=True,
                )
            raise AnsibleError(
                "Failed to load xml data: %s"
                % (to_text(exc, errors="surrogate_or_strict"))
            )

        base_pyang_path = sys.modules["pyang"].__file__
        pyang_exec_path = find_file_in_path("pyang")
        pyang_exec = imp.load_source("pyang", pyang_exec_path)

        saved_arg = deepcopy(sys.argv)
        sys.modules["pyang"].__file__ = base_pyang_path

        saved_stdout = sys.stdout
        saved_stderr = sys.stderr
        sys.stdout = sys.stderr = StringIO()

        xsl_file_path = os.path.join(
            XM2JSONL_DIR_PATH, "%s.%s" % (str(uuid.uuid4()), "xsl")
        )
        json_file_path = os.path.join(
            XM2JSONL_DIR_PATH, "%s.%s" % (str(uuid.uuid4()), "json")
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
        display.display(
            "Generating xsl file '%s' by executing command '%s'"
            % (xls_file_path, " ".join(sys.argv)),
            log_only=True,
        )
        try:
            pyang_exec.run()
        except SystemExit:
            pass
        except Exception as e:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(XM2JSONL_DIR_PATH)),
                    ignore_errors=True,
                )
            raise AnsibleError(
                "Error while generating intermediate (xsl) file: %s" % e
            )
        finally:
            err = sys.stderr.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(
                            os.path.expanduser(XM2JSONL_DIR_PATH)
                        ),
                        ignore_errors=True,
                    )
                raise AnsibleError(
                    "Error while generating (xsl) intermediate file: %s" % err
                )

        xsltproc_exec_path = find_file_in_path("xsltproc")

        # fill in the sys args before invoking xsltproc
        sys.argv = [
            xsltproc_exec_path,
            "-o",
            json_file_path,
            xsl_file_path,
            xml_file_path,
        ]
        display.display(
            "Generating json data in temp file '%s' by executing command '%s'"
            % (json_file_path, " ".join(sys.argv)),
            log_only=True,
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
                        os.path.realpath(
                            os.path.expanduser(XM2JSONL_DIR_PATH)
                        ),
                        ignore_errors=True,
                    )
                raise AnsibleError("Error while translating to json: %s" % err)
            sys.argv = saved_arg
            sys.stdout = saved_stdout
            sys.stderr = saved_stderr

        try:
            display.vvvv(
                "Reading output json data from temporary file: %s"
                % json_file_path
            )
            with open(json_file_path, "r") as fp:
                raw_content = fp.read()
                content = json.loads(raw_content)
        except Exception as e:
            raise AnsibleError(
                "Error while reading json document %s from path %s"
                % (e, json_file_path)
            )
        finally:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(XM2JSONL_DIR_PATH)),
                    ignore_errors=True,
                )
        return content
