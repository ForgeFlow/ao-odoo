# Copyright 2018 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp


class MrpBomCost(models.Model):
    _name = "mrp.bom.cost"

    cost_type = fields.Selection(
        string="Type",
        selection=[('labor', 'Labor'), ('overhead', 'Overhead')],
        required=True,
    )
    product_id = fields.Many2one(
        comodel_name='product.product',
        string='Product',
        required=True,
        domain=[('type', '=', 'service')],
    )
    product_qty = fields.Float(
        string='Product Quantity', default=1.0,
        digits=dp.get_precision('Product Unit of Measure'),
        required=True,
    )
    product_uom_id = fields.Many2one(
        comodel_name='product.uom',
        string='Product Unit of Measure',
        required=True,
    )
    bom_id = fields.Many2one(
        comodel_name='mrp.bom',
        string='Parent BoM',
        index=True,
        ondelete='cascade',
        required=True,
    )
    standard_price = fields.Float(
        string="Standard unit price",
        related="product_id.standard_price",
        readonly=True,
    )

    @api.onchange('product_uom_id')
    def onchange_product_uom_id(self):
        res = {}
        if not self.product_uom_id or not self.product_id:
            return res
        if self.product_uom_id.category_id != \
                self.product_id.uom_id.category_id:
            self.product_uom_id = self.product_id.uom_id.id
            res['warning'] = {
                'title': _('Warning'),
                'message': _('The Product Unit of Measure you chose has a '
                             'different category than in the product form.'),
            }
        return res

    @api.onchange('product_id')
    def onchange_product_id(self):
        if self.product_id:
            self.product_uom_id = self.product_id.uom_id.id
