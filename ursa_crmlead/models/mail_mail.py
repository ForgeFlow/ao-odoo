# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class Mail(models.Model):
    _inherit = "mail.mail"

    @api.multi
    def _get_crm_lead_email_from(self):
        return self.env[self.model].browse(self.res_id).reply_to

    @api.multi
    def _send_prepare_values(self, partner=None):
        self.ensure_one()
        replacefrom = self.env['ir.config_parameter'].sudo().get_param(
            'crm.lead.replace.email.from', default=False)
        if replacefrom and self.model == "crm.lead":
            email_from = self._get_crm_lead_email_from()
            self.email_from = email_from
        return super()._send_prepare_values(partner=partner)
