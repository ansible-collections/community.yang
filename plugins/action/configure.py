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
from ansible.module_utils._text import to_bytes, to_text
from ansible.module_utils import basic
from ansible.errors import AnsibleActionFail

try:
    from lxml.etree import tostring, fromstring, XMLParser
except ImportError:
    from xml.etree.ElementTree import tostring, fromstring

from ansible.module_utils.connection import (
    ConnectionError as AnsibleConnectionError,
)
from ansible_collections.ansible.netcommon.plugins.module_utils.network.common.utils import (
    convert_doc_to_ansible_module_kwargs,
)
from ansible_collections.community.yang.plugins.modules.configure import (
    DOCUMENTATION,
)
from ansible_collections.community.yang.plugins.module_utils.translator import (
    Translator,
)
from ansible_collections.community.yang.plugins.common.base import (
    create_tmp_dir,
    JSON2XML_DIR_PATH,
)

VALID_CONNECTION_TYPES = ["ansible.netcommon.netconf"]


def generate_argspec():
    """ Generate an argspec
    """
    argspec = convert_doc_to_ansible_module_kwargs(DOCUMENTATION)
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

    def _debug(self, msg):
        """Output text using ansible's display

        :param msg: The message
        :type msg: str
        """
        msg = "<{phost}> [configure][action] {msg}".format(
            phost=self._playhost, msg=msg
        )
        self._display.vvvv(msg)

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
        config = json.dumps(self._task.args.get("config"))
        try:
            # validate json
            json.loads(config)
        except Exception as exc:
            msg = "Failed to load json configuration: %s" % (
                to_text(exc, errors="surrogate_or_strict")
            )
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
        """

        :param terms:
        :param variables:
        :param kwargs:
        :return:
        """
        if self._play_context.connection.split(".")[-1] != "netconf":
            return {
                "failed": True,
                "msg": "Connection type %s is not valid for this module. Valid connection type is one of '%s'."
                % (
                    self._play_context.connection,
                    ", ".join(VALID_CONNECTION_TYPES),
                ),
            }
        self._playhost = task_vars.get("inventory_hostname")

        self._check_argspec()
        self._extended_check_argspec()
        if self._result.get("failed"):
            return self._result
        result = super(ActionModule, self).run(tmp, task_vars)

        json_config = self._task.args.get("config")

        yang_files = self._task.args.get("file", [])
        search_path = self._task.args.get("search_path") or None
        if not (
            hasattr(self._connection, "socket_path")
            and self._connection.socket_path is not None
        ):
            raise AnsibleConnectionError(
                "netconf connection to remote host in not active"
            )

        try:
            tmp_dir_path = create_tmp_dir(JSON2XML_DIR_PATH)
            tl = Translator(yang_files, search_path, debug=self._debug)
            xml_data = tl.json_to_xml(json_config, tmp_dir_path)
        except ValueError as exc:
            raise AnsibleActionFail(
                to_text(exc, errors="surrogate_then_replace")
            )
        except Exception as exc:
            raise AnsibleActionFail(
                "Unhandled exception from [action][configure]. Error: {err}".format(
                    err=to_text(exc, errors="surrogate_then_replace")
                )
            )

        parser = XMLParser(ns_clean=True, recover=True, encoding="utf-8")
        xml_data = fromstring(xml_data, parser=parser)
        xml_data = to_text(tostring(xml_data))
        module = "ansible.netcommon.netconf_config"

        if not self._shared_loader_obj.module_loader.has_plugin(module):
            result.update(
                {"failed": True, "msg": "Could not find %s module." % module}
            )
        else:
            new_module_args = self._task.args.copy()
            if "netconf_options" in self._task.args:
                new_module_args.update(
                    self._task.args["netconf_options"].copy()
                )
            new_module_args["content"] = xml_data

            for item in ["file", "search_path", "config", "netconf_options"]:
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
        result.pop("server_capabilities", None)
        return result
