# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import fields, models

_DEPT_SELECTION = [('product', 'Product'),
                   ('ga', 'G&A'),
                   ('rd', 'R&D'),
                   ('sales', 'Sales'),
                   ('service', 'Service'),
                   ('mktg', 'Marketing')]


class AccountInvoiceLine(models.Model):

    _inherit = "account.invoice.line"

    dept = fields.Selection(_DEPT_SELECTION,
                            string='Department',
                            required=False,
                            size=32,
                            help="Department for which the item is required")
