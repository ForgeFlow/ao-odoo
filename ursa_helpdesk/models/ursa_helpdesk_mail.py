# -*- coding: utf-8 -*-
# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models, api


class MailMail(models.Model):
    _inherit = "mail.mail"

    @api.multi
    def send_get_email_dict(self, partner=None):
        self.ensure_one()
        ir_values = self.env['ir.values']
        replacefrom = ir_values.get_default('crm.helpdesk',
                                            'replace_helpdesk_email_from')
        helpdeskemail = ir_values.get_default('crm.helpdesk',
                                              'helpdesk_reply_to')

        if replacefrom and self.model == 'crm.helpdesk':
            self.email_from = 'LulzBot Support <'+helpdeskemail+'>'
        return super(MailMail, self).send_get_email_dict(partner=partner)
