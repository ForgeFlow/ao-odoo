# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
import time

from osv import osv, fields
from tools.translate import _
import decimal_precision as dp

from avalara_api import AvaTaxService, BaseAddress
from compiler.ast import TryFinally


class res_partner(osv.osv):
    """Update partner information by adding new fields according to avalara partner configuration"""
    _inherit = 'res.partner'
    _columns = {
        'exemption_number': fields.char('Exemption Number', size=64, help="Indicates if the customer is exempt or not"),
        'exemption_code_id': fields.many2one('exemption.code', 'Exemption Code', help="Indicates the type of exemption the customer may have"),
        'tax_schedule_id': fields.many2one('tax.schedule', 'Tax Schedule', help="Identifies customers using AVATAX. Only customers with AVATAX designation triggers tax calculation from Avatax otherwise it will follow the normal tax calculation that OpenERP provides"),
        
        'date_validation': fields.date('Last Validation Date', readonly=True, help="The date the address was last validated by AvaTax and accepted"),
        'validation_method': fields.selection([('avatax', 'AVALARA'), ('usps', 'USPS'), ('other', 'Other')], 'Address Validation Method', readonly=True, help="It gets populated when the address is validated by the method"),
        'latitude': fields.char('Latitude', size=32),
        'longitude': fields.char('Longitude', size=32),
        'validated_on_save': fields.boolean('Validated On Save', help="Indicates if the address is already validated on save before calling the wizard"),
        'customer_code': fields.char('Customer Code', size=40, required=True),
        'tax_apply': fields.boolean('Tax Calculation',help="Indicates the avatax calculation is compulsory"),
        'tax_exempt': fields.boolean('Is Tax Exempt',help="Indicates the exemption tax calculation is compulsory"),
        'vat_id': fields.char("VAT ID", help="Customers VAT number (Buyer VAT). Identifies the customer as a “Registered Business” and the tax engine will utilize that information in the tax decision process."),
    }
    _sql_constraints = [
        ('name_uniq', 'unique(customer_code)', 'Customer Code must be unique!'),
    ]
    
    def check_avatax_support(self, cr, uid, avatax_config, country_id, context=None):
        """ Checks if address validation pre-condition meets. """

        if avatax_config.address_validation:
            raise osv.except_osv(_('Avatax: Address Validation is Disabled'), _("The AvaTax Address Validation Service is disabled by the administrator. Please make sure it's enabled for the address validation"))
        if country_id and country_id not in [x.id for x in avatax_config.country_ids] or not country_id:
            return False
