# -*- coding: utf-8 -*-
# Copyright 2018 Eficent <http://www.eficent.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).
{
    "name": "Mail Activity Purpose",
    "version": "9.0.1.0.0",
    "author": "Eficent,"
              "Odoo Community Association (OCA)",
    "license": "LGPL-3",
    "category": "Discuss",
    "depends": [
        'mail_activity',
        'mail_activity_calendar',
    ],
    "data": [
        'security/ir.model.access.csv',
        'views/mail_activity_purpose_views.xml',
        'views/mail_activity_views.xml',
        'views/calendar_event_view.xml',
    ],
}
