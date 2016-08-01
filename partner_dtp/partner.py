# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp import models, fields, api, _
from datetime import datetime

class res_partner(models.Model):
    _inherit = 'res.partner'
    
    @api.multi
    def _dtp_life(self):
        invoice_obj = self.env['account.invoice']
        move_line_obj = self.env['account.move.line']

        average_days_to_pay = 0
        for partner in self:
            total_days_to_pay = 0
            inv_ids = invoice_obj.search([('partner_id', '=', partner.id)])
            total_number_of_invoices = 0
            for invoice in inv_ids:
                invoice_rec = invoice.read(['name', 'type', 'number', 'state', 'date_invoice', 'date_due', 'payment_ids'])[0]
                if invoice_rec['state'] == 'paid' and invoice_rec['type'] == 'out_invoice':
                    total_number_of_invoices += 1
                    date_due = invoice_rec['date_invoice']
                    days_for_latest_payment = 0
                    for payment in invoice_rec['payment_ids']:
                        move_line = move_line_obj.browse(payment)
                        payment_rec = move_line.read(['name', 'state', 'date'])[0]
                        if payment_rec['state'] == 'valid': 
                            days_for_this_payment = (datetime.strptime(payment_rec['date'], '%Y-%m-%d') - datetime.strptime(date_due, '%Y-%m-%d')).days
                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment
                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = total_days_to_pay / total_number_of_invoices
                partner.d2p_life = average_days_to_pay
    
    @api.multi
    def _dtp_ytd(self):
        invoice_obj = self.env['account.invoice']
        move_line_obj = self.env['account.move.line']

        average_days_to_pay = 0
        for partner in self:
            total_days_to_pay = 0
            inv_ids = invoice_obj.search([('partner_id', '=', partner.id)])
            total_number_of_invoices = 0
            for invoice in inv_ids:
                invoice_rec = invoice.read(['name', 'number', 'state', 'type', 'date_invoice', 'date_due', 'payment_ids'])[0]
                if invoice_rec['state'] == 'paid' and invoice_rec['type'] == 'out_invoice' and datetime.strptime(invoice_rec['date_invoice'], '%Y-%m-%d').year == datetime.now().year:
                    total_number_of_invoices += 1
                    date_due = invoice_rec['date_invoice']
                    days_for_latest_payment = 0

                    for payment in invoice_rec['payment_ids']:
                        move_line = move_line_obj.browse(payment)
                        payment_rec = move_line.read(['name', 'state', 'date'])[0]
                        if payment_rec['state'] == 'valid':
                            days_for_this_payment = (datetime.strptime(payment_rec['date'], '%Y-%m-%d') - datetime.strptime(date_due, '%Y-%m-%d')).days
                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment
                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = total_days_to_pay / total_number_of_invoices
            partner.d2p_ytd = average_days_to_pay
    
    @api.multi
    def _dtr_life(self):
        invoice_obj = self.env['account.invoice']
        move_line_obj = self.env['account.move.line']

        average_days_to_pay = 0
        for partner in self:
            total_days_to_pay = 0
            inv_ids = invoice_obj.search([('partner_id', '=', partner.id)])
            total_number_of_invoices = 0
            for invoice in inv_ids:
                invoice_rec = invoice.read(['name', 'type', 'number', 'state', 'date_invoice', 'date_due', 'payment_ids'])[0]
                if invoice_rec['state'] == 'paid' and invoice_rec['type'] == 'in_invoice':
                    total_number_of_invoices += 1
                    date_due = invoice_rec['date_invoice']
                    days_for_latest_payment = 0

                    for payment in invoice_rec['payment_ids']:
                        move_line = move_line_obj.browse(payment)
                        payment_rec = move_line.read(['name', 'state', 'date'])[0]
                        if payment_rec['state'] == 'valid':
                            days_for_this_payment = (datetime.strptime(payment_rec['date'], '%Y-%m-%d') - datetime.strptime(date_due, '%Y-%m-%d')).days
                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment
                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = total_days_to_pay / total_number_of_invoices
            partner.d2r_life = average_days_to_pay
    
    @api.multi
    def _dtr_ytd(self):
        invoice_obj = self.env['account.invoice']
        move_line_obj = self.env['account.move.line']

        average_days_to_pay = 0
        for partner in self:
            total_days_to_pay = 0
            inv_ids = invoice_obj.search([('partner_id', '=', partner.id)])
            total_number_of_invoices = 0
            for invoice in inv_ids:
                invoice_rec = invoice.read(['name', 'number', 'state', 'type', 'date_invoice', 'date_due', 'payment_ids'])[0]
                if invoice_rec['state'] == 'paid' and invoice_rec['type'] == 'in_invoice' and datetime.strptime(invoice_rec['date_invoice'], '%Y-%m-%d').year == datetime.now().year:
                    total_number_of_invoices += 1
                    date_due = invoice_rec['date_invoice']
                    days_for_latest_payment = 0

                    for payment in invoice_rec['payment_ids']:
                        move_line = move_line_obj.browse(payment)
                        payment_rec = move_line.read(['name', 'state', 'date'])[0]
                        if payment_rec['state'] == 'valid':
                            days_for_this_payment = (datetime.strptime(payment_rec['date'], '%Y-%m-%d') - datetime.strptime(date_due, '%Y-%m-%d')).days
                            if days_for_this_payment < 0:
                                days_for_this_payment = 0
                            if days_for_this_payment > days_for_latest_payment:
                                days_for_latest_payment = days_for_this_payment
                    days_to_pay_invoice = days_for_latest_payment
                    total_days_to_pay = total_days_to_pay + days_to_pay_invoice
                    average_days_to_pay = total_days_to_pay / total_number_of_invoices
            partner.d2r_ytd = average_days_to_pay


    d2p_life = fields.Float(compute='_dtp_life', string='AVG Days to Pay (lifetime)')
    d2r_life = fields.Float(compute='_dtr_life', string='AVG Days to Pay (lifetime)')
    d2p_ytd = fields.Float(compute='_dtp_ytd', string='AVG Days to Pay (YTD)')
    d2r_ytd = fields.Float(compute='_dtr_ytd', string='AVG Days to Pay (YTD)')
