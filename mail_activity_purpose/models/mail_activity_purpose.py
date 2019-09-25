# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from odoo import fields, models


class MailActivityPurpose(models.Model):
    _name = 'mail.activity.purpose'
    _description = 'Activity Purposes'
    _rec_name = 'name'
    _order = 'sequence, id'

    name = fields.Char('Name', required=True, translate=True)
    summary = fields.Char('Summary', translate=True)
    sequence = fields.Integer('Sequence', default=10)
    activity_type_ids = fields.Many2many(string='Activity Types',
                                         comodel_name='mail.activity.type')
