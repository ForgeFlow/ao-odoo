# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class MrpBomLine(models.Model):
    _inherit = "mrp.bom.line"

    bom_id_product_tmpl_id = fields.Many2one(
        comodel_name="product.template", related="bom_id.product_tmpl_id",
        string="Parent product", readonly=True
    )
