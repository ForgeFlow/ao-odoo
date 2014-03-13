# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 OpenERP SA (<http://www.openerp.com>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################
from osv import osv, fields
from tools.translate import _
import decimal_precision as dp

class sale_order(osv.osv):
    _inherit = "sale.order"
    
    def onchange_partner_id(self, cr, uid, ids, part, context=None):
        """Override method to add new fields values.
        @param part- update vals with partner exemption number and code, 
        also check address validation by avalara  
        """
        
        res = super(sale_order, self).onchange_partner_id(cr, uid, ids, part, context=None)
        res_obj = self.pool.get('res.partner').browse(cr, uid, part, context=context)
        addr = self.pool.get('res.partner').browse(cr, uid, res['value'] and res['value']['partner_shipping_id'] or part)
        res['value']['exemption_code'] = res_obj.exemption_number or ''
        res['value']['exemption_code_id'] = res_obj.exemption_code_id.id or None
        res['value']['tax_add_shipping'] = True
        res['value']['tax_address'] = str(addr.name+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))
        if res_obj.validation_method:res['value']['is_add_validate'] = True
        else:res['value']['is_add_validate'] = False
        return res
                
    
    def create(self, cr, uid, vals, context=None):
        if vals['partner_id']:
            res_obj = self.pool.get('res.partner').browse(cr, uid, vals['partner_id'], context=context)
            if 'exemption_code' in vals:
                vals['exemption_code'] = vals['exemption_code']
            else:
                vals['exemption_code'] = res_obj.exemption_number or ''
            if 'exemption_code_id' in vals:
                vals['exemption_code_id'] = vals['exemption_code_id']
            else:
                vals['exemption_code_id'] = res_obj.exemption_code_id and res_obj.exemption_code_id.id or False
            vals['tax_add_id'] = vals['partner_id']
            if res_obj.validation_method:vals['is_add_validate'] = True
            
            ship_add_id = False
            if 'tax_add_default' in vals and vals['tax_add_default']:
                ship_add_id = vals['partner_id']
            if 'tax_add_invoice' in vals and vals['tax_add_invoice']:
                ship_add_id = vals['partner_invoice_id']
            if 'tax_add_shipping' in vals and vals['tax_add_shipping']:
                ship_add_id = vals['partner_shipping_id']
                
            addr = self.pool.get('res.partner').browse(cr, uid, ship_add_id or vals['partner_id'])
            vals['tax_address'] = str(addr.name+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))
        return super(sale_order, self).create(cr, uid, vals, context=context)
