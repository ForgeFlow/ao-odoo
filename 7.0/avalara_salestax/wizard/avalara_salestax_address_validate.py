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

class avalara_salestax_address_validate(osv.osv_memory):
    """Address Validation using Avalara API"""
    _name = 'avalara.salestax.address.validate'
    _description = 'Address Validation using AvaTax'
    _columns = {
        'original_street': fields.char('Street', size=64, readonly=True),
        'original_street2': fields.char('Street2', size=64, readonly=True),
        'original_city': fields.char('City', size=64, readonly=True),
        'original_zip': fields.char('Zip', size=64, readonly=True),
        'original_state': fields.char('State', size=64, readonly=True),
        'original_country': fields.char('Country', size=64, readonly=True),
        'street': fields.char('Street', size=64),
        'street2': fields.char('Street2', size=64),
        'city': fields.char('City', size=64),
        'zip': fields.char('Zip', size=64),
        'state': fields.char('State', size=64),
        'country': fields.char('Country', size=64),
        'latitude': fields.char('Laitude', size=64),
        'longitude': fields.char('Longitude', size=64)
    }

    def view_init(self, cr, uid, fields, context=None):
        """ Checks for precondition before wizard executes. """
        address_obj = self.pool.get('res.partner')
        avatax_config_obj= self.pool.get('avalara.salestax')

        if context is None:
            context = {}

        # Check if there is avatax tax service active for the user company.
        # Prevent validating the address if the address validation is disabled by the administrator.

        if context.get('active_id', False) and context.get('active_model', False) == 'res.partner':
            avatax_config = avatax_config_obj._get_avatax_config_company(cr, uid, context=context)
            if not avatax_config:
                raise osv.except_osv(_('Avatax: Service Not Setup'), _("The AvaTax Tax Service is not active."))
            address = address_obj.browse(cr, uid, context['active_id'], context=context)
            if avatax_config.validation_on_save:
                raise osv.except_osv(_('Avatax: Address Already Validated'), _("Address Validation on Save is already active in the AvaTax Configuration."))
            address_obj.check_avatax_support(cr, uid, avatax_config, address.country_id and address.country_id.id or False, context=context)
        return True

    def default_get(self, cr, uid, fields, context=None):
        """  Returns the default values for the fields. """

        res = super(avalara_salestax_address_validate, self).default_get(cr, uid, fields, context)

        if context.get('active_id', False) and context.get('active_model', False) == 'res.partner':
            address_obj = self.pool.get('res.partner')
            address_obj.write(cr, uid, [context['active_id']], {
                                                        'latitude': '',
                                                        'longitude': '',
                                                        'date_validation': False,
                                                        'validation_method': '',
                                                        })
            cr.commit()     #Need to forcefully commit data when address not validate after changes in validate address
            
            address = address_obj.read(cr, uid, context['active_id'], ['street', 'street2', 'city', 'state_id', 'zip', 'country_id'], context=context)
            address['state_id'] = address.get('state_id') and address['state_id'][0]
            address['country_id'] = address.get('country_id') and address['country_id'][0]
            # Get the valid result from the AvaTax Address Validation Service
            valid_address = address_obj._validate_address(cr, uid, address, context=context)

            if 'original_street' in fields:
                res.update({'original_street': address['street']})
            if 'original_street2' in fields:
                res.update({'original_street2': address['street2']})
            if 'original_city' in fields:
                res.update({'original_city': address['city']})
            if 'original_state' in fields:
                res.update({'original_state': address_obj.get_state_code(cr, uid, address['state_id'], context=context)})
            if 'original_zip' in fields:
                res.update({'original_zip': address['zip']})
            if 'original_country' in fields:
                res.update({'original_country': address_obj.get_country_code(cr, uid, address['country_id'], context=context)})
            if 'street' in fields:
                res.update({'street': str(valid_address.Line1 or '')})
            if 'street2' in fields:
                res.update({'street2': str(valid_address.Line2 or '')})
            if 'city' in fields:
                res.update({'city': str(valid_address.City or '')})
            if 'state' in fields:
                res.update({'state': str(valid_address.Region or '')})
            if 'zip' in fields:
                res.update({'zip': str(valid_address.PostalCode or '')})
            if 'country' in fields:
                res.update({'country': str(valid_address.Country or '')})
            if 'latitude' in fields:
                res.update({'latitude': str(valid_address.Latitude or '')})
            if 'longitude' in fields:
                res.update({'longitude': str(valid_address.Longitude or '')})
        return res

    def accept_valid_address(self, cr, uid, ids, context=None):
        """ Updates the existing address with the valid address returned by the service. """

        valid_address = self.read(cr, uid, ids, context=context)[0]
        if context.get('active_id', False):
            address_obj = self.pool.get('res.partner')
            address_result = {
                'street': valid_address['street'],
                'street2': valid_address['street2'],
                'city': valid_address['city'],
                'state_id': address_obj.get_state_id(cr, uid, valid_address['state'], valid_address['country'], context=context),
                'zip': valid_address['zip'],
                'country_id': address_obj.get_country_id(cr, uid, valid_address['country'], context=context),
                'latitude': valid_address['latitude'] or 'unavailable',
                'longitude': valid_address['longitude'] or 'unavailable',
                'date_validation': time.strftime('%Y-%m-%d'),
                'validation_method': 'avatax'
            }
            address_obj.write(cr, uid, [context['active_id']], address_result, context=context)
        return {'type': 'ir.actions.act_window_close'}

avalara_salestax_address_validate()


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
