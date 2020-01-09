# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpBom(models.Model):
    _inherit = "mrp.bom"

    @api.multi
    def get_sub_boms(self, boms=None):
        if boms is None:
            boms = self.ids
        for bom in self:
            for line in bom.bom_line_ids:
                sub_boms = bom._bom_find(product=line.product_id)
                if sub_boms:
                    for sub_bom in sub_boms:
                        boms += sub_bom.ids
                        boms = sub_bom.get_sub_boms(boms=boms)
        return list(set(boms))

    @api.model
    def bom_find(self, product_tmpl=None, product=None, picking_type=None,
                 company_id=False):
        return self._bom_find(self, product_tmpl=product_tmpl, product=product,
                              picking_type=picking_type, company_id=company_id)
