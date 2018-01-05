# -*- coding: utf-8 -*-
# Copyright 2015-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models

_DEPT_SELECTION = [('product', 'Product'),
                   ('ga', 'G&A'),
                   ('rd', 'R&D'),
                   ('sales', 'Sales'),
                   ('service', 'Service'),
                   ('mktg', 'Marketing')]


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    dept = fields.Selection(
        selection=_DEPT_SELECTION,
        string='Department', size=32,
        help="Department for which the item is required",
    )
