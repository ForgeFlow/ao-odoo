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
                "repair_account", "repair_refurbish", "rma_kanban_stage",
                "base_automation",
                ],
    "data": ["data/rma_stage.xml",
             "data/base_automation_data.xml",
             "views/rma_operation_view.xml",
             "views/rma_order_line_view.xml",
             "wizards/rma_order_line_make_repair_view.xml",
             ],
    "demo": ["demo/account_data.xml",
             "demo/stock_data.xml",
             "demo/repair_data.xml",
             "demo/rma_operation.xml",
             "views/rma_operation_view.xml",
             "views/rma_order_line_view.xml",
             "wizards/rma_order_line_make_repair_view.xml",

             ],
    "license": "AGPL-3",
    'installable': True,
}
