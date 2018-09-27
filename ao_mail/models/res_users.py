# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import fields, models


class Users(models.Model):
    _inherit = 'res.users'

    email_notifications = fields.Boolean(string='Email Notifications')
