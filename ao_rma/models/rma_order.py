# Copyright (C) 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import api, models


class RmaOrder(models.Model):
    _inherit = "rma.order"

    @api.multi
    def _compute_in_shipment_count(self):
        for rec in self:
            picking_ids = []
            for line in rec.rma_line_ids:
                for move in line.move_ids:
                    if move.location_dest_id.usage == 'internal' or \
                            move.location_dest_id.return_location:
                        picking_ids.append(move.picking_id.id)
                    else:
                        if line.customer_to_supplier:
                            picking_ids.append(move.picking_id.id)
                shipments = list(set(picking_ids))
                line.in_shipment_count = len(shipments)

    @api.multi
    def _compute_out_shipment_count(self):
        picking_ids = []
        for rec in self:
            for line in rec.rma_line_ids:
                for move in line.move_ids:
                    if move.location_dest_id.usage in (
                            'supplier', 'customer') \
                            and not move.location_dest_id.return_location:
                        if not line.customer_to_supplier:
                            picking_ids.append(move.picking_id.id)
                shipments = list(set(picking_ids))
                line.out_shipment_count = len(shipments)

    @api.multi
    def action_view_in_shipments(self):
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        picking_ids = []
        for line in self.rma_line_ids:
            for move in line.move_ids:
                if move.location_dest_id.usage == 'internal' or \
                        move.location_dest_id.return_location:
                    picking_ids.append(move.picking_id.id)
                else:
                    if line.customer_to_supplier:
                        picking_ids.append(move.picking_id.id)
        if picking_ids:
            shipments = list(set(picking_ids))
            # choose the view_mode accordingly
            if len(shipments) > 1:
                result['domain'] = [('id', 'in', shipments)]
            else:
                res = self.env.ref('stock.view_picking_form', False)
                result['views'] = [(res and res.id or False, 'form')]
                result['res_id'] = shipments[0]
        return result

    @api.multi
    def action_view_out_shipments(self):
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        picking_ids = []
        for line in self.rma_line_ids:
            for move in line.move_ids:
                if move.location_dest_id.usage in (
                        'supplier', 'customer') \
                        and not move.location_dest_id.return_location:
                    if not line.customer_to_supplier:
                        picking_ids.append(move.picking_id.id)
        if picking_ids:
            shipments = list(set(picking_ids))
            # choose the view_mode accordingly
            if len(shipments) != 1:
                result['domain'] = [('id', 'in', shipments)]
            else:
                res = self.env.ref('stock.view_picking_form', False)
                result['views'] = [(res and res.id or False, 'form')]
                result['res_id'] = shipments[0]
        return result
