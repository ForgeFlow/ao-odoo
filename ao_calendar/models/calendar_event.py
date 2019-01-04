# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# Copyright 2019 Aleph Objects, Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    recurrent_id = fields.Integer(index=True)
    active = fields.Boolean(index=True)
    user_id = fields.Many2one(index=True)
    partner_id = fields.Many2one(index=True)
    start_date = fields.Date(index=True)
    start_datetime = fields.Datetime(index=True)
    stop_date = fields.Date(index=True)
    stop_datetime = fields.Datetime(index=True)
    start = fields.Datetime(index=True)
    stop = fields.Datetime(index=True)

