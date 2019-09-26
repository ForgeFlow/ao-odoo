# Copyright 2018 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "MRP BoM Standard Cost",
    "version": "12.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Manufacturing",
    "depends": [
        "account_move_line_manufacture_info",
        "mrp",
        "stock_account"
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/mrp_bom_views.xml",
        "views/mrp_bom_cost_views.xml",
        "views/report_template.xml",
        "views/product_views.xml",
        "reports/mrp_report_bom_structure.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
