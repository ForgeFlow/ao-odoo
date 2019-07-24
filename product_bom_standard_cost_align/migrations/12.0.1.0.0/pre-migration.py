# Copyright 2019 Eficent <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from openupgradelib import openupgrade

xmlid_renames = [
    ('product_bom_standard_cost_align.group_align bom_cost_user',
     'product_bom_standard_cost_align.group_align_bom_cost_user'),
]


@openupgrade.migrate()
def migrate(env, version):
    openupgrade.rename_xmlids(env.cr, xmlid_renames)
