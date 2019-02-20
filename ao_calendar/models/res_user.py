# Copyright 2018 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    calendar_allow_ui_edition = fields.Boolean(
        string="Allow UI calendar edition",
        default=True,
    )
