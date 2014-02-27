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

class ursa_leads_mail(osv.osv):
    _inherit = 'mail.mail'

    #def create(self, cr, uid, values, context=None):

    #    ir_values = self.pool.get('ir.values')
        
    #    replacefrom = ir_values.get_default(cr, uid, 'crm', 'replace_leads_email_from')
    #    leademail = ir_values.get_default(cr, uid, 'crm', 'lead_reply_to')
        
    #    if replacefrom:
    #        values['email_from'] = 'Sales<'+leademail+'>'  
    
    #    return super(ursa_leads_mail, self).create(cr, uid, values, context)

    def send_get_email_dict(self, cr, uid, mail, partner=None, context=None):

        ir_values = self.pool.get('ir.values')
        
        replacefrom = ir_values.get_default(cr, uid, 'crm', 'replace_leads_email_from')
        leademail = ir_values.get_default(cr, uid, 'crm', 'lead_reply_to')
        
        if replacefrom and 'helpdesk' not in mail.model:
            mail.email_from = 'Sales<'+leademail+'>'  
          
        return  super(ursa_leads_mail, self).send_get_email_dict(cr, uid, mail, partner, context)
        
ursa_leads_mail()
