# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'AO Check Writing',
    'version': '8.0.1.0.0',
    'author': 'Eficent Business and IT Consulting Services S.L.',
    'category': 'Customizatins',
    'summary': 'Customizes AO check form',
    'website': 'http://www.openerp.com',
    'depends': [
        'account_check_writing',
    ],
    'data': [
        'reports/account_check_writing_report.xml',
        'views/res_company_view.xml',
        'views/account_voucher_view.xml'
    ],
    'installable': True,
    'active': False,
}
