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
    "name" : "Purchase Customizations",
    "version" : "1.0",
    "author" : ["Ursa Information Systems, USA"],
    "category": 'Purchase',
    'complexity': "normal",
    "description": """
    Purchase customizations: Origin field exposed in the form as Source Document
    Department added to purchase order and pushed to supplier invoice from PO/Incoming Shipment.
    """,
    'website': 'http://www.ursainfosystems.com',
    "depends" : ['base', 'purchase', 'account', 'stock'],
    "data" : [],
    'init_xml': [],
    'update_xml': ['purchase_view.xml'],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
