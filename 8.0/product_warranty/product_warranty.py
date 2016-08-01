# -*- coding: utf-8 -*-
#########################################################################
#                                                                       #
#                                                                       #
#########################################################################
#                                                                       #
# Copyright (C) 2009-2011  Akretion, Emmanuel Samyn, Benoît Guillot     #
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

class return_instruction(models.Model):
    _name = "return.instruction"
    _description = "Instructions for product return"
    
    name = fields.Char(string = 'Title', required=True)
    instructions = fields.Text(string = 'Instructions', help="Instructions for product return")
    is_default = fields.Boolean(string = 'Is default', help="If is default, will be use to set the default value in supplier infos. Be careful to have only one default")

class product_supplierinfo(models.Model):
    _inherit = "product.supplierinfo"

    @api.model
    def get_warranty_return_partner(self):
        result = [
                ('company','Company'),
                ('supplier','Supplier'),
                ('other','Other'),]
        if self.env['ir.module.module'].search([('name','like','product_brand'),('state','like','installed')]):
            result.append(('brand','Brand manufacturer'),)
        return result

    # Get selected lines to add to exchange
    @api.model
    def _get_default_instructions(self):
        instruction_ids = self.env['return.instruction'].search([('is_default','=', True)])
        if instruction_ids:
            return instruction_ids[0]
            # TODO f(supplier) + other.
        return instruction_ids

    @api.multi
    def _get_warranty_return_address(self):
        # Method to return the partner delivery address or if none, the default address
        # dedicated_delivery_address stand for the case a new type of address more particularly dedicated to return delivery would be implemented.
        result ={}
        address_obj = self.env['res.partner']
        for supplier_info in self:
            result[supplier_info.id] = {}
            address_id = False
            return_partner = supplier_info.warranty_return_partner
            if return_partner:
                
                if return_partner == 'supplier':
                    partner_id = supplier_info.name.id
                elif return_partner == 'brand':
                    if not supplier_info.product_id.product_brand_id.partner_id:
                        raise except_orm(_('Error !'), _('You need to define a partner for the brand of the product. !'))
                    partner_id = supplier_info.product_id.product_brand_id.partner_id.id
                else:
                    partner_id = supplier_info.company_id.partner_id.id
# TODO : Find the partner with a delivery address, child of the partner
# v6.1 code with res.partner.address :
#                address_id = address_obj.search(cr, uid, [('partner_id', '=', partner_id), ('type', 'like', 'dedicated_delivery')], context=context)
#                if not address_id:
#                    address_id = address_obj.search(cr, uid, [('partner_id','=', partner_id), ('type','like','delivery')], context=context)
#                    if not address_id:
#                        address_id = address_obj.search(cr, uid, [('partner_id', '=', partner_id), ('type', 'like', 'default')], context=context)
#                if not address_id:
#                    raise osv.except_osv(_('Error !'), _('No address define for the %s!') % return_partner)
#                #result[supplier_info.id] = address_id[0]
                supplier_info.warranty_return_address = partner_id

    warranty_duration = fields.Float(string = 'Warranty', help="Warranty in month for this product/supplier relation. Only for company/supplier relation (purchase order) ; the customer/company relation (sale order) always use the product main warranty field")
    warranty_return_partner =  fields.Selection('get_warranty_return_partner', string = 'Warrantee return', default='company', help="Who is in charge of the warranty return treatment toward the end customer. Company will use the current compagny delivery or default address and so on for supplier and brand manufacturer. Doesn't necessarly mean that the warranty to be applied is the one of the return partner (ie: can be returned to the company and be under the brand warranty")
    return_instructions =  fields.Many2one('return.instruction', string = 'Instructions',help="Instructions for product return", default= _get_default_instructions)
    active_supplier =  fields.Boolean(string= 'Active supplier', help="")
    warranty_return_address =  fields.Many2one('res.partner',compute ='_get_warranty_return_address', string="Warranty return address")
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