#    
    def write(self, cr, uid, ids, vals, context=None):
        for self_obj in self.browse(cr, uid, ids):
            ship_add_id = False
            if 'tax_add_default' in vals and vals['tax_add_default']:
                ship_add_id = self_obj.partner_id.id
            if 'tax_add_invoice' in vals and vals['tax_add_invoice']:
                ship_add_id = self_obj.partner_invoice_id and self_obj.partner_invoice_id.id or self_obj.partner_id.id
            if 'tax_add_shipping' in vals and vals['tax_add_shipping']:
                ship_add_id = self_obj.partner_shipping_id and self_obj.partner_shipping_id.id or self_obj.partner_id.id
            if 'partner_id' in vals:
                addr = self.pool.get('res.partner').address_get(cr, uid, [vals['partner_id']], ['delivery', 'invoice', 'contact'])
                ship_add_id = addr['delivery'] or vals['partner_id']
        if ship_add_id:
            addr = self.pool.get('res.partner').browse(cr, uid, ship_add_id, context=context)
            vals['tax_address'] = str(addr.name+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))   
                
                 
        if 'partner_id' in vals:
            res_obj = self.pool.get('res.partner').browse(cr, uid, vals['partner_id'], context=context)
            if 'exemption_code' in vals:
                vals['exemption_code'] = vals['exemption_code']
            else:
                vals['exemption_code'] = res_obj.exemption_number or ''
            if 'exemption_code_id' in vals:
                vals['exemption_code_id'] = vals['exemption_code_id']
            else:
                vals['exemption_code_id'] = res_obj.exemption_code_id and res_obj.exemption_code_id.id or False
            if res_obj.validation_method:
                vals['is_add_validate'] = True
            else:
                vals['is_add_validate'] = False
        return super(sale_order, self).write(cr, uid, ids, vals, context=context)
    
    def _make_invoice(self, cr, uid, order, lines, context=None):
        """ Override method to add shipping lines in invoice.
        @param lines: Shipping lines with ship method, code and amount and after it will return 
        shipping tax amount using shipping code 
        """
        inv_id = super(sale_order, self)._make_invoice(cr, uid, order, lines, context=None)
        if inv_id and order._table_name == 'sale.order':
            ship_data = []
            for ship_line in order.shipping_lines:
                
               ship_data.append((0,0,{
                          'ship_method_id': ship_line.ship_method_id.id,
                          'shipping_cost': ship_line.shipping_cost,
                          'ship_code_id': ship_line.ship_code_id.id,
                          'sale_account_id': ship_line.sale_account_id.id,
                          'tax_amt': ship_line.tax_amt,
                            }))
            self.pool.get('account.invoice').write(cr,uid,[inv_id],{
                                                         'shipping_lines': ship_data or False,
                                                         'exemption_code': order.exemption_code or '',
                                                         'exemption_code_id': order.exemption_code_id.id or False,
                                                         'shipping_amt': order.amount_shipping,
                                                         'tax_add_default': order.tax_add_default,
                                                         'tax_add_invoice': order.tax_add_invoice,
                                                         'tax_add_shipping': order.tax_add_shipping,
#                                                         'shipping_add_id': order.tax_add_invoice and order.partner_invoice_id.id or order.tax_add_shipping and order.partner_shipping_id.id or order.partner_id.id,
                                                          'shipping_address': order.tax_address,
                                                          'location_code': order.location_code or '',  
                                                        })
            
            
            self.pool.get('account.invoice').button_reset_taxes(cr, uid, [inv_id], context=context)
                    
        return inv_id
    
    def _amount_all(self, cr, uid, ids, field_name, arg, context=None):
        """Method override to add shipping charges, taxes and update sale order total
        @param shipping_line: if shipping line present then it will send shipping charge, tax
        and get tax values and update amount_tax and amount total   
        """
        cur_obj=self.pool.get('res.currency')
        res = {}
        val = val1 = 0.0
        for order in self.browse(cr, uid, ids, context=context):
            res[order.id] = {
                        'amount_untaxed': 0.0,
                        'amount_tax': 0.0,
                        'amount_total': 0.0,
                        'amount_shipping': 0.0,
                        }
            for line in order.order_line:
              res[order.id]['amount_untaxed'] += line.price_subtotal
              val += self._amount_line_tax(cr, uid, line, context=context)
            val1 = val + order.tax_amount
            res[order.id]['amount_tax'] = cur_obj.round(cr, uid, order.pricelist_id.currency_id, val1)
            
            for ship_line in order.shipping_lines:
              res[order.id]['amount_shipping'] += ship_line.shipping_cost
            res[order.id]['amount_total'] = res[order.id]['amount_untaxed'] + res[order.id]['amount_tax'] + res[order.id]['amount_shipping']                 
        return res

    def _get_order(self, cr, uid, ids, context=None):
        result = {}
        for line in self.pool.get('sale.order.line').browse(cr, uid, ids, context=context):
            result[line.order_id.id] = True
        return result.keys()
    
    def _get_ship_order(self, cr, uid, ids, context=None):
        result = {}
        for ship_line in self.pool.get('shipping.order.line').browse(cr, uid, ids, context=context):
            result[ship_line.sale_ship_id.id] = True
        return result.keys()
    
    def default_tax_address(self, cr, uid, ids, ship_id, tax_add_id, context=None):
        if ship_id and tax_add_id:
            addr = self.pool.get('res.partner').browse(cr, uid, tax_add_id, context=context)
            tax_address = str(addr.name+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))
            return {'value':{'tax_add_default':True, 'tax_add_invoice':False, 'tax_add_shipping':False, 'tax_address':tax_address}}
        return {}
    
    def invoice_tax_address(self, cr, uid, ids, inv_id, tax_add_id, part_id, context=None):
        if inv_id and tax_add_id or inv_id and part_id:
            addr = self.pool.get('res.partner').browse(cr, uid, tax_add_id or part_id, context=context)
            tax_address = str(addr.name+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))
            return {'value':{'tax_add_default':False, 'tax_add_invoice':True, 'tax_add_shipping':False, 'tax_address':tax_address}}
        return {}
    
    def delivery_tax_address(self, cr, uid, ids, del_id, tax_add_id, part_id, context=None):
        if del_id and tax_add_id or del_id and part_id:
            addr = self.pool.get('res.partner').browse(cr, uid, tax_add_id or part_id, context=context)
            tax_address = str(addr.name+ '\n'+(addr.street or '')+ '\n'+(addr.city and addr.city+', ' or ' ')+(addr.state_id and addr.state_id.name or '')+ ' '+(addr.zip or '')+'\n'+(addr.country_id and addr.country_id.name or ''))
            return {'value':{'tax_add_default':False, 'tax_add_invoice':False, 'tax_add_shipping':True, 'tax_address':tax_address}}
        return {}
    
    def get_address_for_tax(self, cr, uid, ids, context=None):
        """ Partner address, on which Avalara tax will calculate """
        for order in self.browse(cr, uid, ids, context):
            if order.tax_add_invoice:
                return order.partner_invoice_id.id
            elif order.tax_add_shipping:
                return order.partner_shipping_id.id
            elif order.tax_add_default:
                return order.partner_id.id
            else:
                raise osv.except_osv(_('Avatax: Warning !'), _('Please select address for avalara tax'))
    
    

    _columns = {
        'exemption_code': fields.char('Exemption Number', help="It show the customer exemption number", ),
        'is_add_validate': fields.boolean('Address validated',),
        'exemption_code_id': fields.many2one('exemption.code', 'Exemption Code', help="It show the customer exemption code",),
        'shipping_lines': fields.one2many('shipping.order.line','sale_ship_id', 'Avatax Shipping Lines', readonly=True, states={'draft': [('readonly', False)], 'sent': [('readonly', False)]}),       
        'amount_shipping': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Sale Price'), string='Shipping Cost',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'shipping.order.line': (_get_ship_order, ['name', 'shipping_cost'], 10),
            },
             multi='sums', help="The amount without tax."),
        'amount_untaxed': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Sale Price'), string='Untaxed Amount',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The amount without tax."),
        'amount_tax': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Sale Price'), string='Taxes',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The tax amount."),
        'amount_total': fields.function(_amount_all, method=True, digits_compute= dp.get_precision('Sale Price'), string='Total',
            store = {
                'sale.order': (lambda self, cr, uid, ids, c={}: ids, ['order_line'], 10),
                'sale.order.line': (_get_order, ['price_unit', 'tax_id', 'discount', 'product_uom_qty'], 10),
            },
            multi='sums', help="The total amount."),
          'tax_amount': fields.float('Tax Code Amount', digits_compute=dp.get_precision('Sale Price')),
          'tax_add_default': fields.boolean('Default Address', readonly=True, states={'draft': [('readonly', False)]}),
          'tax_add_invoice': fields.boolean('Invoice Address', readonly=True, states={'draft': [('readonly', False)]}),
          'tax_add_shipping': fields.boolean('Delivery Address', readonly=True, states={'draft': [('readonly', False)]}),
