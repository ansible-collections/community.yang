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
            <th colspan="3">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="3">
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
                <td colspan="3">
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
                <td colspan="3">
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
                <td colspan="3">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>netconf_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Pass arguments to the lower level component, <span class='module'>ansible.netcommon.netconf_config</span>, that this module uses.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backup</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>This argument will cause the module to create a full backup of the current <code>running-config</code> from the remote device before any changes are made. If the <code>backup_options</code> value is not given, the backup file is written to the <code>backup</code> folder in the playbook root directory or role root directory, if playbook is part of an ansible role. If the directory does not exist, it is created.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>backup_options</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This is a dict object containing configurable options related to backup file path. The value of this option is read only when <code>backup</code> is set to <em>yes</em>, if <code>backup</code> is set to <em>no</em> this option will be silently ignored.</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dir_path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This option provides the path ending with directory name in which the backup configuration file will be stored. If the directory does not exist it will be first created and the filename is either the value of <code>filename</code> or default filename as described in <code>filename</code> options description. If the path value is not given in that case a <em>backup</em> directory will be created in the current working directory and backup configuration will be copied in <code>filename</code> within <em>backup</em> directory.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>filename</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The filename to be used to store the backup configuration. If the filename is not given it will be generated based on the hostname, current time and date in format defined by &lt;hostname&gt;_config.&lt;current-date&gt;@&lt;current-time&gt;</div>
                </td>
            </tr>

            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>commit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li><div style="color: blue"><b>yes</b>&nbsp;&larr;</div></li>
                        </ul>
                </td>
                <td>
                        <div>This boolean flag controls if the configuration changes should be committed or not after editing the candidate datastore. This option is supported only if remote Netconf server supports :candidate capability. If the value is set to <em>False</em> commit won&#x27;t be issued after edit-config operation and user needs to handle commit or discard-changes explicitly.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>confirm</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">0</div>
                </td>
                <td>
                        <div>This argument will configure a timeout value for the commit to be confirmed before it is automatically rolled back. If the <code>confirm_commit</code> argument is set to False, this argument is silently ignored. If the value of this argument is set to 0, the commit is confirmed immediately. The remote host MUST support :candidate and :confirmed-commit capability for this option to .</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>confirm_commit</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>This argument will execute commit operation on remote device. It can be used to confirm a previous commit.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>default_operation</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>merge</li>
                                    <li>replace</li>
                                    <li>none</li>
                        </ul>
                </td>
                <td>
                        <div>The default operation for &lt;edit-config&gt; rpc, valid values are <em>merge</em>, <em>replace</em> and <em>none</em>. If the default value is merge, the configuration data in the <code>content</code> option is merged at the corresponding level in the <code>target</code> datastore. If the value is replace the data in the <code>content</code> option completely replaces the configuration in the <code>target</code> datastore. If the value is none the <code>target</code> datastore is unaffected by the configuration in the config option, unless and until the incoming configuration data uses the <code>operation</code> operation to request a different operation.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>delete</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>It instructs the module to delete the configuration from value mentioned in <code>target</code> datastore.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>error_option</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>stop-on-error</b>&nbsp;&larr;</div></li>
                                    <li>continue-on-error</li>
                                    <li>rollback-on-error</li>
                        </ul>
                </td>
                <td>
                        <div>This option controls the netconf server action after an error occurs while editing the configuration.</div>
                        <div>If <em>error_option=stop-on-error</em>, abort the config edit on first error.</div>
                        <div>If <em>error_option=continue-on-error</em>, continue to process configuration data on error. The error is recorded and negative response is generated if any errors occur.</div>
                        <div>If <em>error_option=rollback-on-error</em>, rollback to the original configuration if any error occurs. This requires the remote Netconf server to support the <em>error_option=rollback-on-error</em> capability.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lock</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>never</li>
                                    <li><div style="color: blue"><b>always</b>&nbsp;&larr;</div></li>
                                    <li>if-supported</li>
                        </ul>
                </td>
                <td>
                        <div>Instructs the module to explicitly lock the datastore specified as <code>target</code>. By setting the option value <em>always</em> is will explicitly lock the datastore mentioned in <code>target</code> option. It the value is <em>never</em> it will not lock the <code>target</code> datastore. The value <em>if-supported</em> lock the <code>target</code> datastore only if it is supported by the remote Netconf server.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>save</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>The <code>save</code> argument instructs the module to save the configuration in <code>target</code> datastore to the startup-config if changed and if :startup capability is supported by Netconf server.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source_datastore</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the configuration datastore to use as the source to copy the configuration to the datastore mentioned by <code>target</code> option. The values can be either <em>running</em>, <em>candidate</em>, <em>startup</em> or a remote URL</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: source</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>target</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>auto</b>&nbsp;&larr;</div></li>
                                    <li>candidate</li>
                                    <li>running</li>
                        </ul>
                </td>
                <td>
                        <div>Name of the configuration datastore to be edited. - auto, uses candidate and fallback to running - candidate, edit &lt;candidate/&gt; datastore and then commit - running, edit &lt;running/&gt; datastore directly</div>
                        <div style="font-size: small; color: darkgreen"><br/>aliases: datastore</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>validate</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>no</b>&nbsp;&larr;</div></li>
                                    <li>yes</li>
                        </ul>
                </td>
                <td>
                        <div>This boolean flag if set validates the content of datastore given in <code>target</code> option. For this option to work remote Netconf server should support :validate capability.</div>
                </td>
            </tr>

            <tr>
                <td colspan="3">
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

.. code-block:: yaml

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
