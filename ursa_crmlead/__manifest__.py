# -*- coding: utf-8 -*-
# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Lead Set Reply-To",
    "version": "10.0.1.0.0",
    "author": ["Ursa Information Systems, USA"],
    "category": "CRM",
    "summary": "Sets reply-to in the lead items",
    "website": "http://www.ursainfosystems.com",
    "depends": ["mail", "crm", "fetchmail"],
    "data": [
        "views/ursa_crmlead_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
