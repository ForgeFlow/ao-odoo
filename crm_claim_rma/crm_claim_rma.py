# -*- coding: utf-8 -*-
#########################################################################
#                                                                       #
#                                                                       #
#########################################################################
#                                                                       #
# Copyright (C) 2009-2011  Akretion, Raphaël Valyi, Sébastien Beau,     #
# Emmanuel Samyn                            #
#                                                                       #
# This program is free software: you can redistribute it and/or modify   #
# it under the terms of the GNU General Public License as published by   #
# the Free Software Foundation, either version 3 of the License, or      #
# (at your option) any later version.                                    #
#                                                                       #
# This program is distributed in the hope that it will be useful,        #
# but WITHOUT ANY WARRANTY; without even the implied warranty of         #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
# GNU General Public License for more details.                           #
#                                                                       #
# You should have received a copy of the GNU General Public License      #
# along with this program.  If not, see <http://www.gnu.org/licenses/>.  #
#########################################################################

from openerp import fields, models, api, _
from openerp.addons.crm import crm
from datetime import datetime
from dateutil.relativedelta import relativedelta
import time
from openerp.tools import DEFAULT_SERVER_DATE_FORMAT

# TODO: REFACTOR IN A GENERIC MODULE 
class substate_substate(models.Model): 
    """
    To precise a state (state=refused; substates= reason 1, 2,...)
    """
    _name = 'substate.substate'
    _description = 'substate that precise a given state'
    
    name = fields.Char('Sub state', required=True)
    substate_descr = fields.Text('Description', help="To give more information about the sub state") 
        # ADD OBJECT TO FILTER

