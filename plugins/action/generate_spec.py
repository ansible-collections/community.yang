# (c) 2020, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
from ansible.plugins.action import ActionBase
import os
from ansible.module_utils._text import to_bytes
from ansible.module_utils import basic
from ansible.errors import AnsibleActionFail
from ansible_collections.community.yang.plugins.module_utils.spec import (
    GenerateSpec,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    convert_doc_to_ansible_module_kwargs,
    dict_merge,
)
from ansible_collections.community.yang.plugins.modules.generate_spec import (
    DOCUMENTATION,
)


ARGSPEC_CONDITIONALS = {
    "required_one_of": [["file", "content"]],
    "mutually_exclusive": [["file", "content"]],
}


def generate_argspec():
    """ Generate an argspec
    """
    argspec = convert_doc_to_ansible_module_kwargs(DOCUMENTATION)
    argspec = dict_merge(argspec, ARGSPEC_CONDITIONALS)
    return argspec


class ActionModule(ActionBase):
    def __init__(self, *args, **kwargs):
        super(ActionModule, self).__init__(*args, **kwargs)
        self._result = {}

    def _fail_json(self, msg):
        """ Replace the AnsibleModule fai_json here
        :param msg: The message for the failure
        :type msg: str
        """
        msg = msg.replace("(basic.py)", self._task.action)
        raise AnsibleActionFail(msg)

    def _check_argspec(self):
        """ Load the doc and convert
        Add the root conditionals to what was returned from the conversion
        and instantiate an AnsibleModule to validate
        """
        argspec = generate_argspec()
        basic._ANSIBLE_ARGS = to_bytes(
            json.dumps({"ANSIBLE_MODULE_ARGS": self._task.args})
        )
        basic.AnsibleModule.fail_json = self._fail_json
        basic.AnsibleModule(**argspec)

    def _extended_check_argspec(self):
        """ Check additional requirements for the argspec
        that cannot be covered using stnd techniques
        """
        errors = []
        yang_file = self._task.args.get("file") or None
        if yang_file and not os.path.isfile(yang_file):
            msg = "%s invalid file path" % yang_file
            errors.append(msg)

        if "search_path" in self._task.args:
            search_path = self._task.args["search_path"]
            for path in search_path.split(":"):
                path = os.path.realpath(os.path.expanduser(path))
                if path != "" and not os.path.isdir(path):
                    msg = "%s is invalid directory path" % path
                    errors.append(msg)
        if errors:
            self._result["failed"] = True
            self._result["msg"] = " ".join(errors)

    def run(self, tmp=None, task_vars=None):
        """

        :param terms:
        :param variables:
        :param kwargs:
        :return:
        """
        self._check_argspec()
        self._extended_check_argspec()
        if self._result.get("failed"):
            return self._result
        result = super(ActionModule, self).run(tmp, task_vars)

        yang_file = self._task.args.get("file") or None
        yang_content = self._task.args.get("content") or None
        search_path = self._task.args.get("search_path") or None
        doctype = self._task.args.get("doctype") or "config"
        xml_schema = self._task.args.get("xml_schema") or {}
        tree_schema = self._task.args.get("tree_schema") or {}
        json_schema = self._task.args.get("json_schema") or {}

        genspec_obj = GenerateSpec(
            yang_content=yang_content,
            yang_file_path=yang_file,
            search_path=search_path,
            doctype=doctype,
        )
        defaults = False
        schema_out_path = None
        if json_schema:
            if "defaults" in json_schema:
                defaults = json_schema["defaults"]
            if "path" in json_schema:
                schema_out_path = json_schema["path"]
        result["json_schema"] = genspec_obj.generate_json_schema(
            schema_out_path=schema_out_path, defaults=defaults
        )
        defaults = False
        schema_out_path = None
        annotations = False

        if xml_schema:
            if "defaults" in xml_schema:
                defaults = xml_schema["defaults"]
            if "path" in xml_schema:
                schema_out_path = xml_schema["path"]
            if "annotations" in xml_schema:
                annotations = xml_schema["annotations"]
        result["xml_schema"] = genspec_obj.generate_xml_schema(
            schema_out_path=schema_out_path,
            defaults=defaults,
            annotations=annotations,
        )
        schema_out_path = None
        if tree_schema and "path" in tree_schema:
            schema_out_path = tree_schema["path"]
        result["tree_schema"] = genspec_obj.generate_tree_schema(
            schema_out_path=schema_out_path
        )

        return result
