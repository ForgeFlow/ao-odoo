# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on stock scrap",
    "version": "11.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Warehouse Management",
    "depends": ["stock"],
    "data": [
        "security/stock_scrap_security.xml",
        "security/ir.model.access.csv",
        "views/stock_scrap_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
    'auto_install': False,
}
