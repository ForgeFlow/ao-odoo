# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, _


class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    def open_table(self):
        action = super(StockQuantityHistory, self).open_table()
        if self.compute_at_date:
            tree_view_id = self.env.ref(
                'ao_stock_account.view_stock_product_tree2').id
            action['views'][0] = (tree_view_id, 'tree')
            return action
        return action

