# -*- coding: utf-8 -*-
##############################################################################
#
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

from osv import fields, osv
from tools.translate import _

#import pdb

import logging
_logger = logging.getLogger(__name__)

class ursa_shipwire_product(osv.osv):
    _inherit = 'product.product'

    _columns = {
        'is_shipwired': fields.boolean('Is Shipwired?', help="Stocked and shipped from Shipwire Location")
	}
        
ursa_shipwire_product()

class ursa_shipwire_location(osv.osv):
    _inherit = 'stock.location'

    _columns = {
        'shipwire_loc': fields.selection([('none', 'None'),('LAX','Los Angeles'),('CHI','Chicago'),('PHL','Philadelphia'),('TOR', 'Toronto'),('VAN', 'Vancouver'),('UK', 'United Kingdom'),('HKG', 'Hong Kong')], 'Shipwire Location', required=False, size=128, help="Select Shipwire Warehouse Location")
	}
     
    _defaults = {
        'shipwire_loc': 'none'
    }
    
ursa_shipwire_location()

class ursa_shipwire_inventory(osv.osv):
    _inherit = 'stock.inventory'

    def shipwire_fetch(self,cr, uid, ids, context=None):

        import shipwire

        locdict={}
        proddict={}
        
        #pdb.set_trace()
        
        # get configuration information
        ir_values = self.pool.get('ir.values')
        
        server = ir_values.get_default(cr, uid, 'stock.location', 'shipwire_server')
        apiuser = ir_values.get_default(cr, uid, 'stock.location', 'shipwire_username')
        password = ir_values.get_default(cr, uid, 'stock.location', 'shipwire_password')
        
        # get a list of products that are Shipwire
        product_objs = self.pool.get('product.product')
        product_ids = product_objs.search(cr, uid, [('is_shipwired', '=', True)])
        
        # get a list of locations that are Shipwire
        location_objs = self.pool.get('stock.location')
        location_ids = location_objs.search(cr, uid, [('shipwire_loc', '<>', 'none')])
        
        # inventory object
        for inventory in self.browse(cr, uid, ids, context=context):
        
            inventory.name = "Shipwire API - Auto Fetch"
                        
            inventory_line_objs = self.pool.get('stock.inventory.line')
                
            # for each product        
            for product in product_objs.browse(cr, uid, product_ids, None):
                
                if product.upc <> "":
                    
                    # for each location
                    for location in location_objs.browse(cr, uid, location_ids, None):
                        (statuscode, dict) = shipwire.process(location.shipwire_loc, product.upc, server, apiuser, password)
                        
                        # store qty in each location
                        if statuscode == 200:
                            
                            # testing connection
                            if server == "Test":
                                locdict[location.shipwire_loc]=dict.values()[0]
                            
                            elif dict.has_key(product.upc):
                                locdict[location.shipwire_loc]=dict[product.upc]
                                
                                # create inventory lines for this product/locations
                                if dict[product.upc]:
                                    iline = inventory_line_objs.create(cr, uid,  {'inventory_id' : inventory.id, 'product_id': product.id, 'product_uom': product.uom_id.id, 'location_id': location.id, 'product_qty': dict[product.upc]}, context)
                    
                    # store qty's for the product
                    if locdict.items():
                        proddict[product.upc]=locdict
                else:
                    _logger.warning("UPC not set for product %s.", product.name)
                
            super(ursa_shipwire_inventory, self).action_confirm(cr, uid, ids, context)
                
            super(ursa_shipwire_inventory, self).action_done(cr, uid, ids, context)
                
                 
        return True

ursa_shipwire_inventory()