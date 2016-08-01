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
from tools.translate import _

class product_class(osv.osv):
    
    _name = "product.class"
    _description = "Product Internal Classification"

    _columns = {
        'code': fields.char('Code', size=32, help="Product Classification Code"),
        'name': fields.char('Name', size=64, help="Product Classification Name"),
        'parent_id':  fields.many2one('product.class', 'Parent Category'),
        'sequence_no': fields.integer('Next number', help='Sequence Number')
    }
    
    _defaults = {
        'sequence_no': 1,
    }
    
product_class()

# associate product classification to product
class product_product(osv.osv):
    
    _inherit = "product.product"
    
    def onchange_class(self, cr, uid, ids, product_class, default_code, context=None):
    
        def seq_no(num, cnt=2):
            cnt = cnt - len(str(num))
            nulls = '0' * cnt
            return '%s%s' % (nulls, num)
            
        result = {}
        
        if product_class:
        
            product = ids and self.browse(cr, uid, ids[0], context=context) or False
                
            if not (default_code and len(default_code)) and product_class:
                
                class_obj = self.pool.get('product.class')
                class_ins = class_obj.browse(cr, uid, product_class, context=context)
                    
                seq = class_ins.sequence_no
                code = (class_ins.code + seq_no(seq, 4))
                    
                result['value'] = {'default_code': code}
                    
                class_ins.write({'sequence_no':seq+1})
            else:
                result['value'] = {'product_class': product and product.product_class.id or False}
                result['warning'] = {'title': _('Warning'),
                                         'message': _('Already has a default code.')}
        return result
    
    _columns = {
        'product_class': fields.many2one('product.class', 'product_class', help='Product Class to help generate Internal Reference number'),
    }
        
product_product()
