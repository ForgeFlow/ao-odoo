# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    @api.model
    def create(self, values):
        if not self.env.user.has_group(
                'ao_security.group_bom_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only BoM Maintainers can create Bills of Materials."))
        return super().create(values)

    @api.multi
    def write(self, vals):
        if not self.env.user.has_group(
                'ao_security.group_bom_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only BoM Maintainers can modify fields in Bill of Materials "
                "model"))
        super().write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'ao_security.group_bom_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only BoM Maintainers can delete Bills of Materials."))
        super().unlink()
