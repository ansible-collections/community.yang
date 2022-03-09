# Ansible Collection - community.yang  
![Tests](https://github.com/codeandcosmos/community.yang/actions/workflows/tests.yml/badge.svg)

This repo hosts the `community.yang` Ansible Collection.

The collection includes the community plugins to help the support Yang manily with network devices.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10**.

Plugins and modules within a collection may be tested with only specific Ansible versions.
A collection may contain metadata that identifies these versions.
PEP440 is the schema used to describe the versions of Ansible.
<!--end requires_ansible-->

### Supported connections
The Community yang collection supports ``netconf`` connections.

## Included content
<!--start collection content-->
### Lookup plugins
Name | Description
--- | ---
[community.yang.json2xml](https://github.com/ansible-collections/community.yang/blob/main/docs/community.yang.json2xml_lookup.rst)|Validates json configuration against yang data model and convert it to xml.
[community.yang.spec](https://github.com/ansible-collections/community.yang/blob/main/docs/community.yang.spec_lookup.rst)|This plugin reads the content of given yang document and generates json and xml configuration skeleton and a tree structure of yang document.
[community.yang.xml2json](https://github.com/ansible-collections/community.yang/blob/main/docs/community.yang.xml2json_lookup.rst)|Converts xml input to json structure output by mapping it against corresponding Yang model

### Modules
Name | Description
--- | ---
[community.yang.configure](https://github.com/ansible-collections/community.yang/blob/main/docs/community.yang.configure_module.rst)|Reads the input configuration in JSON format and pushes to the remote host over netconf
[community.yang.fetch](https://github.com/ansible-collections/community.yang/blob/main/docs/community.yang.fetch_module.rst)|Fetch given yang model and it's dependencies
[community.yang.generate_spec](https://github.com/ansible-collections/community.yang/blob/main/docs/community.yang.generate_spec_module.rst)|Generate JSON/XML schema and tree representation for given YANG model
[community.yang.get](https://github.com/ansible-collections/community.yang/blob/main/docs/community.yang.get_module.rst)|Fetch the device configuration and render it in JSON format defined by RFC7951

<!--end collection content-->

## Installation and Usage

### Installing the Collection from Ansible Galaxy

Before using the Community Yang collection, you need to install it with the `ansible-galaxy` CLI:

    ansible-galaxy collection install community.yang

You can also include it in a `requirements.yml` file and install it via `ansible-galaxy collection install -r requirements.yml` using the format:

```yaml
---
collections:
  - name: community.yang
```

### Platforms test against
    1. Cisco IOSXR 6.1.3

### Using modules from the yang Collection in your playbooks

It's preferable to use content in this collection using their Fully Qualified Collection Namespace (FQCN), for example `community.yang.configure`:

```yaml
---
- hosts: iosxr
  gather_facts: false
  connection: ansible.netcommon.netconf

  tasks:
    - name: "Fetch given yang model and all the dependent models from remote host"
      community.yang.fetch:
        name: Cisco-IOS-XR-ifmgr-cfg

    - name: get interface configuration in json/xml format
      community.yang.get:
        filter: |
          <interface-configurations xmlns="http://cisco.com/ns/yang/Cisco-IOS-XR-ifmgr-cfg"><interface-configuration>
          </interface-configuration></interface-configurations>
        file: "./files/cisco/iosxr/*.yang"
        search_path: "./files/cisco/iosxr"
      register: result

    - name: Configure interface description providing json input file
      community.yang.configure:
        config: "{{ lookup('file', config_file) }}"
        file: "{{ yang_file }}"
        search_path: "{{ search_path }}"
      register: result

    - name: Configure interface description with json input
      community.yang.configure:
        config:
          {
              "Cisco-IOS-XR-ifmgr-cfg:interface-configurations": {
                  "interface-configuration": [
                      {
                          "active": "act",
                          "description": "test for ansible 400",
                          "interface-name": "Loopback888",
                          "interface-virtual": [
                              null
                          ],
                          "shutdown": [
                              null
                          ]
                      },
                      {
                          "active": "act",
                          "description": "This interface is configures with Ansible",
                          "interface-name": "GigabitEthernet0/0/0/4"
                      }
                  ]
              }
          }
        file: "{{ yang_file }}"
        search_path: "{{ search_path }}"
      register: result

    - name: generate spec from open-config interface yang model data and represent in xml, json and yang tree
      community.yang.generate_spec:
        file: "{{ spec_yang_file }}"
        search_path: "{{ spec_search_path }}"
        doctype: config
        json_schema:
          path: "./output/{{ inventory_hostname }}/openconfig-interfaces-config.json"
          defaults: True
        xml_schema:
          path: "./output/{{ inventory_hostname }}/openconfig-interfaces-config.xml"
          defaults: True
          annotations: True
        tree_schema:
          path: "./output/{{ inventory_hostname }}/openconfig-interfaces-config.tree"t
```
For documentation on how to use individual modules and other content included in this collection, please see the links in the 'Included content' section earlier in this README.

## Testing and Development

If you want to develop new content for this collection or improve what's already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

### Testing with `ansible-test`

The `tests` directory contains configuration for running sanity and integration tests using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).

To run these network integration tests, use ansible-test network-integration --inventory </path/to/inventory> <tests_to_run>:

    ansible-test network-integration  --inventory ~/myinventory -vvv <name of the plugin>


## Publishing New Versions

Releases are automatically built and pushed to Ansible Galaxy for any new tag. Before tagging a release, make sure to do the following:

  1. Update `galaxy.yml` and this README's `requirements.yml` example with the new `version` for the collection.
  2. Update the CHANGELOG:
    1. Make sure you have [`antsibull-changelog`](https://pypi.org/project/antsibull-changelog/) installed.
    2. Make sure there are fragments for all known changes in `changelogs/fragments`.
    3. Run `antsibull-changelog release`.
  3. Commit the changes and create a PR with the changes. Wait for tests to pass, then merge it once they have.
  4. Tag the version in Git and push to GitHub.
     ```
After the version is published, verify it exists on the [Ansible Yang Community Collection Galaxy page](https://galaxy.ansible.com/community/yang).


### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Ansible Yang collection repository](https://github.com/ansible-collections/community.yang).

1. Make changes
2. Detail changes in a [fragment](changelogs/fragments). [example](https://github.com/ansible-collections/community.yang/pull/58/files)
3. Submit PR

You can also join us on:

- IRC - the ``#ansible-network`` [libera.chat](https://libera.chat/) channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.


## Changelogs

[Change log](changelogs/CHANGELOG.rst)

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [LICENSE](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
