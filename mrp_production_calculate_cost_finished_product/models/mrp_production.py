# 2015-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class MrpProductProduce(models.Model):
    _inherit = "mrp.production"

    def _cal_price(self, consumed_moves):
        """writing the cost on the main product produced by a MO after we
        consume the components."""
        res = super()._cal_price(consumed_moves)
        total_cost = 0.0
        for move in consumed_moves:
            if move.product_id.type == 'consu':
                continue
            total_cost += move.value

        finished_moves = self.move_finished_ids.filtered(
            lambda x: x.product_id == self.product_id and
            x.product_id.tracking == 'none' and
            x.state not in ('done', 'cancel') and x.quantity_done > 0)
        for move in finished_moves:
            qty_done = move.product_uom._compute_quantity(
                move.quantity_done, move.product_id.uom_id)
            price_unit = total_cost / qty_done
            move.write({'price_unit': abs(price_unit)})
        return res
