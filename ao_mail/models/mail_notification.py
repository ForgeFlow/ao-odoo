# -*- coding: utf-8 -*-
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class MailNotification(models.Model):
    _inherit = 'mail.notification'

    @api.multi
    def get_partners_to_email(self, message):
        notify_pids = super(MailNotification, self).get_partners_to_email(
            message)
        for notif in self:
            if (notif.partner_id.id in notify_pids and
                    message.type == 'notification' and
                    notif.partner_id.notify_email ==
                    'all_except_notification'):
                notify_pids.remove(notif.partner_id.id)
        return notify_pids
