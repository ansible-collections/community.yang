# (c) 2020 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
lookup: xml2json
author: Ganesh Nalawade (@ganeshrn)
short_description: Converts xml input to json structure output by mapping it against corresponding Yang model
description:
  - This plugin lookups the input xml data, typically Netconf rpc response received from remote host
    and convert it to json format as defined by RFC 7951 JSON Encoding of Data Modeled with YANG
options:
  _terms:
    description:
      - Input xml file path that adheres to a given yang model. This can be a Netconf/Restconf xml rpc response
        that contains operational and configuration data received from remote host.
    required: True
    type: path
  yang_file:
    description:
      - Path to yang model file against which the xml file is validated and converted to json as per json encoding
        of data modeled with YANG.
    required: True
    type: path
  search_path:
    description:
      - This option is a colon C(:) separated list of directories to search for imported yang modules
        in the yang file mentioned in C(path) option. If the value is not given it will search in
        the current directory.
    required: false
  keep_tmp_files:
    description:
      - This is a boolean flag to indicate if the intermediate files generated while validation json
       configuration should be kept or deleted. If the value is C(true) the files will not be deleted else by
        default all the intermediate files will be deleted irrespective of whether task run is
        successful or not. The intermediate files are stored in path C(~/.ansible/tmp/json2xml), this
        option is mainly used for debugging purpose.
    default: False
    type: bool
"""

EXAMPLES = """
- name: translate json to xml
  debug: msg="{{ lookup('community.yang.xml2json', interfaces_config.xml,
                         yang_file='openconfig/public/release/models/interfaces/openconfig-interfaces.yang',
                         search_path='openconfig/public/release/models:pyang/modules/') }}"
"""

RETURN = """
_raw:
   description: The translated json structure from xml
"""

from ansible.plugins.lookup import LookupBase
from ansible.errors import AnsibleLookupError
from ansible.module_utils.six import raise_from
from ansible.module_utils._text import to_text

from ansible_collections.community.yang.plugins.module_utils.translator import (
    Translator,
)

from ansible_collections.community.yang.plugins.common.base import (
    create_tmp_dir,
    XM2JSON_DIR_PATH,
)

try:
    import pyang  # noqa
except ImportError as imp_exc:
    PYANG_IMPORT_ERROR = imp_exc
else:
    PYANG_IMPORT_ERROR = None

from ansible.utils.display import Display

display = Display()


class LookupModule(LookupBase):
    def _debug(self, msg):
        """Output text using ansible's display

        :param msg: The message
        :type msg: str
        """
        msg = "[xml2json][lookup] {msg}".format(msg=msg)
        display.vvvv(msg)

    def run(self, terms, variables, **kwargs):
        if PYANG_IMPORT_ERROR:
            raise_from(
                AnsibleLookupError(
                    "pyang must be installed to use this plugin"
                ),
                PYANG_IMPORT_ERROR,
            )

        res = []
        try:
            xml_file = terms[0]
        except IndexError:
            raise AnsibleLookupError("path to xml file must be specified")

        try:
            yang_file = kwargs["yang_file"]
        except KeyError:
            raise AnsibleLookupError("value of 'yang_file' must be specified")

        search_path = kwargs.pop("search_path", "")
        keep_tmp_files = kwargs.pop("keep_tmp_files", False)

        try:
            tmp_dir_path = create_tmp_dir(XM2JSON_DIR_PATH)

            tl = Translator(
                yang_file,
                search_path=search_path,
                keep_tmp_files=keep_tmp_files,
                debug=self._debug,
            )

            json_data = tl.xml_to_json(xml_file, tmp_dir_path)
        except ValueError as exc:
            raise AnsibleLookupError(
                to_text(exc, errors="surrogate_then_replace")
            )
        except Exception as exc:
            raise AnsibleLookupError(
                "Unhandled exception from [lookup][xml2json]. Error: {err}".format(
                    err=to_text(exc, errors="surrogate_then_replace")
                )
            )

        res.append(json_data)

        return res
