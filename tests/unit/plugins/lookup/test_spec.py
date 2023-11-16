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
    os.path.dirname(os.path.abspath(__file__)),
    "../../../fixtures/files",
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
            "is invalid, valid value are config, data",
            str(error.exception),
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
            result[0]["json_skeleton"]["openconfig-interfaces:interfaces"]["interface"][
                0
            ]["name"],
            "",
        )
        self.assertEqual(
            result[0]["json_skeleton"]["openconfig-interfaces:interfaces"]["interface"][
                0
            ]["config"]["loopback-mode"],
            "False",
        )
        self.assertEqual(
            result[0]["json_skeleton"]["openconfig-interfaces:interfaces"]["interface"][
                0
            ]["config"]["enabled"],
            "True",
        )

        # check xml skeleton data
        self.assertIn(
            """<?xml version=\'1.0\' encoding=\'UTF-8\'?>\n<config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">\n  <interfaces xmlns="http://openconfig.net/yang/interfaces">\n    <interface>\n      <!-- # keys: name-->\n      <!-- # entries: 0.. -->\n      <name>\n        <!-- type: leafref -->\n      </name>\n      <config>\n        <name>\n          <!-- type: string -->\n        </name>\n        <type>\n          <!-- type: identityref -->\n        </type>\n        <mtu>\n          <!-- type: uint16 -->\n        </mtu>\n        <description>\n          <!-- type: string -->\n        </description>\n      </config>\n      <hold-time>\n        <config/>\n      </hold-time>\n      <subinterfaces>\n        <subinterface>\n          <!-- # keys: index-->\n          <!-- # entries: 0.. -->\n          <index>\n            <!-- type: leafref -->\n          </index>\n          <config>\n            <description>\n              <!-- type: string -->\n            </description>\n          </config>\n        </subinterface>\n      </subinterfaces>\n    </interface>\n  </interfaces>\n</config>\n""",
            result[0]["xml_skeleton"],
        )

        # check tree skeleton data
        self.assertIn(
            """module: openconfig-interfaces\n  +--rw interfaces\n     +--rw interface* [name]\n        +--rw name             -> ../config/name\n        +--rw config\n        |  +--rw name?            string\n        |  +--rw type             identityref\n        |  +--rw mtu?             uint16\n        |  +--rw loopback-mode?   boolean\n        |  +--rw description?     string\n        |  +--rw enabled?         boolean\n        +--ro state\n        |  +--ro name?            string\n        |  +--ro type             identityref\n        |  +--ro mtu?             uint16\n        |  +--ro loopback-mode?   boolean\n        |  +--ro description?     string\n        |  +--ro enabled?         boolean\n        |  +--ro ifindex?         uint32\n        |  +--ro admin-status     enumeration\n        |  +--ro oper-status      enumeration\n        |  +--ro last-change?     oc-types:timeticks64\n        |  +--ro counters\n        |     +--ro in-octets?             oc-yang:counter64\n        |     +--ro in-unicast-pkts?       oc-yang:counter64\n        |     +--ro in-broadcast-pkts?     oc-yang:counter64\n        |     +--ro in-multicast-pkts?     oc-yang:counter64\n        |     +--ro in-discards?           oc-yang:counter64\n        |     +--ro in-errors?             oc-yang:counter64\n        |     +--ro in-unknown-protos?     oc-yang:counter64\n        |     +--ro in-fcs-errors?         oc-yang:counter64\n        |     +--ro out-octets?            oc-yang:counter64\n        |     +--ro out-unicast-pkts?      oc-yang:counter64\n        |     +--ro out-broadcast-pkts?    oc-yang:counter64\n        |     +--ro out-multicast-pkts?    oc-yang:counter64\n        |     +--ro out-discards?          oc-yang:counter64\n        |     +--ro out-errors?            oc-yang:counter64\n        |     +--ro carrier-transitions?   oc-yang:counter64\n        |     +--ro last-clear?            oc-types:timeticks64\n        +--rw hold-time\n        |  +--rw config\n        |  |  +--rw up?     uint32\n        |  |  +--rw down?   uint32\n        |  +--ro state\n        |     +--ro up?     uint32\n        |     +--ro down?   uint32\n        +--rw subinterfaces\n           +--rw subinterface* [index]\n              +--rw index     -> ../config/index\n              +--rw config\n              |  +--rw index?         uint32\n              |  +--rw description?   string\n              |  +--rw enabled?       boolean\n              +--ro state\n                 +--ro index?          uint32\n                 +--ro description?    string\n                 +--ro enabled?        boolean\n                 +--ro name?           string\n                 +--ro ifindex?        uint32\n                 +--ro admin-status    enumeration\n                 +--ro oper-status     enumeration\n                 +--ro last-change?    oc-types:timeticks64\n                 +--ro counters\n                    +--ro in-octets?             oc-yang:counter64\n                    +--ro in-unicast-pkts?       oc-yang:counter64\n                    +--ro in-broadcast-pkts?     oc-yang:counter64\n                    +--ro in-multicast-pkts?     oc-yang:counter64\n                    +--ro in-discards?           oc-yang:counter64\n                    +--ro in-errors?             oc-yang:counter64\n                    +--ro in-unknown-protos?     oc-yang:counter64\n                    +--ro in-fcs-errors?         oc-yang:counter64\n                    +--ro out-octets?            oc-yang:counter64\n                    +--ro out-unicast-pkts?      oc-yang:counter64\n                    +--ro out-broadcast-pkts?    oc-yang:counter64\n                    +--ro out-multicast-pkts?    oc-yang:counter64\n                    +--ro out-discards?          oc-yang:counter64\n                    +--ro out-errors?            oc-yang:counter64\n                    +--ro carrier-transitions?   oc-yang:counter64\n                    +--ro last-clear?            oc-types:timeticks64\n'""",
            result[0]["tree"],
        )
