# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class MrpProduction(models.Model):
    _inherit = "mrp.production"
    _order = "id DESC"

    assigned_to = fields.Many2one(
        comodel_name="res.users", string="Assigned to",
        track_visibility="onchange",
    )
