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
import string

from osv import osv, fields
from tools.translate import _

from avalara_api import AvaTaxService, BaseAddress, Line

class account_tax(osv.osv):
    """Inherit to implement the tax using avatax API"""
    _inherit = "account.tax"
    
    def _get_currency(self, cr, uid, ctx):
        comp = self.pool.get('res.users').browse(cr,uid,uid).company_id
        if not comp:
            comp_id = self.pool.get('res.company').search(cr, uid, [])[0]
            comp = self.pool.get('res.company').browse(cr, uid, comp_id)
        return comp.currency_id.name

    def _get_compute_tax(self, cr, uid, avatax_config, doc_date, doc_code, doc_type, partner, ship_from_address_id, shipping_address_id,
                          lines, user=None, exemption_number=None, exemption_code_name=None, commit=False, invoice_date=False, reference_code=False, location_code=False, context=None):
        address_obj = self.pool.get('res.partner')
        currency_code = self._get_currency(cr, uid, context)
        if not partner.customer_code:
            raise osv.except_osv(_('Avatax: Warning !'), _('Customer Code for customer %s not define'% (partner.name)))
        
        if not shipping_address_id:
            raise osv.except_osv(_('Avatax: No Shipping Address Defined !'), _('There is no shipping address defined for the partner.'))        
        #it's show destination address
        shipping_address = address_obj.browse(cr, uid, shipping_address_id, context=context)
        if not lines:
            raise osv.except_osv(_('Avatax: Error !'), _('AvaTax needs atleast one sale order line defined for tax calculation.'))
        
        if avatax_config.force_address_validation:
            if not shipping_address.date_validation:
                raise osv.except_osv(_('Avatax: Address Not Validated !'), _('Please validate the shipping address for the partner %s.'
                            % (partner.name)))
        if not ship_from_address_id:
            raise osv.except_osv(_('Avatax: No Ship from Address Defined !'), _('There is no company address defined.'))

        #it's show source address
        ship_from_address = address_obj.browse(cr, uid, ship_from_address_id, context=context)
        
        
        if not ship_from_address.date_validation:
            raise osv.except_osv(_('Avatax: Address Not Validated !'), _('Please validate the company address.'))

        #For check credential
        avalara_obj = AvaTaxService(avatax_config.account_number, avatax_config.license_key,
                                 avatax_config.service_url, avatax_config.request_timeout, avatax_config.logging)
        avalara_obj.create_tax_service()
        addSvc = avalara_obj.create_address_service().addressSvc
        origin = BaseAddress(addSvc, ship_from_address.street or None,
                             ship_from_address.street2 or None,
                             ship_from_address.city, ship_from_address.zip,
                             ship_from_address.state_id and ship_from_address.state_id.code or None,
                             ship_from_address.country_id and ship_from_address.country_id.code or None, 0).data
        destination = BaseAddress(addSvc, shipping_address.street or None,
                                  shipping_address.street2 or None,
                                  shipping_address.city, shipping_address.zip,
                                  shipping_address.state_id and shipping_address.state_id.code or None,
                                  shipping_address.country_id and shipping_address.country_id.code or None, 1).data
        
        #using get_tax method to calculate tax based on address                          
        result = avalara_obj.get_tax(avatax_config.company_code, doc_date, doc_type,
                                 partner.customer_code, doc_code, origin, destination,
                                 lines, exemption_number,
                                 exemption_code_name,
                                 user and user.name or None, commit, invoice_date, reference_code, location_code, currency_code, partner.vat_id or None)
        
        return result

    def cancel_tax(self, cr, uid, avatax_config, doc_code, doc_type, cancel_code):
         """Sometimes we have not need to tax calculation, then method is used to cancel taxation"""
         avalara_obj = AvaTaxService(avatax_config.account_number, avatax_config.license_key,
                                  avatax_config.service_url, avatax_config.request_timeout,
                                  avatax_config.logging)
         avalara_obj.create_tax_service()
         try:
             result = avalara_obj.get_tax_history(avatax_config.company_code, doc_code, doc_type)
         except:
             return True
        
         result = avalara_obj.cancel_tax(avatax_config.company_code, doc_code, doc_type, cancel_code)
         return result

account_tax()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
