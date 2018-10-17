# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# Copyright 2018 Odoo, S.A.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).


def post_init_hook(cr, registry):
    """
    The objective of this hook is to default to false all values of field
    'done' of mail.activity
    """
    cr.execute("""
        UPDATE calendar_event as ce
        SET date_deadline = ma.date_deadline
        FROM mail_activity as ma
        WHERE ma.calendar_event_id = ce.id
        AND ma.date_deadline IS NOT NULL
    """)
