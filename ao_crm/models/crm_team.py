# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    stage_ids = fields.Many2many('crm.stage', 'crm_team_stage_rel',
                                 'team_id', 'stage_id', 'Stages')
