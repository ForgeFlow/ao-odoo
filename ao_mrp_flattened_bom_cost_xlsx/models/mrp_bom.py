# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


from openerp.osv import osv


class MrpBom(osv.osv):
    """ Defines bills of material for a product or a product template """
    _inherit = 'mrp.bom'

    def _get_flattened_totals(self, factor=1, totals=None):
        """
        Generate a summary of product quantities as a dict of flattened BOM
        """
        if totals is None:
            totals = {}
        factor /= self.product_qty * self.product_uom.factor_inv
        for line in self.bom_line_ids:
            sub_bom = self._bom_find(product_id=line.product_id.id)
            sub_bom = self.browse(sub_bom)
            if sub_bom:
                factor *= line.product_uom.factor_inv * line.product_qty
                sub_bom._get_flattened_totals(factor, totals)
            else:
                if totals.get(line.product_id):
                    totals[line.product_id] += line.product_qty * line.product_id.uom_id.factor * factor
                else:
                    totals[line.product_id] = line.product_qty * line.product_id.uom_id.factor * factor
        return totals
