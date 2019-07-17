# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Align standard cost",
    "summary": "Align standard cost to BOM Standard Cost",
    "version": "12.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L., "
              "Odoo Community Association (OCA)",
    "website": "https://github.com/OCA/stock-logistics-warehouse",
    "category": "Warehouse",
    "depends": ["product_bom_standard_cost", "stock_account"],
    "data": [
        "security/product_bom_cost_align_security.xml",
        "wizards/stock_change_standard_price_views.xml",
        "views/product_view.xml",
    ],
    "license": "AGPL-3",
    'installable': True,
}
