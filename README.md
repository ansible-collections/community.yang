# Ansible Collection - community.yang

This repo hosts the `community.yang` Ansible Collection.

The collection includes the community plugins to help the support Yang manily with network devices.

<!--start requires_ansible-->
## Ansible version compatibility

This collection has been tested against following Ansible versions: **>=2.9.10,<2.11**.

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
collections:
- name: community.yang
```


## Testing and Development

If you want to develop new content for this collection or improve what's already here, the easiest way to work on the collection is to clone it into one of the configured [`COLLECTIONS_PATHS`](https://docs.ansible.com/ansible/latest/reference_appendices/config.html#collections-paths), and work on it there.

### Testing with `ansible-test`

The `tests` directory contains configuration for running sanity and integration tests using [`ansible-test`](https://docs.ansible.com/ansible/latest/dev_guide/testing_integration.html).

To run these network integration tests, use ansible-test network-integration --inventory </path/to/inventory> <tests_to_run>:

    ansible-test network-integration  --inventory ~/myinventory -vvv <name of the plugin>


## Publishing New Version

The current process for publishing new versions of the Community Collection is manual, and requires a user who has access to the `community` namespace on Ansible Galaxy to publish the build artifact.

  1. Ensure `CHANGELOG.md` contains all the latest changes.
  2. Update `galaxy.yml` with the new `version` for the collection.
  3. Create a release in GitHub to tag the commit at the version to build.
  4. Run the following commands to build and release the new version on Galaxy:

     ```
     ansible-galaxy collection build
     ansible-galaxy collection publish ./community-yang-$VERSION_HERE.tar.gz
     ```

After the version is published, verify it exists on the [Ansible Yang Community Collection Galaxy page](https://galaxy.ansible.com/community/yang).


### See Also:

* [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

## Contributing to this collection

We welcome community contributions to this collection. If you find problems, please open an issue or create a PR against the [Ansible Yang collection repository](https://github.com/ansible-collections/community.yang).

You can also join us on:

- Freenode IRC - ``#ansible-network`` Freenode channel
- Slack - https://ansiblenetwork.slack.com

See the [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html) for details on contributing to Ansible.


## Changelogs
<!--Add a link to a changelog.md file or an external docsite to cover this information. -->

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
