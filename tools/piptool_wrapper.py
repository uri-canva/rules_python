#!/usr/bin/env python

# Copyright 2017 The Bazel Authors. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Wrapper to invoke piptool.py with vendored third-party dependencies.

This wrapper must work under Python 2.7.*, or any Python 3.* >= 3.4.0.
It must also work under Linux, Mac OS, Windows, and any other
operating system.  It must work inside or outside a virtualenv, inside
or outside a runfiles tree, and inside or outside a Bazel execroot.
It must work with arbitrary other packages on the Python import path.
"""

import os
import sys

# Never do what we're about to do.
#
# Add our first-party source, and vendored third_party packages, to
# the start of sys.path, so that we win any collision with already
# installed modules.

_this_file = __file__
if (_this_file is None) or not os.path.isfile(_this_file):
    sys.exit("piptool_wrapper.py failed.  Cannot determine __file__")

_tool_dir = os.path.dirname(_this_file)
_root_dir = os.path.abspath(os.path.join(_tool_dir, '..'))
sys.path[0:0] = [
    # Vendored third_party packages
    os.path.join(_root_dir, 'third_party'),
    # First party source (not a Python import package, just a directory)
    os.path.join(_root_dir, 'rules_python'),
    ]

# Safe to import
import setuptools
import pkg_resources
import wheel
import pip

# Sanity check that vendoring logic worked
assert setuptools.__version__ == '38.5.1'
assert wheel.__version__ == '0.30.0'
assert pip.__version__ == '9.0.1'

# Invoke piptool
import piptool
piptool.main()
