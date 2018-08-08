# -*- coding: utf-8 -*-
# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
from openerp import api, fields, models, _
from openerp.exceptions import ValidationError


class MailActivity(models.Model):

    _inherit = 'mail.activity'

    purpose_id = fields.Many2one(
        'mail.activity.purpose', 'Purpose',
        index=True, ondelete='restrict')

    @api.onchange('activity_type_id')
    def _onchange_activity_type_id(self):
        res = super(MailActivity, self)._onchange_activity_type_id()
        if self.activity_type_id not in self.purpose_id.activity_type_ids:
            self.purpose_id = False
        if not res:
            res = {}
        if 'domain' not in res:
            res['domain'] = {}
        if self.activity_type_id:
            res['domain']['purpose_id'] = [
                '|', ('activity_type_ids', 'in', [self.activity_type_id.id]),
                ('activity_type_ids', 'in', [])]
            return res
        res['domain']['purpose_id'] = [('activity_type_ids', '=', False)]
        return res

    @api.constrains
    def _constrain_purpose_activity_type(self):
        for rec in self:
            if rec.purpose_id and rec.activity_type_id not in \
                    rec.purpose_id.activity_type_ids:
                raise ValidationError(
                    _('The purpose %s is not allowed for the '
                      'selected activity type %s.') %
                    (rec.purpose_id.name, rec.activity_type_id.name))
