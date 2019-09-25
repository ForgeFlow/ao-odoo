# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, models


class QualityControlTeam(models.Model):
    _inherit = ['qc.team']

    @api.multi
    def write(self, vals):
        if vals.get('member_ids') and self.env.user.has_group(
                'quality_control.group_quality_control_manager'):
            result = super(QualityControlTeam, self.sudo()).write(vals)
        else:
            result = super(QualityControlTeam, self).write(vals)
        return result

    @api.model
    def create(self, vals):
        if vals.get('member_ids') and self.env.user.has_group(
                'quality_control.group_quality_control_manager'):
            result = super(QualityControlTeam, self.sudo()).create(vals)
        else:
            result = super(QualityControlTeam, self).create(vals)
        return result
