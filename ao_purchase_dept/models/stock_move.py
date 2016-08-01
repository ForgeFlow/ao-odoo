# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, models


class StockMove(models.Model):
    _inherit = "stock.move"

    @api.model
    def _create_invoice_line_from_vals(self, move, invoice_line_vals):
        if move.purchase_line_id:
            invoice_line_vals['dept'] = move.purchase_line_id.dept
        res = super(StockMove, self)._create_invoice_line_from_vals(
            move, invoice_line_vals)
        return res
