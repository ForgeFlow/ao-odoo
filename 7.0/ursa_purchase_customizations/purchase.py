##############################################################################
#
#    Authors: Balaji Kannan <bkannan@ursainfosystems.com>
# 
#    Copyright (C) 2013 Ursa Information Systems Inc (<http://www.ursainfosystems.com>). 
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
from openerp import SUPERUSER_ID
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import fields, osv
from openerp import netsvc
from openerp import pooler
from openerp.tools.translate import _
from openerp.osv.orm import browse_record, browse_null
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT, DEFAULT_SERVER_DATETIME_FORMAT, DATETIME_FORMATS_MAP

class purchase_order(osv.osv):
    _inherit = "purchase.order"

    def _prepare_inv_line(self, cr, uid, account_id, order_line, context=None):
    
        res = super(purchase_order, self)._prepare_inv_line(cr, uid, account_id, order_line, context=context)
        
        res['dept'] = order_line.dept
        
        return res

    def _prepare_order_line_move(self, cr, uid, order, order_line, picking_id, context=None):
    
        res = super(purchase_order, self)._prepare_order_line_move(cr, uid, order, order_line, picking_id, context=context)
        
        res['location_dest_id'] = (order_line.location_dest_id and order_line.location_dest_id.id) or order.location_id.id
        
        return res
    
purchase_order()

class purchase_order_line(osv.osv):
    _inherit = "purchase.order.line"

    _columns = {
        'dept': fields.selection([('product', 'Product'),('ga','G&A'),('rd', 'R&D'),('sales','Sales'),('service','Service'),('mktg','Marketing')], 'Department', required=False, size=32, help="Department for which the item is required"),
        'location_dest_id': fields.many2one('stock.location', 'Dest. Location', help="Location where the system will stock the finished products.", select=True),
	} 

class account_invoice_line(osv.osv):

    _inherit = "account.invoice.line"

    _columns = {
        'dept': fields.selection([('product', 'Product'),('ga','G&A'),('rd', 'R&D'),('sales','Sales'),('service','Service'),('mktg','Marketing')], 'Department', required=False, size=32, help="Department for which the item is required"),        'h_or_f': fields.char('Product_type', size=1, help="Product Type - Header, Footer, Others "),
    }
    
account_invoice_line()

class stock_picking(osv.osv):
    _inherit = "stock.picking"

    # update the information on the invoice  line  
    def _prepare_invoice_line(self, cr, uid, group, picking, move_line, invoice_id,
        invoice_vals, context=None):
        
        res = super(stock_picking, self)._prepare_invoice_line(cr, uid, group, picking, move_line, invoice_id, invoice_vals, context=context)
     
        if picking.purchase_id and move_line.purchase_line_id:
            res['dept'] = move_line.purchase_line_id.dept

        return res
        
stock_picking()
