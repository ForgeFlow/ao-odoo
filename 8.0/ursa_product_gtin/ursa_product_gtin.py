# -*- encoding: utf-8 -*-
##############################################################################
#
# Copyright (c) 2004-2006 TINY SPRL. (http://tiny.be) All Rights Reserved.
#
# $Id: account.py 1005 2005-07-25 08:41:42Z nicoe $
#
# WARNING: This program as such is intended to be used by professional
# programmers who take the whole responsability of assessing all potential
# consequences resulting from its eventual inadequacies and bugs
# End users who are looking for a ready-to-use solution with commercial
# garantees and support are strongly adviced to contract a Free Software
# Service Company
#
# This program is Free Software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import math
from openerp import models, fields, api, _

def is_pair(x):
    return not x%2

def check_upc(upccode):
    if not upccode:
        return True
    if not len(upccode) in [12]:
        return False
    try:
        int(upccode)
    except:
        return False
    sum=0
    upc_len=len(upccode)
    for i in range(upc_len-1):
        pos=int(upc_len-2-i)
        if is_pair(i):
            sum += 3 * int(upccode[pos])
        else:
            sum += int(upccode[pos])
        check = int(math.ceil(sum / 10.0) * 10 - sum)

	i += 1
    if check != int(upccode[upc_len-1]): # last digit
        return False
    return True
    
def check_ean(eancode):
    if not eancode:
        return True
    if not len(eancode) in [8,12,13,14]:
        return False
    try:
        int(eancode)
    except:
        return False
    sum=0
    ean_len=len(eancode)
    for i in range(ean_len-1):
        pos=int(ean_len-2-i)
        if is_pair(i):
            sum += 3 * int(eancode[pos])
        else:
            sum += int(eancode[pos])
        check = int(math.ceil(sum / 10.0) * 10 - sum)

	i += 1
    if check != int(eancode[ean_len-1]): # last digit
        return False
    return True

class product_product(models.Model):
    _inherit = "product.product"

    # this def shouldn't be necessary, but is not available from product_product
    @api.one
    @api.constrains('ean13')
    def _check_ean_key(self):
        res = check_ean(self.ean13)
        if not res:
            raise Warning(_('Invalid Bar Code Number'))

    # check function for upc key
    @api.one
    @api.constrains('upc')
    def _check_upc_key(self):
        res = check_upc(self.upc)
        if not res:
            raise Warning(_('Invalid UPC Code Number'))

    ean13 = fields.Char(string='EAN', help ='Barcode number for EAN8 EAN13 JPC GTIN http://en.wikipedia.org/wiki/Global_Trade_Item_Number')
    upc = fields.Char(string='UPC', help='Barcode number for UPC http://en.wikipedia.org/wiki/Universal_Product_Code')

    _sql_constraints = [('upc', 'UNIQUE(upc)', 'Cannot have duplicate UPC'), ('ean13', 'UNIQUE(ean13)','Cannot have duplicate EAN Code')]

# ******* Just to be complete ****
# the ean13 is defined in partner.py but apparently not used in any xml
class res_partner(models.Model):
    _inherit = "res.partner"

    ean13 = fields.Char(string='EAN', help ='Barcode number for EAN8 EAN13 JPC GTIN')
    upc = fields.Char(string='UPC', help ='Barcode number for UPC')

    @api.one
    @api.constrains('ean13')
    def _check_ean_key(self):
        res = check_ean(self.ean13)
        if not res:
            raise Warning(_('Invalid Bar Code Number'))

    # check function for upc key
    @api.one
    @api.constrains('upc')
    def _check_upc_key(self):
        res = check_upc(self.upc)
        if not res:
            raise Warning(_('Invalid UPC Code Number'))
        
    _sql_constraints = [('upc', 'UNIQUE(upc)', 'Cannot have duplicate UPC'), ('ean13', 'UNIQUE(ean13)','Cannot have duplicate EAN Code')]


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    # related to display product product information if is_product_variant
    upc = fields.Char(related='product_variant_ids.upc', readonly=True,
                      help='Barcode number for UPC')
