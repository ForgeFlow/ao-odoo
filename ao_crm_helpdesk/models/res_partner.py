# -*- coding: utf-8 -*-
# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = "res.partner"

    helpdesk_ids = fields.One2many(
        comodel_name="crm.helpdesk", inverse_name="partner_id",
    )
    helpdesk_count = fields.Integer(compute="_compute_helpdesk_count")

    @api.multi
    def _compute_helpdesk_count(self):
        for rec in self:
            rec.helpdesk_count = len(rec.helpdesk_ids)

    @api.multi
    def action_view_helpdesk_ids(self):
        action = self.env.ref('crm_helpdesk.crm_case_helpdesk_act111')
        result = action.read()[0]
        result['domain'] = [('id', 'in', self.helpdesk_ids.ids)]
        result['context'] = {}
        return result
