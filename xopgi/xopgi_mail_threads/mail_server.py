#!/usr/bin/env python
# -*- encoding: utf-8 -*-
# ---------------------------------------------------------------------
# xopgi.mail_threads.mail_server
# ---------------------------------------------------------------------
# Copyright (c) 2015-2017 Merchise Autrement [~º/~] and Contributors
# All rights reserved.
#
# This is free software; you can redistribute it and/or modify it under the
# terms of the LICENCE attached (see LICENCE file) in the distribution
# package.
#
# Created on 2015-01-15

'''General outgoing server selection.

Allow to specify rules about which outgoing SMTP server to choose.  Actually,
simply ensures that mail-sending facilities of OpenERP check for more options
when the "default" server is to be chosen.

'''

from __future__ import (division as _py3_division,
                        print_function as _py3_print,
                        absolute_import as _py3_abs_import)


# TODO: Review with gevent-based model.
from xoutil.context import context as execution_context
from xoutil import logger as _logger

try:
    from openerp.models import Model
    from openerp import api
except ImportError:
    from odoo.models import Model
    from odoo import api


def get_kwargs(func):
    from xoutil.inspect import getfullargspec
    spec = getfullargspec(func)
    argsspec = spec.args
    if argsspec and spec.defaults:
        argsspec = argsspec[-len(spec.defaults):]
    else:
        argsspec = []
    argsspec.extend(spec.kwonlyargs or [])
    return argsspec


class MailServer(Model):
    _inherit = 'ir.mail_server'

    @api.model
    def send_email(self, message, **kw):
        '''Sends an email.

        Overrides the basic OpenERP's sending to allow transports to kick in.
        Basically it selects a transport and delivers the email with it if
        possible.

        The transport may choose to deliver the email by itself.  In this case
        the basic OpenERP is not used (unless the transport uses the provided
        `direct_send`:func: function).

        Otherwise, the transport may change the message to be deliver and the
        connection data.

        It is strongly suggested that transport only change headers and
        connection data.

        '''
        _super = super(MailServer, self).send_email
        if DIRECT_SEND_CONTEXT not in execution_context:
            transport = None
            try:
                from .transports import MailTransportRouter as transports
                mail_server_id = kw.get('mail_server_id', None)
                smtp_server = kw.get('smtp_server', None)
                context = self._context
                if neither(mail_server_id, smtp_server):
                    transport, querydata = transports.select(
                        self, message
                    )
                    if transport:
                        with transport:
                            message, conndata = transport.prepare_message(
                                self, message,
                                data=querydata,
                            )
                            return transport.deliver(self,message, conndata)
            except Exception as e:
                from openerp.addons.base.ir.ir_mail_server import \
                    MailDeliveryException
                if not isinstance(e, MailDeliveryException):
                    _logger.exception(
                        'Transport %s failed. Falling back',
                        transport,
                        extra=dict(message_from=message.get('From'),
                                   message_to=message.get('To'),
                                   message_cc=message.get('Cc'),
                                   message_subject=message.get('Subject'))
                    )
                else:
                    raise
        return _super(message, **kw)

    @api.model
    def send_without_transports(self, message, **kw):
        '''Send a message without using third-party transports.'''
        with execution_context(DIRECT_SEND_CONTEXT):
            self.send_email(message, **kw)


DIRECT_SEND_CONTEXT = object()
neither = lambda *args: all(not a for a in args)
