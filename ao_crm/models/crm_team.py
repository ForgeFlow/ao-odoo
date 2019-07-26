# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    stage_ids = fields.Many2many('crm.stage', 'crm_team_stage_rel',
                                 'team_id', 'stage_id', 'Stages')

    @api.multi
    def write(self, vals):
        if vals.get('member_ids') and self.env.user.has_group(
                'sales_team.group_sale_manager'):
            result = super(CrmTeam, self.sudo()).write(vals)
        else:
            result = super(CrmTeam, self).write(vals)
        return result

    @api.model
    def action_your_pipeline(self):
        action = super(CrmTeam, self).action_your_pipeline()
        action['context'].pop('default_team_id', None)
        return action
