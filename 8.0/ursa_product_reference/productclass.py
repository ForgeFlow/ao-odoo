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

from openerp import models, fields, api, _

class product_class(models.Model):
    
    _name = "product.class"
    _description = "Product Internal Classification"

    code = fields.Char(string='Code', help="Product Classification Code")
    name =fields.Char(string='Name', help="Product Classification Name")
    parent_id = fields.Many2one('product.class',string='Parent Category')
    sequence_no = fields.Integer(string='Next number', default=1 ,help='Sequence Number')
        

# associate product classification to product
class product_product(models.Model):
    
    _inherit = "product.product"
    product_class = fields.Many2one('product.class',string='product_class', help='Product Class to help generate Internal Reference number')

    @api.onchange('product_class')
    def onchange_class(self):
        def seq_no(num, cnt=2):
            cnt = cnt - len(str(num))
            nulls = '0' * cnt
            return '%s%s' % (nulls, num)

        result = {}                   
        if self.product_class:
            if not (self.default_code and len(self.default_code)) and self.product_class:
                seq = self.product_class.sequence_no
                code = (self.product_class.code or '' + seq_no(seq, 4))
                self.default_code = code
                self.product_class.write({'sequence_no' : self.product_class.sequence_no + 1})
            else:
                result['warning'] = {'title': _('Warning'),
                                         'message': _('Already has a default code.')}
            return result
