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

from osv import fields, osv
from tools.translate import _

class ursa_helpdesk(osv.osv):
    _inherit = 'crm.helpdesk'

    _columns = {
        'reply_to': fields.char('Reply-To', invisible=True, readonly=True, size=128, help="Reply")
	}
    
    _defaults = {
        'reply_to': lambda *a: 'support@lulzbot.com',
    }
 
    def message_update(self, cr, uid, ids, msg, update_vals=None, context=None):
        

        for ticket in self.browse(cr, uid, ids, context=context):
            if ticket.state == 'done':
                self.write(cr, uid, ids, {'state':'open'},context=context)
        
        return super(ursa_helpdesk,self).message_update(cr, uid, ids, msg, update_vals=update_vals, context=context)
        
    def message_get_reply_to(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        helpdeskemail = ir_values.get_default(cr, uid, 'crm.helpdesk', 'helpdesk_reply_to')
        return [helpdeskemail]
        
        #helpdesk_ins  = self.browse(cr, uid, ids, context=context)[0]
        #return [helpdesk_ins.reply_to]
    
ursa_helpdesk()
    


