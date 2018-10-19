# -*- coding: utf-8 -*-
# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    amount_invoiced = fields.Float(
        string="Amount Invoiced", readonly=True, compute='_compute_balance_due',
        store=False
    )
    balance_due = fields.Float(
        string="Balance due", readonly=True, compute='_compute_balance_due',
        store=False
    )

    @api.multi
    def _compute_balance_due(self):
        to_compute = self.filtered(
            lambda r: r.state in ['purchase'])
        for rec in to_compute:
            if rec.invoice_lines:
                for invoice_line in rec.invoice_lines:
                    rec.amount_invoiced += invoice_line.price_subtotal_signed
            rec.balance_due = rec.price_total - rec.amount_invoiced