class claim_line(models.Model):
    """
    Class to handle a product return line (corresponding to one invoice line)
    """
    _name = 'claim.line'
    _description = "List of product to return"
        
    # Method to calculate total amount of the line : qty*UP
    @api.depends('unit_sale_price', 'product_returned_quantity')
    def _line_total_amount(self):
        for line in self:            
            line.return_value = line.unit_sale_price * line.product_returned_quantity
        
    name = fields.Char('Description', required=True, default='none')
    claim_origine = fields.Selection([('none', 'Not specified'),
                                ('legal', 'Legal retractation'),
                                ('cancellation', 'Order cancellation'),
                                ('damaged', 'Damaged delivered product'),
                                ('error', 'Shipping error'),
                                ('exchange', 'Exchange request'),
                                ('lost', 'Lost during transport'),
                                ('other', 'Other')], 'Claim Subject', required=True, help="To describe the line product problem")
    claim_descr = fields.Text('Claim description', help="More precise description of the problem")  
    product_id = fields.Many2one('product.product', 'Product', help="Returned product")
    product_returned_quantity = fields.Float('Quantity', digits=(12, 2), help="Quantity of product returned")
    unit_sale_price = fields.Float('Unit sale price', digits=(12, 2), help="Unit sale price of the product. Auto filed if retrun done by invoice selection. BE CAREFUL AND CHECK the automatic value as don't take into account previous refounds, invoice discount, can be for 0 if product for free,...")
    return_value = fields.Float(compute='_line_total_amount', string='Total return', help="Quantity returned * Unit sold price")
    prodlot_id = fields.Many2one('stock.production.lot', 'Serial/Lot n°', help="The serial/lot of the returned product")
    applicable_guarantee = fields.Selection([('us', 'Company'), ('supplier', 'Supplier'), ('brand', 'Brand manufacturer')], 'Warranty type')  # TODO: Replace with function field. type supplier might generate an auto draft forward to the supplier
    guarantee_limit = fields.Date('Warranty limit', help="The warranty limit is computed as: invoice date + warranty defined on selected product.", readonly=True)
    warning = fields.Char('Warranty', readonly=True, help="If warranty has expired")
    warranty_type = fields.Char('Warranty type', readonly=True, help="from product form")
    warranty_return_partner = fields.Many2one('res.partner', 'Warranty return', help="Where the customer has to send back the product(s)")        
    claim_id = fields.Many2one('crm.claim', 'Related claim', help="To link to the case.claim object")
    state = fields.Selection([('draft', 'Draft'),
                                ('refused', 'Refused'),
                                ('confirmed', 'Confirmed, waiting for product'),
                                ('in_to_control', 'Received, to control'),
                                ('in_to_treate', 'Controlled, to treate'),
                                ('treated', 'Treated')], 'State', default='draft')
    substate_id = fields.Many2one('substate.substate', 'Sub state', help="Select a sub state to precise the standard state. Example 1: state = refused; substate could be warranty over, not in warranty, no problem,... . Example 2: state = to treate; substate could be to refund, to exchange, to repair,...")
    last_state_change = fields.Date('Last change', help="To set the last state / substate change")
    invoice_line_id = fields.Many2one('account.invoice.line', 'Invoice Line', help='The invoice line related to the returned product')
    refund_line_id = fields.Many2one('account.invoice.line', 'Refund Line', help='The refund line related to the returned product')
    move_in_id = fields.Many2one('stock.move', 'Move Line from picking in', help='The move line related to the returned product')
    move_out_id = fields.Many2one('stock.move', 'Move Line from picking out', help='The move line related to the returned product')

    # Method to calculate warranty limit
    @api.model
    def set_warranty_limit(self, claim_line):
        date_invoice = claim_line.invoice_line_id.invoice_id.date_invoice
        if date_invoice:
            warning = 'Valid'
            if claim_line.claim_id.claim_type == 'supplier':
                if claim_line.prodlot_id :
                    limit = (datetime.strptime(date_invoice, DEFAULT_SERVER_DATE_FORMAT) + relativedelta(months=int(claim_line.product_id.seller_ids[0].warranty_duration))).strftime(DEFAULT_SERVER_DATE_FORMAT)  # TODO: To be implemented
                else :
                    limit = (datetime.strptime(date_invoice, DEFAULT_SERVER_DATE_FORMAT) + relativedelta(months=int(claim_line.product_id.seller_ids[0].warranty_duration))).strftime(DEFAULT_SERVER_DATE_FORMAT) 
            else :
                limit = (datetime.strptime(date_invoice, DEFAULT_SERVER_DATE_FORMAT) + relativedelta(months=int(claim_line.product_id.warranty))).strftime(DEFAULT_SERVER_DATE_FORMAT)
            if limit < claim_line.claim_id.date:
                warning = 'Expired'
            self.write({
                'guarantee_limit' : limit,
                'warning' : warning,
            })
        else:
            raise Warning(_('Error !'), _('Cannot find any date for invoice ! Must be a validated invoice !'))
        return True

    # Method to calculate warranty return address
    @api.model
    def set_warranty_return_address(self, claim_line):
        return_address = None
        warranty_type = 'company'
        seller = claim_line.product_id.seller_info_id
        if seller:
            return_partner = seller.warranty_return_partner
            if return_partner:
                warranty_type = return_partner
            else:
                warranty_type = 'company'
            return_address = seller.warranty_return_address.id
#                if return_partner == 'company': 
#                    return_address = self._get_partner_address(cr, uid, ids, context,claim_line.claim_id.company_id.partner_id)[0]
#                elif return_partner == 'supplier':
#                    return_address = self._get_partner_address(cr, uid, ids, context,claim_line.product_id.seller_ids[0].name)[0]
#                    warranty_type = 'supplier'
#                elif return_partner == 'brand':
#                    return_address = self._get_partner_address(cr, uid, ids, context, claim_line.product_id.product_brand_id.partner_id)[0]
#                    warranty_type = 'brand'
#                else :
#                    warranty_type = 'other'
#                    # TO BE IMPLEMENTED if something to do...
#            else :
#                warranty_type = 'company'
#                return_address = self._get_default_company_address(cr, uid, claim_line.claim_id.company_id, context=context)
                # TODO fix me use default address
#                self.write(cr,uid,ids,{'warranty_return_partner':1,'warranty_type': 'company'})
#                return True

                # raise osv.except_osv(_('Error !'), _('Cannot find any warranty return partner for this product !'))
        else : 
            warranty_type = 'company'
            if claim_line.claim_id.company_id.crm_return_address_id:
                return_address = [claim_line.claim_id.company_id.crm_return_address_id.id]
            else:
                return_address = [claim_line.claim_id.company_id.partner_id.address[0].id]
