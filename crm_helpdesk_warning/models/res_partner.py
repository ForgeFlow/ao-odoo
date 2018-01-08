# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


WARNING_MESSAGE = [
    ('no-message', 'No Message'),
    ('warning', 'Warning'),
    ('block', 'Blocking Message'),
]


class ResPartner(models.Model):
    _inherit = 'res.partner'

    helpdesk_warn = fields.Selection(selection=WARNING_MESSAGE,
                                     string='Warning message',
                                     default='no-message')
    helpdesk_warn_log = fields.Boolean(
        string='Log the message in the helpdesk ticket', default=False)
    helpdesk_warn_msg = fields.Text('Message for Helpdesk Tickets')

    @api.multi
    @api.onchange('helpdesk_warn')
    def _onchange_helpdesk_warn(self):
        for rec in self:
            rec.helpdesk_warn_log = rec.helpdesk_warn != 'no-message'
