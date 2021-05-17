.. _community.yang.get_module:


******************
community.yang.get
******************

**Fetch the device configuration and render it in JSON format defined by RFC7951**



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The module will fetch the configuration data for a given YANG model and render it in JSON format (as per RFC 7951).



Requirements
------------
The below requirements are needed on the host that executes this module.

- ncclient (>=v0.5.2)
- pyang
- xsltproc


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
                    <b>filter</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This argument specifies the XML string which acts as a filter to restrict the portions of the data to be are retrieved from the remote device. If this option is not specified entire configuration or state data is returned in result depending on the value of <code>source</code> option. The <code>filter</code> value can be either XML string or XPath, if the filter is in XPath format the NETCONF server running on remote host should support xpath capability else it will result in an error.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>lock</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>never</b>&nbsp;&larr;</div></li>
                                    <li>always</li>
                                    <li>if-supported</li>
                        </ul>
                </td>
                <td>
                        <div>Instructs the module to explicitly lock the datastore specified as <code>source</code>. If no <em>source</em> is defined, the <em>running</em> datastore will be locked. By setting the option value <em>always</em> is will explicitly lock the datastore mentioned in <code>source</code> option. By setting the option value <em>never</em> it will not lock the <code>source</code> datastore. The value <em>if-supported</em> allows better interworking with NETCONF servers, which do not support the (un)lock operation for all supported datastores.</div>
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
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>source</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>running</li>
                                    <li>candidate</li>
                                    <li>startup</li>
                        </ul>
                </td>
                <td>
                        <div>This argument specifies the datastore from which configuration data should be fetched. Valid values are <em>running</em>, <em>candidate</em> and <em>startup</em>. If the <code>source</code> value is not set both configuration and state information are returned in response from running datastore.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module requires the NETCONF system service be enabled on the remote device being managed.
   - This module supports the use of connection=ansible.netcommon.netconf
   - To use this module xsltproc should be installed on control node



Examples
--------

.. code-block:: yaml

    - name: fetch interface configuration and return it in JSON format
      community.yang.get:
        filter: |
            <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"><interface-configuration>
            </interface-configuration></interface-configurations>
        file: "{{ playbook_dir }}/YangModels/yang/tree/master/vendor/cisco/xr/613/*.yang"
        search_path: "{{ playbook_dir }}/YangModels/yang/tree/master/vendor/cisco/xr/613:{{ playbook_dir }}/pyang/modules"



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
                    <b>json_data</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The running configuration in json format</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{
        &quot;openconfig-interfaces:interfaces&quot;:
         {
            &quot;interface&quot;: [{
                &quot;name&quot; : &quot;GigabitEthernet0/0/0/2&quot;,
                &quot;config&quot; : {
                    &quot;name&quot; : &quot;GigabitEthernet0/0/0/2&quot;,
                    &quot;description&quot;: &quot;configured by Ansible yang collection&quot;,
                    &quot;mtu&quot;: 1024
                }
            }]
         }
    }</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>xml_data</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">string</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The running configuration in xml format</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">&lt;data xmlns=&quot;urn:ietf:params:xml:ns:netconf:base:1.0&quot; xmlns:nc=&quot;urn:ietf:params:xml:ns:netconf:base:1.0&quot;&gt;
      &lt;interface-configurations xmlns=&quot;http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg&quot;&gt;
        &lt;interface-configuration&gt;
            &lt;active&gt;act&lt;/active&gt;
            &lt;interface-name&gt;GigabitEthernet0/0/0/2&lt;/interface-name&gt;
            &lt;description&gt;configured by Ansible yang collection&lt;/description&gt;
            &lt;mtu&gt;1024&lt;/mtu&gt;
        &lt;/interface-configuration&gt;
      &lt;/interface-configurations&gt;
    &lt;/data&gt;</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)
