# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).
from odoo import api, fields, models
from odoo.addons import decimal_precision as dp


class SaleOrderLine(models.Model):
    """Disable Check Availability because is not accurated"""
    _inherit = 'sale.order.line'

    @api.onchange('product_uom_qty', 'product_uom', 'route_id')
    def _onchange_product_id_check_availability(self):
        return {}

    @api.depends('product_uom_qty', 'qty_delivered',
                 'product_id.service_policy', 'product_id.type')
    def _compute_qty_to_deliver(self):
        for rec in self:
            if (rec.product_id.type == 'service' and
                    rec.product_id.service_policy != 'delivered_manual'):
                rec.qty_to_deliver = 0
            else:
                rec.qty_to_deliver = rec.product_uom_qty - rec.qty_delivered

    confirmation_date = fields.Datetime(related='order_id.confirmation_date')
    qty_to_deliver = fields.Float(
        string='Qty To Deliver', copy=False,
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True, compute=_compute_qty_to_deliver, store=True)
