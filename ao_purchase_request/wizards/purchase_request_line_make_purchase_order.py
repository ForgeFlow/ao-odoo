# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0).
from odoo import fields, models
from odoo.exceptions import UserError


class PurchaseRequestLineMakePurchaseOrderItem(models.TransientModel):
    _inherit = "purchase.request.line.make.purchase.order.item"

    product_type = fields.Selection(related='product_id.type', readonly=True)

    def check_group(self, request_lines):
        try:
            super().check_group(request_lines)
        except UserError:
            # TODO: add some logic for handle this UserError in a better way
            pass
