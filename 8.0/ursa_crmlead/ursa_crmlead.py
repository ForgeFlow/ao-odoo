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


class UrsaLeads(models.Model):
    _inherit = 'crm.lead'

    reply_to = fields.Char(string='Reply-To', invisible=True,
                           readonly=True, help="Reply",
                           default='sales@lulzbot.com')


class MailThread(models.AbstractModel):
    _inherit = 'mail.thread'

    @api.cr_uid_context
    def message_get_reply_to(self, cr, uid, ids, default=None, context=None):
        model_name = context.get('thread_model') or self._name
        if model_name == 'crm.lead':
            ir_values = self.pool.get('ir.values')
            lead_reply_to = ir_values.get_default(cr, uid, 'crm',
                                                  'lead_reply_to')
            res = dict.fromkeys(ids, lead_reply_to)
            return res
        else:
            return super(MailThread, self).message_get_reply_to(
                cr, uid, ids, default=default, context=context)
