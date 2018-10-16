# -*- coding: utf-8 -*-
# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class MailActivity(models.Model):

    _inherit = 'mail.activity'

    @api.multi
    def action_create_calendar_event(self):
        action = super(MailActivity, self).action_create_calendar_event()
        if action.get('context'):
            action['context'].update({
                'default_date_deadline': self.date_deadline,
            })
        return action
