# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp

UNIT = dp.get_precision('Product Price')


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.multi
    @api.depends('standard_price', 'bom_ids.bom_line_ids',
                 'bom_ids.product_qty')
    def _compute_bom_standard_cost(self):
        bom_obj = self.env['mrp.bom']
        for template in self:
            template.bom_standard_cost = 0.0
            price = 0.0
            for variant in template.product_variant_ids:
                bom = bom_obj._bom_find(product=variant)
                for sbom in bom.bom_line_ids:
                    my_qty = sbom.product_qty
                    if not sbom.attribute_value_ids:
                        # No attribute_value_ids means the bom line
                        # is not variant specific
                        price += sbom.product_id.uom_id._compute_price(
                            sbom.product_id.bom_standard_cost,
                            sbom.product_uom_id) * my_qty
                # Todo: cost when using workcenters
                # Convert on product UoM quantities
                if price > 0:
                    price = bom.product_uom_id._compute_price(
                        price / bom.product_qty, bom.product_id.uom_id)
                else:
                    price = template.standard_price
            template.bom_standard_cost = price

    bom_standard_cost = fields.Float(string='Standard cost of BOM',
                                     compute='_compute_bom_standard_cost',
                                     store=True,
                                     digits=UNIT)
