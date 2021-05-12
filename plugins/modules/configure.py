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
  netconf_options:
    description:
    - Pass arguments to the lower level component, M(ansible.netcommon.netconf_config), that this module uses.
    type: dict
    suboptions:
      target:
        description: Name of the configuration datastore to be edited. - auto, uses candidate
          and fallback to running - candidate, edit <candidate/> datastore and then commit
          - running, edit <running/> datastore directly
        default: auto
        type: str
        choices:
        - auto
        - candidate
        - running
        aliases:
        - datastore
      source_datastore:
        description:
        - Name of the configuration datastore to use as the source to copy the configuration
          to the datastore mentioned by C(target) option. The values can be either I(running),
          I(candidate), I(startup) or a remote URL
        type: str
        aliases:
        - source
      lock:
        description:
        - Instructs the module to explicitly lock the datastore specified as C(target).
          By setting the option value I(always) is will explicitly lock the datastore
          mentioned in C(target) option. It the value is I(never) it will not lock the
          C(target) datastore. The value I(if-supported) lock the C(target) datastore
          only if it is supported by the remote Netconf server.
        type: str
        default: always
        choices:
        - never
        - always
        - if-supported
      default_operation:
        description:
        - The default operation for <edit-config> rpc, valid values are I(merge), I(replace)
          and I(none). If the default value is merge, the configuration data in the C(content)
          option is merged at the corresponding level in the C(target) datastore. If the
          value is replace the data in the C(content) option completely replaces the configuration
          in the C(target) datastore. If the value is none the C(target) datastore is
          unaffected by the configuration in the config option, unless and until the incoming
          configuration data uses the C(operation) operation to request a different operation.
        type: str
        choices:
        - merge
        - replace
        - none
      confirm:
        description:
        - This argument will configure a timeout value for the commit to be confirmed
          before it is automatically rolled back. If the C(confirm_commit) argument is
          set to False, this argument is silently ignored. If the value of this argument
          is set to 0, the commit is confirmed immediately. The remote host MUST support
          :candidate and :confirmed-commit capability for this option to .
        type: int
        default: 0
      confirm_commit:
        description:
        - This argument will execute commit operation on remote device. It can be used
          to confirm a previous commit.
        type: bool
        default: no
      error_option:
        description:
        - This option controls the netconf server action after an error occurs while editing
          the configuration.
        - If I(error_option=stop-on-error), abort the config edit on first error.
        - If I(error_option=continue-on-error), continue to process configuration data
          on error. The error is recorded and negative response is generated if any errors
          occur.
        - If I(error_option=rollback-on-error), rollback to the original configuration
          if any error occurs. This requires the remote Netconf server to support the
          I(error_option=rollback-on-error) capability.
        default: stop-on-error
        type: str
        choices:
        - stop-on-error
        - continue-on-error
        - rollback-on-error
      save:
        description:
        - The C(save) argument instructs the module to save the configuration in C(target)
          datastore to the startup-config if changed and if :startup capability is supported
          by Netconf server.
        default: false
        type: bool
      backup:
        description:
        - This argument will cause the module to create a full backup of the current C(running-config)
          from the remote device before any changes are made. If the C(backup_options)
          value is not given, the backup file is written to the C(backup) folder in the
          playbook root directory or role root directory, if playbook is part of an ansible
          role. If the directory does not exist, it is created.
        type: bool
        default: no
      delete:
        description:
        - It instructs the module to delete the configuration from value mentioned in
          C(target) datastore.
        type: bool
        default: no
      commit:
        description:
        - This boolean flag controls if the configuration changes should be committed
          or not after editing the candidate datastore. This option is supported only
          if remote Netconf server supports :candidate capability. If the value is set
          to I(False) commit won't be issued after edit-config operation and user needs
          to handle commit or discard-changes explicitly.
        type: bool
        default: true
      validate:
        description:
        - This boolean flag if set validates the content of datastore given in C(target)
          option. For this option to work remote Netconf server should support :validate
          capability.
        type: bool
        default: false
      backup_options:
        description:
        - This is a dict object containing configurable options related to backup file
          path. The value of this option is read only when C(backup) is set to I(yes),
          if C(backup) is set to I(no) this option will be silently ignored.
        suboptions:
          filename:
            description:
            - The filename to be used to store the backup configuration. If the filename
              is not given it will be generated based on the hostname, current time and
              date in format defined by <hostname>_config.<current-date>@<current-time>
            type: str
          dir_path:
            description:
            - This option provides the path ending with directory name in which the backup
              configuration file will be stored. If the directory does not exist it will
              be first created and the filename is either the value of C(filename) or
              default filename as described in C(filename) options description. If the
              path value is not given in that case a I(backup) directory will be created
              in the current working directory and backup configuration will be copied
              in C(filename) within I(backup) directory.
            type: path
        type: dict
requirements:
- ncclient (>=v0.5.2)
- pyang
notes:
- This module requires the NETCONF system service be enabled on the remote device
  being managed.
- This module supports the use of connection=ansible.netcommon.netconf
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

- name: Netconf options
  community.yang.configure:
    config: "{{ lookup('file', 'interfaces-config.json') }}"
    file: "{{ playbook_dir }}/public/release/models/interfaces/openconfig-interfaces.yang"
    search_path: "{{ playbook_dir }}/public/release/models"
    netconf_options:
      lock: never
      username: system
      password: complex_password
"""
