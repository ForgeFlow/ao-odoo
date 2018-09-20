# -*- coding: utf-8 -*-
# © 2017 Sergio Teruel <sergio.teruel@tecnativa.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models


class StockPickingOperationWizard(models.TransientModel):
    _inherit = 'stock.picking.operation.wizard'

    change_all = fields.Boolean(default=True)

    @api.multi
    def action_apply(self):
        res = super(StockPickingOperationWizard, self).action_apply()
        if self.change_all:
            vals = {'location_dest_id': self.new_location_dest_id.id}
            pickings = self.env['stock.picking'].browse(
                self.env.context['active_ids'])
            pickings.write(vals)
            for picking in pickings:
                picking.message_post(body=_(
                    "Destination location changed to %s"
                    % self.new_location_dest_id.name))
        return res
