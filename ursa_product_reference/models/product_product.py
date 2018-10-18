# Copyright 2018 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from odoo import api, fields, models, _
from odoo.exceptions import UserError


class ProductProduct(models.Model):
    _inherit = "product.product"

    product_class = fields.Many2one(
        comodel_name="product.class", string="product_class",
        help="Product Class to help generate Internal Reference number",
    )

    @api.onchange('product_class')
    def onchange_class(self):
        """Associate product classification to product."""
        def seq_no(num, cnt=2):
            cnt = cnt - len(str(num))
            nulls = '0' * cnt
            return '%s%s' % (nulls, num)

        result = {}
        if self.product_class:
            if not (self.default_code and len(
                    self.default_code)) and self.product_class:
                seq = self.product_class.sequence_no
                code = (self.product_class.code or '' + seq_no(seq, 4))
                self.default_code = code
                self.product_class.write(
                    {'sequence_no': self.product_class.sequence_no + 1})
            else:
                raise UserError(_("Already has a default code."))
            return result
