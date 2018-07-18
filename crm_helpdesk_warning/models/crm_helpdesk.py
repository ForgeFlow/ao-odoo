# -*- coding: utf-8 -*-
# Copyright 2017-18 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _


class CrmHelpdesk(models.Model):
    _inherit = 'crm.helpdesk'

    partner_id = fields.Many2one(track_visibility='always')
    helpdesk_warn = fields.Selection(
        selection=lambda self: self.env['res.partner']._columns[
            'helpdesk_warn'].selection,
        string='Warning message',
        related='partner_id.helpdesk_warn')
    helpdesk_warn_msg = fields.Text('Message for Helpdesk Tickets',
                                    compute='_compute_helpdesk_msg')
    helpdesk_block_msg = fields.Text('Message for Helpdesk Tickets',
                                     compute='_compute_helpdesk_msg')

    @api.depends('partner_id')
    def _compute_helpdesk_msg(self):
        for rec in self:
            rec.helpdesk_warn_msg = rec.partner_id.helpdesk_warn_msg \
                if rec.helpdesk_warn == 'warning' else ''
            rec.helpdesk_block_msg = rec.partner_id.helpdesk_warn_msg \
                if rec.helpdesk_warn == 'block' else ''
