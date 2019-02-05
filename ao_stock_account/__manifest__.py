# Copyright 2018 Aleph Objects Inc.
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on stock account",
    "version": "11.0.1.2.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "https://www.alephobjects.com",
    "category": "Stock",
    "depends": [
        "stock_account",
        "stock_account_valuation_report",
    ],
    "license": "AGPL-3",
    "data": [
        'views/stock_account_views.xml',
        'views/product_product_views.xml',
        'views/stock_quant_views.xml',
        'wizards/stock_quantity_history_views.xml',
    ],
    'installable': True,
}
