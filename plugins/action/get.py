# (c) 2020, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import json
import glob
import os

from ansible.plugins.action import ActionBase
from ansible.module_utils._text import to_bytes
from ansible.module_utils import basic
from ansible.module_utils.connection import (
    ConnectionError as AnsibleConnectionError,
)
from ansible.errors import AnsibleActionFail
from ansible_collections.community.yang.plugins.module_utils.translator import (
    Translator,
)

from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    convert_doc_to_ansible_module_kwargs,
)
from ansible_collections.community.yang.plugins.modules.get import (
    DOCUMENTATION,
)


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
        argspec = convert_doc_to_ansible_module_kwargs(DOCUMENTATION)
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
        yang_file = self._task.args.get("file")
        if yang_file:
            yang_file = os.path.realpath(os.path.expanduser(yang_file))
            if not os.path.isfile(yang_file):
                # Maybe we are passing a glob?
                _yang_files = glob.glob(yang_file)
                if not _yang_files:
                    msg = "%s invalid yang_file path" % yang_file
                    errors.append(msg)

        if "search_path" in self._task.args:
            search_path = self._task.args["search_path"]
            for path in search_path.split(":"):
                path = os.path.realpath(os.path.expanduser(path))
                if path != "" and not os.path.isdir(path):
                    msg = "%s is invalid search_path directory" % path
                    errors.append(msg)
        if errors:
            self._result["failed"] = True
            self._result["msg"] = " ".join(errors)

    def run(self, tmp=None, task_vars=None):
        self._check_argspec()
        self._extended_check_argspec()
        if self._result.get("failed"):
            return self._result
        result = super(ActionModule, self).run(tmp, task_vars)

        yang_file = self._task.args.get("file")
        search_path = self._task.args.get("search_path")

        if not (
            hasattr(self._connection, "socket_path")
            and self._connection.socket_path is not None
        ):
            raise AnsibleConnectionError(
                "netconf connection to remote host in not active"
            )

        module = "ansible.netcommon.netconf_get"

        if not self._shared_loader_obj.module_loader.has_plugin(module):
            result.update(
                {"failed": True, "msg": "Could not find %s module." % module}
            )
        else:
            new_module_args = self._task.args.copy()
            for item in ["file", "search_path"]:
                new_module_args.pop(item, None)

            self._display.vvvv(
                "Running %s module to fetch data from remote host" % module
            )
            result.update(
                self._execute_module(
                    module_name=module,
                    module_args=new_module_args,
                    task_vars=task_vars,
                    wrap_async=self._task.async_val,
                )
            )

        # convert XML data to JSON data as per RFC 7951 format
        tl = Translator(yang_file, search_path=search_path)

        result["json_data"] = tl.xml_to_json(result["stdout"])
        result["xml_data"] = result["stdout"]
        result.pop("stdout", None)
        result.pop("stdout_lines", None)
        return result
