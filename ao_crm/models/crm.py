# Copyright 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import fields, models


class Lead(models.Model):
    _inherit = 'crm.lead'
    _order = 'id DESC'

    understanding_of_need = fields.Text('Understanding of Need')
    understanding_of_impact = fields.Text('Understanding of Impact')
    buying_process = fields.Text('Buying Process')
