# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    @api.multi
    def _compute_bom_id_product_code(self):
        for rec in self:
            if rec.bom_id.product_id:
                rec.bom_id_product_code = rec.bom_id.product_id.default_code
            else:
                rec.bom_id_product_code = rec.bom_id.product_tmpl_id.\
                    product_variant_ids[0].default_code

    bom_id_product_code = fields.Char(
        compute="_compute_bom_id_product_code",
        string="Parent Reference", readonly=True
    )