#            raise osv.except_osv(_('Avatax: Address Validation not Supported for this country'), _("The AvaTax Address Validation Service does not support this country in the configuration, please continue with your normal process."))
        return True
    
    
    def onchange_tax_exemption(self, cr, uid, ids, tax_exempt, context=None):
        if not tax_exempt:
            return {'value': {'exemption_number':'', 'exemption_code_id':None}}
        else:
            return {}

    def get_state_id(self, cr, uid, code, c_code, context=None):
        """ Returns the id of the state from the code. """
        state_obj = self.pool.get('res.country.state')
        c_id = self.pool.get('res.country').search(cr, uid, [('code', '=', c_code)], context=context)[0]
        s_id = state_obj.search(cr, uid, [('code', '=', code),('country_id', '=',c_id)], context=context)
        if s_id: return s_id[0]
        return False

    def get_country_id(self, cr, uid, code, context=None):
        """ Returns the id of the country from the code. """

        country_obj = self.pool.get('res.country')
        return country_obj.search(cr, uid, [('code', '=', code)], context=context)[0]

    def get_state_code(self, cr, uid, state_id, context=None):
        """ Returns the code from the id of the state. """

        state_obj = self.pool.get('res.country.state')
        return state_id and state_obj.browse(cr, uid, state_id, context=context).code

    def get_country_code(self, cr, uid, country_id, context=None):
        """ Returns the code from the id of the country. """

        country_obj = self.pool.get('res.country')
        return country_id and country_obj.browse(cr, uid, country_id, context=context).code
    
    def multi_address_validation(self, cr, uid, ids, context=None):
        add_val_ids = []
        address_obj = self.pool.get('res.partner')
        if context:
            add_val_ids = context.get('active_ids')
        for val_id in add_val_ids:
            vals = address_obj.read(cr, uid, val_id, ['street', 'street2', 'city', 'state_id', 'zip', 'country_id'], context=context)
            vals['state_id'] = vals.get('state_id') and vals['state_id'][0]
            vals['country_id'] = vals.get('country_id') and vals['country_id'][0]
            
            avatax_config_obj= self.pool.get('avalara.salestax')
            avatax_config = avatax_config_obj._get_avatax_config_company(cr, uid, context=context)

            if avatax_config:
                try:
                    valid_address = self._validate_address(cr, uid, vals, avatax_config, context=context)
                    vals.update({
                        'street': valid_address.Line1,
                        'street2': valid_address.Line2,
                        'city': valid_address.City,
                        'state_id': self.get_state_id(cr, uid, valid_address.Region, valid_address.Country, context=context),
                        'zip': valid_address.PostalCode,
                        'country_id': self.get_country_id(cr, uid, valid_address.Country, context=context),
                        'latitude': valid_address.Latitude,
                        'longitude': valid_address.Longitude,
                        'date_validation': time.strftime('%Y-%m-%d'),
                        'validation_method': 'avatax',
                        'validated_on_save': True
                    })
                    self.write(cr, uid, [val_id], vals, context=context)
                    cr.commit()
                except:
                    pass
        mod_obj = self.pool.get('ir.model.data')
        res = mod_obj.get_object_reference(cr, uid, 'base', 'view_partner_tree')
        res_id = res and res[1] or False,

        return {
            'view_type': 'list',
            'view_mode': 'list,form',
            'res_model': 'res.partner',
            'type':'ir.actions.act_window',
            'context': {'search_default_customer':1},
        }

    def _validate_address(self, cr, uid, address, avatax_config=False, context=None):
        """ Returns the valid address from the AvaTax Address Validation Service. """
        avatax_config_obj= self.pool.get('avalara.salestax')
        if context is None:
            context = {}

        if not avatax_config:
            avatax_config = avatax_config_obj._get_avatax_config_company(cr, uid, context=context)
        # Create the AvaTax Address service with the configuration parameters set for the instance
        avapoint = AvaTaxService(avatax_config.account_number, avatax_config.license_key,
                        avatax_config.service_url, avatax_config.request_timeout, avatax_config.logging)
        addSvc = avapoint.create_address_service().addressSvc

        # Obtain the state code & country code and create a BaseAddress Object
        state_code = address.get('state_id') and self.get_state_code(cr, uid, address['state_id'], context=context)
        country_code = address.get('country_id') and self.get_country_code(cr, uid, address['country_id'], context=context)
        baseaddress = BaseAddress(addSvc, address.get('street') or None, address.get('street2') or None,
                         address.get('city'), address.get('zip'), state_code, country_code, 0).data
        result = avapoint.validate_address(baseaddress, avatax_config.result_in_uppercase and 'Upper' or 'Default')
        
        valid_address = result.ValidAddresses[0][0]
        return valid_address

    def update_address(self, cr, uid, ids, vals, from_write=False, context=None):
        """ Updates the vals dictionary with the valid address as returned from the Avalara Address Validation. """
        address = vals        
        if vals and ids:
            if (vals.get('street') or vals.get('street2') or vals.get('zip') or vals.get('city') or \
                vals.get('country_id') or vals.get('state_id')):
                address_obj = self.pool.get('res.partner')
                avatax_config_obj= self.pool.get('avalara.salestax')
                avatax_config = avatax_config_obj._get_avatax_config_company(cr, uid, context=context)
    
                if avatax_config and avatax_config.validation_on_save:
                    brw_address = address_obj.read(cr, uid, ids[0], ['street', 'street2', 'city', 'state_id', 'zip', 'country_id'], context=context)
                    address['country_id'] = 'country_id' in vals and vals['country_id'] or brw_address.get('country_id') and brw_address['country_id'][0]
                    if self.check_avatax_support(cr, uid, avatax_config, address['country_id'], context=context):
                        if from_write:
                            address['street'] = 'street' in vals and vals['street'] or ''
                            address['street2'] = 'street2' in vals and vals['street2'] or ''
                            address['city'] = 'city' in vals and vals['city'] or ''
                            address['zip'] = 'zip' in vals and vals['zip'] or ''
                            address['state_id'] = 'state_id' in vals and vals['state_id'] or brw_address.get('state_id') and brw_address['state_id'][0] or False
                        valid_address = self._validate_address(cr, uid, address, avatax_config, context=context)
                        vals.update({
                            'street': valid_address.Line1,
                            'street2': valid_address.Line2,
                            'city': valid_address.City,
                            'state_id': self.get_state_id(cr, uid, valid_address.Region, valid_address.Country, context=context),
                            'zip': valid_address.PostalCode,
                            'country_id': self.get_country_id(cr, uid, valid_address.Country, context=context),
                            'latitude': valid_address.Latitude,
                            'longitude': valid_address.Longitude,
                            'date_validation': time.strftime('%Y-%m-%d'),
                            'validation_method': 'avatax',
                            'validated_on_save': True
                        })
        return vals

    def create(self, cr, uid, vals, context=None):
        if vals.get('parent_id') and vals.get('use_parent_address'):
            domain_siblings = [('parent_id', '=', vals['parent_id']), ('use_parent_address', '=', True)]
            update_ids = [vals['parent_id']] + self.search(cr, uid, domain_siblings, context=context)
            vals = self.update_address(cr, uid, update_ids, vals, context=context)
        else:
            address = vals
            if (vals.get('street') or vals.get('street2') or vals.get('zip') or vals.get('city') or \
                vals.get('country_id') or vals.get('state_id')):
    
                address_obj = self.pool.get('res.partner')
                avatax_config_obj= self.pool.get('avalara.salestax')
                avatax_config = avatax_config_obj._get_avatax_config_company(cr, uid, context=context)
                
                if vals.get('tax_exempt'):
                    if not vals.get('exemption_number') and vals.get('exemption_code_id') == False :
                        raise osv.except_osv("Avatax: Warning !", "Please enter either Exemption Number or Exemption Code for marking customer as Exempt.") 
                
                
                #It will work when user want to validate address at customer creation, check option in avalara api form
                if avatax_config and avatax_config.validation_on_save:
                    if self.check_avatax_support(cr, uid, avatax_config, address.get('country_id'), context=context):
                        fields_to_read = filter(lambda x: x not in vals, ['street', 'street2', 'city', 'state_id', 'zip', 'country_id'])
                        address = fields_to_read and address_obj.read(cr, uid, ids, fields_to_read, context=context)[0] or {}
                        address['state_id'] = address.get('state_id') and address['state_id'][0]
                        address['country_id'] = address.get('country_id') and address['country_id'][0]
                        address.update(vals)
    
                        valid_address = self._validate_address(cr, uid, address, avatax_config, context=context)
                        vals.update({
                            'street': valid_address.Line1,
                            'street2': valid_address.Line2,
                            'city': valid_address.City,
                            'state_id': self.get_state_id(cr, uid, valid_address.Region, valid_address.Country, context=context),
                            'zip': valid_address.PostalCode,
                            'country_id': self.get_country_id(cr, uid, valid_address.Country, context=context),
                            'latitude': valid_address.Latitude,
                            'longitude': valid_address.Longitude,
                            'date_validation': time.strftime('%Y-%m-%d'),
                            'validation_method': 'avatax',
                            'validated_on_save': True
                        })
        return super(res_partner, self).create(cr, uid, vals, context)

    def write(self, cr, uid, ids, vals, context=None):
        vals.update({
            'latitude': '',
            'longitude': '',
            'date_validation': False,
            'validation_method': '',
            'validated_on_save': False,
        })

        if context is None:
            context = {}

        #when tax exempt check then atleast exemption number or exemption code should be filled            
        if vals.get('tax_exempt'):
            if not vals.get('exemption_number') and not vals.get('exemption_code_id'):
                raise osv.except_osv("Avatax: Warning !", "Please enter either Exemption Number or Exemption Code for marking customer as Exempt.")
        # Follow the normal write process if it's a write operation from the wizard
        if context.get('from_validate_button', False):
            return super(res_partner, self).write(cr, uid, ids, vals, context)
#        if context.get('active_id', False):
        vals1 = self.update_address(cr, uid, ids, vals, True, context=context)
        return super(res_partner, self).write(cr, uid, ids, vals1, context)
    

res_partner()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: