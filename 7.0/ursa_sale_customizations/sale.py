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

class sale_order(osv.osv):
    _inherit = "sale.order"
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):

        result = super(sale_order,self).onchange_partner_id(cr, uid, ids, part, context=context)
        
        part = self.pool.get('res.partner').browse(cr, uid, part, context=context)
        addr = self.pool.get('res.partner').address_get(cr, uid, [part.id], ['delivery', 'invoice', 'contact'])

        # get country
        if addr['delivery'] <> part.id:
            ship_part = self.pool.get('res.partner').browse(cr, uid, addr['delivery'], context=context)
            country = ship_part.country_id and ship_part.country_id.name or False
        else:
            country = part.country_id and part.country_id.name or False
        
        # if it is a foreign sale
        if country and country <> 'United States':
            result['value'].update({'foreign_sale': True})
            result['value'].update({'order_policy': 'manual'})
            result['value'].update({'incoterm': 15})
            
        # US sale
        else:
            result['value'].update({'foreign_sale': False})
            result['value'].update({'order_policy': 'picking'})
            result['value'].update({'incoterm': 14})
            
        return result
    
    _columns = {
        'foreign_sale': fields.boolean('Non-US Address', help='Set if delivery address is non-US address'),
        'incoterm': fields.many2one('stock.incoterms', 'Incoterm', help="International Commercial Terms are a series of predefined commercial terms used in international transactions."),
        'order_policy': fields.selection([('manual', 'On Demand'),('picking', 'On Delivery Order'),('prepaid', 'Before Delivery'),], 
                'Create Invoice', required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
                help="""On demand: A draft invoice can be created from the sales order when needed. \n
                On delivery order: A draft invoice can be created from the delivery order when the products have been delivered. \n
                Before delivery: A draft invoice is created from the sales order and must be paid before the products can be delivered."""),    
    } 
    
    def _prepare_order_line_move(self, cr, uid, order, line, picking_id, date_planned, context=None):
        
        location_id = order.shop_id.warehouse_id.lot_stock_id.id
        res = super(sale_order, self)._prepare_order_line_move(cr, uid, order, line, picking_id, date_planned, context=context)
       
        # set source location in move if the sale order line has a location set       
        res['location_id'] = (line.location_src_id and line.location_src_id.id) or location_id
        
        return res
        
    def _make_invoice(self, cr, uid, order, lines, context=None):    
    
        inv_id = super(sale_order, self)._make_invoice(cr, uid, order, lines, context=context)
        
        # check to see if the invoice must be auto-progressed to proforma state
        ir_values = self.pool.get('ir.values')
        auto_proforma2 = ir_values.get_default(cr, uid, 'account.invoice', 'auto_proforma2')
        
        # proceed if state transition is required
        if auto_proforma2 == 'True':
        
            # country where the product is shipped to
            country = (order.partner_shipping_id and order.partner_shipping_id.country_id and order.partner_shipping_id.country_id.name) or (order.partner_id.country_id and order.partner_id.country_id.name) or 'United States'
        
            if country <> 'United States':
                invoice_obj = self.pool.get('account.invoice')
                invoice = invoice_obj.browse(cr, uid, [inv_id], context=context)[0]
            
                invoice.write({'state': 'proforma2'})
        
        return inv_id
                
sale_order()

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    _columns = {
        'location_src_id': fields.many2one('stock.location', 'Source Location', help="Location from where the system will deliver the finished products.", select=True),
	} 
