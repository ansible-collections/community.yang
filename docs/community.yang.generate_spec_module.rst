.. _community.yang.generate_spec_module:


****************************
community.yang.generate_spec
****************************

**Generate JSON/XML schema and tree representation for given YANG model**



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- The module will be read the given Yang model and generate the corresponding JSON, XML schema and the YANG tree representation (as per RFC 8340) of the model and return in the result and optionally store it in this individual files on control node.



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
            <th colspan="2">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>content</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The text content of the top level YANG model for the the should be generated. This option is mutually-exclusive with <code>path</code> option.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>doctype</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li><div style="color: blue"><b>config</b>&nbsp;&larr;</div></li>
                                    <li>data</li>
                        </ul>
                </td>
                <td>
                        <div>Identifies the root node of the configuration skeleton. If value is <code>config</code> only configuration data will be present in skeleton, if value is <code>data</code> both config and state data fields will be present in output.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>file</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">list</span>
                         / <span style="color: purple">elements=path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The file path of the top level YANG model for the spec should be generated. This option is mutually-exclusive with <code>content</code> option.</div>
                </td>
            </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>json_schema</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The options to control the way JSON schema is generated</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>defaults</b>
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
                        <div>This boolean flag indicates if the generated JSON configuration schema should have fields initialized with default values or not.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The file path to which the generated JSON schema should be stored.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
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
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>tree_schema</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The options to control the way tree schema is generated</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The file path to which the generated tree schema should be stored.</div>
                </td>
            </tr>

            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>xml_schema</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The options to control the way XML schema is generated</div>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>annotations</b>
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
                        <div>The boolean flag identifies if the XML skeleton should have comments describing the field or not.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>defaults</b>
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
                        <div>This boolean flag indicates if the generated XML configuration schema should have fields initialized with default values or not.</div>
                </td>
            </tr>
            <tr>
                    <td class="elbow-placeholder"></td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>path</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">path</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>The file path to which the generated XML schema should be stored.</div>
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
                    <b>json_schema</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The json schema generated from yang document</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{
        &quot;openconfig-interfaces:interfaces&quot;: {
            &quot;interface&quot;: [
                {
                    &quot;hold-time&quot;: {
                        &quot;config&quot;: {
                            &quot;down&quot;: &quot;&quot;,
                            &quot;up&quot;: &quot;&quot;
                        }
                    },
                    &quot;config&quot;: {
                        &quot;description&quot;: &quot;&quot;,
                        &quot;type&quot;: &quot;&quot;,
                        &quot;enabled&quot;: &quot;&quot;,
                        &quot;mtu&quot;: &quot;&quot;,
                        &quot;loopback-mode&quot;: &quot;&quot;,
                        &quot;name&quot;: &quot;&quot;
                    },
                    &quot;name&quot;: &quot;&quot;,
                    &quot;subinterfaces&quot;: {
                        &quot;subinterface&quot;: [
                            {
                                &quot;index&quot;: &quot;&quot;,
                                &quot;config&quot;: {
                                    &quot;index&quot;: &quot;&quot;,
                                    &quot;enabled&quot;: &quot;&quot;,
                                    &quot;description&quot;: &quot;&quot;
                                }
                            }
                        ]
                    }
                }
            ]
        }</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>tree_schema</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The tree schema representation of yang scehma as per RFC 8340</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">module: openconfig-interfaces
      +--rw interfaces
         +--rw interface* [name]
            +--rw name             -&gt; ../config/name
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
            |  +--ro last-change?     oc-types:timeticks64</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>xml_schema</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always</td>
                <td>
                            <div>The xml configuration schema generated from yang document</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">&lt;config xmlns=&quot;urn:ietf:params:xml:ns:netconf:base:1.0&quot;&gt;
      &lt;interfaces xmlns=&quot;http://openconfig.net/yang/interfaces&quot;&gt;
        &lt;interface&gt;
          &lt;name/&gt;
          &lt;config&gt;
            &lt;name/&gt;
            &lt;type/&gt;
            &lt;mtu/&gt;
            &lt;loopback-mode&gt;&lt;/loopback-mode&gt;
            &lt;description/&gt;
            &lt;enabled&gt;True&lt;/enabled&gt;
          &lt;/config&gt;
          &lt;hold-time&gt;
            &lt;config&gt;
              &lt;up&gt;&lt;/up&gt;
              &lt;down&gt;&lt;/down&gt;
            &lt;/config&gt;
          &lt;/hold-time&gt;
          &lt;subinterfaces&gt;
            &lt;subinterface&gt;
              &lt;index/&gt;
              &lt;config&gt;
                &lt;index&gt;&lt;/index&gt;
                &lt;description/&gt;
                &lt;enabled&gt;&lt;/enabled&gt;
              &lt;/config&gt;
            &lt;/subinterface&gt;
          &lt;/subinterfaces&gt;
        &lt;/interface&gt;
      &lt;/interfaces&gt;
    &lt;/config&gt;</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Rohit Thakur (@rohitthakur2590)
