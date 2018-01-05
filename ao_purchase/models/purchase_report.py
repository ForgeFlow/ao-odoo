# -*- coding: utf-8 -*-
# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import UserError


class ReportPurchasePurchaseQuotation(models.AbstractModel):
    _name = 'report.purchase.report_purchasequotation'

    @api.model
    def render_html(self, docids, data=None):
        pos = self.env['purchase.order'].browse(docids)
        if 'to approve' in pos.mapped('state'):
            raise UserError('You cannot print a RFQ that is pending to '
                            'approve.')
        values = {
            'doc_model': 'purchase.order',
            'doc_ids': pos.ids,
            'docs': pos
        }
        return self.env['report'].render(
            'purchase.report_purchasequotation', values)


class ReportPurchasePurchaseOrder(models.AbstractModel):
    _name = 'report.purchase.report_purchaseorder'

    @api.model
    def render_html(self, docids, data=None):
        pos = self.env['purchase.order'].browse(docids)
        if any(state in ['sent', 'to approve', 'draft'] for state in
               pos.mapped('state')):
            raise UserError('You cannot print a Purchase Order that is not '
                            'approved.')
        values = {
            'doc_model': 'purchase.order',
            'doc_ids': pos.ids,
            'docs': pos
        }
        return self.env['report'].render(
            'purchase.report_purchaseorder', values)
