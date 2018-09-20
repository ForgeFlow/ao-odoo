# Copyright 2015-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

from .purchase import _DEPT_SELECTION


class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    dept = fields.Selection(
        selection=_DEPT_SELECTION,
        string='Department', size=32,
        help="Department for which the item is required",
    )

    def _set_additional_fields(self, invoice):
        if self.purchase_line_id:
            self.dept = self.purchase_line_id.dept
        super(AccountInvoiceLine, self)._set_additional_fields(invoice)
