# -*- coding: utf-8 -*-
# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class UrsaLeadsMail(models.Model):
    _inherit = "mail.mail"

    @api.multi
    def send_get_email_dict(self, partner=None):
        self.ensure_one()
        ir_values = self.env["ir.values"]
        replacefrom = ir_values.get_default("crm", "replace_leads_email_from")
        leademail = ir_values.get_default("crm", "lead_reply_to")
        if replacefrom and self.model == "crm.lead":
            self.email_from = "LulzBot Sales<"+leademail+">"
        return super(UrsaLeadsMail, self).send_get_email_dict(
            partner=partner)
