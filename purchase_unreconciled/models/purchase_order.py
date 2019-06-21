# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    unreconciled = fields.Boolean(
        compute="_compute_unreconciled",
        search="_search_unreconciled",
        help="Indicates that a Purchase Order has related Journal items not "
             "reconciled.\nNote that if it is false it can be either that "
             "everything is reconciled or that the related accounts do not "
             "allow reconciliation",
    )

    @api.multi
    def _compute_unreconciled(self):
        acc_item = self.env["account.move.line"]
        for rec in self:
            unreconciled_items = acc_item.search([
                ("purchase_id", "=", rec.id),
                ("account_id.reconcile", "=", True),
                ("reconciled", "=", False),
            ])
            rec.unreconciled = len(unreconciled_items) > 0

    @api.model
    def _search_unreconciled(self, operator, value):
        if operator != '=' or not isinstance(value, bool):
            raise ValueError(_("Unsupported search operator"))
        pos = self.search([
            ("state", "=", "purchase")]).filtered(
            lambda r: r.unreconciled is value)
        return [('id', 'in', pos.ids)]
