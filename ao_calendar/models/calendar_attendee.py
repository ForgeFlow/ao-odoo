# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# Copyright 2019 Aleph Objects, Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CalendarAttendee(models.Model):
    _inherit = 'calendar.attendee'

    partner_id = fields.Many2one(index=True)
