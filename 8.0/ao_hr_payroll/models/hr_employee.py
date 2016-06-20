# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp import api, fields, models


class HrEmployee(models.Model):

    _inherit = 'hr.employee'

    @api.one
    def _payslip_count(self):
        self.payslip_count = len(self.sudo().slip_ids)

    payslip_count = fields.Integer(
        compute='_payslip_count',
        string='Payslips',
    )
