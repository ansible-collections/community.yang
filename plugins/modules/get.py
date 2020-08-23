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
options:
  get_filter:
    description:
      - The filter in xml string format to fetch a subset of running-configuration for the YANG model
        given in C(file) option.
    type: str
  file:
    description:
      - The file path of the YANG model that corresponds to the configuration fetch from the remote host.
        This options accepts wildcard (*) as well for the filename in case the configuration requires
        to parse multiple yang file. For example "openconfig/public/tree/master/release/models/interfaces/*.yang"
  search_path:
    description:
      - is a colon C(:) separated list of directories to search for imported yang modules
        in the yang file mentioned in C(path) option. If the value is not given it will search in
        the default directory path.
    type: path
    default: "~/.ansible/yang/spec"
"""
RETURN = """
json:
description: The running configuration in json format
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
xml:
description: The running configuration in xml format
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
    get_filter: |
        <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"><interface-configuration>
        </interface-configuration></interface-configurations>
    file: "{{ playbook_dir }}/YangModels/yang/tree/master/vendor/cisco/xr/613/*.yang"
    search_path: "{{ playbook_dir }}/openconfig/public/release/models:{{ playbook_dir }}/pyang/modules"
"""
