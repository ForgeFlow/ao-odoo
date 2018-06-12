# -*- coding: utf-8 -*-
# Copyright 2015 Innoviu srl <http://www.innoviu.it>
# Copyright 2015 Agile Business Group <http://www.agilebg.com>
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
#           <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import logging
import imaplib
from datetime import datetime, timedelta
import time
import email
from openerp import api, fields, models

_logger = logging.getLogger(__name__)


class FetchmailServer(models.Model):

    _inherit = "fetchmail.server"

    nbr_days = fields.Integer(
        '# Days to fetch',
        help="Remote emails with a date greater today's date - # days will "
             "be fetched if not already processed",
        default=30)

    @api.model
    def _fetch_missing_imap(self, imap_server, count, failed):
        MailThread = self.env['mail.thread']
        messages = []
        # Retrieve all the message id's stored in odoo
        mail_messages = self.env['mail.message'].search([])
        mail_messages_trashed = self.env['mail.message.trash'].search([])
        mail_msg_d = mail_messages.read(['message_id'])
        stored_mids = []
        for m in mail_msg_d:
            stored_mids.append(m['message_id'])
        fetch_from_date = datetime.today() - timedelta(days=self.nbr_days)
        search_status, uids = imap_server.search(
            None,
            'SINCE', '%s' % fetch_from_date.strftime('%d-%b-%Y')
            )
        new_uids = uids[0].split()
        for new_uid in new_uids:
            fetch_status, data = imap_server.fetch(
                int(new_uid),
                '(BODY[HEADER.FIELDS (MESSAGE-ID)])'
                )
            msg_str = email.message_from_string(data[0][1])
            message_id = msg_str.get('Message-ID')
            trashed_mids = mail_messages_trashed.mapped('message_id')
            if unicode(message_id) not in stored_mids and \
                    message_id not in trashed_mids:
                messages.append(new_uid)
        for num in messages:
            # SEARCH command *always* returns at least the most
            # recent message, even if it has already been synced
            res_id = None
            result, data = imap_server.fetch(num, '(RFC822)')
            if data and data[0]:
                try:
                    res_id = MailThread.message_process(
                        self.object_id.model,
                        data[0][1],
                        save_original=self.original,
                        strip_attachments=(not self.attach))
                except Exception:
                    _logger.exception(
                        'Failed to process mail \
                        from %s server %s.',
                        self.type,
                        self.name)
                    failed += 1
                if res_id and self.action_id:
                    self.action_id.run({
                        'active_id': res_id,
                        'active_ids': [res_id],
                        'active_model': self.env.context.get(
                            "thread_model", self.object_id.model)
                    })
                imap_server.store(num, '+FLAGS', '\\Seen')
                self._cr.commit()
                count += 1
        return count, failed

    @api.multi
    def fetch_mail(self):
        context = self.env.context.copy()
        context['fetchmail_cron_running'] = True
        for server in self:
            if server.type == 'imap' and server.nbr_days:
                _logger.info(
                    'start checking for new emails, %s days in the past, '
                    'on %s server %s',
                    server.nbr_days, server.type, server.name)
                context.update({'fetchmail_server_id': server.id,
                                'server_type': server.type})
                count, failed = 0, 0
                last_date = False
                imap_server = False
                try:
                    imap_server = server.connect()
                    imap_server.select()
                    count, failed = server._fetch_missing_imap(
                        imap_server, count, failed)
                except Exception:
                    _logger.exception(
                        "General failure when trying to fetch mail by date \
                        from %s server %s.",
                        server.type,
                        server.name
                        )
                finally:
                    if imap_server:
                        imap_server.close()
                        imap_server.logout()
                if last_date:
                    _logger.info(
                        "Fetched %d email(s) on %s server %s, starting from "
                        "%s; %d succeeded, %d failed.", count,
                        server.type, server.name, last_date,
                        (count - failed), failed)
        return super(FetchmailServer, self).fetch_mail()
