# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models
from openerp.osv import orm


class MrpRepair(models.Model):
    _inherit = "mrp.repair"

    @api.multi
    def _compute_invoice_count(self):
        for rec in self:
            invoices = rec.invoice_id
            rec.invoice_count = len(invoices)

    invoice_count = fields.Integer(
        compute='_compute_invoice_count', string='# of Invoices',
    )

    @api.multi
    def action_view_invoice(self):
        action = self.env.ref('account.action_invoice_tree')
        result = action.read()[0]
        invoice_ids = self.invoice_id.ids
        # choose the view_mode accordingly
        if len(invoice_ids) != 1:
            result['domain'] = [('id', 'in', invoice_ids)]
        elif len(invoice_ids) == 1:
            res = self.env.ref('account.invoice_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = invoice_ids[0]
        return result


class mrp_repair_line(orm.Model):
    """To inherit using old api is needed here in order to be able to modify
    the onchange method for `type`.
    NOTE: This should be moved to new api in v10, when the standard is also
    migrated.
    """
    _inherit = 'mrp.repair.line'

    def onchange_operation_type(self, cr, uid, ids, type, guarantee_limit,
                                company_id=False, context=None):
        res = super(mrp_repair_line, self).onchange_operation_type(
            cr, uid, ids, type, guarantee_limit, company_id=company_id,
            context=context)
        if context.get('rma_line_id'):
            rma_line = self.pool['rma.order.line'].browse(
                cr, uid, context.get('rma_line_id'), context=context)
            res['value']['location_id'] = rma_line.location_id.id
        return res
