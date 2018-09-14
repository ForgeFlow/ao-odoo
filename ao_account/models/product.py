# © 2017 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, models
from odoo.exceptions import UserError


class ProductTemplate(models.Model):
    _inherit = "product.template"

    @api.multi
    def write(self, vals):
        try:
            res = super(ProductTemplate, self).write(vals)
        except UserError as e:
            if e.name == 'You can not change the unit of ' \
                         'measure of a product that has been already ' \
                         'used in an account journal item. ' \
                         'If you need to change the unit of measure, ' \
                         'you may deactivate this product.':
                return True
            else:
                raise
        return res
