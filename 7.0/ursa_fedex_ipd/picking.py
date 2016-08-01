# -*- coding: utf-8 -*-

##############################################################################
#
#    Ursa Information Systems
#    Authors: Adam O'Connor, Balaji Kannan
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

import time
import datetime
from openerp.report import report_sxw
from openerp.osv import fields, osv
from openerp import pooler
import json

#capture the date that the delivery slip was first printed
class fedex_ipd(osv.osv):
    _inherit = "stock.picking.out"

    def fedex_get(self, cr, uid, idstring):
        res = {}
        ids=[]
        context={}
        context['uid']=1
        uid = 1

        picking = self.pool.get('stock.picking.out')
        ids = picking.search(cr, uid, [('name', '=', idstring)], context=context)
        
        #get the delivery order based on the id that is passed in
        for delivery_order in self.browse(cr, uid, ids, context=context):
            picking_fields =['auto_picking','backorder_id','carrier_id','carrier_tracking_ref','company_id','date','date_done','invoice_state','invoice_type_id','location_dest_id','location_id','max_date','message_follower_ids','message_ids','message_is_follower','message_summary','message_unread','min_date','move_lines','move_type','name','note','number_of_packages','origin','partner_id','product_id','sale_id','state','stock_journal_id','type','volume','weight','weight_net']
            delivery = delivery_order.read(picking_fields, context=context)
			
            #delivery_order.write({'carrier_tracking_ref':'tracking_num_test'})
            move_fields=['auto_validate','backorder_id','company_id','create_date','date','date_expected','location_dest_id','location_id','move_dest_id','move_history_ids','move_history_ids2','name','note','origin','partner_id','picking_id','price_currency_id','price_unit','priority','procurements','prodlot_id','product_id','production_id','product_packaging','product_qty','product_uom','product_uos','product_uos_qty','purchase_line_id','sale_line_id','scrapped','state','tracking_id','type','weight','weight_net','weight_uom_id']
            

            #company = delivery_order.partner_id
            sale_fields =['partner_id', 'partner_invoice_id', 'partner_shipping_id','carrier_id']
            sale = self.pool.get('sale.order').browse(cr, uid, delivery[0]['sale_id'][0], context=context)
            sale_order = sale.read(sale_fields, context=context)
			
            partner_fields =['partner_type','is_company','city','country_id','company_id','email','fax','name','phone','state_id','street','street2','website','zip',]
            partner = self.pool.get('res.partner').browse(cr, uid, sale_order[0]['partner_shipping_id'][0], context=context)
			
			#ship to information
            res['contact'] = delivery[0]['partner_id'][1]
            res['company'] = partner.name
            res['address1'] = partner.street
            res['address2'] = partner.street2 or ''
            res['city'] = partner.city
            res['zip'] = partner.zip
            res['phone'] = partner.phone

            if partner.state_id:
                res['state'] = partner.state_id.name

            if partner.country_id:
                res['country'] = partner.country_id.code

            res['sale_num'] = delivery[0]['sale_id'][1]
            res['total_weight'] = delivery[0]['weight']

            value=0
            line_prod_code=[]
            line_prod_schedb=[]
            line_prod_upc=[]
            line_prod_manf_country=[]
            line_prod_desc=[]
            line_weight=[]
            line_uom=[]
            line_quantity=[]
            line_price=[]
            i=0

            if delivery_order.move_lines:
                for line in delivery_order.move_lines:

                    move = self.pool.get('stock.move').browse(cr, uid, delivery[0]['move_lines'][i], context=context)
                    move_lines = move.read(move_fields, context=context)
                    product = self.pool.get('product.product').browse(cr, uid, move_lines[0]['product_id'][0], context=context)

                    value += line.price_unit

                    line_prod_upc.append(str(product.upc))
                    line_prod_desc.append(str(product.name_template))
                    line_prod_schedb.append(product.scheduleb)
                    line_prod_manf_country.append(str(product.manf_country.code))                
                    
                    line_prod_code.append(str(move_lines[0]['product_id'][1]))
                    line_weight.append(str(move_lines[0]['weight']))
                    line_uom.append(str(move_lines[0]['product_uom'][1]))
                    line_quantity.append(str(move_lines[0]['product_qty']))
                    line_price.append(str(move_lines[0]['price_unit']))
                    i+=1
            res['declared_value']=str(round(value,2))
            res['upc']=line_prod_upc					
            res['part_num']=line_prod_code
            res['manuf_ctry']=line_prod_manf_country
            res['commodity_desc']=line_prod_desc
            res['harmonized_code']=line_prod_schedb
            res['line_qtys']=line_quantity
            res['line_uom']=line_uom
            res['line_weight']=line_weight
            res['line_price']=line_price
        
        return res
			

