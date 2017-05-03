# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class AccountInvoiceReport(models.Model):
    _inherit = "account.invoice.report"

    default_product_code = fields.Char(
        string='Product Internal Reference', related='product_id.default_code')
