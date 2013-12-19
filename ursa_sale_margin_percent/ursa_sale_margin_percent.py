# -*- coding: utf-8 -*-
##############################################################################
#
#    Initial Author: Paul Thiry, Belshore Industries, (c) 2013
#    Ursa Information Systems
#    Author: Balaji Kannan
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

from openerp.osv import fields, osv

# modify sale order lines to include margin % field
class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    # function to compute margin % per sale order line
    def _product_margin_percent(self, cr, uid, ids, field_name, arg, context=None):
        res = {}
        for line in self.browse(cr, uid, ids, context=context):

            res[line.id] = 0
            
            if line.product_id:
                
                # only if sale price is defined                
                if line.price_unit!=0:
                
                    # if purchase_price is not in the sale order line, use product standard price
                    if line.purchase_price:
                        res[line.id] = round((1 - (line.purchase_price*line.product_uos_qty) / (line.price_unit*line.product_uos_qty*(100.0-line.discount)/100.0))*100, 2)
                        
                    else:
                        res[line.id] = round((1 - (line.product_id.standard_price*line.product_uos_qty) / (line.price_unit*line.product_uos_qty*(100.0-line.discount)/100.0))*100, 2)
                        
                else:
                    res[line.id] = 0
                    
        return res

    _columns = {
        'margin_percent': fields.function(_product_margin_percent, string='Margin %', store = True),
    }

sale_order_line()

# add margin percent to the sale order
class sale_order(osv.osv):
    _inherit = "sale.order"

    # compute overall margin percent
    def _product_margin_percent(self, cr, uid, ids, field_name, arg, context=None):
        
        res = {}
        
        for sale in self.browse(cr, uid, ids, context=context):
            
            line_amount = 0.00
            line_margin = 0.00
            
            # get line totals
            for line in sale.order_line:
                line_amount += (line.price_unit*line.product_uos_qty*(100.0-line.discount)/100.0) or 0.0
                line_margin += line.margin or 0.0
                
            # overall margin    
            if line_amount:
                res[sale.id] = (line_margin / line_amount) * 100
            else:
                res[sale.id] = 0.0
            
        return res
    
    _columns = {
        'margin_percent': fields.function(_product_margin_percent, string='Margin %',
              store = True),
    }

sale_order()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
