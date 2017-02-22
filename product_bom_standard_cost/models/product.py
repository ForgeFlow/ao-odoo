# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models
from openerp.addons import decimal_precision as dp

UNIT = dp.get_precision('Product Price')


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.multi
    def _compute_bom_standard_cost(self):
        bom_obj = self.env['mrp.bom']
        uom_obj = self.env["product.uom"]
        for template in self:
            template.bom_standard_cost = 0.0
            price = 0.0
            for variant in template.product_variant_ids:
                bom_id = bom_obj._bom_find(product_id=variant.id)
                bom = bom_obj.sudo().browse(bom_id)
                for sbom in bom.bom_line_ids:
                    my_qty = sbom.product_qty / sbom.product_efficiency
                    if not sbom.attribute_value_ids:
                        # No attribute_value_ids means the bom line
                        # is not variant specific
                        price += uom_obj._compute_price(
                            sbom.product_id.uom_id.id,
                            sbom.product_id.bom_standard_cost,
                            sbom.product_uom.id) * my_qty

                if bom.routing_id:
                    for wline in bom.routing_id.workcenter_lines:
                        wc = wline.workcenter_id
                        cycle = wline.cycle_nbr
                        hour = (wc.time_start + wc.time_stop + cycle *
                                wc.time_cycle) * (wc.time_efficiency or 1.0)
                        price += wc.costs_cycle * cycle + wc.costs_hour * hour
                        price = uom_obj._compute_price(
                            bom.product_uom.id, price,
                            bom.product_id.uom_id.id)

                # Convert on product UoM quantities
                if price > 0:
                    price = uom_obj._compute_price(bom.product_uom.id,
                                                   price / bom.product_qty,
                                                   bom.product_id.uom_id.id)
                else:
                    price = template.standard_price
            template.bom_standard_cost = price

    bom_standard_cost = fields.Float(string='Standard cost of BOM',
                                     compute='_compute_bom_standard_cost',
                                     digits=UNIT)
