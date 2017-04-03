# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class ProjectTaskWork(models.Model):
    _name = 'project.task.work'
    _description = "Project Task Work"

    name = fields.Char(string="Work summary")
    date = fields.Datetime(string="Date", default=fields.Date.today())
    task_id = fields.Many2one(comodel_name='project.task', string="Task",
                              required=True)
    user_id = fields.Many2one(comodel_name='res.users', string="Done by",
                              required=True,
                              default=lambda self: self.env.user)
    company_id = fields.Many2one(comodel_name='res.company',
                                 string="Company",
                                 related='task_id.company_id',
                                 required=True)
