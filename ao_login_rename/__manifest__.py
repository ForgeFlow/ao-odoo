# -*- coding: utf-8 -*-
# Copyright 2016-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
{
    "name": "AO Login Rename",
    "summary": "Renames the login from Email Address to Username.",
    "version": "10.0.1.0.0",
    "category": "Customizations",
    "website": "http://www.eficent.com",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "web"
    ],
    "data": [
        'views/template.xml',
        'views/res_users_view.xml',
    ],
}
