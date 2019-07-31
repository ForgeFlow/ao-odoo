# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from odoo import fields, models


class PurchaseRequestLine(models.Model):
    _inherit = "purchase.request.line"

    product_type = fields.Selection(related='product_id.type', readonly=True)
