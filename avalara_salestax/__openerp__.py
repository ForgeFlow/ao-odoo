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

{
    "name" : "OpenERP Avalara connector for Sales tax calculation",
    "version" : "1.0.1",
    "author" : 'Kranbery Technologies / Pragmatic',
    'summary': 'Quotations, Sales Orders, Invoicing',
    "description": """ 
This module helps to calculate sale tax from Avalara while creating Sale Orders or Customer Invoices. 
Sale tax calculated is based on customer address which needs to be get validated from Avalara before 
calculating sale tax for particular customer order or invoice.
 
This module has Following Features:

1. Customer and Company Address Validation.
2. In Line or Total Order amount sale tax calculation. 
3. Handling of Customer Refunds.
4. Customer Exemption handling. 
5. Calculation of Shipping Cost tax. 
6. Use both Avalara and OpenERP Taxes etc.
                     
Some important points. 

1. Prior Using this module make sure you have Avalara admin console login for configuring your avalara settings https://www.avalara.com.

2. Once module is installed configure your Avalara setting in OpenERP under "Accounting/Configuration/Avatax".

3. Default Tax will be created make sure you configure it correctly under "Accounting/Configuration/Tax"

4. Configure Company Address and Validate it from Avalara. (Use customer link for finding res.partner for company and validate it from partner record use Sales/Sales/Customers and remove Customer filter on this tree view) 

5. Make sure you validate customer address.

Improvement for version 1.0.1

Following improvements are made after first review:

1. Country wise state code validation on address form.

2. Updated rights for users.

3. Resolve invoice creation issues from delivery order.
     
Note: Make sure you have proper internet connection.
""",
    "category" : "Generic Modules/Accounting",
    "website" : "http://www.pragtech.co.in/",
    "depends" : [ 'base','sale','account','account_accountant', 'stock'],
    "init_xml" : [],
    "demo_xml" : [],
    "update_xml" : [
    "wizard/avalara_salestax_ping_view.xml",
    "wizard/avalara_salestax_address_validate_view.xml",
    "avalara_salestax_view.xml",
    "avalara_salestax_data.xml",
    "partner_view.xml",
    "product_view.xml",
    "account_invoice_workflow.xml",
    "account_invoice_view.xml",
    "sale_order_view.xml",
    "security/avalara_salestax_security.xml",
    "security/ir.model.access.csv",
    ],
    "test" : [],
    'installable': True,
    'auto_install': False,
    'application': True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
