# -*- coding: utf-8 -*-
# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CrmHelpdesk(models.Model):
    _inherit = 'crm.helpdesk'

    partner_id = fields.Many2one(track_visibility='always')

    @api.onchange('partner_id')
    def _onchange_partner_id(self):
        if self.partner_id:
            partner = self.partner_id
            if (partner.helpdesk_warn != 'no-message' and
                    partner.helpdesk_warn == 'block'):
                raise UserError(_(
                    "Warning for %s\n%s" %
                    (partner.name, partner.helpdesk_warn_msg)
                ))
        return super(CrmHelpdesk, self)._onchange_partner_id()

    @api.multi
    def write(self, vals):
        res = super(CrmHelpdesk, self).write(vals)
        for rec in self:
            if 'partner_id' in vals and rec.partner_id.helpdesk_warn_log and \
                    not self.env.context.get('warning_message'):
                message = _('Warning on %s: %s' % (
                    rec.partner_id.name, rec.partner_id.helpdesk_warn_msg))
                rec.with_context(warning_message=True).message_post(
                    message, message_type='comment')
        return res

    @api.model
    def create(self, vals):
        rec = super(CrmHelpdesk, self).create(vals)
        if rec.partner_id.helpdesk_warn_log:
            message = _('Warning on %s: %s' % (
                rec.partner_id.name, rec.partner_id.helpdesk_warn_msg))
            rec.message_post(
                message, message_type='comment')
        return rec
