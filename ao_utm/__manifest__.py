# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "AO-specific customizations on UTM trackers",
    "version": "12.0.1.0.0",
    "author": "Eficent Business and IT Consulting Services S.L.",
    "website": "http://www.eficent.com",
    "category": "CRM",
    "depends": ["sales_team", "utm"],
    "data": [
        "security/ir.model.access.csv",
        "views/utm_view.xml",
    ],
    "license": "AGPL-3",
    "installable": True,
}
