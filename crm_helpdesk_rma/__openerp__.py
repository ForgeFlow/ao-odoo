# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "CRM Helpdesk RMA",
    "version": "9.0.1.0.0",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "category": "CRM",
    "depends": ["crm_helpdesk", "rma"],
    "license": "AGPL-3",
    "data": [
        'views/crm_helpdesk_view.xml',
        'views/rma_order_view.xml',
    ],
    'installable': True,
}
