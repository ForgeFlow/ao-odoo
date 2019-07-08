# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models, SUPERUSER_ID, _
from odoo.exceptions import ValidationError


class Warehouse(models.Model):
    _inherit = 'stock.warehouse'

    @api.model
    def create(self, values):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can create Warehouses."))
        return super().create(values)

    @api.multi
    def write(self, vals):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can modify fields in Warehouse model"))
        super().write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can delete Warehouses."))
        super().unlink()


class Location(models.Model):
    _inherit = 'stock.location'

    @api.model
    def create(self, values):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can create Locations."))
        return super().create(values)

    @api.multi
    def write(self, vals):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can modify fields in Locations model"))
        super().write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can delete Locations."))
        super().unlink()


class ProcurementRule(models.Model):
    _inherit = 'procurement.rule'

    @api.model
    def create(self, values):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can create Procurement Rules."))
        return super().create(values)

    @api.multi
    def write(self, vals):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can modify fields in Procurement Rules"
                " model"))
        super().write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can delete Procurement Rules."))
        super().unlink()


class Route(models.Model):
    _inherit = 'stock.location.route'

    @api.model
    def create(self, values):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can create Routes."))
        return super().create(values)

    @api.multi
    def write(self, vals):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can modify fields in Location Routes"
                " model"))
        super().write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can delete Routes."))
        super().unlink()


class PickingType(models.Model):
    _inherit = "stock.picking.type"

    @api.model
    def create(self, values):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can create Picking Types."))
        return super().create(values)

    @api.multi
    def write(self, vals):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can modify fields in Picking Types"
                " model"))
        super().write(vals)

    @api.multi
    def unlink(self):
        if not self.env.user.has_group(
                'ao_security.group_stock_maintainer') and \
                self.env.uid != SUPERUSER_ID:
            raise ValidationError(_(
                "Only Stock Maintainers can delete Picking Types."))
        super().unlink()
