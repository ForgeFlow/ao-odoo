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

from openerp import models, fields, api, _

class product_product(models.Model):
    _inherit = "product.product"
    
    @api.one
    def _product_code(self):
        for p in self:
            self.code = self._get_partner_code_name(p, self.env.context.get('partner_id', None))['code']
    
    code = fields.Char(compute = '_product_code', string='Internal Code')
    manf_country =  fields.Many2one('res.country', string= 'Country of Origin')
    scheduleb =  fields.Char(string = 'Schedule B #', help='Schedule B number for item')
