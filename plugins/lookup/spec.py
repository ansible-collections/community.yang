# (c) 2020 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.

from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
    lookup: spec
    author: Ganesh Nalawade (@ganeshrn)
    short_description:  This plugin reads the content of given yang document and generates json and xml
                        configuration skeleton and a tree structure of yang document.
    description:
      - This plugin parses yang document and generates json and xml configuration skeleton and a tree
        structure of yang document. The tree structure document is as per RFC 8340 which helps to consume
        the yang document along with json and xml configuration skeleton.
    options:
      _terms:
        description: The path points to the location of the top level yang module which
                      is to be transformed into to Ansible spec.
        required: True
        type: str
      search_path:
        description:
          - is a colon C(:) separated list of directories to search for imported yang modules
            in the yang file mentioned in C(path) option. If the value is not given it will search in
            the same directory as that of C(yang_file).
        type: path
      defaults:
        description:
          - This boolean flag indicates if the generated json and xml configuration schema should have
            fields initialized with default values or not.
        default: False
      doctype:
        description:
          - Identifies the root node of the configuration skeleton. If value is C(config) only configuration
            data will be present in skeleton, if value is C(data) both config and state data fields will be present
            in output.
        default: config
        choices: ['config', 'data']
        type: bool
      annotations:
        description:
          - The boolean flag identifies if the xml skeleton should have comments describing the field or not.
        default: False
        type: bool
      keep_tmp_files:
        description:
          - This is a boolean flag to indicate if the intermediate files generated while creating spec
            should be kept or deleted. If the value is C(true) the files will not be deleted else by
            default all the intermediate files will be deleted irrespective of whether task run is
            successful or not. The intermediate files are stored in path C(~/.ansible/tmp/yang/spec), this
            option is mainly used for debugging purpose.
        default: False
        type: bool
"""

EXAMPLES = """
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
"""

RETURN = """
  _list:
    description:
      - It returns json skeleton configuration schema, xml skeleton schema and tree structure (as per RFC 8340)
        for given yang schema.
    type: complex
    contains:
      tree:
        description: The tree representation of yang scehma as per RFC 8340
        returned: success
        type: dict
        sample: |
            module: openconfig-interfaces
              +--rw interfaces
                 +--rw interface* [name]
                    +--rw name             -> ../config/name
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
                    |  +--ro last-change?     oc-types:timeticks64
      json_skeleton:
        description: The json configuration skeleton generated from yang document
        returned: success
        type: dict
        sample: |
            {
                "openconfig-interfaces:interfaces": {
                    "interface": [
                        {
                            "hold-time": {
                                "config": {
                                    "down": "",
                                    "up": ""
                                }
                            },
                            "config": {
                                "description": "",
                                "type": "",
                                "enabled": "",
                                "mtu": "",
                                "loopback-mode": "",
                                "name": ""
                            },
                            "name": "",
                            "subinterfaces": {
                                "subinterface": [
                                    {
                                        "index": "",
                                        "config": {
                                            "index": "",
                                            "enabled": "",
                                            "description": ""
                                        }
                                    }
                                ]
                            }
                        }
                    ]
                }
      xml_skeleton:
        description: The xml configuration skeleton generated from yang document
        returned: success
        type: dict
        sample: |
            <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
              <interfaces xmlns="http://openconfig.net/yang/interfaces">
                <interface>
                  <name/>
                  <config>
                    <name/>
                    <type/>
                    <mtu/>
                    <loopback-mode></loopback-mode>
                    <description/>
                    <enabled>True</enabled>
                  </config>
                  <hold-time>
                    <config>
                      <up></up>
                      <down></down>
                    </config>
                  </hold-time>
                  <subinterfaces>
                    <subinterface>
                      <index/>
                      <config>
                        <index></index>
                        <description/>
                        <enabled></enabled>
                      </config>
                    </subinterface>
                  </subinterfaces>
                </interface>
              </interfaces>
            </config>
"""
import os
from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleLookupError
from ansible.module_utils._text import to_text
from ansible_collections.community.yang.plugins.module_utils.spec import (
    GenerateSpec,
)
from ansible_collections.community.yang.plugins.common.base import (
    create_tmp_dir,
    YANG_SPEC_DIR_PATH,
)

from ansible.utils.display import Display

display = Display()


class LookupModule(LookupBase):
    def run(self, terms, variables, **kwargs):

        res = []
        output = {}
        try:
            yang_file = terms[0]
        except IndexError:
            raise AnsibleLookupError("value of 'yang_file' must be specified")

        yang_file = os.path.realpath(os.path.expanduser(yang_file))
        if not os.path.isfile(yang_file):
            raise AnsibleLookupError("%s invalid file path" % yang_file)

        search_path = kwargs.pop("search_path", "")

        for path in search_path.split(":"):
            path = os.path.realpath(os.path.expanduser(path))
            if path != "" and not os.path.isdir(path):
                raise AnsibleLookupError("%s is invalid directory path" % path)

        keep_tmp_files = kwargs.pop("keep_tmp_files", False)
        defaults = kwargs.pop("defaults", False)
        annotations = kwargs.pop("annotations", False)
        doctype = kwargs.pop("doctype", "config")

        valid_doctype = ["config", "data"]
        if doctype not in valid_doctype:
            raise AnsibleLookupError(
                "doctype value %s is invalid, valid value are %s"
                % (path, ", ".join(valid_doctype))
            )

        try:
            tmp_dir_path = create_tmp_dir(YANG_SPEC_DIR_PATH)

            genspec_obj = GenerateSpec(
                yang_file_path=yang_file,
                search_path=search_path,
                doctype=doctype,
                keep_tmp_files=keep_tmp_files,
                tmp_dir_path=tmp_dir_path,
            )
            output["json_skeleton"] = genspec_obj.generate_json_schema(
                defaults=defaults
            )
            defaults = False

            output["xml_skeleton"] = genspec_obj.generate_xml_schema(
                defaults=defaults, annotations=annotations
            )
            output["tree"] = genspec_obj.generate_tree_schema()

            res.append(output)
        except ValueError as exc:
            raise AnsibleLookupError(
                to_text(exc, errors="surrogate_then_replace")
            )
        except Exception as exc:
            raise AnsibleLookupError(
                "Unhandled exception from [lookup][spec]. Error: {err}".format(
                    err=to_text(exc, errors="surrogate_then_replace")
                )
            )

        return res
