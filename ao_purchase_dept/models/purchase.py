# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models

_DEPT_SELECTION = [('product', 'Product'),
                   ('ga', 'G&A'),
                   ('rd', 'R&D'),
                   ('sales', 'Sales'),
                   ('service', 'Service'),
                   ('mktg', 'Marketing')]


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    @api.model
    def _prepare_inv_line(self, account_id, order_line):
    
        res = super(PurchaseOrder, self)._prepare_inv_line(account_id,
                                                           order_line)
        res['dept'] = order_line.dept
        return res


class PurchaseOrderLine(models.Model):
    _inherit = "purchase.order.line"

    dept = fields.Selection(_DEPT_SELECTION,
                            string='Department',
                            required=False,
                            size=32,
                            help="Department for which the item is required")
