# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models, _

class StockMove(models.Model):

    _inherit = "stock.move"

    @api.multi
    def product_price_update_before_done(self):
        """ In case of manufactured finished product, if the product is
        managed under average price, the average cost should be calculated
        and updated.
        """
        super(StockMove, self).product_price_update_before_done()
        tmpl_dict = {}
        for move in self:
            # adapt standard price on returns moves if the product cost_method
            #  is 'average'
            if move.product_id.cost_method != 'average':
                continue

            if (move.location_id.usage == 'production') and (
                    move.location_dest_id.usage == 'internal'):
                product = move.product_id
                prod_tmpl_id = self.product_id.product_tmpl_id.id
                qty_available = self.product_id.product_tmpl_id.qty_available
                if tmpl_dict.get(prod_tmpl_id):
                    product_avail = qty_available + tmpl_dict[prod_tmpl_id]
                else:
                    tmpl_dict[prod_tmpl_id] = 0
                    product_avail = qty_available
                if product_avail <= 0:
                    new_std_price = self.price_unit
                else:
                    product = self.product_id
                    # Get the standard price
                    amount_unit = product.standard_price
                    if (product_avail - self.product_qty) > 0.0:
                        new_std_price = ((amount_unit * product_avail) - (
                            self.price_unit * self.product_qty)) / (
                            product_avail - self.product_qty)
                    else:
                        new_std_price = 0.0
                tmpl_dict[prod_tmpl_id] += self.product_qty
                # Write the standard price, as SUPERUSER_ID because a
                # warehouse manager may not have the right to write on products
                product.sudo().with_context(
                    force_company=move.company_id.id).write(
                    {'standard_price': new_std_price})
