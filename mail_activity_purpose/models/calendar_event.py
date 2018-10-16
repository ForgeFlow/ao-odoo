# -*- coding: utf-8 -*-
# Copyright 2016 Odoo SA <https://www.odoo.com>
# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from openerp import api, models, fields


class CalendarEvent(models.Model):
    _inherit = "calendar.event"

    purpose_id = fields.Many2one(
        'mail.activity.purpose', 'Purpose',
        index=True, ondelete='restrict')

    def _sync_activities(self, values):
        res = super(CalendarEvent, self)._sync_activities(values)
        if self.mapped('activity_ids'):
            activity_values = {}
            if values.get('name'):
                activity_values['purpose_id'] = values['purpose_id']
        return res
