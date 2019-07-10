# Copyright 2013 Ursa Information Systems (http://www.ursainfosystems.com).
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Internal Reference Generation",
    "version": "12.0.1.0.0",
    "author": "Ursa Information Systems, USA",
    "license": "AGPL-3",
    "category": "Stock",
    "summary": "Generate product internal reference number",
    "website": "http://www.ursainfosystems.com",
    "depends": ["base", "stock", "product"],
    "data": [
        "security/ir.model.access.csv",
        "views/productclass_view.xml",
        "views/product_product_view.xml",
    ],
    "installable": True,
    "auto_install": False,
}
