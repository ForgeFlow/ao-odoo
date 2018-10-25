# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class StockMoveLine(models.Model):
    _inherit = "stock.move"

    @api.multi
    def _compute_qty_available_in_source_loc(self):
        for rec in self:
            product_available = rec.product_id.with_context(
                location=rec.location_id.id)._product_available()[
                rec.product_id.id]['qty_available']
            res = rec.product_id.product_tmpl_id.uom_id._compute_quantity(
                product_available, rec.product_uom)
            rec.qty_available_in_source_loc = res

    @api.multi
    def _compute_display_source_loc(self):
        for rec in self:
            rec.display_source_loc = \
                rec.picking_id.picking_type_id.code != 'incoming'

    qty_available_in_source_loc = fields.Float(
        string="Qty Available in Source",
        compute="_compute_qty_available_in_source_loc",
    )
    display_source_loc = fields.Boolean(
        compute="_compute_display_source_loc",
    )
