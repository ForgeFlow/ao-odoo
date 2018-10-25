# Copyright 2018 Eficent Business and IT Consulting Services S.L.
#   (http://www.eficent.com)
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).


def migrate(cr, version):
    cr.execute("""
        UPDATE res_users SET notification_by_email = False
        WHERE id IN (
            SELECT ru.id FROM res_users ru
            RIGHT JOIN res_partner rp ON ru.partner_id = rp.id
            WHERE rp.notify_email = 'all_except_notification'
        );
    """)
