# -*- coding: utf-8 -*-
# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models


class MailActivity(models.Model):

    _inherit = 'mail.activity'

    purpose_id = fields.Many2one(
        'mail.activity.purpose', 'Purpose',
        index=True, ondelete='restrict')

    @api.onchange('activity_type_id')
    def _onchange_activity_type_id(self):
        super(MailActivity, self)._onchange_activity_type_id()
        if self.activity_type_id:
            return {
                'domain': {
                    'purpose_id': ['|',
                                    ('activity_type_ids', 'in',
                                     [self.activity_type_id.id]),
                                    ('activity_type_ids', '=', False)]
                },
            }
        return {'domain': {'purpose_id': [
            ('activity_type_ids', '=', False)]}}
