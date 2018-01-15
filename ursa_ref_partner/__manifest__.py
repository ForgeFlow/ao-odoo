# -*- coding: utf-8 -*-
# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Ursa Partner Info",
    "version": "10.0.1.0.0",
    "author": ["Ursa Information Systems, USA"],
    "category": 'CRM',
    "license": "AGPL-3",
    "summary": "Adds Reference field to tree view.",
    'website': 'http://www.ursainfosystems.com',
    "depends": ["base"],
    'data': [
        'views/ursa_ref_partner_view.xml',
    ],
    'installable': True,
    'auto_install': False,
}
