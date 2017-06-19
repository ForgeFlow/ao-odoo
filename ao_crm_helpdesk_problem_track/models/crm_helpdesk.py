# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CrmHelpdesk(models.Model):
    _inherit = "crm.helpdesk"

    problem_track_ids = fields.Many2many(
        comodel_name="qc.problem.track", string="Problems",
        relation="helpdesk_problem_rel", column1="crm_helpdesk_id",
        column2="qc_problem_id")
