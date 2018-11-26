# Copyright 2018 Aleph Objects Inc.
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductProduct(models.Model):
    _inherit = "product.product"

    last_date_moved = fields.Datetime('Last date moved',
                                      readonly=True,
                                      compute='_compute_last_date_moved')

    @api.multi
    def _compute_last_date_moved(self):
        last_move = {}
        self.env.cr.execute("""
            SELECT product_id, max(date) as last_move_date
            FROM stock_move
            GROUP BY product_id
        """)
        for product_id,  last_move_date in self.env.cr.fetchall():
            last_move[product_id] = last_move_date
        for rec in self:
            if rec.id in last_move.keys():
                rec.last_date_moved = last_move[rec.id]
