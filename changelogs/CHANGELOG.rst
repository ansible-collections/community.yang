==========================================
Ansible Netcommon Collection Release Notes
==========================================

.. contents:: Topics

v1.1.0
======

Minor Changes
-------------

- community.yang.configure - Since ``configure`` module is built on top of ``netconf_config`` we add a new option argument, ``netconf_options``, allowing passing options directly to ``netconf_config``.

v1.0.1
======

Minor Changes
-------------

- Added unit test for xml2json, json2xml and spec lookup plugins (https://github.com/ansible-collections/community.yang/pull/50)
- Refactored module_utils to fix ansible-test sanity issues (https://github.com/ansible-collections/community.yang/pull/50)
- added optional attribute for fetch action to continue if it hits a module that cannot be found

Bugfixes
--------

- Fixed json2xml py3 compatibility issues (https://github.com/ansible-collections/community.yang/pull/45)
- Sort yang_files to address dependency issue (https://github.com/ansible-collections/community.yang/pull/46)

v1.0.0
======

Major Changes
-------------

- Added configure module to push json format configuration on to remote host over netconf connection.
- Added generate_spec module (https://github.com/ansible-collections/community.yang/pull/6)
- Added get module (https://github.com/ansible-collections/community.yang/pull/8)
- Added json2xml lookup plugin (https://github.com/ansible-collections/community.yang/pull/5)
- Added module to fetch yang model and it's dependenices from remote host (https://github.com/ansible-collections/community.yang/issues/1).
- Added spec lookup plugin (https://github.com/ansible-collections/community.yang/pull/4)
- Added xml2json lookup plugin (https://github.com/ansible-collections/community.yang/pull/7)

Minor Changes
-------------

- Added support to sort supported yang models returned with fetch (https://github.com/ansible-collections/community.yang/issues/21).

Bugfixes
--------

- Fixed issue when pyang is installed in a venv, can't find `jsonxsl-templates.xsl` file path (https://github.com/ansible-collections/community.yang/issues/25)
- Fixed jxmlease is required for fetch, but not listed in docs. Use xmltodict instead of jxmlease (https://github.com/ansible-collections/community.yang/issues/18)
- Fixed traceback in fetch when the ansible_connection is set to ansible.netcommon.network_cli (https://github.com/ansible-collections/community.yang/issues/18)
- Fixed traceback when using fetch with nxos (https://github.com/ansible-collections/community.yang/issues/20)
- Update file option to list with elements as path (https://github.com/ansible-collections/community.yang/issues/30)
- fetch module docstring updated with supported_yang_modules attribute.
- file attribute set as mandatory to validate the input json config.
- input config type is dict now and json config can provided when translator object invoked.
