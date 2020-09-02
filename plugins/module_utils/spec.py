# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys
import shutil
import json
import uuid
import errno

import subprocess
from copy import deepcopy

from ansible.module_utils.six import StringIO
from ansible.utils.path import unfrackpath, makedirs_safe
from ansible.errors import AnsibleError
from ansible.utils.display import Display

from ansible_collections.community.yang.plugins.module_utils.common import (
    find_file_in_path,
)

display = Display()

try:
    from pyang import error  # noqa: F401
except ImportError:
    raise AnsibleError("pyang is not installed")

YANG_SPEC_DIR_PATH = "~/.ansible/tmp/yang/spec"


class GenerateSpec(object):
    def __init__(
        self,
        yang_file_path,
        search_path=None,
        doctype="config",
        keep_tmp_files=False,
        xml_schema=None,
        json_schema=None,
        tree_schema=None
    ):
        self._yang_file_path = yang_file_path
        self._doctype = doctype
        self._keep_tmp_files = keep_tmp_files
        self._pyang_exec_path = find_file_in_path("pyang")
        self.xml_schema = xml_schema,
        self.json_schema = json_schema,
        self.tree_schema = tree_schema,


        self._plugindir = unfrackpath(YANG_SPEC_DIR_PATH)
        makedirs_safe(self._plugindir)

        if search_path is None:
            search_path = os.path.dirname(yang_file_path)

        self._search_path = search_path

    def __del__(self):
        if not self._keep_tmp_files:
            shutil.rmtree(self._plugindir, ignore_errors=True)
        super(GenerateSpec, self).__del__()

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
            YANG_SPEC_DIR_PATH, "%s.%s" % (str(uuid.uuid4()), "txt")
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
            self._yang_file_path,
            "-p",
            self._search_path,
            "--lax-quote-checks",
        ]

        try:
            subprocess.check_output(
                " ".join(tree_cmd), stderr=subprocess.STDOUT, shell=True
            )
        except SystemExit:
            pass
        except Exception as e:
            if not self._keep_tmp_files:
                shutil.rmtree(
                    os.path.realpath(os.path.expanduser(YANG_SPEC_DIR_PATH)),
                    ignore_errors=True,
                )
            raise AnsibleError(
                "Error while generating skeleton xml file: %s" % e.output
            )
        finally:
            err = sys.stdout.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(
                            os.path.expanduser(YANG_SPEC_DIR_PATH)
                        ),
                        ignore_errors=True,
                    )
                raise AnsibleError(
                    "Error while generating tree file: %s" % err
                )

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
            YANG_SPEC_DIR_PATH, "%s.%s" % (str(uuid.uuid4()), "xml")
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
            self._yang_file_path,
            "-p",
            self._search_path,
            "--sample-xml-skeleton-doctype",
            self._doctype,
            "--lax-quote-checks",
        ]

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
                    os.path.realpath(os.path.expanduser(YANG_SPEC_DIR_PATH)),
                    ignore_errors=True,
                )
            raise AnsibleError(
                "Error while generating skeleton xml file: %s" % e.output
            )
        finally:
            err = sys.stdout.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(
                            os.path.expanduser(YANG_SPEC_DIR_PATH)
                        ),
                        ignore_errors=True,
                    )
                raise AnsibleError(
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
        :return: JSON scehma in string format.
        """
        saved_arg = deepcopy(sys.argv)
        sys.stdout = sys.stderr = StringIO()

        json_tmp_file_path = os.path.join(
            YANG_SPEC_DIR_PATH, "%s.%s" % (str(uuid.uuid4()), "json")
        )
        json_tmp_file_path = os.path.realpath(
            os.path.expanduser(json_tmp_file_path)
        )

        plugin_file_src = os.path.join(
            os.path.dirname(os.path.abspath(__file__)),
            "pyang_json_skeleton_plugin.py",
        )
        shutil.copy(plugin_file_src, self._plugindir)

        # fill in the sys args before invoking pyang to retrieve json skeleton
        sample_json_skeleton_cmd = [
            self._pyang_exec_path,
            "--plugindir",
            self._plugindir,
            "-f",
            "sample-json-skeleton",
            "-o",
            json_tmp_file_path,
            self._yang_file_path,
            "-p",
            self._search_path,
            "--lax-quote-checks",
            "--sample-json-skeleton-doctype",
            self._doctype,
        ]

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
                    os.path.realpath(os.path.expanduser(YANG_SPEC_DIR_PATH)),
                    ignore_errors=True,
                )
            raise AnsibleError(
                "Error while generating skeleton json file: %s" % e.output
            )
        finally:
            err = sys.stdout.getvalue()
            if err and "error" in err.lower():
                if not self._keep_tmp_files:
                    shutil.rmtree(
                        os.path.realpath(
                            os.path.expanduser(YANG_SPEC_DIR_PATH)
                        ),
                        ignore_errors=True,
                    )
                raise AnsibleError(
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
