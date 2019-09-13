# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, models


class RmaLineMakeSaleOrder(models.TransientModel):
    _inherit = "rma.order.line.make.sale.order"

    @api.model
    def _prepare_item(self, line):
        return {
            'line_id': line.id,
            'rma_line_id': line.id,
            'product_id': line.product_id.id,
            'name': line.product_id.name,
            'product_qty': line.qty_to_sell,
            'rma_id': line.rma_id.id,
            'out_warehouse_id': line.out_warehouse_id.id,
            'product_uom_id': line.uom_id.id,
        }

    @api.model
    def default_get(self, fields):
        res = super(RmaLineMakeSaleOrder, self).default_get(
            fields)
        res['item_ids'] = []
        return res
