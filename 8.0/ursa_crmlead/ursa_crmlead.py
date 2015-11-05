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

class ursa_leads(models.Model):
    _inherit = 'crm.lead'

    reply_to = fields.Char(string = 'Reply-To', invisible=True, readonly=True, help="Reply", default = 'sales@lulzbot.com')
    
    @api.multi
    def message_get_reply_to(self,):
        ir_values = self.env['ir.values']
        leademail = ir_values.get_default( 'crm', 'lead_reply_to')
        return [leademail]
        
        #lead_ins  = self.browse(cr, uid, ids, context=context)[0]
        #return [lead_ins.reply_to]
    
