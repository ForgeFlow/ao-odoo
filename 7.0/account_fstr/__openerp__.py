# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C)
#    2011 Colin MacMillan - Enapps Ltd.
#    All Rights Reserved
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
    'name' : 'Financial Statement Template reporting module',
    'version' : '1.1.1',
    'depends' : ['base', 'account'],
    'author' : ['Enapps Ltd.', 'Ursa Information Systems'],
    'description': '''This module provides functionality to create customised financial statements.  Examples of a financial statement would be a trial balance, balance sheet, profit and loss, etc.  Any report that is produced by organising sets of accounts can be created using this module.

User documentation can be found here - www.publicus-solutions.com/blog/post1

Compatible with OpenERP v. 7.0

''',
    'website' : ['http://www.enapps.co.uk/', 'http://www.ursainfosystems.com'],
    "category": 'Accounting & Finance',
    'demo' : [],
    'data' :  [
        'security/ir.model.access.csv',
        'account_fstr_wizard_view.xml',
        'account_fstr_view.xml',
        'account_fstr_menu.xml',
    ],
    'active': False,
    'installable': True,
    'images': ['images/fstr_form.png',],
}
