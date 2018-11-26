# Copyright 2018 Aleph Objects Inc.
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


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
