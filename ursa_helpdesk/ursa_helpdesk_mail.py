# -*- coding: utf-8 -*-
##############################################################################
#
#    Ursa Information Systems
#    Copyright (C) 2013 (<http://www.ursainfosystems.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields, api, _


class ursa_helpdesk_mail(models.Model):
    _inherit = 'mail.mail'

    @api.multi
    def send_get_email_dict(self, partner=None):
        self.ensure_one()
        ir_values = self.env['ir.values']
        replacefrom = ir_values.get_default('crm.helpdesk',
                                            'replace_helpdesk_email_from')
        helpdeskemail = ir_values.get_default('crm.helpdesk',
                                              'helpdesk_reply_to')

        if replacefrom and 'helpdesk' in self.model:
            self.email_from = 'Helpdesk <'+helpdeskemail+'>'
        return super(ursa_helpdesk_mail, self).send_get_email_dict(
            partner=partner)
