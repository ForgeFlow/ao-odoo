# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class QcProblemTrack(models.Model):
    _inherit = "qc.problem.track"

    @api.one
    @api.depends('issue_ids', 'crm_helpdesk_ids')
    def _compute_count(self):
        super(QcProblemTrack, self)._compute_count()
        self.crm_helpdesk_count = len(self.crm_helpdesk_ids)

    crm_helpdesk_ids = fields.Many2many(
        comodel_name="crm.helpdesk", string="Helpdesk Tickets",
        relation="helpdesk_problem_rel", column1="qc_problem_id",
        column2="crm_helpdesk_id")
    crm_helpdesk_count = fields.Integer(
        string="Helpdesk Tickets Count", compute=_compute_count, store=True)
