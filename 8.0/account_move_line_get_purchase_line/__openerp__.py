# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Account Move Line Get Purchase Line",
    "summary": "Facilitates GR/IR Reconciliation by calculating the "
               "the purchase line if not recorded before.",
    "version": "7.0.1.0.0",
    "author": "Eficent, Odoo Community Association (OCA)",
    "website": "http://www.eficent.com",
    "category": "Generic",
    "depends": ["account",
                "purchase",
                "account_move_line_purchase_info"
    ],
    "license": "AGPL-3",
    "data": [
        "wizards/account_move_line_get_purchase_line_view.xml"
    ],
    'installable': True,
    'active': False,
}
