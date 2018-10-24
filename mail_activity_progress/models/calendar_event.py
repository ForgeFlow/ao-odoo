# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    progress_id = fields.Many2one(
        'mail.activity.progress', 'Progress',
        index=True, ondelete='restrict',
        domain="[('activity_type_ids.category', '=', 'meeting')]")

    def _sync_activities(self, values):
        res = super(CalendarEvent, self)._sync_activities(values)
        if self.mapped('activity_ids'):
            activity_values = {}
            if values.get('progress_id'):
                activity_values['progress_id'] = values['progress_id']
            if activity_values.keys():
                self.mapped('activity_ids').write(activity_values)
        return res
