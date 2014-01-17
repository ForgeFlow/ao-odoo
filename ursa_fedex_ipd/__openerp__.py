# -*- coding: utf-8 -*-

##############################################################################
#
#    Ursa Information Systems
#    Authors: Adam O'Connor, Balaji Kannan
#    Copyright (C) 2013 (<http://www.ursainfosystems.com>).
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
    "name" : "FedEx IPD Integration Module",
    "version" : "1.0",
    "author" : "Ursa Information Systems, USA",
    "category": 'Accounting & Finance',
    "description": """
    This module provides integration to OpenERP from FedEx IPD application.
    
    1. Given a delivery order number, the details required for the package will be sent to FedEx IPD application.
    2. The delivery order in OpenERP will be updated with the given set of tracking numbers.
    """,
    "depends" : ['stock', 'sale'],
    'init_xml': [],
    'data':[],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
