# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import models, fields


class RmaOrder(models.Model):
    _inherit = "rma.order"

    originating_helpdesk_id = fields.Many2one(
        string='Originating Helpdesk Ticket',
        comodel_name='crm.helpdesk',
        copy=False,
    )
