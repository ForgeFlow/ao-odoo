# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class CrmProspectingStatus(models.Model):
    _name = 'crm.prospecting.status'
    _order = 'sequence'

    name = fields.Char('Name', required=True)
    sequence = fields.Integer('Sequence', default=10)
    summary = fields.Text('Summary')
    active = fields.Boolean(default=True)
