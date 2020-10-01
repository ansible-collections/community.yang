.. _community.yang.configure_module:


************************
community.yang.configure
************************

**Reads the input configuration in JSON format and pushes to the remote host over netconf**



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The module takes the JSON configuration as input.
- Pre-validates the config with the corresponding YANG model.
- Converts input JSON configuration to XML payload to be pushed on the remote host using netconf connection.



Requirements
------------
The below requirements are needed on the host that executes this module.

- ncclient (>=v0.5.2)
- pyang


Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>config</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The running-configuration to be pushed onto the device in JSON format (as per RFC 7951).</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=path</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The file path of the YANG model that corresponds to the configuration fetch from the remote host. This options accepts wildcard (*) as well for the filename in case the configuration requires to parse multiple yang file. For example &quot;openconfig/public/tree/master/release/models/interfaces/*.yang&quot;</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>get_filter</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The filter in xml string format to fetch a subset of the running-configuration for the YANG model given in <code>file</code> option. If this option is provided it will compare the current running-configuration on the device with what is provided in the <code>config</code> option and push to <code>config</code> value to device only if it is different to ensure idempotent task run.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>search_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"~/.ansible/yang/spec"</div>
                </td>
                <td>
                        <div>is a colon <code>:</code> separated list of directories to search for imported yang modules in the yang file mentioned in <code>path</code> option. If the value is not given it will search in the default directory path.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module requires the NETCONF system service be enabled on the remote device being managed.
   - This module supports the use of connection=ansible.netcommon.netconf



Examples
--------

.. code-block:: yaml+jinja

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



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this module:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>diff</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>when diff is enabled</td>
                <td>
                            <div>If --diff option in enabled while running, the before and after configuration change are returned as part of before and after key.</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;after&#x27;: &#x27;&lt;rpc-reply&gt; &lt;data&gt; &lt;configuration&gt; &lt;version&gt;17.3R1.10&lt;/version&gt;...&lt;--snip--&gt;&#x27;, &#x27;before&#x27;: &#x27;&lt;rpc-reply&gt; &lt;data&gt; &lt;configuration&gt; &lt;version&gt;17.3R1.10&lt;/version&gt;...&lt;--snip--&gt;&#x27;}</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Rohit Thakur (@rohitthakur2590)
