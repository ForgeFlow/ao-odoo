# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# Copyright 2019 Aleph Objects, Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on purchase request",
    "version": "11.0.1.1.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Product",
    "depends": ["purchase_request",
                "purchase_request_product_usage",
                ],
    "data": [
        "views/purchase_request_view.xml",
        "wizards/purchase_request_line_make_purchase_order_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
