# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ProjectTask(models.Model):
    _inherit = 'project.task'

    work_ids = fields.One2many(
        comodel_name='project.task.work',
        inverse_name='task_id', string='Work done',
    )