#          'tax_add_id': fields.many2one('res.partner', 'Tax Address', readonly=True, states={'draft': [('readonly', False)]}),
          'tax_address': fields.text('Tax Address'),  
          'location_code': fields.related('shop_id', 'location_code', type="char", string="Location Code", store=True, readonly=True, help="Origin address location code"),
    }
    _defaults = {
        'tax_add_shipping': True,
        }

    def create_lines(self, cr, uid, order_lines):
        """ Tax line creation for calculating tax amount using avalara tax code. """
        lines = []
        for line in order_lines:
            lines.append({
                'qty': line.product_uom_qty,
                'itemcode': line.product_id and line.product_id.default_code or None,
                'description': line.product_id.description or None,
                'amount': line.price_unit * (1-(line.discount or 0.0)/100.0) * line.product_uom_qty,
                'tax_code': line.product_id and ((line.product_id.tax_code_id and line.product_id.tax_code_id.name) or
                        (line.product_id.categ_id.tax_code_id  and line.product_id.categ_id.tax_code_id.name)) or None
            })
        return lines
    
    def create_shipping_line(self, cr, uid, shipping_lines):
        """ Shipping line creation for calculating ship tax amount using avalara shipping codes"""
        lines = []
        for line in shipping_lines:
            lines.append({
                'qty': 1,
                'itemcode': 'Ship/Freight',
                'description': 'Ship/Freight',
                'amount': line.shipping_cost,
                'tax_code': line.ship_code_id.name,
            })
        return lines

    def compute_tax(self, cr, uid, ids, context=None):
        """ Create and update tax amount for each and every order line and shipping line.
        @param order_line: send sub_total of each line and get tax amount
        @param shiiping_line: send shipping amount of each ship line and get ship tax amount  
        """
        avatax_config_obj = self.pool.get('avalara.salestax')
        account_tax_obj = self.pool.get('account.tax')
        avatax_config = avatax_config_obj._get_avatax_config_company(cr, uid)
        partner_obj = self.pool.get('res.partner')
        order_line = self.pool.get('sale.order.line')
        ship_order_line = self.pool.get('shipping.order.line')
        tax_amount = 0.0
        o_tax_amt = 0.0
        s_tax_amt = 0.0
        lines = []
        for order in self.browse(cr, uid, ids):
            if avatax_config and not avatax_config.disable_tax_calculation:
                shipping_add_id = self.get_address_for_tax(cr, uid, ids, context)
                
                lines1 = self.create_lines(cr, uid, order.order_line)
                lines2 = self.create_shipping_line(cr, uid, order.shipping_lines)
                
                if avatax_config.on_line:
                    # Line level tax calculation
                    #tax based on individual order line 
                    for line1, o_line in zip(lines1, order.order_line):
                        ol_tax_amt =  account_tax_obj._get_compute_tax(cr, uid, avatax_config, order.date_confirm or order.date_order,
                                                                    order.name, 'SalesOrder', order.partner_id, order.company_id.partner_id.id,
                                                                    shipping_add_id, [line1], order.user_id, order.exemption_code or None, order.exemption_code_id.code or None, 
                                                                    context=context).TotalTax
                        o_tax_amt += ol_tax_amt  #tax amount based on total order line total   
                        order_line.write(cr, uid, [o_line.id], {'tax_amt': ol_tax_amt,})
                
                    #tax based on individual shipping order line
                    for line2, s_line in zip(lines2, order.shipping_lines):
                        sl_tax_amt = account_tax_obj._get_compute_tax(cr, uid, avatax_config, order.date_confirm or order.date_order,
                                                                    order.name, 'SalesOrder', order.partner_id, order.company_id.partner_id.id,
                                                                    shipping_add_id, [line2], order.user_id, order.exemption_code or None, order.exemption_code_id.code or None,
                                                                    context=context).TotalTax
                        s_tax_amt += sl_tax_amt #tax amount based on total shipping line total
                        ship_order_line.write(cr, uid, [s_line.id], {'tax_amt': sl_tax_amt,})
                    tax_amount = o_tax_amt + s_tax_amt
                    
                elif avatax_config.on_order:
                    # Order level tax calculation
                    lines1.extend(lines2)
                   
                    tax_amount = account_tax_obj._get_compute_tax(cr, uid, avatax_config, order.date_confirm or order.date_order,
                                                                    order.name, 'SalesOrder', order.partner_id, order.company_id.partner_id.id,
                                                                    shipping_add_id, lines1, order.user_id, order.exemption_code or None, order.exemption_code_id.code or None,
                                                                    context=context).TotalTax
                                                                    
                    for o_line in order.order_line:
                        order_line.write(cr, uid, [o_line.id], {'tax_amt': 0.0,})
                    for s_line in order.shipping_lines:
                       ship_order_line.write(cr, uid, [s_line.id], {'tax_amt': 0.0,}) 
                else:
                    raise osv.except_osv(_('Avatax: Warning !'), _('Please select system calls in API Configuration'))
            else:
                for o_line in order.order_line:
                    order_line.write(cr, uid, [o_line.id], {'tax_amt': 0.0,})
                for s_line in order.shipping_lines:
                   ship_order_line.write(cr, uid, [s_line.id], {'tax_amt': 0.0,}) 
                        
            self.write(cr, uid, [order.id], {'tax_amount': tax_amount, 'order_line': []})
        return True

    def button_dummy(self, cr, uid, ids, context=None):
        """ It used to called manually calculation method of avalara and get tax amount"""
        self.compute_tax(cr, uid, ids, context=context)
        return super(sale_order, self).button_dummy(cr, uid, ids, context=context)

    def action_wait(self, cr, uid, ids, context=None):
        res = super(sale_order, self).action_wait(cr, uid, ids, context=context)
        self.compute_tax(cr, uid, ids, context=context)
        return res

