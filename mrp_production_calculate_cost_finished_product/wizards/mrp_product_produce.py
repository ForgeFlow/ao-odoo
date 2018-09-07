# 2015-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.multi
    def do_produce(self):
        """writing the cost on the main product produced by a MO before
        produce."""
        moves = self.production_id.move_raw_ids
        total_cost = 0.0
        for move in moves.filtered(
                lambda x: x.product_id.tracking == 'none' and
                x.state not in ('done', 'cancel')):
            if move.product_id.type == 'consu':
                continue
            unit_cost = move._get_price_unit()
            move_value = unit_cost * move.product_qty
            total_cost += move_value
        prod_product = self.production_id.product_id
        # Total cost per unit in the product uom:
        prod_qty = self.production_id.product_uom_id._compute_quantity(
            self.production_id.product_qty, prod_product.uom_id)
        price_unit = total_cost / prod_qty
        moves = self.production_id.move_finished_ids.filtered(
            lambda x: x.product_id == prod_product and
            x.product_id.tracking == 'none' and
            x.state not in ('done', 'cancel'))
        for move in moves:
            move.write({'price_unit': price_unit})
        return super(MrpProductProduce, self).do_produce()
