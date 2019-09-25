# Copyright 2015-19 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# - Lois Rilo Antelo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on account",
    "version": "12.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Accounting",
    "depends": ["account"],
    "data": [
        "views/account_invoice_views.xml",
        "views/report_invoice.xml",
        "views/partner_view.xml",
        "views/invoice_analysis_report.xml"
    ],
    "license": "AGPL-3",
    'installable': True,
}
