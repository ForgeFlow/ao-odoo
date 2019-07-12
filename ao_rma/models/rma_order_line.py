# Copyright (C) 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

import operator
ops = {'=': operator.eq,
       '!=': operator.ne}


class RmaOrderLine(models.Model):
    _inherit = "rma.order.line"

    in_shipment_count = fields.Integer(compute='_compute_in_shipment_count',
                                       string='# of Shipments')
    out_shipment_count = fields.Integer(compute='_compute_out_shipment_count',
                                        string='# of Deliveries')
    operation_id = fields.Many2one(
        comodel_name="rma.operation", string="Operation",
        readonly=False, states={'done': [('readonly', True)]},
    )

    @api.constrains('in_route_id', 'out_route_id', 'location_id',
                    'in_warehouse_id', 'out_warehouse_id', 'operation_id')
    def check_operation_consistency(self):
        if self.state not in ('approved', 'done') or not self.move_ids:
            return
        if not self.operation_id:
            raise ValidationError(_('Cannot set operation to blank,'
                                    ' there are stock moves involved'))
        if (self.in_route_id != self.operation_id.in_route_id) or \
                (self.out_route_id != self.operation_id.out_route_id):
            raise ValidationError(
                _('Cannot set that operation, there are stock moves using'
                  ' different routes'))
        if self.location_id != self.operation_id.location_id:
            raise ValidationError(
                _('Cannot set that operation, there are stock moves using'
                  ' different receiving location'))
        if (self.in_warehouse_id != self.operation_id.in_warehouse_id) or \
                (self.out_warehouse_id != self.operation_id.out_warehouse_id):
            raise ValidationError(
                _('Cannot set that operation, there are stock moves using'
                  ' different warehouses'))

    @api.multi
    def _compute_in_shipment_count(self):
        for line in self:
            picking_ids = []
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
        for line in self:
            for move in line.move_ids:
                if move.location_dest_id.usage in ('supplier', 'customer') \
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
        for line in self:
            for move in line.move_ids:
                if move.location_dest_id.usage == 'internal' or \
                        move.location_dest_id.return_location:
                    picking_ids.append(move.picking_id.id)
                else:
                    if line.customer_to_supplier:
                        picking_ids.append(move.picking_id.id)

        shipments = list(set(picking_ids))
        # choose the view_mode accordingly
        if len(shipments) != 1:
            result['domain'] = "[('id', 'in', " + \
                               str(shipments) + ")]"
        elif len(shipments) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = shipments[0]
        return result

    @api.multi
    def action_view_out_shipments(self):
        action = self.env.ref('stock.action_picking_tree_all')
        result = action.read()[0]
        picking_ids = []
        for line in self:
            for move in line.move_ids:
                if move.location_dest_id.usage in ('supplier', 'customer') \
                        and not move.location_dest_id.return_location:
                    if not line.customer_to_supplier:
                        picking_ids.append(move.picking_id.id)
        shipments = list(set(picking_ids))
        # choose the view_mode accordingly
        if len(shipments) != 1:
            result['domain'] = "[('id', 'in', " + \
                               str(shipments) + ")]"
        elif len(shipments) == 1:
            res = self.env.ref('stock.view_picking_form', False)
            result['views'] = [(res and res.id or False, 'form')]
            result['res_id'] = shipments[0]
        return result

    @api.onchange('operation_id')
    def _onchange_operation_id(self):
        result = super(RmaOrderLine, self)._onchange_operation_id()
        self.under_warranty = self.operation_id.repair_type_id.under_warranty
        return result

    @api.multi
    def _get_rma_move_qty(self, states, direction='in'):
        for rec in self:
            product_obj = self.env['product.uom']
            qty = 0.0
            if direction == 'in':
                op = ops['=']
                moves = rec.move_ids.filtered(
                    lambda m: m.state in states and (
                        op(m.location_id.usage,
                           rec.type)
                        and not m.location_id.return_location or
                        m.location_dest_id.return_location))
            else:
                op = ops['!=']
                moves = rec.move_ids.filtered(
                    lambda m: m.state in states and (
                        op(m.location_id.usage,
                           rec.type)
                        and not m.location_dest_id.return_location or
                        m.location_id.return_location))
            for move in moves:
                qty += product_obj._compute_quantity(
                    move.product_uom_qty, rec.uom_id)
            return qty
