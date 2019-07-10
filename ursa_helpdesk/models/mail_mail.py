# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MailMail(models.Model):
    _inherit = "mail.mail"

    @api.multi
    def _send_prepare_values(self, partner=None):
        self.ensure_one()
        ir_default = self.env["ir.default"]
        replacefrom = self.env['ir.config_parameter'].sudo().get_param(
            'crm.helpdesk.replace.email.from', default=False)
        helpdeskemail = ir_default.get("crm.helpdesk", "reply_to")
        if replacefrom and self.model == 'crm.helpdesk':
            self.email_from = 'LulzBot Support <' + helpdeskemail + '>'
        return super()._send_prepare_values(partner=partner)
