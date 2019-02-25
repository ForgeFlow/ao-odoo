# Copyright 2019 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl.html).
from odoo import models, fields


class ResUsers(models.Model):
    _inherit = "res.users"

    calendar_allow_ui_edition = fields.Boolean(
        string="Allow in-calendar edition",
        help="When set you can modify the dates of existing calendar events "
             "by moving them in the calendar view.",
        default=True,
    )
