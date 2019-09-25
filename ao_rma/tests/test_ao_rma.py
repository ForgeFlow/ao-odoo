# © 2017 Eficent Business and IT Consulting Services S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html)

from odoo.tests import common


class TestRma(common.SavepointCase):
    """ Test AO flows"""

    @classmethod
    def setUpClass(cls):
        super(TestRma, cls).setUpClass()
        cls.rma_make_picking = cls.env['rma_make_picking.wizard']
        cls.repair_line_obj = cls.env['repair.line']
        cls.rma = cls.env['rma.order']
        cls.rma_line = cls.env['rma.order.line']
        cls.rma_op = cls.env['rma.operation']
        cls.RepairMakeInvoice = cls.env['repair.order.make_invoice']
        cls.product_id = cls.env.ref('product.product_product_4')
        cls.uom_unit = cls.env.ref('uom.product_uom_unit')
        cls.partner_id = cls.env.ref('base.res_partner_2')
        cls.stock_location = cls.env.ref('stock.stock_location_stock')
        cls.stock_location_repair_refurbish = cls.env.ref(
            'ao_rma.stock_location_repair_refurbish')
        cls.customer_location = cls.env.ref(
            'stock.stock_location_customers')
        cls.supplier_location = cls.env.ref(
            'stock.stock_location_suppliers')
        cls.product_uom_id = cls.env.ref('uom.product_uom_unit')
        cls.rma_external_location = cls.env.ref(
            'ao_rma.rma_external_location')
        cls.stock_location_customers = cls.env.ref(
            'stock.stock_location_customers')
        cls.wiz_make_picking = cls.env['rma_make_picking.wizard']
        cls.operation_nw = cls.env.ref('ao_rma.rma_operation_repair_nw')
        cls.operation_warranty = cls.env.ref(
            'ao_rma.rma_operation_repair_warranty')
        cls.operation_int = cls.env.ref(
            'ao_rma.rma_operation_repair_facilities')
        cls.operation_ref = cls.env.ref(
            'ao_rma.rma_operation_repair_refurbish')
        cls.rma_make_repair_wiz = cls.env['rma.order.line.make.repair']
        cls.repair_team = cls.env.ref(
            'ao_rma.repair_team_dep1')
        cls.repair_type = cls.env.ref(
            'ao_rma.repair_type_no_warranty')
        cls.wip_account = cls.env['account.account'].create(
            {'name': 'WIP',
             'code': 'WIP',
             'user_type_id': cls.env.ref(
                 "account.data_account_type_expenses").id})
        cls.ref_account = cls.env['account.account'].create(
            {'name': 'Refurbish',
             'code': 'Refurbish',
             'user_type_id': cls.env.ref(
                 "account.data_account_type_expenses").id})
        cls.rep_account = cls.env['account.account'].create(
            {'name': 'Repair',
             'code': 'Repair',
             'user_type_id': cls.env.ref(
                 "account.data_account_type_expenses").id})
        cls.lab_account = cls.env['account.account'].create(
            {'name': 'Labor',
             'code': 'Labor',
             'user_type_id': cls.env.ref(
                 "account.data_account_type_expenses").id})
        cls.oh_account = cls.env['account.account'].create(
            {'name': 'Overhead',
             'code': 'Overhead',
             'user_type_id': cls.env.ref(
                 "account.data_account_type_expenses").id})
        # cannot do in data because account exists in ao
        if not cls.repair_team.labor_allocation_account_id:
            cls.repair_team.labor_allocation_account_id = cls.lab_account.id
        if not cls.repair_team.overhead_allocation_account_id:
            cls.repair_team.overhead_allocation_account_id = cls.oh_account.id
        if not cls.operation_nw.repair_type_id.wip_account_id:
            cls.operation_nw.repair_type_id.wip_account_id = cls.wip_account
            cls.operation_nw.repair_type_id.\
                default_raw_material_prod_location_id. \
                valuation_in_account_id = cls.wip_account
            cls.operation_nw.repair_type_id.\
                default_raw_material_prod_location_id. \
                valuation_out_account_id = cls.wip_account
        if not cls.operation_ref.repair_type_id.wip_account_id:
            cls.operation_ref.repair_type_id.wip_account_id = cls.ref_account
            cls.operation_ref.repair_type_id.\
                default_raw_material_prod_location_id. \
                valuation_in_account_id = cls.ref_account
            cls.operation_ref.repair_type_id.\
                default_raw_material_prod_location_id. \
                valuation_out_account_id = cls.ref_account
        if not cls.operation_warranty.repair_type_id.wip_account_id:
            cls.operation_warranty.repair_type_id.wip_account_id = \
                cls.wip_account
            cls.operation_warranty.repair_type_id.\
                default_raw_material_prod_location_id. \
                valuation_in_account_id = cls.wip_account
            cls.operation_warranty.repair_type_id.\
                default_raw_material_prod_location_id. \
                valuation_out_account_id = cls.wip_account
        cls.repair_type.force_repair_location = cls.rma_external_location.id
        cls.aml_obj = cls.env['account.move.line']
        cls.acc_type_model = cls.env['account.account.type']
        cls.move_obj = cls.env['stock.move']

        cls.env.user.repair_team_id = cls.repair_team.id
        cls.product_obj = cls.env['product.product']
        cls.refurbish_product = cls.product_obj.create({
            'name': 'Refurbished Awesome Screen',
            'type': 'product',
        })
        cls.refurbish_product.product_tmpl_id.standard_price = 21
        cls.refurbish_product.categ_id.property_valuation = 'real_time'

        cls.product1 = cls.product_obj.create({
            'name': 'Awesome Screen',
            'type': 'product',
            'refurbish_product_id': cls.refurbish_product.id,
        })
        cls.product1.product_tmpl_id.standard_price = 10
        cls.product1.categ_id.property_valuation = 'real_time'
        cls.material = cls.product_obj.create({
            'name': 'Materials',
            'type': 'product',
        })

        cls.material.product_tmpl_id.standard_price = 10
        cls.material.categ_id.property_valuation = 'real_time'
        cls.company = cls.env.ref('base.main_company')
        a_name = 'expense'
        a_type = 'other'
        acc_type = cls._create_account_type(cls, a_name, a_type)
        name = 'Cost of Goods Sold'
        code = 'cogs'
        cls.account_cogs = cls._create_account(cls, acc_type, name, code,
                                               cls.company)
        cls.material.property_stock_account_output = cls.account_cogs.id
        cls.product1.property_stock_account_output = cls.account_cogs.id
        cls.refurbish_product.property_stock_account_output = \
            cls.account_cogs.id

    def _create_account_type(cls, name, a_type):
        acc_type = cls.acc_type_model.create({
            'name': name,
            'type': a_type
        })
        return acc_type

    def _create_account(cls, acc_type, name, code, company):
        """Create an account."""
        account = cls.env['account.account'].create({
            'name': name,
            'code': code,
            'user_type_id': acc_type.id,
            'company_id': company.id
        })
        return account

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
        cls.assertEqual(rma.delivery_policy, 'repair')
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

        cls.assertEqual(repair.location_id, cls.rma_external_location,
                        "wrong repair location %s instead of %s" %
                        (repair.location_id.name,
                         cls.rma_external_location.name))
        cls.assertEqual(repair.location_dest_id, cls.rma_external_location,
                        "wrong repair location %s instead of %s" %
                        (repair.location_dest_id.name,
                         cls.rma_external_location.name))

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
        make_invoice = cls.RepairMakeInvoice.create({
            'group': True})
        # I click on "Create Invoice" button of this wizard to make invoice.
        context = {
            "active_model": 'repair_order',
            "active_ids": [repair.id],
            "active_id": repair.id
        }
        make_invoice.with_context(context).make_invoices()
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

    def test_12_repair_under_warranty(cls):
        """Accounting entries for a reparation with warranty
           Very similar to previous test, considering remove
        """

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
        cls.assertEqual(rma.qty_repaired, 1.0)
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

    def test_13_repair_internal(cls):
        """Accounting entries for an internal reparation.
           Everything is handled in the repair order
        """

        # create rma and receive in external location
        rma = cls.create_customer_rma(cls.partner_id, cls.product_id,
                                      cls.operation_int)
        rma._onchange_operation_id()
        cls.assertEqual(rma.repair_type, 'ordered')
        # create repair order
        make_repair = cls.rma_make_repair_wiz.with_context({
            'customer': True,
            'active_ids': rma.id,
            'active_model': 'rma.order.line',
        }).create({
            'description': 'Test internal',
        })
        make_repair.make_repair_order()
        repair = rma.repair_ids
        rma.repair_ids.action_repair_confirm()

        cls.assertEqual(repair.location_id, cls.stock_location)
        cls.assertEqual(repair.location_dest_id, cls.stock_location)

        # check stock moves
        moves = cls.move_obj.search([('reference', '=', rma.name)])
        cls.assertEqual(len(moves), 0)

        # check no JE are generated
        aml = cls.aml_obj.search([('name', '=', rma.name)])
        cls.assertEqual(len(aml), 0)

        # end repair
        repair.onchange_type_id()
        repair.onchange_team_id()
        repair.action_repair_ready()
        repair.action_repair_start()
        repair.action_repair_end()

        # check no JE are generated
        aml = cls.aml_obj.search([('name', '=', rma.name)])
        cls.assertEqual(len(aml), 0)

    def test_14_repair_refursbish(cls):
        """Accounting entries for return and refurbish.
           The repair is performed inside the company
        """

        # create rma and receive in external location
        rma = cls.create_customer_rma(cls.partner_id, cls.product1,
                                      cls.operation_ref)
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

        # check incoming shipment created JE
        aml = cls.aml_obj.search([('rma_line_id', '=', rma.id)])
        cls.assertEqual(len(aml), 1)
        amlr = aml.filtered(lambda a: a.account_id == cls.account_cogs)
        cls.assertEqual(sum(amlr.mapped('credit')), 10)

        # create repair order
        make_repair = cls.rma_make_repair_wiz.with_context({
            'customer': True,
            'active_ids': rma.id,
            'active_model': 'rma.order.line',
        }).create({
            'description': 'Test refursbish',
        })
        make_repair.make_repair_order()
        repair = rma.repair_ids
        line = cls.repair_line_obj.create({
            'name': 'consume stuff to repair',
            'repair_id': repair.id,
            'type': 'add',
            'product_id': cls.material.id,
            'product_uom': cls.material.uom_id.id,
            'product_uom_qty': 1.0,
            'location_id': cls.stock_location.id,
            'location_dest_id': cls.stock_location.id,
            'price_unit': 10.0
        })

        line.onchange_product_id()
        repair.onchange_type_id()
        repair.onchange_team_id()
        repair._onchange_to_refurbish()
        cls.assertEqual(repair.location_id, cls.stock_location)
        cls.assertEqual(
            repair.location_id, cls.stock_location,
            "wrong repair location %s instead of %s" %
            (repair.location_id.name,
             cls.stock_location.name))
        cls.assertTrue(repair.to_refurbish)

        rma.repair_ids.action_repair_confirm()

        # end repair
        repair.action_repair_ready()
        repair.action_repair_start()
        repair.action_repair_end()

        # check no extra JE are generated(handled by repair order)
        amlrma = cls.aml_obj.search([('rma_line_id', '=', rma.id)])
        cls.assertEqual(len(amlrma), 1)

        # check cogs
        aml = cls.aml_obj.search([('name', '=', repair.name)])
        cls.assertEqual(len(aml), 10)
        amli = aml.filtered(
            lambda a: a.account_id.name == 'Stock Valuation Account')
        cls.assertEqual(len(amli), 3)
        amlrr = aml.filtered(
            lambda a: a.account_id.name == 'Refurbish')
        cls.assertEqual(len(amlrr), 5)
        amlr = amlrma.filtered(lambda a: a.account_id == cls.account_cogs)
        cls.assertEqual(sum(amlr.mapped('credit')), 10)
