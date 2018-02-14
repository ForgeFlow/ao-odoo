# -*- coding: utf-8 -*-
# Copyright 2015-18 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on mrp",
    "version": "10.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Manfacturing",
    "depends": [
        "mrp",
        "ursa_product_gtin",
        "mrp_bom_matrix_report",
    ],
    "data": [
        "security/ao_mrp_security.xml",
        "security/ir.model.access.csv",
        "views/stock_move_view.xml",
        "views/mrp_view.xml",
        "views/mrp_production_report.xml",
        "views/ao_mrp_production_report.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
