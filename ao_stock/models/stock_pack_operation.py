# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.pack.operation"

    @api.one
    def _compute_qty_available_in_source_loc(self):
        product_available = self.product_id.with_context(
            location=self.location_id.id)._product_available()[
            self.product_id.id]['qty_available']
        res = self.product_uom_id._compute_qty(
            self.product_id.product_tmpl_id.uom_id.id, product_available,
            self.product_uom_id.id)
        self.qty_available_in_source_loc = res

    @api.one
    def _compute_display_source_loc(self):
        self.display_source_loc = \
            self.picking_id.picking_type_id.code != 'incoming'

    qty_available_in_source_loc = fields.Float(
        string="Qty Available in Source",
        compute=_compute_qty_available_in_source_loc)

    display_source_loc = fields.Boolean(
        compute=_compute_display_source_loc)
