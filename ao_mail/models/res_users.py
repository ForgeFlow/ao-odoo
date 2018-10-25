# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    notification_by_email = fields.Boolean(
        string="System notifications by Email",
        default=True,
        help="Uncheck this box if you don't want to receive System"
             "notification in your email.",
    )
