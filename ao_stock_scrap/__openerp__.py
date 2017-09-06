# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on stock scrap",
    "version": "9.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Warehouse Management",
    "depends": ["stock_scrap"],
    "data": [
        "security/stock_scrap_security.xml",
        "security/ir.model.access.csv",
        "views/stock_scrap_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
    'auto_install': True,
}
