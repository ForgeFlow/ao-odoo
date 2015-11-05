# -*- coding: utf-8 -*-
##############################################################################
#
#    Ursa Information Systems
#    Author: Balaji Kannan
#    Copyright (C) 2014 (<http://www.ursainfosystems.com>).
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
############################################################################################################################################################

{
    "name" : "Sale Customizations",
    "version" : "1.0",
    "author" : ["Ursa Information Systems, USA"],
    "category": 'Purchase',
    'complexity': "normal",
    "description": """
    Sale customizations:
    1. Source location for the item identified in the sale order line,
    pushed to stock move.
    2. For sales shipped to foreign addresses, set Incoterms to DTP and invoice method to manual.
    3. Auto progress the invoice state to "Proforma" for international orders if the user default is set.
    """,
    'website': 'http://www.ursainfosystems.com',
    "depends" : ['base', 'sale', 'stock', 'sale_stock'],
    "data" : [],
    'init_xml': [],
    'update_xml': ['sale_view.xml'],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
