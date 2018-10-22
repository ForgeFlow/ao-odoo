# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmLead(models.Model):
    _inherit = "crm.lead"

    reply_to = fields.Char(
        string="Reply-To",
        readonly=True,
        default="sales@lulzbot.com",
    )

    @api.model
    def message_get_reply_to(self, res_ids, default=None):
        model_name = self.env.context.get('thread_model') or self._name
        if model_name == 'crm.lead':
            lead_reply_to = self.env['ir.default'].get(
                'crm.lead', 'reply_to')
            if lead_reply_to:
                res = dict.fromkeys(res_ids, lead_reply_to)
                return res
        return super().message_get_reply_to(
            res_ids, default=default)
