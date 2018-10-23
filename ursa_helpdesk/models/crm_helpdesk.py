# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmHelpdesk(models.Model):
    _inherit = 'crm.helpdesk'

    reply_to = fields.Char(
        string='Reply-To',
        readonly=True, invisible=True,
        default='support@lulzbot.com',
    )

    @api.multi
    def message_update(self, msg, update_vals=None):
        for ticket in self:
            if ticket.state == 'done':
                self.sudo().write({'state': 'open'})
        return super().message_update(
            msg, update_vals=update_vals)

    @api.model
    def message_get_reply_to(self, res_ids, default=None):
        model_name = self.env.context.get('thread_model') or self._name
        if model_name == 'crm.helpdesk':
            help_reply_to = self.env['ir.default'].get(
                'crm.helpdesk', 'reply_to')
            if help_reply_to:
                res = dict.fromkeys(res_ids, help_reply_to)
                return res
        return super().message_get_reply_to(
            res_ids, default=default)
