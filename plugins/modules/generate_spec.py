#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright 2020 Red Hat
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
---
module: generate_spec
short_description: Generate JSON/XML schema and tree representation for given YANG model
author: Rohit Thakur (@rohitthakur2590)
description:
    - The module will be read the given Yang model and generate the corresponding JSON, XML
      schema and the YANG tree representation (as per RFC 8340) of the model and return in the
      result and optionally store it in this individual files on control node.
options:
  content:
    description:
      - The text content of the top level YANG model for the the should be generated.
        This option is mutually-exclusive with C(path) option.
    type: str
  file:
    description:
      - The file path of the top level YANG model for the spec should be generated.
        This option is mutually-exclusive with C(content) option.
    type: list
    elements: path
  search_path:
    description:
      - is a colon C(:) separated list of directories to search for imported yang modules
        in the yang file mentioned in C(path) option. If the value is not given it will search in
        the default directory path.
    type: path
    default: "~/.ansible/yang/spec"
  doctype:
    description:
      - Identifies the root node of the configuration skeleton. If value is C(config) only configuration
        data will be present in skeleton, if value is C(data) both config and state data fields will be present
        in output.
    default: config
    choices: ['config', 'data']
  json_schema:
    description: The options to control the way JSON schema is generated
    type: dict
    suboptions:
      path:
        description: The file path to which the generated JSON schema should be stored.
        type: path
      defaults:
        description:
          - This boolean flag indicates if the generated JSON configuration schema should have
            fields initialized with default values or not.
        type: bool
        default: False
  xml_schema:
    description: The options to control the way XML schema is generated
    type: dict
    suboptions:
      path:
        description: The file path to which the generated XML schema should be stored.
        type: path
      defaults:
        description:
          - This boolean flag indicates if the generated XML configuration schema should have
            fields initialized with default values or not.
        type: bool
        default: False
      annotations:
        description:
          - The boolean flag identifies if the XML skeleton should have comments describing the field or not.
        default: False
        type: bool
  tree_schema:
    description: The options to control the way tree schema is generated
    type: dict
    suboptions:
      path:
        description: The file path to which the generated tree schema should be stored.
        type: path
requirements:
- ncclient (>=v0.5.2)
- pyang
notes:
- This module requires the NETCONF system service be enabled on the remote device
  being managed.
- This module supports the use of connection=ansible.netcommon.netconf
"""
RETURN = """
tree_schema:
  description: The tree schema representation of yang scehma as per RFC 8340
  returned: always
  type: dict
  sample: |
    module: openconfig-interfaces
      +--rw interfaces
         +--rw interface* [name]
            +--rw name             -> ../config/name
            +--rw config
            |  +--rw name?            string
            |  +--rw type             identityref
            |  +--rw mtu?             uint16
            |  +--rw loopback-mode?   boolean
            |  +--rw description?     string
            |  +--rw enabled?         boolean
            +--ro state
            |  +--ro name?            string
            |  +--ro type             identityref
            |  +--ro mtu?             uint16
            |  +--ro loopback-mode?   boolean
            |  +--ro description?     string
            |  +--ro enabled?         boolean
            |  +--ro ifindex?         uint32
            |  +--ro admin-status     enumeration
            |  +--ro oper-status      enumeration
            |  +--ro last-change?     oc-types:timeticks64
json_schema:
  description: The json schema generated from yang document
  returned: always
  type: dict
  sample: |
    {
        "openconfig-interfaces:interfaces": {
            "interface": [
                {
                    "hold-time": {
                        "config": {
                            "down": "",
                            "up": ""
                        }
                    },
                    "config": {
                        "description": "",
                        "type": "",
                        "enabled": "",
                        "mtu": "",
                        "loopback-mode": "",
                        "name": ""
                    },
                    "name": "",
                    "subinterfaces": {
                        "subinterface": [
                            {
                                "index": "",
                                "config": {
                                    "index": "",
                                    "enabled": "",
                                    "description": ""
                                }
                            }
                        ]
                    }
                }
            ]
        }
xml_schema:
  description: The xml configuration schema generated from yang document
  returned: always
  type: dict
  sample: |
    <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
      <interfaces xmlns="http://openconfig.net/yang/interfaces">
        <interface>
          <name/>
          <config>
            <name/>
            <type/>
            <mtu/>
            <loopback-mode></loopback-mode>
            <description/>
            <enabled>True</enabled>
          </config>
          <hold-time>
            <config>
              <up></up>
              <down></down>
            </config>
          </hold-time>
          <subinterfaces>
            <subinterface>
              <index/>
              <config>
                <index></index>
                <description/>
                <enabled></enabled>
              </config>
            </subinterface>
          </subinterfaces>
        </interface>
      </interfaces>
    </config>
"""
EXAMPLES = """
- name: generate spec from openconfig interface data and in result
  community.yang.generate_spec:
    file: "openconfig/public/release/models/interfaces/openconfig-interfaces.yang"
    search_path: "{{ playbook_dir }}/openconfig/public/release/models:pyang/modules"

- name: generate spec from openconfig interface config data and store it in file
  community.yang.generate_spec:
    file: "openconfig/public/release/models/interfaces/openconfig-interfaces.yang"
    search_path: "{{ playbook_dir }}/openconfig/public/release/models:pyang/modules"
    doctype: config
    json_schema:
      path: "~/.ansible/yang/spec/{{ inventory_hostname }}/openconfig-interfaces-config.json"
      defaults: True
    xml_schema:
      path: "~/.ansible/yang/spec/{{ inventory_hostname }}/openconfig-interfaces-config.xml"
      defaults: True
      annotations: True
    tree_schema:
      path: "~/.ansible/yang/spec/{{ inventory_hostname }}/openconfig-interfaces-config.tree"
"""
