# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    prospecting_status = fields.Many2one(
        comodel_name='crm.prospecting.status',
        string='Prospecting Status',
    )
