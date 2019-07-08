# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


class ProductUoM(models.Model):
    _inherit = 'product.uom'

    @api.model
    def create(self, values):
        if not self.env.user.has_group(
                'ao_security.group_uom_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only UoM Maintainers can create Units of Measure."))
        return super().create(values)

    @api.multi
    def write(self, vals):
        if not self.env.user.has_group(
                'ao_security.group_uom_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only UoM Maintainers can modify fields in Units of Measure "
                "model"))
        super().write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'ao_security.group_uom_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only UoM Maintainers can delete Units of Measure."))
        super().unlink()


class ProductUoMCategory(models.Model):
    _inherit = 'product.uom.categ'

    @api.model
    def create(self, values):
        if not self.env.user.has_group(
                'ao_security.group_uom_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only UoM Maintainers can create UoM Categories."))
        return super().create(values)

    @api.multi
    def write(self, vals):
        if not self.env.user.has_group(
                'ao_security.group_uom_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only UoM Maintainers can modify fields in UoM Category "
                "model"))
        super().write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'ao_security.group_uom_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only UoM Maintainers can delete UoM Categories."))
        super().unlink()
