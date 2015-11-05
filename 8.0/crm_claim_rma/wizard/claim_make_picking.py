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
from openerp.exceptions import except_orm, Warning, RedirectWarning


class claim_make_picking(models.TransientModel):
    _name='claim_make_picking.wizard'
    _description='Wizard to create pickings from claim lines'


    @api.model
    def _get_claim_lines(self):
        #TODO use custom states to show buttons of this wizard or not instead of raise an error
        line_obj = self.env['claim.line']
        if self._context.get('picking_type') in ['in', 'loss']:
            move_field = 'move_in_id'
        elif self._context.get('picking_type') == 'out':
            move_field = 'move_out_id'
        good_lines = []
        line_ids =  line_obj.search([('claim_id', '=', self._context['active_id'])])
        for line in line_ids:
            if not line[move_field] or line[move_field].state == 'cancel':
                good_lines.append(line.id)
        if not good_lines:
            raise Warning(_('A picking has already been created for this claim !'))
        return good_lines


    # Get default source location
    @api.model
    def _get_source_loc(self):
        warehouse_obj = self.env['stock.warehouse']
        warehouse_id = self._context.get('warehouse_id')
        if self._context.get('picking_type') == 'out':
            loc_id = warehouse_obj.browse(warehouse_id).lot_stock_id or False
        elif self._context.get('picking_type') in ['in', 'loss'] and context.get('partner_id'):
            loc_id = self.env['res.partner'].browse(self._context['partner_id']).property_stock_customer or False
        return loc_id

    @api.model
    # Get default destination location
    def _get_dest_loc(self):
        warehouse_obj = self.env['stock.warehouse']
        warehouse_id = self._context.get('warehouse_id')
        if self._context.get('picking_type') == 'out':
            loc_id = self.env['res.partner'].browse(self._context.get('partner_id')).property_stock_customer or False
        elif self._context.get('picking_type') == 'in':
            loc_id = warehouse_obj.browse(warehouse_id).lot_rma_id or False
        elif self._context.get('picking_type') == 'loss':
            loc_id = warehouse_obj.browse(warehouse_id).lot_carrier_loss_id or False
        return loc_id

    claim_line_source_location = fields.Many2one('stock.location', string='Source Location',help="Location where the returned products are from.", required=True, default=_get_source_loc)
    claim_line_dest_location = fields.Many2one('stock.location', string='Dest. Location',help="Location where the system will stock the returned products.", required=True, default=_get_dest_loc)
    claim_line_ids = fields.Many2many('claim.line', string='Claim lines', default=_get_claim_lines)

    @api.model
    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close',}

    # If "Create" button pressed
    @api.model
    def action_create_picking(self):
        picking_obj = self.env['stock.picking']
        claim_picking = False
        dummy, view_xml_id = self.env['ir.model.data'].get_object_reference('stock', 'view_picking_form')

        if self._context.get('picking_type') in ['in', 'loss']:
            p_type = 'in'
            write_field = 'move_in_id'
            if self._context.get('picking_type') == 'in':
                claim_picking = True
                note = 'RMA picking in'
            elif self._context.get('picking_type') == 'loss':
                name = 'Customer product loss'
                note = 'RMA product loss'
        elif self._context.get('picking_type') == 'out':
            p_type = 'out'
            write_field = 'move_out_id'
            note = 'RMA picking out'
        claim = self.env['crm.claim'].browse(self._context['active_id'])
        partner_id = claim.partner_id.id
        # create picking
        picking_id = picking_obj.create({
                    'origin': claim.number,
                    'type': p_type,
                    'move_type': 'one', # direct
                    'state': 'draft',
                    'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'partner_id': claim.partner_id.id,
                    'invoice_state': "none",
                    'company_id': claim.company_id.id,
                    'location_id': self.claim_line_source_location.id,
                    'location_dest_id': self.claim_line_dest_location.id,
                    'note' : note,
                    'claim_id': claim.id,
                    'claim_picking': claim_picking
                })
        # Create picking lines
        for wizard_claim_line in self.claim_line_ids:
            move_id = self.env['stock.move'].create({
                    'name' : wizard_claim_line.product_id.name_template, # Motif : crm id ? stock_picking_id ?
                    'priority': '0',
                    #'create_date':
                    'date': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'date_expected': time.strftime(DEFAULT_SERVER_DATETIME_FORMAT),
                    'product_id': wizard_claim_line.product_id.id,
                    'product_qty': wizard_claim_line.product_returned_quantity,
                    'product_uom': wizard_claim_line.product_id.uom_id.id,
                    'partner_id': claim.partner_id.id,
                    'prodlot_id': wizard_claim_line.prodlot_id.id,
                    # 'tracking_id':
                    'picking_id': picking_id,
                    'state': 'draft',
                    'price_unit': wizard_claim_line.unit_sale_price,
                    # 'price_currency_id': claim_id.company_id.currency_id.id, # from invoice ???
                    'company_id': claim.company_id.id,
                    'location_id': self.claim_line_source_location.id,
                    'location_dest_id': self.claim_line_dest_location.id,
                    'note': note,
                })
            self.env['claim.line'].write(wizard_claim_line.id, {write_field: move_id})
        if picking_id:
            workflow.trg_validate(self._uid, 'stock.picking', picking_id,'button_confirm', self._cr)
            picking_obj.action_assign([picking_id])
        return {
            'name': '%s' % name,
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': view_xml_id,
            'domain' : "[('type', '=', '%s'),('partner_id','=',%s)]" % (p_type, partner_id),
            'res_model': 'stock.picking',
            'res_id': picking_id,
            'type': 'ir.actions.act_window',
        }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
