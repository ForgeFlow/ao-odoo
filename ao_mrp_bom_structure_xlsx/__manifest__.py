# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "AO - Export BoM Structure to Excel",
    'version': '11.0.1.0.0',
    'category': 'Manufacturing',
    'author': "Eficent",
    'license': 'AGPL-3',
    "depends": ['report_xlsx', 'mrp', 'product_manufacturer'],
    "data": [
        'report/bom_structure_xlsx.xml',
    ],
    "installable": True
}
