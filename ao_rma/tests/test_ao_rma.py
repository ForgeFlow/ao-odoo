# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from openerp.addons.rma.tests import test_rma


class TestRma(test_rma.TestRma):
    """ Test AO RMA flows"""

    @classmethod
    def setUpClass(cls):
        super(TestRma, cls).setUpClass()
        cls.rma_external_location = cls.env.ref(
            'ao_rma.rma_external_location')
        cls.wiz_make_picking = cls.env['rma_make_picking.wizard']
        cls.operation_nw = cls.env.ref('ao_rma.rma_operation_repair_nw')
        cls.operation_warranty = cls.env.ref(
            'ao_rma.rma_operation_repair_warranty')
        cls.rma_make_repair_wiz = cls.env['rma.order.line.make.repair']
        cls.repair_team = cls.env.ref(
            'mrp_repair_account.mrp_repair_team_dep1')
        cls.repair_type = cls.env.ref(
            'mrp_repair_account.mrp_repair_type_no_warranty')
        cls.aml_obj = cls.env['account.move.line']
        cls.move_obj = cls.env['stock.move']

    def create_customer_rma(cls, partner, product, operation):
        vals = {'partner_id': partner.id,
                'product_id': product.id,
                'uom_id': product.uom_id.id,
                'receipt_policy': operation.receipt_policy,
                'delivery_policy': operation.delivery_policy,
                'refund_policy': operation.refund_policy,
                'in_route_id': operation.in_route_id.id,
                'out_route_id': operation.out_route_id.id,
                'in_warehouse_id': operation.in_warehouse_id.id,
                'out_warehouse_id': operation.out_warehouse_id.id,
                'location_id': operation.location_id.id,
                'operation_id': operation.id}
        rma = cls.rma_line.create(vals)
        return rma

    def test_10_rma_location_out_of_the_company(cls):
        """tests computes when receiving out of the company"""
        rma = cls.create_customer_rma(cls.partner_id, cls.product_id,
                                      cls.operation_nw)
        rma._onchange_operation_id()
        rma.action_rma_approve()
        wizard = cls.wiz_make_picking.with_context({
            'active_ids': rma.id,
            'active_model': 'rma.order.line',
            'picking_type': 'incoming',
            'active_id': rma.id
        }).create({})
        wizard._create_picking()
        res = rma.action_view_in_shipments()
        picking = cls.env['stock.picking'].browse(res['res_id'])
        cls.assertEqual(len(picking), 1)
        res = rma.action_view_out_shipments()
        picking = cls.env['stock.picking'].browse(res['res_id'])
        cls.assertEqual(len(picking), 0)

    def test_11_repair_no_warranty(cls):
        """Accounting entries for a reparation with no warranty """

        # create rma and receive in external location
        rma = cls.create_customer_rma(cls.partner_id, cls.product_id,
                                      cls.operation_warranty)
        rma._onchange_operation_id()
        cls.assertEqual(rma.repair_type, 'received')
        rma.action_rma_approve()
        wizard = cls.wiz_make_picking.with_context({
            'active_ids': rma.id,
            'active_model': 'rma.order.line',
            'picking_type': 'incoming',
            'active_id': rma.id
        }).create({})
        wizard._create_picking()
        res = rma.action_view_in_shipments()
        picking = cls.env['stock.picking'].browse(res['res_id'])
        picking.move_lines.write({'quantity_done': 1.0})
        picking.button_validate()
        cls.assertEqual(picking.state, 'done')
        # create repair order
        make_repair = cls.rma_make_repair_wiz.with_context({
            'customer': True,
            'active_ids': rma.id,
            'active_model': 'rma.order.line',
        }).create({
            'description': 'Test no warranty',
        })
        make_repair.item_ids.team_id = cls.repair_team
        make_repair.make_repair_order()
        repair = rma.repair_ids
        rma.repair_ids.action_repair_confirm()

        cls.assertEqual(repair.location_id, cls.rma_external_location)
        cls.assertEqual(repair.location_dest_id, cls.rma_external_location)

        # check stock moves
        moves = cls.move_obj.search([('reference', '=', rma.name)])
        for m in moves:
            cls.assertEqual(m.state, 'done')
            cls.assertEqual(m.location_id,
                            cls.customer_location)
            cls.assertEqual(m.location_dest_id,
                            cls.stock_location_rma_external)

        # check no JE are generated
        aml = cls.aml_obj.search([('name', '=', rma.name)])
        cls.assertEqual(len(aml), 0)

        # end repair
        repair.onchange_type_id()
        repair.onchange_team_id()
        repair.action_repair_ready()
        repair.action_repair_start()
        repair.action_repair_end()

        # deliver
        cls.assertEqual(rma.qty_to_deliver, 1.0)
        wizard = cls.rma_make_picking.with_context({
            'active_ids': rma.id,
            'active_model': 'rma.order.line',
            'picking_type': 'outgoing',
            'active_id': rma.id
        }).create({})
        wizard._create_picking()
        res = rma.action_view_out_shipments()
        picking = cls.env['stock.picking'].browse(res['res_id'])
        picking.move_lines.write({'quantity_done': 1.0})
        picking.button_validate()
        cls.assertEqual(picking.state, 'done')
        # check no JE are generated
        aml = cls.aml_obj.search([('name', '=', rma.name)])
        cls.assertEqual(len(aml), 0)

    def test_12_repair_no_warranty(cls):
        """Accounting entries for a reparation with warranty
           Very similar to previous test, considering remove
        """

        # create rma and receive in external location
        rma = cls.create_customer_rma(cls.partner_id, cls.product_id,
                                      cls.operation_nw)
        rma._onchange_operation_id()
        cls.assertEqual(rma.repair_type, 'received')
        rma.action_rma_approve()
        wizard = cls.wiz_make_picking.with_context({
            'active_ids': rma.id,
            'active_model': 'rma.order.line',
            'picking_type': 'incoming',
            'active_id': rma.id
        }).create({})
        wizard._create_picking()
        res = rma.action_view_in_shipments()
        picking = cls.env['stock.picking'].browse(res['res_id'])
        picking.move_lines.write({'quantity_done': 1.0})
        picking.button_validate()
        cls.assertEqual(picking.state, 'done')
        # create repair order
        make_repair = cls.rma_make_repair_wiz.with_context({
            'customer': True,
            'active_ids': rma.id,
            'active_model': 'rma.order.line',
        }).create({
            'description': 'Test no warranty',
        })
        make_repair.item_ids.team_id = cls.repair_team
        make_repair.make_repair_order()
        repair = rma.repair_ids
        rma.repair_ids.action_repair_confirm()

        cls.assertEqual(repair.location_id, cls.rma_external_location)
        cls.assertEqual(repair.location_dest_id, cls.rma_external_location)

        # check stock moves
        moves = cls.move_obj.search([('reference', '=', rma.name)])
        for m in moves:
            cls.assertEqual(m.state, 'done')
            cls.assertEqual(m.location_id,
                            cls.customer_location)
            cls.assertEqual(m.location_dest_id,
                            cls.stock_location_rma_external)

        # check no JE are generated
        aml = cls.aml_obj.search([('name', '=', rma.name)])
        cls.assertEqual(len(aml), 0)

        # end repair
        repair.onchange_type_id()
        repair.onchange_team_id()
        repair.action_repair_ready()
        repair.action_repair_start()
        repair.action_repair_end()

        # deliver
        cls.assertEqual(rma.qty_to_deliver, 1.0)
        wizard = cls.rma_make_picking.with_context({
            'active_ids': rma.id,
            'active_model': 'rma.order.line',
            'picking_type': 'outgoing',
            'active_id': rma.id
        }).create({})
        wizard._create_picking()
        res = rma.action_view_out_shipments()
        picking = cls.env['stock.picking'].browse(res['res_id'])
        picking.move_lines.write({'quantity_done': 1.0})
        picking.button_validate()
        cls.assertEqual(picking.state, 'done')
        # check no JE are generated
        aml = cls.aml_obj.search([('name', '=', rma.name)])
        cls.assertEqual(len(aml), 0)
