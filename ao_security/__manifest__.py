# Copyright 2019 Aleph Objects, Inc. (https://www.alephobjects.com)
# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    'name': 'Ao Security',
    'description': """
        Manage security rules for different models""",
    'version': '11.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'Eficent Business and IT Consulting Services S.L.',
    'website': 'http://www.eficent.com',
    'depends': ['base'],
    'data': [
        "security/ao_security_groups.xml",
        "security/ir.model.access.csv",
    ],
}
