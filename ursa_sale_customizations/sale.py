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

    def _prepare_order_line_move(self, cr, uid, order, line, picking_id, date_planned, context=None):
        
        location_id = order.shop_id.warehouse_id.lot_stock_id.id
        res = super(sale_order, self)._prepare_order_line_move(cr, uid, order, line, picking_id, date_planned, context=context)
        
        res['location_id'] = (line.location_src_id and line.location_src_id.id) or location_id
        
        return res
    
sale_order()

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"

    _columns = {
        'location_src_id': fields.many2one('stock.location', 'Source Location', help="Location from where the system will deliver the finished products.", select=True),
	} 
