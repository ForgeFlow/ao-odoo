# Copyright 2019 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models


class ProductTemplate(models.Model):

    _inherit = 'product.template'

    @api.multi
    def _compute_is_cost_misaligned(self):
        for template in self:
            template.is_cost_misaligned = False
            for price in template.product_variant_ids.mapped(
                    'standard_price'):
                if template.bom_standard_cost != price:
                    template.is_cost_misaligned = True

    @api.multi
    def _search_is_cost_misaligned(self, operator, value):
        template_ids = []
        for template in self.search([]).filtered(
                lambda pt: pt.bom_count):
            for price in template.product_variant_ids.mapped(
                    'standard_price'):
                if template.bom_standard_cost != price:
                    template_ids.append(template.id)
        return [('id', 'in', template_ids)]

    is_cost_misaligned = fields.Boolean(
        string='Cost is misaligned with BOM cost',
        compute='_compute_is_cost_misaligned',
        search='_search_is_cost_misaligned')
