# -*- coding: utf-8 -*-
# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import fields, models


class CrmHelpdesk(models.Model):

    _inherit = "crm.helpdesk"

    contact_name = fields.Char('Contact Name', size=64)
