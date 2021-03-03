# (c) 2020 Red Hat, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import, division, print_function

__metaclass__ = type

DOCUMENTATION = """
lookup: json2xml
author: Ganesh Nalawade (@ganeshrn)
short_description: Validates json configuration against yang data model and convert it to xml.
description:
  - This plugin lookups the input json configuration, validates it against the respective yang data
    model which is also given as input to this plugin and coverts it to xml format which can be used
    as payload within Netconf rpc.
options:
  _terms:
    description:
      - Input json configuration file path that adheres to a particular yang model.
    required: True
    type: path
  doctype:
    description:
      - Specifies the target root node of the generated xml. The default value is C(config)
    default: config
  yang_file:
    description:
      - Path to yang model file against which the json configuration is validated and
        converted to xml.
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
  debug: msg="{{ lookup('yang_json2xml', config_json,
                         yang_file='openconfig/public/release/models/interfaces/openconfig-interfaces.yang',
                         search_path='openconfig/public/release/models:pyang/modules/') }}"
"""

RETURN = """
_raw:
   description: The translated xml string from json
"""

import os
import json

from ansible.plugins.lookup import LookupBase
from ansible.module_utils.six import raise_from
from ansible.module_utils._text import to_text
from ansible.errors import AnsibleLookupError

from ansible_collections.community.yang.plugins.module_utils.translator import (
    Translator,
)

try:
    import pyang  # noqa
except ImportError as imp_exc:
    PYANG_IMPORT_ERROR = imp_exc
else:
    PYANG_IMPORT_ERROR = None


from ansible.utils.display import Display

from ansible_collections.community.yang.plugins.common.base import (
    create_tmp_dir,
    JSON2XML_DIR_PATH,
)

display = Display()


class LookupModule(LookupBase):
    def _debug(self, msg):
        """Output text using ansible's display

        :param msg: The message
        :type msg: str
        """
        msg = "[json2xml][lookup] {msg}".format(msg=msg)
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
            json_config = terms[0]
        except IndexError:
            raise AnsibleLookupError("path to json file must be specified")

        try:
            yang_file = kwargs["yang_file"]
        except KeyError:
            raise AnsibleLookupError("value of 'yang_file' must be specified")

        search_path = kwargs.pop("search_path", "")
        keep_tmp_files = kwargs.pop("keep_tmp_files", False)

        json_config = os.path.realpath(os.path.expanduser(json_config))
        try:
            # validate json
            with open(json_config) as fp:
                json.load(fp)
        except Exception as exc:
            raise AnsibleLookupError(
                "Failed to load json configuration: %s"
                % (to_text(exc, errors="surrogate_or_strict"))
            )

        try:
            tmp_dir_path = create_tmp_dir(JSON2XML_DIR_PATH)
            doctype = kwargs.get("doctype", "config")

            tl = Translator(
                yang_file,
                search_path,
                doctype,
                keep_tmp_files,
                debug=self._debug,
            )

            xml_data = tl.json_to_xml(json_config, tmp_dir_path)
        except ValueError as exc:
            raise AnsibleLookupError(
                to_text(exc, errors="surrogate_then_replace")
            )
        except Exception as exc:
            raise AnsibleLookupError(
                "Unhandled exception from [lookup][json2xml]. Error: {err}".format(
                    err=to_text(exc, errors="surrogate_then_replace")
                )
            )

        res.append(xml_data)

        return res
