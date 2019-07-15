# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from openerp.addons.rma.tests import test_rma
from openerp.exceptions import ValidationError


class TestRma(test_rma.TestRma):
    """ Test the routes and the quantities """

    @classmethod
    def setUpClass(cls):
        super(TestRma, cls).setUpClass()

    def test_10_rma_location_out_of_the_company(cls):
        """tests computes when receiving out of the company"""
        wizard = cls.rma_make_picking.with_context({
            'active_ids': cls.rma_customer_id.rma_line_ids.ids,
            'active_model': 'rma.order.line',
            'picking_type': 'incoming',
            'active_id': 1
        }).create({})
        wizard._create_picking()
        res = cls.rma_customer_id.rma_line_ids.action_view_in_shipments()
        picking = cls.env['stock.picking'].browse(res['res_id'])
        cls.assertEqual(len(picking), 1)
        res = cls.rma_customer_id.rma_line_ids.action_view_out_shipments()
        picking = cls.env['stock.picking'].browse(res['res_id'])
        cls.assertEqual(len(picking), 0)
