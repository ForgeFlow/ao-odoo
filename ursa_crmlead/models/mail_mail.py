# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Mail(models.Model):
    _inherit = "mail.mail"

    @api.multi
    def send_get_email_dict(self, partner=None):
        self.ensure_one()
        ir_default = self.env["ir.default"]
        replacefrom = self.env['ir.config_parameter'].sudo().get_param(
            'crm.lead.replace.email.from', default=False)
        leademail = ir_default.get("crm.lead", "reply_to")
        if replacefrom and self.model == "crm.lead" and leademail:
            self.email_from = "LulzBot Sales<"+leademail+">"
        return super().send_get_email_dict(partner=partner)
