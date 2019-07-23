# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# - Lois Rilo Antelo
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO Purchase Auto Close",
    "version": "12.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "Purchases",
    "depends": [
        "purchase",
        "purchase_open_qty",
        "purchase_unreconciled",
    ],
    "data": [
        "data/ir_cron.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
