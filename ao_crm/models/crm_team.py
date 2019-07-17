# Copyright 2017-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class CrmTeam(models.Model):
    _inherit = 'crm.team'

    stage_ids = fields.Many2many(
        comodel_name="crm.stage",
        relation="crm_team_stage_rel",
        column1="team_id",
        column2="stage_id",
        string="Stages",
    )

    @api.multi
    def write(self, vals):
        if vals.get('member_ids') and self.env.user.has_group(
                'sales_team.group_sale_manager'):
            result = super(CrmTeam, self.sudo()).write(vals)
        else:
            result = super(CrmTeam, self).write(vals)
        return result
