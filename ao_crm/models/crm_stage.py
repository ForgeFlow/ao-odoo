# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmStage(models.Model):
    _inherit = 'crm.stage'

    team_ids = fields.Many2many(
        'crm.team', 'crm_team_stage_rel',
        'stage_id', 'team_id', 'Teams',
        help="Link between stages and sales teams. When set, this "
             "limitate the current stage to the selected sales teams.")
