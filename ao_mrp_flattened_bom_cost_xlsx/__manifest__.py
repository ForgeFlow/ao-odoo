# Copyright 2018-19 Eficent Business and IT Consulting Services S.L.
#   (https://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Export Flattened BOM Cost to Excel",
    "version": "12.0.1.0.0",
    "category": "Manufacturing",
    "author": "Eficent",
    "website": "https:www.eficent.com",
    "license": "AGPL-3",
    "depends": ["report_xlsx", "mrp_flattened_bom_xlsx"],
    "data": [
        "report/flattened_bom_cost_xlsx.xml",
    ],
    "installable": True
}
