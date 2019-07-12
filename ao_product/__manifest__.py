# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations for Products",
    "version": "11.0.1.1.1",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "https://www.eficent.com",
    "category": "Product",
    "depends": ["stock"],
    "data": [
        "security/product_security.xml",
        "security/ir.model.access.csv",
        "views/ao_cluster_product.xml",
        "views/product_product_view.xml",
        "views/product_template_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
