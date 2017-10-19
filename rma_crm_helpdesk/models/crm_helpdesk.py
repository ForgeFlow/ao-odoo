# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CrmHelpdesk(models.Model):
    _inherit = "crm.helpdesk"

    @api.multi
    def _compute_rma_count(self):
        for rec in self:
            rmas = rec.rma_order_line_ids
            rec.rma_count = len(rmas)

    rma_count = fields.Integer(
        compute='_compute_rma_count', string='# of RMA',
    )
    rma_order_line_ids = fields.One2many(
        string='RMA Order Lines',
        comodel_name='rma.order.line',
        inverse_name='helpdesk_id',
        copy=False,
    )

    @api.multi
    def action_view_rma_customer(self):
        action = self.env.ref('rma.action_rma_customer_lines')
        result = action.read()[0]
        rma_list = self.rma_order_line_ids.ids
        result['context'] = {}
        if len(rma_list) != 1:
            result['domain'] = [('id', 'in', rma_list)]
        elif len(rma_list) == 1:
            res = self.env.ref('rma.view_rma_line_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = rma_list[0]
        return result
