# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO CRM Prospecting Status",
    "version": "12.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "CRM",
    "depends": ["crm"],
    "data": [
        'views/res_partner_views.xml',
        'views/crm_prospecting_status_views.xml',
        'security/ir.model.access.csv',
    ],
    "license": "AGPL-3",
    'installable': True,
}
