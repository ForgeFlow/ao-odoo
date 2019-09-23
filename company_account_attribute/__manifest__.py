# Copyright 2017 Creu Blanca
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Company Account Attribute',
    'version': '12.0.1.0.0',
    'summary': 'Maintain accounting-specific attributes of the company '
               'in the company settings',
    'author': 'Creu Blanca, Eficent',
    'sequence': 30,
    'license': 'LGPL-3',
    'website': 'http://www.eficent.com',
    'depends': ['account'],
    'data': [
        'views/res_company_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
