# Copyright 2016 Odoo SA <https://www.odoo.com>
# Copyright 2018 Eficent <https://www.eficent.com>
# Copyright 2018 Aleph Objects Inc. <https://www.alephobjects.com>
# License LGPL-3.0 or later (http://www.gnu.org/licenses/lgpl.html).

{
    "name": "AO-specific customizations on mail activity",
    "version": "12.0.1.0.0",
    "author": "Eficent, Aleph Objects Inc.",
    "website": "https://www.alephobjects.com",
    "category": "CRM",
    "depends": [
        "mail_activity_done",
        "calendar",
        "mail_activity_board",
    ],
    "data": [
        'views/mail_activity_views.xml',
        'views/calendar_event_views.xml',
    ],
    "license": "LGPL-3",
    "installable": True,
    "post_init_hook": "post_init_hook",
}
