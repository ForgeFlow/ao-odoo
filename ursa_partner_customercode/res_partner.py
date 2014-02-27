# -*- coding: utf-8 -*-
##############################################################################
#
#    Ursa Information Systems
#    Author: Balaji Kannan
#    Copyright (C) 2014 (<http://www.ursainfosystems.com>).
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
import openerp.exceptions
import logging

class res_partner(osv.osv):

    _inherit = 'res.partner'
    
    _columns = {
        'customer_code': fields.char('Customer Code', size=40, readonly="1", help='Customer code required for AvaTax processing'),
	}
    
    def create(self, cr, uid, vals, context=None):
        if vals.get('customer_code','/')=='/' or not vals.get('customer_code','/'):
            vals['customer_code'] = self.pool.get('ir.sequence').get(cr, uid, 'res.partner.customercode') or '/'
        return super(res_partner, self).create(cr, uid, vals, context=context)

    def copy(self, cr, uid, id, default=None, context=None):
        pdb.set_trace()
        if not default:
            default = {}
        default.update({
            'customer_code': self.pool.get('ir.sequence').get(cr, uid, 'res.partner.customercode'),
        })
        return super(res_partner, self).copy(cr, uid, id, default, context=context)
    
res_partner()