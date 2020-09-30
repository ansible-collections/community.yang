#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2020 Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: configure
short_description: Reads the input configuration in JSON format and pushes to the remote host over netconf
author: Rohit Thakur (@rohitthakur2590)
description:
    - The module takes the JSON configuration as input.
    - Pre-validates the config with the corresponding YANG model.
    - Converts input JSON configuration to XML payload to be pushed on the remote host
      using netconf connection.
options:
  config:
    description:
      - The running-configuration to be pushed onto the device in JSON format (as per RFC 7951).
    type: dict
    required: True
  get_filter:
    description:
      - The filter in xml string format to fetch a subset of the running-configuration for the YANG model
        given in C(file) option. If this option is provided it will compare the current running-configuration
        on the device with what is provided in the C(config) option and push to C(config) value to device only
        if it is different to ensure idempotent task run.
    type: str
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
"""
RETURN = """
diff:
  description: If --diff option in enabled while running, the before and after configuration change are
               returned as part of before and after key.
  returned: when diff is enabled
  type: dict
  sample:
    "after": "<rpc-reply>\n<data>\n<configuration>\n<version>17.3R1.10</version>...<--snip-->"
    "before": "<rpc-reply>\n<data>\n<configuration>\n <version>17.3R1.10</version>...<--snip-->"
"""
EXAMPLES = """
- name: configure interface using structured data in JSON format
  community.yang.configure:
    config:
        {
            "openconfig-interfaces:interfaces":
             {
                "interface": [{
                    "name" : "GigabitEthernet0/0/0/2",
                    "config" : {
                        "name" : "GigabitEthernet0/0/0/2",
                        "enabled": true,
                        "description": "configured by Ansible yang role",
                        "mtu": 1024
                    }
                }]
             }
        }
    get_filter: |
        <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"><interface-configuration>
        </interface-configuration></interface-configurations>
    file: "{{ playbook_dir }}/public/release/models/interfaces/openconfig-interfaces.yang"
    search_path: "{{ playbook_dir }}/public/release/models"

- name: configure by reading data from file and ensure idempotent task run
  community.yang.configure:
    config: "{{ lookup('file', 'interfaces-config.json') }}"
    get_filter: |
        <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"><interface-configuration>
        </interface-configuration></interface-configurations>
    file: "{{ playbook_dir }}/public/release/models/interfaces/openconfig-interfaces.yang"
    search_path: "{{ playbook_dir }}/public/release/models"

- name: Configure native data to running-config
  community.yang.configure:
    config: "{{ candidate['json_data'] }}"
    file: "{{ yang_file }}"
    search_path: "{{ search_path }}"
"""
