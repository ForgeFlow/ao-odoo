# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmHelpdesk(models.Model):
    _inherit = 'crm.helpdesk'

    reply_to = fields.Char(
        string='Reply-To',
        readonly=True, invisible=True,
        default='support@lulzbot.com',
    )

    @api.model
    def _notify_get_reply_to(
            self, default=None, records=None, company=None, doc_names=None,
    ):
        help_reply_to = self.env["ir.default"].get(
            "crm.helpdesk", "reply_to")
        if help_reply_to:
            res = dict.fromkeys(self.ids, help_reply_to)
            return res
        return super()._notify_get_reply_to(
            default=default, records=records,
            company=company, doc_names=doc_names,
        )
