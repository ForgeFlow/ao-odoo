# Copyright 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Product BOM Standard Cost",
    "summary": "Shows the standard cost of a product that has a BOM "
               "considering the BOM components, labor and overhead",
    "version": "11.0.2.0.1",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-warehouse",
    "category": "Warehouse",
    "depends": ["mrp", "mrp_bom_standard_cost"],
    "data": [
        "views/product_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
