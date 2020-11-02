# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import optparse
import json

from ansible.module_utils.common._collections_compat import Sequence
from ansible.module_utils.basic import missing_required_lib

try:
    from pyang import plugin, error

    HAS_PYANG = True
except ImportError:
    HAS_PYANG = False


def to_list(val):
    if isinstance(val, Sequence):
        return list(val)
    elif val is not None:
        return [val]
    else:
        return list()


class SampleJSONSkeletonPlugin(plugin.PyangPlugin):
    def add_opts(self, optparser):
        optlist = [
            optparse.make_option(
                "--sample-json-skeleton-doctype",
                dest="doctype",
                default="data",
                help="Type of sample JSON document " + "(data or config).",
            ),
            optparse.make_option(
                "--sample-json-skeleton-defaults",
                action="store_true",
                dest="sample_defaults",
                default=False,
                help="Insert data with defaults values.",
            ),
        ]
        g = optparser.add_option_group(
            "Sample-json-skeleton output specific options"
        )
        g.add_options(optlist)

    def add_output_format(self, fmts):
        self.multiple_modules = True
        fmts["sample-json-skeleton"] = self

    def setup_fmt(self, ctx):
        ctx.implicit_errors = False

    def emit(self, ctx, modules, fd):
        """Main control function.
        """
        for (epos, etag, eargs) in ctx.errors:
            if error.is_error(error.err_level(etag)):
                raise error.EmitError(
                    "sample-json-skeleton plugin needs a valid module"
                )
        tree = {}
        self.defaults = ctx.opts.sample_defaults
        self.doctype = ctx.opts.doctype
        if self.doctype not in ("config", "data"):
            raise error.EmitError(
                "Unsupported document type: %s" % self.doctype
            )

        for module in modules:
            self.process_children(module, tree, None)
        json.dump(tree, fd, indent=4)

    def process_children(self, node, parent, pmod):
        """Process all children of `node`, except "rpc" and "notification".
        """
        for ch in node.i_children:
            if self.doctype == "config" and not ch.i_config:
                continue
            if ch.keyword in ["rpc", "notification"]:
                continue
            if ch.keyword in ["choice", "case"]:
                self.process_children(ch, parent, pmod)
                continue
            if ch.i_module.i_modulename == pmod:
                nmod = pmod
                nodename = ch.arg
            else:
                nmod = ch.i_module.i_modulename
                nodename = "%s:%s" % (nmod, ch.arg)
            if ch.keyword == "container":
                ndata = dict()
                self.process_children(ch, ndata, nmod)
                parent[nodename] = ndata
            elif ch.keyword == "list":
                ndata = list()
                ndata.append({})
                self.process_children(ch, ndata[0], nmod)
                parent[nodename] = ndata
            elif ch.keyword == "leaf":
                if ch.arg == "keepalive-interval":
                    pass
                ndata = (
                    str(ch.i_default)
                    if (self.defaults and ch.i_default is not None)
                    else ""
                )
            elif ch.keyword == "leaf-list":
                ndata = (
                    to_list(str(ch.i_default))
                    if (self.defaults and ch.i_default is not None)
                    else [""]
                )
            parent[nodename] = ndata

    def base_type(self, type):
        """Return the base type of `type`."""
        while 1:
            if type.arg == "leafref":
                node = type.i_type_spec.i_target_node
            elif type.i_typedef is None:
                break
            else:
                node = type.i_typedef
            type = node.search_one("type")
        if type.arg == "decimal64":
            return [type.arg, int(type.search_one("fraction-digits").arg)]
        elif type.arg == "union":
            return [
                type.arg,
                [self.base_type(x) for x in type.i_type_spec.types],
            ]
        else:
            return type.arg


def pyang_plugin_init():
    if not HAS_PYANG:
        raise ImportError(missing_required_lib("pyang"))
    plugin.register_plugin(SampleJSONSkeletonPlugin())
