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

class ursa_leads(osv.osv):
    _inherit = 'crm.lead'

    _columns = {
        'reply_to': fields.char('Reply-To', invisible=True, readonly=True, size=128, help="Reply")
	}
    
    _defaults = {
        'reply_to': lambda *a: 'sales@lulzbot.com',
    }

    def message_get_reply_to(self, cr, uid, ids, context=None):
        ir_values = self.pool.get('ir.values')
        leademail = ir_values.get_default(cr, uid, 'crm', 'lead_reply_to')
        return [leademail]
        
        #lead_ins  = self.browse(cr, uid, ids, context=context)[0]
        #return [lead_ins.reply_to]
    
ursa_leads()