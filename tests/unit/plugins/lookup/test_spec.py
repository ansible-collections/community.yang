# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import unittest

from ansible.errors import AnsibleLookupError
from ansible_collections.community.yang.plugins.lookup.spec import LookupModule

YANG_FILE_SEARCH_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "../../../fixtures/files"
)
OC_INTF_XML_CONFIG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../../../fixtures/config/openconfig/interface_oc_xml_valid.xml",
)
OC_INTF_YANG_FILE_PATH = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "../../../fixtures/files/openconfig/interfaces/openconfig-interfaces.yang",
)
LOOKUP_VARIABLES = {}


class TestValidate(unittest.TestCase):
    def setUp(self):
        self._lp = LookupModule()

    def test_invalid_argspec(self):
        """Check passing invalid argspec"""

        # invalid yang file value arguments
        kwargs = {}
        with self.assertRaises(AnsibleLookupError) as error:
            self._lp.run(["invalid path"], LOOKUP_VARIABLES, **kwargs)
        self.assertIn("path invalid file path", str(error.exception))

        # invalid search yang file value arguments
        kwargs = {"search_path": "invalid path"}
        with self.assertRaises(AnsibleLookupError) as error:
            self._lp.run([OC_INTF_YANG_FILE_PATH], LOOKUP_VARIABLES, **kwargs)
        self.assertIn("path is invalid directory path", str(error.exception))

        # invalid search yang file value arguments
        kwargs = {"search_path": YANG_FILE_SEARCH_PATH, "doctype": "invalid"}
        with self.assertRaises(AnsibleLookupError) as error:
            self._lp.run([OC_INTF_YANG_FILE_PATH], LOOKUP_VARIABLES, **kwargs)
        self.assertIn(
            "is invalid, valid value are config, data", str(error.exception)
        )

    def test_valid_spec_data(self):
        """Check passing valid data as per criteria"""

        terms = [OC_INTF_YANG_FILE_PATH]
        variables = {}
        kwargs = {
            "yang_file": OC_INTF_YANG_FILE_PATH,
            "search_path": YANG_FILE_SEARCH_PATH,
            "defaults": True,
            "annotations": True,
            "doctype": "config",
        }
        result = self._lp.run(terms, variables, **kwargs)
        # check json_skeleton data
        self.assertEqual(
            result[0]["json_skeleton"]["openconfig-interfaces:interfaces"][
                "interface"
            ][0]["name"],
            "",
        )
        self.assertEqual(
            result[0]["json_skeleton"]["openconfig-interfaces:interfaces"][
                "interface"
            ][0]["config"]["loopback-mode"],
            "False",
        )
        self.assertEqual(
            result[0]["json_skeleton"]["openconfig-interfaces:interfaces"][
                "interface"
            ][0]["config"]["enabled"],
            "True",
        )

        # check xml skeleton data
        self.assertIn(
            "<interface>\n      <!-- # keys: name-->\n      <!-- # entries: 0.. -->\n",
            result[0]["xml_skeleton"],
        )

        # check tree skeleton data
        self.assertIn(
            "module: openconfig-interfaces\n  +--rw interfaces\n     +--rw interface* [name]\n",
            result[0]["tree"],
        )
