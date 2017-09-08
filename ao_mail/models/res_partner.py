# -*- coding: utf-8 -*-
# Copyright (C) 2016-2017 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    notify_email = fields.Selection(
        selection_add=[
            ('all_except_notification', 'All Messages Except Notifications')])
