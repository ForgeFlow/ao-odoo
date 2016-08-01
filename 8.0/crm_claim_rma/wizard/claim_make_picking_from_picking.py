# -*- coding: utf-8 -*-
#########################################################################
#                                                                       #
#                                                                       #
#########################################################################
#                                                                       #
# crm_claim_rma for OpenERP                                             #
# Copyright (C) 2009-2012  Akretion, Emmanuel Samyn,                    #
#       Benoît GUILLOT <benoit.guillot@akretion.com>                    #
#This program is free software: you can redistribute it and/or modify   #
#it under the terms of the GNU General Public License as published by   #
#the Free Software Foundation, either version 3 of the License, or      #
#(at your option) any later version.                                    #
#                                                                       #
#This program is distributed in the hope that it will be useful,        #
#but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#GNU General Public License for more details.                           #
#                                                                       #
#You should have received a copy of the GNU General Public License      #
#along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#########################################################################

import time
from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp import models, fields, api, _
from openerp import netsvc, workflow


class claim_make_picking_from_picking(models.TransientModel):
    _name='claim_make_picking_from_picking.wizard'
    _description='Wizard to create pickings from picking lines'
    
    @api.model
    def _get_picking_lines(self):
        return self.env['stock.picking'].read(self._context['active_id'], ['move_lines'])['move_lines']

    # Get default source location
    @api.model
    def _get_source_loc(self):
        warehouse_obj = self.env['stock.warehouse']
        warehouse_id = self._context.get('warehouse_id')
        return warehouse_obj.read(warehouse_id, ['lot_rma_id'])['lot_rma_id'][0]

    # Get default destination location
    @api.model
    def _get_dest_loc(self):
        warehouse_obj = self.env['stock.warehouse']
        warehouse_id = self._context.get('warehouse_id')
        if self._context.get('picking_type'):
            context_loc = self._context.get('picking_type')[8:]
            loc_field = 'lot_%s_id' %self._context.get('picking_type')[8:]
            loc_id = warehouse_obj.read(warehouse_id, [loc_field])[loc_field][0]
        return loc_id

    picking_line_source_location = fields.Many2one('stock.location', string='Source Location',help="Location where the returned products are from.", required=True, default=_get_source_loc)
    picking_line_dest_location = fields.Many2one('stock.location', string='Dest. Location',help="Location where the system will stock the returned products.", required=True, default=_get_dest_loc)
    picking_line_ids = fields.Many2many('stock.move', string='Picking lines', default=_get_picking_lines)

    @api.model
    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close',}

    # If "Create" button pressed
    @api.model
    def action_create_picking_from_picking(self):
        picking_obj = self.env['stock.picking']
        move_obj = self.env['stock.move']
        dummy, view_id = self.env['ir.model.data'].get_object_reference('stock', 'view_picking_form')
        p_type = 'internal'
        if self._context.get('picking_type'):
            context_type = self._context.get('picking_type')[8:]
            note = 'Internal picking from RMA to %s' %context_type
            name = 'Internal picking to %s' %context_type
        prev_picking = picking_obj.browse(self._context['active_id'])
        partner_id = prev_picking.partner_id.id
        # create picking
        picking_id = picking_obj.create({
                    'origin': prev_picking.origin,
                    'type': p_type,
                    'move_type': 'one', # direct
                    'state': 'draft',
                    'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'partner_id': prev_picking.partner_id.id,
                    'invoice_state': "none",
                    'company_id': prev_picking.company_id.id,
                    'location_id': self.picking_line_source_location.id,
                    'location_dest_id': self.picking_line_dest_location.id,
                    'note' : note,
                    'claim_id': prev_picking.claim_id.id,
                })
        # Create picking lines
        for wizard_picking_line in self.picking_line_ids:
            move_id = move_obj.create({
                    'name' : wizard_picking_line.product_id.name_template, # Motif : crm id ? stock_picking_id ?
                    'priority': '0',
                    #'create_date':
                    'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'date_expected': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'product_id': wizard_picking_line.product_id.id,
                    'product_qty': wizard_picking_line.product_qty,
                    'product_uom': wizard_picking_line.product_uom.id,
                    'partner_id': prev_picking.partner_id.id,
                    'prodlot_id': wizard_picking_line.prodlot_id.id,
                    # 'tracking_id':
                    'picking_id': picking_id,
                    'state': 'draft',
                    'price_unit': wizard_picking_line.price_unit,
                    # 'price_currency_id': claim_id.company_id.currency_id.id, # from invoice ???
                    'company_id': prev_picking.company_id.id,
                    'location_id': self.picking_line_source_location.id,
                    'location_dest_id': self.picking_line_dest_location.id,
                    'note': note,
                })
            wizard_move = move_obj.write(wizard_picking_line.id, {'move_dest_id': move_id})
        if picking_id:
            workflow.trg_validate(self._uid, 'stock.picking', picking_id,'button_confirm', self._cr)
            picking_obj.action_assign([picking_id])
        return {
            'name': '%s' % name,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_id,
            'domain' : "[('type', '=', '%s'),('partner_id','=',%s)]" % (p_type, partner_id),
            'res_model': 'stock.picking',
            'res_id': picking_id,
            'type': 'ir.actions.act_window',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
