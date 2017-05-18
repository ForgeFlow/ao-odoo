# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class RmaOrderLine(models.Model):
    _inherit = "rma.order.line"

    helpdesk_id = fields.Many2one(
        string='Helpdesk Ticket',
        comodel_name='crm.helpdesk',
        copy=False,
    )

    @api.model
    def create(self, values):
        if ('rma_id' in values.keys() and
                'helpdesk_id' not in values.keys()):
            rma = self.env['rma.order'].browse(values['rma_id'])
            values['helpdesk_id'] = rma.originating_helpdesk_id.id or False
        return super(RmaOrderLine, self).create(values)
