# Copyright 2018-19 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmProspectingStatus(models.Model):
    _name = 'crm.prospecting.status'
    _order = 'sequence'
    _description = "Prospecting Status"

    name = fields.Char(required=True)
    sequence = fields.Integer(default=10)
    summary = fields.Text()
    active = fields.Boolean(default=True)