sale_order()

class sale_order_line(osv.osv):
    _inherit = "sale.order.line"
    _columns = {
            'tax_amt': fields.float('Avalara Tax', help="tax calculate by avalara"),
            }
sale_order_line()

"""
    Create shipping order line class and perform all operation same as sale order line
"""
class shipping_order_line(osv.osv):
    _name = 'shipping.order.line'
    _description = 'Shipping Order lines'
    
    def get_default_ship_code(self, cr, uid, context=None):
        """get default shipping code FR if already created otherwise it will create and get it"""
        ids = self.pool.get('product.tax.code').search(cr, uid, [('name','=','FR')], context=context)
        if ids:
            return ids[0]
        else:
            return self.pool.get('product.tax.code').create(cr, uid, {
                    'name':'FR',
                    'description': 'Default Shipping Code',
                    'type':'freight',       
                 })
                
    
    def onchange_select(self, cr, uid, ids, rate_select, context={}):
        new_list = {}
        ship_rate = self.pool.get('shipping.rate.config')
        account_id = False
        for line in ship_rate.browse(cr,uid,[rate_select]):
            new_list['name'] = line.name,
            new_list['shipping_cost'] = line.shipping_cost
            new_list['sale_account_id']= line.account_id.id
        return {'value': new_list}
    
    _columns = {
            'name': fields.char('Shipping Method',size=128,help='Shipping method name. Displayed in the wizard.'),
            'ship_method_id': fields.many2one('shipping.rate.config','Ship By', required=True),
            'shipping_cost': fields.float('Shipping Cost'),
            'ship_code_id': fields.many2one('product.tax.code', "Ship Code", required=True, help="Show shipping code"),
            'sale_account_id':fields.many2one('account.account','Shipping Account',help='This account represents the g/l account for booking shipping income.'),
            'tax_amt': fields.float('Avalara Tax', help="tax amount based on shipping cost"),
            'sale_ship_id': fields.many2one('sale.order', 'Sale Ship ID'),
            'invoice_ship_id': fields.many2one('account.invoice', 'Invoice ship ID'),
        }
    
    _defaults = {
                 'ship_code_id':get_default_ship_code,
            }
    
shipping_order_line()

class shipping_rate_config(osv.osv):
    """ Shipping Rate Configuration with shipping cost, Shipping method and also shipping account"""
    _name = 'shipping.rate.config'
    _description = "Configuration for shipping rate"
    _columns = {
                'real_id':fields.integer('ID',readonly=True, ),
                'name':fields.char('Shipping Method Name',size=128,help='Shipping method name. Displayed in the wizard.'),
                'active':fields.boolean('Active',help='Indicates whether a shipping method is active'),
                'shipping_cost':fields.float('Shipping Cost'),
                'account_id':fields.many2one('account.account','Account',help='This account represents the g/l account for booking shipping income.'),
    }
    
    _defaults = {
                 'active':True,
            }

shipping_rate_config()

class sale_shop(osv.osv):
    _inherit = "sale.shop"
    _columns = {
            'location_code': fields.char('Location Code', size=128),
            }
sale_shop()
    


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
