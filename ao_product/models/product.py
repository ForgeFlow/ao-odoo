# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


class AoProductSecurity(models.AbstractModel):
    _name = 'ao.product.security'

    @api.model
    def create(self, values):
        if not self.env.user.has_group(
                'ao_product.group_product_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Product Maintainers can create products."))
        return super().create(values)

    @api.multi
    def write(self, vals):
        pm_fields = ['standard_price', 'type', 'categ_id']
        if any([x in vals for x in pm_fields]) and not self.env.user.has_group(
                'ao_product.group_product_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Product Maintainers can modify the following fields "
                "in products:\n%s" % pm_fields))
        super().write(vals)


class ProductProduct(models.Model):
    _name = 'product.product'
    _inherit = ['product.product', 'ao.product.security']

    @api.multi
    def action_view_stock_moves(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id', '=', self.id)]
        return action


class ProductTemplate(models.Model):
    _name = 'product.template'
    _inherit = ['product.template', 'ao.product.security']

    @api.multi
    def action_view_stock_moves(self):
        self.ensure_one()
        action = self.env.ref('stock.stock_move_action').read()[0]
        action['domain'] = [('product_id.product_tmpl_id', 'in', self.ids)]
        return action
