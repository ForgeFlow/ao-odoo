# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# Copyright 2018 Tecnativa, S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from openerp import api, SUPERUSER_ID


def update_calendar_event(env):
    """Update the meetings to add the purpose_id"""
    env.cr.execute("""
        UPDATE calendar_event as ce
        SET purpose_id = ma.purpose_id
        FROM mail_activity as ma
        WHERE ma.calendar_event_id = ce.id
        AND ma.purpose_id IS NOT NULL
    """)


def migrate(cr, version):
    with api.Environment.manage():
        env = api.Environment(cr, SUPERUSER_ID, {})
        update_calendar_event(env)
