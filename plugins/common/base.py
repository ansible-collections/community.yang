# (c) 2020, Ansible by Red Hat, inc
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import os
import uuid

from ansible.utils.path import makedirs_safe, unfrackpath


JSON2XML_DIR_PATH = "~/.ansible/tmp/yang/json2xml"
XM2JSON_DIR_PATH = "~/.ansible/tmp/xml2json"
YANG_SPEC_DIR_PATH = "~/.ansible/tmp/yang/spec"


def create_tmp_dir(dir_path):
    plugin_instance = str(uuid.uuid4())
    plugindir = unfrackpath(dir_path)
    makedirs_safe(plugindir)
    tmp_dir_path = os.path.join(plugindir, plugin_instance)
    makedirs_safe(tmp_dir_path)
    return tmp_dir_path
