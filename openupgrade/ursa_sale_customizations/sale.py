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

from openerp import models, fields, api, _

class sale_order(models.Model):
    _inherit = "sale.order"
   
    @api.v7
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        if not part:
            return {'value': {}}

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
    
    foreign_sale = fields.Boolean(string='Non-US Address', help='Set if delivery address is non-US address')
    incoterm = fields.Many2one('stock.incoterms', string='Incoterm', help="International Commercial Terms are a series of predefined commercial terms used in international transactions.")
    order_policy = fields.Selection([('manual', 'On Demand'),('picking', 'On Delivery Order'),('prepaid', 'Before Delivery'),], 
            string='Create Invoice', required=True, readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]},
            help="""On demand: A draft invoice can be created from the sales order when needed. \n
            On delivery order: A draft invoice can be created from the delivery order when the products have been delivered. \n
            Before delivery: A draft invoice is created from the sales order and must be paid before the products can be delivered.""")

    @api.model
    def _make_invoice(self, order, lines):    
        inv_id = super(sale_order, self)._make_invoice(order, lines)
        # check to see if the invoice must be auto-progressed to proforma state
        ir_values = self.env['ir.values']
        auto_proforma2 = ir_values.get_default('account.invoice', 'auto_proforma2')
        # proceed if state transition is required
        if auto_proforma2 == 'True':
            # country where the product is shipped to
            country = (order.partner_shipping_id and order.partner_shipping_id.country_id and order.partner_shipping_id.country_id.name) or (order.partner_id.country_id and order.partner_id.country_id.name) or 'United States'
            if country <> 'United States':
                invoice_obj = self.env['account.invoice']
                invoice = invoice_obj.browse([inv_id])[0]
                invoice.write({'state': 'proforma2'})
        return inv_id
