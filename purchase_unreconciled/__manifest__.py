# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# - Lois Rilo Antelo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Purchase Unreconciled",
    "version": "11.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Purchases",
    "depends": [
        "purchase",
        "account_move_line_purchase_info",
    ],
    "data": [
        "views/purchase_order_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
