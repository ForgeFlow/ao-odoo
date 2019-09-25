# Copyright 2018 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class MrpProductProduce(models.TransientModel):
    _inherit = "mrp.product.produce"

    @api.multi
    def do_produce(self):
        res = super(MrpProductProduce, self).do_produce()
        # Quantity to produce
        quantity = self.product_qty
        # For every line in non-material components of the bom create account
        # move lines
        for bom_cost_line in self.production_id.non_material_ids:
            self.production_id._create_account_move_line_non_materials(
                bom_cost_line, quantity)
        return res
