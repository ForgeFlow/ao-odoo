# -*- coding: utf-8 -*-
# Copyright 2004 TINY SPRL. Fabien Pinckaers <fp@tiny.Be>
# Copyright 2008 ChriCar Beteilugungs- und Beratungs
#                Ferdinand Gassauer <tiny@chricar.at>
# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

import math
from odoo import api, fields, models, _
from odoo.exceptions import UserError


def is_pair(x):
    return not x % 2


def check_upc(upccode):
    if not upccode:
        return True
    if not len(upccode) in [12]:
        return False
    try:
        int(upccode)
    except:
        return False
    sum = 0
    i = 0
    check = 0
    upc_len = len(upccode)
    for i in range(upc_len-1):
        pos = int(upc_len-2-i)
        if is_pair(i):
            sum += 3 * int(upccode[pos])
        else:
            sum += int(upccode[pos])
        check = int(math.ceil(sum / 10.0) * 10 - sum)
    i += 1
    if check != int(upccode[upc_len-1]):# last digit
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
    sum = 0
    i = 0
    check = 0
    ean_len=len(eancode)
    for i in range(ean_len-1):
        pos=int(ean_len-2-i)
        if is_pair(i):
            sum += 3 * int(eancode[pos])
        else:
            sum += int(eancode[pos])
        check = int(math.ceil(sum / 10.0) * 10 - sum)

    i += 1
    if check != int(eancode[ean_len-1]):  # last digit
        return False
    return True


class ProductProduct(models.Model):
    _inherit = "product.product"

    # this def shouldn't be necessary,
    # but is not available from product_product
    @api.one
    @api.constrains('barcode')
    def _check_ean_key(self):
        res = check_ean(self.barcode)
        if not res:
            raise UserError(_('Invalid Bar Code Number'))

    # check function for upc key
    @api.one
    @api.constrains('upc')
    def _check_upc_key(self):
        res = check_upc(self.upc)
        if not res:
            raise UserError(_('Invalid UPC Code Number'))

    barcode = fields.Char(
        string="EAN",
        help="Barcode number for EAN8 EAN13 JPC GTIN "
             "http://en.wikipedia.org/wiki/Global_Trade_Item_Number")
    upc = fields.Char(
        string="UPC",
        help="Barcode number for UPC "
             "http://en.wikipedia.org/wiki/Universal_Product_Code")

    _sql_constraints = [("upc", "UNIQUE(upc)", "Cannot have duplicate UPC"),
                        ("barcode", "UNIQUE(barcode)",
                         "Cannot have duplicate EAN Code")]


# ******* Just to be complete ****
# the ean13 is defined in partner.py but apparently not used in any xml
class ResPartner(models.Model):
    _inherit = "res.partner"

    barcode = fields.Char(string='EAN',
                          help='Barcode number for EAN8 EAN13 JPC GTIN')
    upc = fields.Char(string='UPC',
                      help='Barcode number for UPC')

    @api.one
    @api.constrains('barcode')
    def _check_ean_key(self):
        res = check_ean(self.barcode)
        if not res:
            raise UserError(_('Invalid Bar Code Number'))

    # check function for upc key
    @api.one
    @api.constrains('upc')
    def _check_upc_key(self):
        res = check_upc(self.upc)
        if not res:
            raise UserError(_('Invalid UPC Code Number'))
        
    _sql_constraints = [('upc', 'UNIQUE(upc)', 'Cannot have duplicate UPC'),
                        ('barcode', 'UNIQUE(barcode)',
                         'Cannot have duplicate EAN Code')]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    # related to display product product information if is_product_variant
    upc = fields.Char(
        related="product_variant_ids.upc", readonly=True,
        help="Barcode number for UPC",
    )
