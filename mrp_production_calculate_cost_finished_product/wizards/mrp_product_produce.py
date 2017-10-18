# -*- coding: utf-8 -*-
# 2015-17 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.multi
    def do_produce(self):
        # writing the cost before produce
        moves = self.production_id.move_raw_ids
        total_cost = 0.0
        for move in moves.filtered(lambda x: x.product_id.tracking == 'none' and x.state not in ('done', 'cancel')):
            total_value = 0.0
            for quant in move.reserved_quant_ids:
                if quant.product_id.type != 'product':
                    continue
                if quant.product_id.cost_method != 'real':
                    unit_cost = quant.product_id.standard_price
                else:
                    unit_cost = quant.cost
                total_value += unit_cost * quant.qty
            unit_cost = total_value / self.product_qty
            total_cost += unit_cost
            move.write({'price_unit': unit_cost})
        moves = self.production_id.move_finished_ids.filtered(
            lambda x: x.product_id.tracking == 'none' and x.state not in ('done', 'cancel'))
        for move in moves:
            move.write({'price_unit': total_cost})
        return super(MrpProductProduce, self).do_produce()
