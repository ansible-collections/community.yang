# -*- coding: utf-8 -*-
# Copyright 2020 Red Hat
# GNU General Public License v3.0+
# (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import absolute_import, division, print_function

__metaclass__ = type

import os
import sys

from collections import Sequence


def to_list(val):
    if isinstance(val, Sequence):
        return list(val)
    elif val is not None:
        return [val]
    else:
        return list()


def find_file_in_path(filename):
    # Check $PATH first, followed by same directory as sys.argv[0]
    paths = os.environ["PATH"].split(os.pathsep) + [
        os.path.dirname(sys.argv[0])
    ]
    for dirname in paths:
        fullpath = os.path.join(dirname, filename)
        if os.path.isfile(fullpath):
            return fullpath


def find_share_path(filename):
    # Check $PATH first, followed by same directory as sys.argv[0]
    paths = os.environ["PATH"].split(os.pathsep) + [
        os.path.dirname(sys.argv[0])
    ]
    for dirname in paths:
        env_path = os.sep.join(dirname.split(os.sep)[:-1])
        share_path = os.path.join(env_path, 'share')
        if os.path.isfile(os.path.join(share_path, filename)):
            return share_path
