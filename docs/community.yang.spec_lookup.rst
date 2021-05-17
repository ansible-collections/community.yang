.. _community.yang.spec_lookup:


*******************
community.yang.spec
*******************

**This plugin reads the content of given yang document and generates json and xml configuration skeleton and a tree structure of yang document.**



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- This plugin parses yang document and generates json and xml configuration skeleton and a tree structure of yang document. The tree structure document is as per RFC 8340 which helps to consume the yang document along with json and xml configuration skeleton.




Parameters
----------

.. raw:: html

    <table  border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="1">Parameter</th>
            <th>Choices/<font color="blue">Defaults</font></th>
                <th>Configuration</th>
            <th width="100%">Comments</th>
        </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>_terms</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">string</span>
                         / <span style="color: red">required</span>
                    </div>
                </td>
                <td>
                </td>
                    <td>
                    </td>
                <td>
                        <div>The path points to the location of the top level yang module which is to be transformed into to Ansible spec.</div>
                </td>
            </tr>
            <tr>
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
                    </td>
                <td>
                        <div>The boolean flag identifies if the xml skeleton should have comments describing the field or not.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>defaults</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                        <b>Default:</b><br/><div style="color: blue">"no"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>This boolean flag indicates if the generated json and xml configuration schema should have fields initialized with default values or not.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>doctype</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">boolean</span>
                    </div>
                </td>
                <td>
                        <ul style="margin: 0; padding: 0"><b>Choices:</b>
                                    <li>no</li>
                                    <li>yes</li>
                        </ul>
                        <b>Default:</b><br/><div style="color: blue">"config"</div>
                </td>
                    <td>
                    </td>
                <td>
                        <div>Identifies the root node of the configuration skeleton. If value is <code>config</code> only configuration data will be present in skeleton, if value is <code>data</code> both config and state data fields will be present in output.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>keep_tmp_files</b>
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
                    </td>
                <td>
                        <div>This is a boolean flag to indicate if the intermediate files generated while creating spec should be kept or deleted. If the value is <code>true</code> the files will not be deleted else by default all the intermediate files will be deleted irrespective of whether task run is successful or not. The intermediate files are stored in path <code>~/.ansible/tmp/yang/spec</code>, this option is mainly used for debugging purpose.</div>
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
                </td>
                    <td>
                    </td>
                <td>
                        <div>is a colon <code>:</code> separated list of directories to search for imported yang modules in the yang file mentioned in <code>path</code> option. If the value is not given it will search in the same directory as that of <code>yang_file</code>.</div>
                </td>
            </tr>
    </table>
    <br/>




Examples
--------

.. code-block:: yaml

    - name: Get interface yang config spec without defaults
      set_fact:
        interfaces_spec: "{{ lookup('community.yang.spec', 'openconfig/public/release/models/interfaces/openconfig-interfaces.yang',
                                search_path='openconfig/public/release/models:pyang/modules/', defaults=True,
                                doctype='data') }}"

    - name: Get interface yang spec with defaults and state data
      set_fact:
        interfaces_spec: "{{ lookup('community.yang.spec', 'openconfig/public/release/models/interfaces/openconfig-interfaces.yang',
                                search_path='openconfig/public/release/models:pyang/modules/', defaults=True,
                                doctype='data') }}"



Return Values
-------------
Common return values are documented `here <https://docs.ansible.com/ansible/latest/reference_appendices/common_return_values.html#common-return-values>`_, the following are the fields unique to this lookup:

.. raw:: html

    <table border=0 cellpadding=0 class="documentation-table">
        <tr>
            <th colspan="2">Key</th>
            <th>Returned</th>
            <th width="100%">Description</th>
        </tr>
            <tr>
                <td colspan="2">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>_list</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">complex</span>
                    </div>
                </td>
                <td></td>
                <td>
                            <div>It returns json skeleton configuration schema, xml skeleton schema and tree structure (as per RFC 8340) for given yang schema.</div>
                    <br/>
                </td>
            </tr>
                                <tr>
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>json_skeleton</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>The json configuration skeleton generated from yang document</div>
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
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>tree</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>The tree representation of yang scehma as per RFC 8340</div>
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
                    <td class="elbow-placeholder">&nbsp;</td>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>xml_skeleton</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>success</td>
                <td>
                            <div>The xml configuration skeleton generated from yang document</div>
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

- Ganesh Nalawade (@ganeshrn)


.. hint::
    Configuration entries for each entry type have a low to high priority order. For example, a variable that is lower in the list will override a variable that is higher up.
