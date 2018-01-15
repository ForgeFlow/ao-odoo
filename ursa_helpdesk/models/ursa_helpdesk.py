# -*- coding: utf-8 -*-
# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, fields, api, _


class UrsaHelpdesk(models.Model):
    _inherit = 'crm.helpdesk'

    reply_to = fields.Char(string='Reply-To', invisible=True,
                           readonly=True, help="Reply",
                           default='support@lulzbot.com')

    @api.multi
    def message_update(self, msg, update_vals=None):
        for ticket in self:
            if ticket.state == 'done':
                self.sudo().write({'state': 'open'})
        return super(UrsaHelpdesk, self).message_update(
            msg, update_vals=update_vals)

    @api.model
    def message_get_reply_to(self, res_ids, default=None):

        model_name = self.env.context.get('thread_model') or self._name
        if model_name == 'crm.helpdesk':
            helpdeskemail = self.env['ir.values'].get_default(
                'crm.helpdesk', 'helpdesk_reply_to')
            res = dict.fromkeys(res_ids, helpdeskemail)
            return res
        else:
            return super(UrsaHelpdesk, self).message_get_reply_to(
                res_ids, default=default)
