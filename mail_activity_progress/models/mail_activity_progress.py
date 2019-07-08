# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class MailActivityProgress(models.Model):
    _name = 'mail.activity.progress'
    _description = 'Activity Progress'
    _order = 'sequence, id'

    name = fields.Char(required=True, translate=True)
    summary = fields.Char(translate=True)
    sequence = fields.Integer(default=10)
    activity_type_ids = fields.Many2many(
        string='Activity Types',
        comodel_name='mail.activity.type',
    )
