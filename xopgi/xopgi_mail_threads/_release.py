#!/usr/bin/env python
# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# Copyright (c) Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can do what the LICENCE file allows you to.
#

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        absolute_import as _py3_abs_imports)


def read_terpfile():
    import os
    from os.path import join
    with open(join(os.path.dirname(__file__), '__manifest__.py'), 'rU') as fh:
        content = fh.read()
        # This ODOO version is just to avoid SyntaxErrors.
        return eval(content, dict(MAJOR_ODOO_VERSION=8), {})


_TERP = read_terpfile()
VERSION = _TERP['version']
