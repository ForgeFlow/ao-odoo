# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# Copyright 2019 Aleph Objects, Inc.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import models


class AccountAnalyticAccount(models.Model):
    _inherit = 'account.analytic.account'
    _order = 'name, code asc'
