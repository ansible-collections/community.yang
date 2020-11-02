# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import glob
import os
import sys
import shutil
import json
import uuid
import errno

import subprocess
from copy import deepcopy

from ansible.module_utils.six import StringIO
from ansible.module_utils.basic import missing_required_lib

from ansible_collections.community.yang.plugins.module_utils.common import (
    find_file_in_path,
    to_list,
)

try:
    from pyang import error  # noqa: F401

    HAS_PYANG = True
except ImportError:
    HAS_PYANG = False

YANG_SPEC_DIR_PATH = "~/.ansible/tmp/yang/spec"


class GenerateSpec(object):
    def __init__(
        self,
        yang_content=None,
        yang_file_path=None,
        search_path=None,
        doctype="config",
        keep_tmp_files=False,
        tmp_dir_path=YANG_SPEC_DIR_PATH,
    ):
        if not HAS_PYANG:
            raise ImportError(missing_required_lib("pyang"))

        yang_file_path = to_list(yang_file_path) if yang_file_path else []
        self._yang_file_path = []
        self._yang_content = yang_content
        self._doctype = doctype
        self._keep_tmp_files = keep_tmp_files
        self._pyang_exec_path = find_file_in_path("pyang")

        self._tmp_dir_path = tmp_dir_path

        self._handle_yang_file_path(yang_file_path)
        self._handle_search_path(search_path)

    def __del__(self):
        if not self._keep_tmp_files:
            shutil.rmtree(self._tmp_dir_path, ignore_errors=True)
        super(GenerateSpec, self).__del__()

    def _handle_yang_file_path(self, yang_files):
        if not yang_files:
            content_tmp_file_path = os.path.join(
                self._tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "yang")
            )
            content_tmp_file_path = os.path.realpath(
                os.path.expanduser(content_tmp_file_path)
            )
            with open(content_tmp_file_path, "w") as opened_file:
                opened_file.write(self._yang_content)
            self._yang_file_path.append(content_tmp_file_path)
        else:
            for yang_file in yang_files:
                yang_file = os.path.realpath(os.path.expanduser(yang_file))
                if not os.path.isfile(yang_file):
                    # Maybe we are passing a glob?
                    _yang_files = glob.glob(yang_file)
                    if not _yang_files:
                        # Glob returned no files
                        raise ValueError("%s invalid file path" % yang_file)
                    self._yang_file_path.extend(_yang_files)
                else:
                    self._yang_file_path.append(yang_file)
        # ensure file path entry is unique
        self._yang_file_path = list(set(self._yang_file_path))

    def _handle_search_path(self, search_path):
        if search_path is None:
            search_path = os.path.dirname(self._yang_file_path[0])

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

    def generate_tree_schema(self, schema_out_path=None):
        """
        This method generates tree schema by parsing the yang file and stores
        the content of tree schema into a file (optional)
        :param schema_out_path: This option provide the file path to
                                store the generated.
        :param defaults: If set to True the default values will be added in json schema
                         from the YANG model for the corresponding option.
        :param annotations: The boolean flag identifies if the xml skeleton should have
                            comments describing the field or not.
        :return: YANG tree in string format.
        """
        saved_arg = deepcopy(sys.argv)
        sys.stdout = sys.stderr = StringIO()

        tree_tmp_file_path = os.path.join(
            self._tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "txt")
        )
        tree_tmp_file_path = os.path.realpath(
            os.path.expanduser(tree_tmp_file_path)
        )
        # fill in the sys args before invoking pyang to retrieve tree structure
        tree_cmd = [
            self._pyang_exec_path,
            "-f",
            "tree",
            "-o",
            tree_tmp_file_path,
            "-p",
            self._search_path,
            "--lax-quote-checks",
        ] + self._yang_file_path

        try:
            subprocess.check_output(
                " ".join(tree_cmd), stderr=subprocess.STDOUT, shell=True
            )
        except SystemExit:
            pass
        except Exception as e:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(self._tmp_dir_path)),
                    ignore_errors=True,
                )
            raise ValueError(
                "Error while generating skeleton xml file: %s" % e.output
            )
        finally:
            err = sys.stdout.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(
                            os.path.expanduser(self._tmp_dir_path)
                        ),
                        ignore_errors=True,
                    )
                raise ValueError("Error while generating tree file: %s" % err)

        sys.stdout.flush()
        sys.stderr.flush()
        sys.argv = saved_arg

        with open(tree_tmp_file_path, "r") as f:
            tree_schema = f.read()

        if schema_out_path:
            try:
                shutil.copy(tree_tmp_file_path, schema_out_path)
            except IOError as e:
                # ENOENT(2): file does not exist, raised also on missing dest parent dir
                if e.errno != errno.ENOENT:
                    raise
                # try creating parent directories
                os.makedirs(os.path.dirname(schema_out_path))
                shutil.copyfile(tree_tmp_file_path, schema_out_path)

        if not self._keep_tmp_files:
            os.remove(tree_tmp_file_path)

        return tree_schema

    def generate_xml_schema(
        self, schema_out_path=None, defaults=False, annotations=False
    ):
        """
        This method generates XML schema by parsing the yang file and stores
        the content of XML schema into a file (optional)
        :param schema_out_path: This option provide the file path to
                                store the generated.
        :param defaults: If set to True the default values will be added in XML schema
                         from the YANG model for the corresponding option.
        :param annotations: The boolean flag identifies if the XML skeleton should have
                            comments describing the field or not.
        :return: XML scehma in string format.
        """
        saved_arg = deepcopy(sys.argv)
        sys.stdout = sys.stderr = StringIO()

        xml_tmp_file_path = os.path.join(
            self._tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "xml")
        )
        xml_tmp_file_path = os.path.realpath(
            os.path.expanduser(xml_tmp_file_path)
        )
        # fill in the sys args before invoking pyang to retrieve xml skeleton
        sample_xml_skeleton_cmd = [
            self._pyang_exec_path,
            "-f",
            "sample-xml-skeleton",
            "-o",
            xml_tmp_file_path,
            "-p",
            self._search_path,
            "--sample-xml-skeleton-doctype",
            self._doctype,
            "--lax-quote-checks",
        ] + self._yang_file_path

        if defaults:
            sample_xml_skeleton_cmd.append("--sample-xml-skeleton-defaults")

        if annotations:
            sample_xml_skeleton_cmd.append("--sample-xml-skeleton-annotations")

        try:
            subprocess.check_output(
                " ".join(sample_xml_skeleton_cmd),
                stderr=subprocess.STDOUT,
                shell=True,
            )
        except SystemExit:
            pass
        except Exception as e:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(self._tmp_dir_path)),
                    ignore_errors=True,
                )
            raise ValueError(
                "Error while generating skeleton xml file: %s" % e.output
            )
        finally:
            err = sys.stdout.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(
                            os.path.expanduser(self._tmp_dir_path)
                        ),
                        ignore_errors=True,
                    )
                raise ValueError(
                    "Error while generating skeleton xml file: %s" % err
                )

        sys.stdout.flush()
        sys.stderr.flush()

        sys.argv = saved_arg

        with open(xml_tmp_file_path, "r") as f:
            xml_schema = f.read()

        if schema_out_path:
            try:
                shutil.copy(xml_tmp_file_path, schema_out_path)
            except IOError as e:
                # ENOENT(2): file does not exist, raised also on missing dest parent dir
                if e.errno != errno.ENOENT:
                    raise
                # try creating parent directories
                os.makedirs(os.path.dirname(schema_out_path))
                shutil.copyfile(xml_tmp_file_path, schema_out_path)

        if not self._keep_tmp_files:
            os.remove(xml_tmp_file_path)

        return xml_schema

    def generate_json_schema(self, schema_out_path=None, defaults=False):
        """
        This method generates json schema by parsing the yang file and stores
        the content of json schema into a file (optional)
        :param schema_out_path: This option provide the file path to
                                store the generated.
        :param defaults: If set to True the default values will be added in json schema
                         from the YANG model for the corresponding option.
        :return: JSON schema in string format.
        """
        saved_arg = deepcopy(sys.argv)
        sys.stdout = sys.stderr = StringIO()

        json_tmp_file_path = os.path.join(
            self._tmp_dir_path, "%s.%s" % (str(uuid.uuid4()), "json")
        )
        json_tmp_file_path = os.path.realpath(
            os.path.expanduser(json_tmp_file_path)
        )

        plugin_file_src = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "../pyang/plugins/json_skeleton_plugin.py",
        )
        shutil.copy(plugin_file_src, self._tmp_dir_path)
        # fill in the sys args before invoking pyang to retrieve json skeleton
        sample_json_skeleton_cmd = [
            self._pyang_exec_path,
            "--plugindir",
            self._tmp_dir_path,
            "-f",
            "sample-json-skeleton",
            "-o",
            json_tmp_file_path,
            "-p",
            self._search_path,
            "--lax-quote-checks",
            "--sample-json-skeleton-doctype",
            self._doctype,
        ] + self._yang_file_path

        if defaults:
            sample_json_skeleton_cmd.append("--sample-json-skeleton-defaults")

        try:
            subprocess.check_output(
                " ".join(sample_json_skeleton_cmd),
                stderr=subprocess.STDOUT,
                shell=True,
            )
        except SystemExit:
            pass
        except Exception as e:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(self._tmp_dir_path)),
                    ignore_errors=True,
                )
            raise ValueError(
                "Error while generating skeleton json file: %s" % e.output
            )
        finally:
            err = sys.stdout.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(
                            os.path.expanduser(self._tmp_dir_path)
                        ),
                        ignore_errors=True,
                    )
                raise ValueError(
                    "Error while generating json schema: %s" % err
                )

        sys.stdout.flush()
        sys.stderr.flush()

        sys.argv = saved_arg

        with open(json_tmp_file_path, "r") as f:
            json_schema = json.load(f)

        if schema_out_path:
            try:
                shutil.copy(json_tmp_file_path, schema_out_path)
            except IOError as e:
                # ENOENT(2): file does not exist, raised also on missing dest parent dir
                if e.errno != errno.ENOENT:
                    raise
                # try creating parent directories
                os.makedirs(os.path.dirname(schema_out_path))
                shutil.copyfile(json_tmp_file_path, schema_out_path)

        if not self._keep_tmp_files:
            os.remove(json_tmp_file_path)

        return json_schema
