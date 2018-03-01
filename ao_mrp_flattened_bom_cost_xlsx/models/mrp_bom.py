# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class MrpBom(models.Model):
    """ Defines bills of material for a product or a product template """
    _inherit = 'mrp.bom'

    @api.multi
    def _get_flattened_totals(self, factor=1, totals=None):
        """
        Generate a summary of product quantities as a dict of flattened BOM
        """
        self.ensure_one()
        uom = self.env["product.uom"]
        bom = self.env["mrp.bom"]
        if totals is None:
            totals = {}
        # TODO: product or product template?
        factor /= uom._compute_qty(
            self.product_uom.id, self.product_qty,
            self.product_tmpl_id.uom_id.id, round=False)
        for line in self.bom_line_ids:
            sub_bom_id = self._bom_find(product_id=line.product_id.id)
            if sub_bom_id:
                sub_bom = bom.browse(sub_bom_id)
                new_factor = factor * uom._compute_qty(
                    line.product_uom.id,
                    line.product_qty,
                    line.product_id.uom_id.id, round=False)
                sub_bom._get_flattened_totals(new_factor, totals)
            else:
                if totals.get(line.product_id):
                    totals[line.product_id] += uom._compute_qty(
                        line.product_uom.id,
                        line.product_qty * factor,
                        line.product_id.uom_id.id, round=False)
                else:
                    totals[line.product_id] = uom._compute_qty(
                        line.product_uom.id,
                        line.product_qty * factor,
                        line.product_id.uom_id.id, round=False)
        return totals
