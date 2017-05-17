# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import api, fields, models


class CrmHelpdesk(models.Model):
    _inherit = "crm.helpdesk"

    rma_order_line_ids = fields.One2Many(
        string='RMA Order Lines',
        comodel_name='rma.order.line',
        inverse_name='helpdesk_id',
        copy=False,
    )
