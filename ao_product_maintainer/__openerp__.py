# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product Maintainer",
    "version": "9.0.1.0.0",
    "license": "AGPL-3",
    "summary": "Adds a new security group, Product Maintainer. Only members "
               "of this group can modify products",
    "author": "Eficent",
    "website": "www.eficent.com",
    "category": "Product",
    "depends": [
        "product",
        "purchase",
        "stock",
        "point_of_sale",
        "hr_expense",
    ],
    "data": [
        "security/product_maintainer_security.xml",
        "security/ir.model.access.csv",
    ],
    "installable": True,
}