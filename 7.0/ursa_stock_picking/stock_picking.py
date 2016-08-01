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

class stock_move(osv.osv):
    """Add Product location fields - aisle, rack, shelf to stock move"""

    _inherit = "stock.move"

    _columns = {
        'aisle': fields.related('product_id', 'loc_row', type="char", size=64, store=False, string="Aisle", help="Warehouse Aisle"),
        'rack': fields.related('product_id', 'loc_rack', type="char", size=64, store=False, string="Rack", help="Warehouse Rack in Aisle"),
        'shelf': fields.related('product_id', 'loc_case', type="char", size=64, store=False, string="Shelf", help="Warehouse Shelf in Rack"),
        }    

stock_move()