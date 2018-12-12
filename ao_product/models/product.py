# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class ProductProduct(models.Model):
    _inherit = 'product.product'

    @api.multi
    def action_view_stock_moves(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id', '=', self.id)]
        return action


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.multi
    def action_view_stock_moves(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id.product_tmpl_id', 'in', self.ids)]
        return action
