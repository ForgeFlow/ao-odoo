# -*- coding: utf-8 -*-
# © 2016 Eficent Business and IT Consulting Services S.L.
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).

from openerp import _, api, fields, models


class StockPicking(models.Model):
    _inherit = "stock.picking"

    @api.multi
    @api.depends('origin')
    def _compute_sale_order_origin(self):
        if self.origin:
            sale_obj = self.env['sale.order']
            sale = sale_obj.search([('name', '=', self.origin)],
                                   limit=1)
            if sale:
                self.sale_order_origin = True

    @api.multi
    @api.depends('origin')
    def _compute_sale_note(self):
        if self.origin:
            sale_obj = self.env['sale.order']
            sale = sale_obj.search([('name', '=', self.origin)],
                                   limit=1)
            if sale:
                self.sale_note = sale.note

    sale_order_origin = fields.Boolean(
        string='Has sales order',
        compute='_compute_sale_order_origin'
    )
    sale_note = fields.Text(
        string='Sales Order Terms and Conditions',
        compute='_compute_sale_note')
