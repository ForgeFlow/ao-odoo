# Copyright 2018 Eficent <https://www.eficent.com>
# Copyright 2018 Aleph Objects Inc. <https://www.alephobjects.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    date_deadline = fields.Date('Due Date')

    def _sync_activities(self, values):
        res = super(CalendarEvent, self)._sync_activities(values)
        if self.mapped('activity_ids'):
            activity_values = {}
            if values.get('date_deadline'):
                activity_values['date_deadline'] = values['date_deadline']
            if activity_values.keys():
                self.mapped('activity_ids').write(activity_values)
        return res
