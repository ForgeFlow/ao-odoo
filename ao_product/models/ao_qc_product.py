# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


class AoQCProductTemplate(models.Model):
    _inherit = 'product.template'

    inspection_criteria = fields.Text(
        string='Inspection Criteria'
    )
    spec_sheet = fields.Char(
        string='Link to Spec Sheet Directory'
    )

    @api.multi
    def write(self, vals):
        pm_fields = ['inspection_criteria', 'spec_sheet']
        if any([x in vals for x in pm_fields]) and not self.env.user.has_group(
                'quality_control.group_quality_control_manager') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Quality Control Managers can modify the following fields"
                " in products:\n%s" % pm_fields))
        super().write(vals)
