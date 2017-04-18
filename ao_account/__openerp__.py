# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on account",
    "version": "9.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Accounting",
    "depends": ["account"],
    "data": [
        "security/ir.model.access.csv",
        "views/report_invoice.xml",
        "views/partner_view.xml",
        "views/invoice_analysis_report.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
