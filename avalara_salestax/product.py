# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
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
from osv import osv, fields
from pkg_resources import require

class product_tax_code(osv.osv):
    """ Define type of tax code: 
    @param type: product is use as product code,
    @param type: freight is use for shipping code
    @param type: service is use for service type product  
    """
    _name = 'product.tax.code'
    _description = 'Tax Code'
    _columns = {
        'name': fields.char('Code', size=8, required=True),
        'description': fields.char('Description', size=64),
        'type': fields.selection([('product', 'Product'), ('freight', 'Freight'), ('service', 'Service'),
                          ('digital', 'Digital'), ('other', 'Other')], 'Type', required=True, help="Type of tax code as defined in AvaTax"),
        'company_id': fields.many2one('res.company', 'Company', required=True),
    }
    _defaults = {
        'company_id': lambda s,cr,uid,c: s.pool.get('res.company')._company_default_get(cr, uid, 'product.tax.code', context=c),
    }

product_tax_code()

class product_template(osv.osv):
    _inherit = "product.template"
    _columns = {
        'tax_code_id': fields.many2one('product.tax.code', 'Tax Code', help="AvaTax Tax Code"),
        'tax_apply': fields.boolean('Tax Calculation',help="Use Following Tax code for this Product"),
    }

product_template()

class product_product(osv.osv):
    _inherit = 'product.product'
    _columns = {
            'default_code' : fields.char('Product Code', size=64, select=True, required=True),
        }
    _sql_constraints = [
        ('name_uniq', 'unique(default_code)', 'Product Reference Code must be unique per Company!'),
    ]
    

class product_category(osv.osv):
    _inherit = "product.category"
    _columns = {
        'tax_code_id': fields.many2one('product.tax.code', 'Tax Code', help="AvaTax Tax Code")
    }

product_category()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: