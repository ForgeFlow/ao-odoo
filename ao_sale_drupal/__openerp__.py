# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on Sale Drupal",
    "summary": "AO Customization for Drupal integration.",
    "category": "Sales",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "depends": [
        "sale", "sale_exception",
    ],
    "data": [
        "views/sale_order_view.xml",
        "data/sale_exception_data.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
