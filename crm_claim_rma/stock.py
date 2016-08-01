# -*- coding: utf-8 -*-
#########################################################################
#                                                                       #
#                                                                       #
#########################################################################
#                                                                       #
# Copyright (C) 2009-2011  Akretion, Raphaël Valyi, Sébastien Beau, 	#
# Emmanuel Samyn, Benoît Guillot                                        #
#                                                                       #
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

from openerp import fields, models, api, _

class stock_picking(models.Model):
    _inherit = "stock.picking"
    
    claim_id = fields.Many2one('crm.claim', 'Claim')
    claim_picking = fields.Boolean('Picking from Claim')

class stock_warehouse(models.Model):
    _inherit = 'stock.warehouse'
    
    lot_rma_id = fields.Many2one('stock.location', 'Location RMA')
    lot_carrier_loss_id = fields.Many2one('stock.location', 'Location Carrier Loss')
    lot_breakage_loss_id = fields.Many2one('stock.location', 'Location Breakage Loss')
    lot_refurbish_id = fields.Many2one('stock.location', 'Location Refurbish')

#This part concern the case of a wrong picking out. We need to create a new stock_move in a micking already open.
#In order to don't have to confirm the stock_move we override the create and confirm it at the creation only for this case

class stock_move(models.Model):
    _inherit = "stock.move"
    
    @api.model
    def create(self, vals):
        move_id = super(stock_move, self).create(vals)
        if vals.get('picking_id'):
            picking = self.env['stock.picking'].browse(vals['picking_id'])
            if picking.claim_picking and picking.type == u'in':
                move = move_id.write({'state': 'confirmed'})
        return move_id