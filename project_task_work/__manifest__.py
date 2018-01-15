# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

{
    "name": "Project Task Work",
    "version": "10.0.1.0.0",
    "summary": "Allows to log work associated to a task, not related to "
               "timesheet activities.",
    "author": "Eficent",
    "website": "http://www.eficent.com",
    "category": "Procurements",
    "depends": ['project'],
    "data": [
        'security/ir.model.access.csv',
        'views/project_task_work_view.xml',
        'views/project_task_view.xml',
    ],
    "installable": True
}
