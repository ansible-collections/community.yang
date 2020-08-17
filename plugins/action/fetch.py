# (c) 2020, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#
from __future__ import absolute_import, division, print_function

__metaclass__ = type

from ansible.plugins.action import ActionBase
from ansible.module_utils._text import to_text
from ansible.module_utils.connection import Connection
from ansible_collections.community.yang.plugins.module_utils.fetch import (
    SchemaStore,
)


class ActionModule(ActionBase):
    def run(self, tmp=None, task_vars=None):
        if task_vars is None:
            task_vars = dict()

        result = super(ActionModule, self).run(tmp, task_vars)

        try:
            schema = self._task.args["schema"]
        except KeyError as exc:
            return {
                "failed": True,
                "msg": "missing required argument: %s" % exc,
            }

        socket_path = self._connection.socket_path
        conn = Connection(socket_path)

        ss = SchemaStore(conn)

        result["fetched"] = dict()
        try:
            changed, counter = ss.run(schema, result)
        except ValueError as exc:
            return {"failed": True, "msg": to_text(exc)}

        result["changed"] = changed
        result["number_schema_fetched"] = counter
        return result
