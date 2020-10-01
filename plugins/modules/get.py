#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2020 Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: get
short_description: Fetch the device configuration and render it in JSON format defined by RFC7951
description:
    - The module will fetch the configuration data for a given YANG model and render it in
      JSON format (as per RFC 7951).
author: Ganesh Nalawade (@ganeshrn)
options:
  filter:
    description:
    - This argument specifies the XML string which acts as a filter to restrict the
      portions of the data to be are retrieved from the remote device. If this option
      is not specified entire configuration or state data is returned in result depending
      on the value of C(source) option. The C(filter) value can be either XML string
      or XPath, if the filter is in XPath format the NETCONF server running on remote
      host should support xpath capability else it will result in an error.
    type: str
  source:
    description:
    - This argument specifies the datastore from which configuration data should be
      fetched. Valid values are I(running), I(candidate) and I(startup). If the C(source)
      value is not set both configuration and state information are returned in response
      from running datastore.
    type: str
    choices:
    - running
    - candidate
    - startup
  lock:
    description:
    - Instructs the module to explicitly lock the datastore specified as C(source).
      If no I(source) is defined, the I(running) datastore will be locked. By setting
      the option value I(always) is will explicitly lock the datastore mentioned in
      C(source) option. By setting the option value I(never) it will not lock the
      C(source) datastore. The value I(if-supported) allows better interworking with
      NETCONF servers, which do not support the (un)lock operation for all supported
      datastores.
    type: str
    default: never
    choices:
    - never
    - always
    - if-supported
  file:
    description:
      - The file path of the YANG model that corresponds to the configuration fetch from the remote host.
        This options accepts wildcard (*) as well for the filename in case the configuration requires
        to parse multiple yang file. For example "openconfig/public/tree/master/release/models/interfaces/*.yang"
    required: True
    type: list
    elements: path
  search_path:
    description:
      - is a colon C(:) separated list of directories to search for imported yang modules
        in the yang file mentioned in C(path) option. If the value is not given it will search in
        the default directory path.
    type: path
    default: "~/.ansible/yang/spec"
requirements:
- ncclient (>=v0.5.2)
- pyang
- xsltproc
notes:
- This module requires the NETCONF system service be enabled on the remote device
  being managed.
- This module supports the use of connection=ansible.netcommon.netconf
- To use this module xsltproc should be installed on control node
"""

RETURN = """
json_data:
  description: The running configuration in json format
  returned: always
  type: dict
  sample: |
    {
        "openconfig-interfaces:interfaces":
         {
            "interface": [{
                "name" : "GigabitEthernet0/0/0/2",
                "config" : {
                    "name" : "GigabitEthernet0/0/0/2",
                    "description": "configured by Ansible yang collection",
                    "mtu": 1024
                }
            }]
         }
    }
xml_data:
  description: The running configuration in xml format
  returned: always
  type: str
  sample: |
     <data xmlns=\"urn:ietf:params:xml:ns:netconf:base:1.0\" xmlns:nc=\"urn:ietf:params:xml:ns:netconf:base:1.0\">
       <interface-configurations xmlns=\"http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg\">
         <interface-configuration>
             <active>act</active>
             <interface-name>GigabitEthernet0/0/0/2</interface-name>
             <description>configured by Ansible yang collection</description>
             <mtu>1024</mtu>
         </interface-configuration>
       </interface-configurations>
     </data>
"""
EXAMPLES = """
- name: fetch interface configuration and return it in JSON format
  community.yang.get:
    filter: |
        <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"><interface-configuration>
        </interface-configuration></interface-configurations>
    file: "{{ playbook_dir }}/YangModels/yang/tree/master/vendor/cisco/xr/613/*.yang"
    search_path: "{{ playbook_dir }}/YangModels/yang/tree/master/vendor/cisco/xr/613:{{ playbook_dir }}/pyang/modules"
"""
