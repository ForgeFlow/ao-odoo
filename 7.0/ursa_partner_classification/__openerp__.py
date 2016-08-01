# -*- coding: utf-8 -*-
##############################################################################
#
#    Ursa Information Systems
#    Author: Balaji Kannan
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
############################################################################################################################################################

{
    "name" : "Partner Classification",
    "version" : "1.0",
    "author" : ["Ursa Information Systems, USA"],
    "category": 'CRM',
    'complexity': "normal",
    "description": """
    Adds Classification Object with Code and Name.
    Adds Class Code to Partner.
    """,
    'website': 'http://www.ursainfosystems.com',
    "depends" : ['base'],
    "data" : ['security/ir.model.access.csv',],
    'init_xml': [],
    'update_xml': ['ursa_partner_classification_view.xml', 'demo/res_partner_classification.xml'],
    'demo_xml': [],
    'installable': True,
    'auto_install': False,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
