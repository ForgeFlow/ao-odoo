# Copyright 2018 Aleph Objects Inc.
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockQuant(models.Model):
    _inherit = "stock.quant"

    last_date_moved = fields.Datetime(
        related='product_id.last_date_moved',
    )
    standard_valuation = fields.Float(
        string="Standard Cost Valuation",
        compute="_compute_standard_valuation",
        store=True,
    )

    @api.depends('quantity', 'product_id.standard_price')
    @api.multi
    def _compute_standard_valuation(self):
        for rec in self:
            rec.standard_valuation = \
                rec.product_id.standard_price * rec.quantity
