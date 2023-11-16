# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function


__metaclass__ = type

import os
import sys


try:
    import importlib.util

    imp = None
except ImportError:
    import imp

from ansible.module_utils._text import to_bytes, to_native


def to_list(val):
    if isinstance(val, (list, tuple, set)):
        return list(val)
    elif val is not None:
        return [val]
    else:
        return list()


def find_file_in_path(filename):
    # Check $PATH first, followed by same directory as sys.argv[0]
    paths = os.environ["PATH"].split(os.pathsep) + [
        os.path.dirname(sys.argv[0]),
    ]
    for dirname in paths:
        fullpath = os.path.join(dirname, filename)
        if os.path.isfile(fullpath):
            return fullpath


def find_share_path(filename):
    # Check $PATH first, followed by same directory as sys.argv[0]
    paths = os.environ["PATH"].split(os.pathsep) + [
        os.path.dirname(sys.argv[0]),
    ]
    for dirname in paths:
        env_path = os.sep.join(dirname.split(os.sep)[:-1])
        share_path = os.path.join(env_path, "share")
        if os.path.isfile(os.path.join(share_path, filename)):
            return share_path


def load_from_source(path, name):
    if imp is None:
        loader = importlib.machinery.SourceFileLoader(name, path)
        module = loader.load_module()
        sys.modules[name] = module
    else:
        with open(to_bytes(path), "rb") as module_file:
            # to_native is used here because imp.load_source's path is for tracebacks and python's traceback formatting uses native strings
            module = imp.load_source(
                to_native(name),
                to_native(path),
                module_file,
            )
    return module
