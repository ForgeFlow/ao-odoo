# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmTeam(models.Model):
    _inherit = "crm.team"

    reply_to_alias = fields.Boolean(
        string="Reply to Email Alias",
        help="Use Email Alias as 'Reply to' in composed mails."
    )
