# -*- coding: utf-8 -*-
#########################################################################
#                                                                       #
#                                                                       #
#########################################################################
#                                                                       #
# Copyright (C) 2009-2011  Akretion, Emmanuel Samyn                     #
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

from openerp import models, fields, api, _

class returned_lines_from_serial(models.TransientModel):
    _name='returned_lines_from_serial.wizard'
    _description='Wizard to create product return lines from serial numbers'


    # Get partner from case is set to filter serials
    @api.model
    def _get_default_partner_id(self):
        return self.env['crm.claim'].browse(self._context['active_id']).partner_id or False


    prodlot_id_1 = fields.Many2one('stock.production.lot', string='Serial / Lot Number 1', required=True)
    prodlot_id_2 = fields.Many2one('stock.production.lot', string='Serial / Lot Number 2')
    prodlot_id_3 = fields.Many2one('stock.production.lot', string='Serial / Lot Number 3')
    prodlot_id_4 = fields.Many2one('stock.production.lot', string='Serial / Lot Number 4')
    prodlot_id_5 = fields.Many2one('stock.production.lot', string='Serial / Lot Number 5')
    qty_1 = fields.Float(string='Quantity 1', digits=(12,2), required=True, default=1.0)
    qty_2 = fields.Float(string='Quantity 2', digits=(12,2), default=1.0)
    qty_3 = fields.Float(string='Quantity 3', digits=(12,2), default=1.0)
    qty_4 = fields.Float(string='Quantity 4', digits=(12,2), default=1.0)
    qty_5 = fields.Float(string='Quantity 5', digits=(12,2), default=1.0)
    claim_1 = fields.Selection([('none','Not specified'),
                                ('legal','Legal retractation'),
                                ('cancellation','Order cancellation'),
                                ('damaged','Damaged delivered product'),                                    
                                ('error','Shipping error'),
                                ('exchange','Exchange request'),
                                ('lost','Lost during transport'),
                                ('other','Other')], default='none', string='Claim Subject', required=True, help="To describe the product problem")
    claim_2 = fields.Selection([('none','Not specified'),
                                ('legal','Legal retractation'),
                                ('cancellation','Order cancellation'),
                                ('damaged','Damaged delivered product'),                                    
                                ('error','Shipping error'),
                                ('exchange','Exchange request'),
                                ('lost','Lost during transport'),
                                ('other','Other')], default='none', string='Claim Subject', required=True, help="To describe the line product problem")
    claim_3 = fields.Selection([('none','Not specified'),
                                ('legal','Legal retractation'),
                                ('cancellation','Order cancellation'),
                                ('damaged','Damaged delivered product'),                                    
                                ('error','Shipping error'),
                                ('exchange','Exchange request'),
                                ('lost','Lost during transport'),
                                ('other','Other')], default='none', string='Claim Subject', required=True, help="To describe the line product problem")
    claim_4 = fields.Selection([('none','Not specified'),
                                ('legal','Legal retractation'),
                                ('cancellation','Order cancellation'),
                                ('damaged','Damaged delivered product'),                                    
                                ('error','Shipping error'),
                                ('exchange','Exchange request'),
                                ('lost','Lost during transport'),
                                ('other','Other')], default='none', sting='Claim Subject', required=True, help="To describe the line product problem")
    claim_5 = fields.Selection([('none','Not specified'),
                                ('legal','Legal retractation'),
                                ('cancellation','Order cancellation'),
                                ('damaged','Damaged delivered product'),                                    
                                ('error','Shipping error'),
                                ('exchange','Exchange request'),
                                ('lost','Lost during transport'),
                                ('other','Other')], default='none', string='Claim Subject', required=True, help="To describe the line product problem")
    partner_id = fields.Many2one('res.partner', string='Partner', default=_get_default_partner_id)
    

    # If "Cancel" button pressed
    @api.model
    def action_cancel(self):
        return {'type': 'ir.actions.act_window_close',}
    
    # If "Add & close" button pressed
    @api.multi
    def action_add_and_close(self):
        self.add_return_lines()    
        return {'type': 'ir.actions.act_window_close',}
    
    # If "Add & new" button pressed
    @api.multi    
    def action_add_and_new(self):
        self.add_return_lines()
        return {
            'context': self._context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'returned_lines_from_serial.wizard',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
        }
    
    # Method to get the product id from set
    @api.model
    def get_product_id(self, product_set):
        product_id = False
        for product in self.prodlot_2_product([product_set]):
            product_id = product
        return product_id

    # Method to create return lines
    @api.model
    def add_return_lines(self):
        # NOTE- RETURN.LINE - NO SUCH MODEL EXISTS. SO GIVING ERROR
        return_line = self.env['return.line']
        # Refactor code : create 1 "createmethode" called by each if with values as parameters    
        return_line.create({
                    'claim_id': self._context['active_id'],
                    'claim_origine': self.claim_1,
                    'product_id' : self.get_product_id(self.prodlot_id_1.id),
                    #'invoice_id' : self.prodlot_2_invoice(cr, uid,[result.prodlot_id_1.id],[result.prodlot_id_1.product_id.id]), #PRODLOT_ID can be in many invoice !!
                    'product_returned_quantity' : self.qty_1,
                    'prodlot_id' : self.prodlot_id_1.id,
					'selected' : False,		
					'state' : 'draft',                    
					#'guarantee_limit' : warranty['value']['guarantee_limit'],
					#'warning' : warranty['value']['warning'],
               }) 
        if self.prodlot_id_2.id : 
            return_line.create({
                    'claim_id': self._context['active_id'],
                    'claim_origine': self.claim_2,
                    'product_id' : self.get_product_id(self.prodlot_id_2.id),
#                    'invoice_id' : self.prodlot_2_invoice(cr, uid,[result.prodlot_id_1.id]),
                    'product_returned_quantity' : self.qty_2,
                    'prodlot_id' : self.prodlot_id_2.id,
					'selected' : False,		
					'state' : 'draft',                    
					#'guarantee_limit' : warranty['value']['guarantee_limit'],
					#'warning' : warranty['value']['warning'],
               })
        if self.prodlot_id_3.id : 
            return_line.create({
                    'claim_id': self._context['active_id'],
                    'claim_origine': self.claim_3,
                    'product_id' : self.get_product_id(self.prodlot_id_3.id),
#                    'invoice_id' : self.prodlot_2_invoice(cr, uid,[result.prodlot_id_1.id]),
                    'product_returned_quantity' : self.qty_3,
                    'prodlot_id' : self.prodlot_id_3.id,
                    'selected' : False,		
					'state' : 'draft', 
					#'guarantee_limit' : warranty['value']['guarantee_limit'],
					#'warning' : warranty['value']['warning'],
               })
        if self.prodlot_id_4.id : 
            return_line.create({
                    'claim_id': self._context['active_id'],
                    'claim_origine': self.claim_4,
                    'product_id' : self.get_product_id(self.prodlot_id_4.id),
#                    'invoice_id' : self.prodlot_2_invoice(cr, uid,[result.prodlot_id_1.id]),
                    'product_returned_quantity' : self.qty_4,
                    'prodlot_id' : self.prodlot_id_4.id,
                    'selected' : False,		
					'state' : 'draft', 
					#'guarantee_limit' : warranty['value']['guarantee_limit'],
					#'warning' : warranty['value']['warning'],
               })
        if self.prodlot_id_5.id : 
            return_line.create({
                    'claim_id': self._context['active_id'],
                    'claim_origine': self.claim_5,
                    'product_id' : self.get_product_id(self.prodlot_id_5.id),
#                    'invoice_id' : self.prodlot_2_invoice(cr, uid,[result.prodlot_id_1.id],[result.prodlot_id_1.product_id.id]),
                    'product_returned_quantity' : self.qty_5,
                    'prodlot_id' : self.prodlot_id_5.id,
                    'selected' : False,		
					'state' : 'draft', 
					#'guarantee_type':
					#'guarantee_limit' : warranty['value']['guarantee_limit'],
					#'warning' : warranty['value']['warning'],					
               })  					
					                 
        return True
        
    @api.model
    def prodlot_2_product(self, prodlot_ids):          
        stock_move_ids=self.env['stock.move'].search([('prodlot_id', 'in', prodlot_ids)])
        res=self.env['stock.move'].read(stock_move_ids, ['product_id'])
        return set([x['product_id'][0] for x in res if x['product_id']])

    @api.model        
    def prodlot_2_invoice(self, prodlot_id,product_id):
        print "prodlot_ids : ", prodlot_id
        print "product_id : ", product_id
        # get stock_move_ids
        stock_move_ids = self.env['stock.move'].search([('prodlot_id', 'in', prodlot_id)])
        print "stock_move_ids : ", stock_move_ids
        # if 1 id
            # (get stock picking (filter on out ?))
            # get invoice_ids from stock_move_id where invoice.line.product = prodlot_product and invoice customer = claim_partner
            # if 1 id
                # return invoice_id
            # else
        # else : move_in / move_out ; 1 move per order line so if many order lines with same lot, ...
        
        
        #
        #return set(self.stock_move_2_invoice(cr, uid, stock_move_ids))
        return True

    @api.model
    def stock_move_2_invoice(self, stock_move_ids):
        inv_line_ids = []
        res=self.env['stock.move'].read(stock_move_ids, ['sale_line_id'])
        sale_line_ids = [x['sale_line_id'][0] for x in res if x['sale_line_id']]
        if not sale_line_ids:
            return []
        cr.execute("select invoice_id from sale_order_line_invoice_rel where order_line_id in ("+ ','.join(map(lambda x: str(x),sale_line_ids))+')')
        res = cr.fetchall()     
        for i in res:
            for j in i:
                inv_line_ids.append(j)

        res=self.env['account.invoice.line'].read(inv_line_ids,['invoice_id'])
        return [x['invoice_id'][0] for x in res if x['invoice_id']]  
                      
returned_lines_from_serial()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
