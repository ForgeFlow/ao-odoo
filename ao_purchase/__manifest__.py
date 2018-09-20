# Copyright 2015-18 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on purchase",
    "version": "11.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Product",
    "depends": ["purchase", "product"],
    "data": [
        "views/purchase_order_view.xml",
        "views/product_view.xml",
        "views/report_purchase_order.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
