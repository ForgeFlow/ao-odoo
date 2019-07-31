# Copyright 2015-18 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on purchase",
    "version": "12.0.2.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Product",
    "depends": [
        "purchase_stock",
        "product",
        "purchase_product_usage"
    ],
    "data": [
        "views/purchase_order_view.xml",
        "views/purchase_order_line_view.xml",
        "views/product_view.xml",
        "views/report_purchase_order.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