#            return_address = self._get_default_company_address(cr, uid, claim_line.claim_id.company_id, context=context)
            # TODO fix me use default address
#            self.write(cr,uid,ids,{'warranty_return_partner':1,'warranty_type': 'company'})
#            return True
            # raise osv.except_osv(_('Error !'), _('Cannot find any supplier for this product !'))                
        self.write({'warranty_return_partner': return_address, 'warranty_type': warranty_type}) 
        return True
               
    # Method to calculate warranty limit and validity
    @api.multi
    def set_warranty(self):
        for claim_line in self:
            if claim_line.product_id and claim_line.invoice_line_id:
                self.set_warranty_limit(claim_line)
                self.set_warranty_return_address(claim_line)
            else:
                raise Warning(_('Error !'), _('PLEASE SET PRODUCT & INVOICE!'))
        return True 

# TODO add the option to split the claim_line in order to manage the same product separately

class crm_claim(models.Model):
    _inherit = 'crm.claim'

    number = fields.Char('Number', readonly=True, required=True, help="Company internal claim unique number", default=lambda obj: obj.env['ir.sequence'].get('crm.claim'))
    claim_type = fields.Selection([('customer', 'Customer'),
                                    ('supplier', 'Supplier'),
                                    ('other', 'Other')], 'Claim type', default='customer', required=True, help="customer = from customer to company ; supplier = from company to supplier")
    claim_line_ids = fields.One2many('claim.line', 'claim_id', 'Return lines')

        # NOTE- COMMENTED CODE REFERERS TO MODEL product.exchange WHICH DOESN'T EXIST
    # product_exchange_ids = fields.One2many('product.exchange', 'claim_return_id', 'Product exchanges')

    # Aftersale outsourcing        
#        'in_supplier_picking_id = fields.Many2one('stock.picking', 'Return To Supplier Picking', required=False, select=True),
#        'out_supplier_picking_id = fields.Many2one('stock.picking', 'Return From Supplier Picking', required=False, select=True),

    # Financial management
    planned_revenue = fields.Float('Expected revenue')
    planned_cost = fields.Float('Expected cost')
    real_revenue = fields.Float('Real revenue')
    real_cost = fields.Float('Real cost')
    invoice_ids = fields.One2many('account.invoice', 'claim_id', 'Refunds')
    picking_ids = fields.One2many('stock.picking', 'claim_id', 'RMA')
    invoice_id = fields.Many2one('account.invoice', 'Invoice', help='Related invoice')
    warehouse_id = fields.Many2one('stock.warehouse', 'Warehouse', required=True, default=1)

    @api.multi
    def onchange_partner_address_id(self, add, email=False):
        res = super(crm_claim, self).onchange_partner_address_id(add, email=email)
        if add:
            if not res['value']['email_from'] or not res['value']['partner_phone']:
                address = self.env['res.partner'].browse(add)
                for other_add in address.partner_id.address:
                    if other_add.email and not res['value']['email_from']:
                        res['value']['email_from'] = other_add.email
                    if other_add.phone and not res['value']['partner_phone']:
                        res['value']['partner_phone'] = other_add.phone
        return res
    
    @api.multi
    def onchange_invoice_id(self, invoice_id):
        invoice_line_obj = self.env['account.invoice.line']
        invoice_line_ids = invoice_line_obj.search([('invoice_id', '=', invoice_id)])
        claim_lines = []
        for invoice_line in invoice_line_ids:
#            claim_line_obj = self.pool.get('claim.line')
            claim_lines.append({
                    'name': invoice_line.name,
                    'claim_origine' : "none",
                    'invoice_line_id': invoice_line.id,
                    'product_id' : invoice_line.product_id.id,
                    'product_returned_quantity' : invoice_line.quantity,
                    'unit_sale_price' : invoice_line.price_unit,
#                    'prodlot_id' : invoice_line.,
                    'state' : 'draft',
                })
#            for line in claim_line_obj.browse(cr,uid,[line_id],context):
#                line.set_warranty()
        return  {'value' : {'claim_line_ids' : claim_lines}}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
