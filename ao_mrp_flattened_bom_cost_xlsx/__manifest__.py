# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': "Export Flattened BOM Cost to Excel",
    'version': '11.0.1.0.0',
    'category': 'Manufacturing',
    'author': "Eficent",
    'website': 'https://github.com/Eficent',
    'license': 'AGPL-3',
    'depends': ['report_xlsx', 'mrp'],
    'data': [
        'report/flattened_bom_cost_xlsx.xml',
    ],
    'installable': True
}
