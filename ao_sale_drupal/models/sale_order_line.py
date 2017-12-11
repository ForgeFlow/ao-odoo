# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    price_tax_external = fields.Monetary(
        string="Drupal Taxes", readonly=True,
    )
    price_total_external = fields.Monetary(
        string="Drupal Total", readonly=True,
    )
    price_subtotal_external = fields.Monetary(
        string="Drupal Subtotal", readonly=True,
    )
