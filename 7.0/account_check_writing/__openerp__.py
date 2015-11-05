# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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
{
    'name': 'Check Writing',
    'version': '1.1',
    'author': 'OpenERP SA, Ursa Information Systems',
    'category': 'Generic Modules/Accounting',
    'description': """
With this module, you will be able to write checks to your vendors in OpenERP.
==============================================================================

This module supports the following:
-----------------------------------
    * Multiple currencies: it is possible to write checks in different currencies.
    * Multiple journals: each check can use a different payment method.
    * Multiple formats: checks can be printed on top, in the middle or at the bottom to fit Quickbooks/Peachtree/... templates.
    * Batch check number assignation.
    * Batch printing of checks.
    * Complete check number sequence management: number auto-suggestion, sequence recalibration, optional overwrite if already specified, duplicates detection.
    * Optional printing of check number: if the paper checks of your bank already include numbers, you can use these numbers instead of OpenERP’s check numbers.
    * Optional spill-over on multiple stubs: when the check includes more than 10 invoice lines, they will be printed  on several pages.
    * Optional printing of credits.
    * Integration with payments workflow: checks are an integrated part of the payment workflow in OpenERP.
    * Comprehensive and accurate information displayed on stub: supplier's invoice number, void status, memo, suppresses invoices that are not paid with this check.
    """,
    'website': 'http://www.openerp.com',
    'depends': ['account_voucher'],
    'data': [
        'wizard/account_check_batch_printing_view.xml',
        'account_view.xml',
        'account_voucher_view.xml',
        'res_company_view.xml',
        'account_check_writing_data.xml',
    ],
    'demo': ['account_demo.xml'],
    'test': [],
    'installable': True,
    'active': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
