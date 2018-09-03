# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Add Read-Only Accountant Group',
    'version': '9.0.1.0.0',
    'category': 'Accounting & Finance',
    'summary': """Adds a read-only accountant group to have an external
                  accountant go through your accounting records in Odoo.""",
    'author': 'Rooms For (Hong Kong) Limited T/A OSCG',
    'website': 'http://www.openerp-asia.net/',
    'depends': ['account_accountant'],
    'data': [
        'security/account_security.xml',
        'security/ir.model.access.csv',
        'views/account_reconcile_view.xml',
        ],
    'installable': True,
}
