# Copyright 2015-18 Eficent Business and IT Consulting Services S.L.
# - Héctor Villarreal Ortega
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "RMA Customizations",
    "version": "12.0.1.0.0",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "category": "rma",
    "depends": ["rma", "account_move_line_rma_order_line", "rma_repair",
                "repair_account", "repair_refurbish",
                ],
    "data": ["views/rma_operation_view.xml",
             "views/rma_order_line_view.xml",
             "wizards/rma_order_line_make_repair_view.xml",
             ],
    "demo": [
        "data/account_data.xml",
        "data/repair_data.xml",
        "data/stock_data.xml",
        "data/rma_operation.xml",

    ],
    "license": "AGPL-3",
    'installable': True,
}
