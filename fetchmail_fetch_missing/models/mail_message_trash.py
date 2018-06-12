# -*- coding: utf-8 -*-
# Copyright 2015 Innoviu srl <http://www.innoviu.it>
# Copyright 2015 Agile Business Group <http://www.agilebg.com>
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
#           <http://www.eficent.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import api, fields, models


class MailMessageTrash(models.Model):

    _name = "mail.message.trash"
    _description = "Deleted Mail Messages"

    message_id = fields.Char('Message-Id', help='Message unique identifier',
                             index=True, readonly=1, copy=False)
