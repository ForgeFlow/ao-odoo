# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services, S.L.
# - Jordi Ballester Alomar
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl.html).
from openerp.osv import fields, orm
from openerp.tools.translate import _


class AccountMoveLineGetPurchaseLine(orm.TransientModel):

    _name = 'account.move.line.get.purchase.line'
    _description = 'Account Move Line Get Purchase Order Line'

    def default_get(self, cr, uid, fields, context=None):
        res = super(AccountMoveLineGetPurchaseLine, self).default_get(
            cr, uid, fields, context=context)
        request_line_ids = context.get('active_ids', [])
        active_model = context.get('active_model')

        if not request_line_ids:
            return res
        assert active_model == 'account.move.line', \
            'Bad context propagation'
        return res

    def process(self, cr, uid, ids, context=None):
        if context is None:
            context = {}
        res = []
        move_line_ids = context.get('active_ids', [])
        move_line_obj = self.pool['account.move.line']
        picking_obj = self.pool['stock.picking']
        purchase_obj = self.pool['purchase.order']
        purchase_line_obj = self.pool['purchase.order.line']

        for aml in move_line_obj.browse(cr, uid, move_line_ids,
                                        context=context):
            purchase_id = False
            if aml.ref:
                # Check if the reference field matches with the name of a stock
                # picking
                picking_ids = picking_obj.search(cr, uid,
                                                 [('name', '=', aml.ref)],
                                                 context=context)
                if picking_ids:
                    for picking in picking_obj.browse(cr, uid, picking_ids,
                                                      context=context):
                        for sml in picking.move_lines:
                            if sml.purchase_line_id and sml.product_id == \
                                    aml.product_id:
                                purchase_id = sml.purchase_line_id.order_id.id
                                continue
                if not purchase_id:
                    # Check if the reference field matches with the name of
                    # a PO
                    purchase_ids = purchase_obj.search(
                            cr, uid, [('name', '=', aml.ref[:7])],
                            context=context)
                    purchase_id = purchase_ids and purchase_ids[0] or False

            if purchase_id:
                # Look for a purchase order line matching with po_id and
                # product_id
                po_line_ids = purchase_line_obj.search(
                        cr, uid, [('order_id', '=', purchase_id),
                                  ('product_id', '=', aml.product_id.id)],
                        context=context)
                if po_line_ids:
                    move_line_obj.write(cr, uid, [aml.id],
                                        {'purchase_line_id': po_line_ids[0]},
                                        context=context)
                    res.append(aml.id)

        return {
            'domain': "[('id','in', ["+','.join(map(str, res))+"])]",
            'name': _('Account Move Lines updated with Purchase Order Line'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'account.move.line',
            'view_id': False,
            'context': False,
            'type': 'ir.actions.act_window'
        }
