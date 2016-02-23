# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------
# xopgi.xopgi_mail_threads
# ---------------------------------------------------------------------
# Copyright (c) 2013-2016 Merchise Autrement
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# @created: 2013-11-11


{
    "name": "Mail Threads (xopgi)",
    "version": "3.0",
    "post_load": "post_load_hook",
    "author": "Merchise Autrement",
    "website": "http://xopgi.merchise.org/addons/xopgi_mail_threads",
    'category': 'Social Network',
    "description": "Improves OpenERP's basic mail management.",
    "depends": ['mail'],
    "data": [
        "views/mail_message_view.xml",
    ],
    "demo_xml": [],
    "application": False,
    "installable": True,
    "auto_install": True,
}
