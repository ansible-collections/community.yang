# (c) 2020, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.plugins.action import ActionBase
import os
from ansible.errors import AnsibleError

from ansible.module_utils._text import to_text
YANG_SPEC_DIR_PATH = "~/.ansible/tmp/yang_spec"
from ansible_collections.community.yang.plugins.lookup.spec import (
    LookupModule,
)

class ActionModule(ActionBase):
    def run(self, terms=None, variables=None, **kwargs):

        result = super(ActionModule, self).run(terms, variables)

        # Read and validate yang file path
        try:
            yang_file = self._task.args["file"]
        except KeyError as exc:
            return {
                "failed": True,
                "msg": "missing required argument: %s" % exc,
            }

        yang_file = os.path.realpath(os.path.expanduser(yang_file))
        if not os.path.isfile(yang_file):
            raise AnsibleError('%s invalid file path' % yang_file)

        # Read search_path and validate

        if "search_path" in self._task.args:
            search_path = self._task.args["search_path"]
        else:
            search_path = YANG_SPEC_DIR_PATH
        if search_path:
            for path in search_path.split(':'):
                path = os.path.realpath(os.path.expanduser(path))
                if path != '' and not os.path.isdir(path):
                    raise AnsibleError('%s is invalid directory path' % path)

        # Read and validate doctype file path
        if "doctype" in self._task.args:
            doctype = self._task.args["doctype"]
        else:
            doctype = "config"

        valid_doctype = ['config', 'data']
        if doctype not in valid_doctype:
            raise AnsibleError('doctype value %s is invalid, valid value are %s' % (doctype, ', '.join(valid_doctype)))

        if "xml_schema" in self._task.args:
            xml_schema = self._task.args["xml_schema"]
        else:
            xml_schema = {}

        if "tree_schema" in self._task.args:
            tree_schema = self._task.args["tree_schema"]
        else:
            tree_schema = {}

        if "json_schema" in self._task.args:
            json_schema = self._task.args["json_schema"]
        else:
            json_schema = {}

        lm = LookupModule()
        try:
            schema_output = lm.run(
                'community.yang.spec',
                yang_file=yang_file,
                search_path=search_path,
                defaults=True,
                doctype=doctype,
                xml_schema=xml_schema,
                tree_schema=tree_schema,
                json_schema=json_schema)
        except ValueError as exc:
            return {"failed": True, "msg": to_text(exc)}
        result["xml_schema"] = schema_output["xml_skeleton"]
        result["json_schema"] = schema_output["json_skeleton"]
        result["tree_schema"] = schema_output["tree"]
        return result
