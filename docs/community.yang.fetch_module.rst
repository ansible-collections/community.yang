.. _community.yang.fetch_module:


********************
community.yang.fetch
********************

**Fetch given yang model and it's dependencies**



.. contents::
   :local:
   :depth: 1


Synopsis
--------
- Fetch given yang model and its dependant yang model from device using netconf rpc.



Requirements
------------
The below requirements are needed on the host that executes this module.

- ncclient (>=v0.5.2)
- pyang
- xmltodict


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
                    <b>continue_on_failure</b>
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
                        <div>This is an optional arguement that allows schema fetch to continue if one the desired models fails download</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>dir</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>This is an optional argument which provide the directory path in which the fetched yang modules will be saved. The name of the file is same as that of the yang module name prefixed with `.yang` extension.</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="parameter-"></div>
                    <b>name</b>
                    <a class="ansibleOptionLink" href="#parameter-" title="Permalink to this option"></a>
                    <div style="font-size: small">
                        <span style="color: purple">-</span>
                    </div>
                </td>
                <td>
                </td>
                <td>
                        <div>Name of the yang model to fetched from remote host. This will also fetch all the dependent yang models and return as part of result. If the value is set to <em>all</em> in that case all the yang models supported by remote host will be fetched.</div>
                </td>
            </tr>
    </table>
    <br/>


Notes
-----

.. note::
   - This module requires the NETCONF system service be enabled on the remote device being managed.
   - This module supports the use of connection=ansible.netcommon.netconf
   - If no options provided it will return list of yang model name supported by remote host



Examples
--------

.. code-block:: yaml

    - name: Fetch given yang model from remote host
      community.yang.fetch:
        name: "{{ item }}"
      loop:
        - openconfig-interface
        - openconfig-bgp

    - name: Fetch list of supported yang model names
      community.yang.fetch:

    - name: Fetch all the yang models supported by remote host and store it in dir location
      community.yang.fetch:
        name: all
        dir: "{{ playbook_dir }}/yang_files"

    - name: Fetch all the yang models supported by remote host and store it in dir location do not stop on error
      community.yang.fetch:
        name: all
        dir: "{{ playbook_dir }}/yang_files"
        continue_on_failure: true



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
                    <b>failed_yang_modules</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>only when continue_on_failure is true</td>
                <td>
                            <div>List of yang models that failed download</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ietf-netconf-monitoring&#x27;, &#x27;cisco-xr-ietf-netconf-monitoring-deviations&#x27;]</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>fetched</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">dictionary</span>
                    </div>
                </td>
                <td>always apart from low-level errors (such as action plugin)</td>
                <td>
                            <div>This is a key-value pair were key is the name of the yang model and value is the yang model itself in string format</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">{&#x27;ietf-inet-types&#x27;: &#x27;module ietf-inet-types ...&lt;--snip--&gt;&#x27;}</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>number_schema_fetched</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">integer</span>
                    </div>
                </td>
                <td>always apart from low-level errors (such as action plugin)</td>
                <td>
                            <div>Total number of yang model fetched from remote host</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">10</div>
                </td>
            </tr>
            <tr>
                <td colspan="1">
                    <div class="ansibleOptionAnchor" id="return-"></div>
                    <b>supported_yang_modules</b>
                    <a class="ansibleOptionLink" href="#return-" title="Permalink to this return value"></a>
                    <div style="font-size: small">
                      <span style="color: purple">list</span>
                    </div>
                </td>
                <td>only when model name is not provided</td>
                <td>
                            <div>List of supported yang models name</div>
                    <br/>
                        <div style="font-size: smaller"><b>Sample:</b></div>
                        <div style="font-size: smaller; color: blue; word-wrap: break-word; word-break: break-all;">[&#x27;ietf-netconf-monitoring&#x27;, &#x27;cisco-xr-ietf-netconf-monitoring-deviations&#x27;]</div>
                </td>
            </tr>
    </table>
    <br/><br/>


Status
------


Authors
~~~~~~~

- Ganesh Nalawade (@ganeshrn)
