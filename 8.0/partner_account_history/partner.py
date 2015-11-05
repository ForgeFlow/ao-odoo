# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp import fields, models, api, _
from openerp import tools

class partner_account_history(models.Model):
    _name = 'partner.account.history'
    _auto = False

    @api.multi
    def allopen(self):
        self.ensure_one()
        inv_view = self.env.ref('account.invoice_form')
        inv_view_id = inv_view and inv_view.id or False
        vou_view = self.env.ref('account_voucher.view_voucher_form')
        vou_view_id = vou_view and vou_view.id or False
        mov_view = self.env.ref('account.view_move_form')
        mov_view_id = mov_view and mov_view.id or False

        inv_id = self.iid.id
        vou_id = self.vid.id
        mov_id = self.midd.id

        inv_type = self.t

        if inv_type == 'Supplier Invoice' or inv_type == 'Supplier Credit':
            invoice_type_to_return = 'out_invoice' 
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [inv_view_id],
                'res_model': 'account.invoice',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': inv_id,
           }
        elif inv_type == 'Customer Credit' or inv_type == 'Customer Invoice':
            invoice_type_to_return = 'in_invoice'    
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [inv_view_id],
                'res_model': 'account.invoice',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': inv_id,
           }
        elif inv_type == 'Supplier Payment' or inv_type == 'Purchase Receipt':
            invoice_type_to_return = 'out_invoice'
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [vou_view_id],
                'res_model': 'account.voucher',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': vou_id,
            }
        elif inv_type == 'Customer Payment' or inv_type == 'Sales Receipt':
            invoice_type_to_return = 'in_invoice'
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [vou_view_id],
                'res_model': 'account.voucher',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': vou_id,
            }
        else:
            dic_to_ret = {
                'name': inv_type,
                'view_type': 'form',
                'view_mode': 'form',
                'view_id': [mov_view_id],
                'res_model': 'account.move',
                'context': "",
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'current',
                'res_id': mov_id,
            }
        return dic_to_ret

    p = fields.Many2one('res.partner', string='Partner')
    ic = fields.Boolean(string='Customer')
    iss = fields.Boolean(string='Supplier')
    iid = fields.Many2one('account.invoice', string='Related Document')
    vid = fields.Many2one('account.voucher', string='Related Document')
    midd = fields.Many2one('account.move', string='Related Document')
    e = fields.Char(string='Entered')
    ef = fields.Char(string='Effective')
    efd = fields.Date(string='Effective')
    d = fields.Char(string='Due')
    pn = fields.Char(string='Name')
    doc = fields.Char(string='Document')
    r = fields.Char(string='Reference/Number')
    t = fields.Char(string='Type')
    s = fields.Char(string='State')
    oa = fields.Float(string='Original Amount', digits=(12, 2))
    b = fields.Float(string='Balance', digits=(12, 2))

    _order = 'pn, efd'

    def init(self, cr):
    
        query = """
select cast(100000000000 + ai.id as bigint) as id, '' as number, customer as IC, supplier as ISS, partner_id as P, p.name as PN, ai.id as IID, 0 as VID, 0 as MIDD,
to_char(ai.create_date,'MM-DD-YYYY') as E, to_char(date_invoice,'MM-DD-YYYY') as EF, date_invoice as efd, to_char(date_due,'MM-DD-YYYY') as D,  ai.supplier_invoice_number as DOC, number as R, 
'Supplier Invoice' as T,
CASE WHEN state ='draft' THEN 'Draft' WHEN state ='proforma2' THEN 'Pro-forma' WHEN state ='proforma' THEN 'Pro-forma'
WHEN state ='paid' THEN 'Paid' WHEN state = 'open' THEN 'Open' WHEN state ='cancel' THEN 'Cancelled' END as S,amount_total as  OA,residual as B 
from account_invoice as ai,res_partner as p where ai.type = 'in_invoice' and ai.partner_id = p.id
UNION
select cast(100000000000 + ai.id as bigint) as id, '' as number, customer as IC, supplier as ISS, partner_id as P, p.name as PN, ai.id as IID, 0 as VID, 0 as MIDD,
to_char(ai.create_date,'MM-DD-YYYY') as E, to_char(date_invoice,'MM-DD-YYYY') as EF, date_invoice as efd, to_char(date_due,'MM-DD-YYYY') as D,  ai.name as DOC, number as R, 
'Supplier Credit' as T,
CASE WHEN state ='draft' THEN 'Draft' WHEN state ='proforma2' THEN 'Pro-forma' WHEN state ='proforma' THEN 'Pro-forma'
WHEN state ='paid' THEN 'Paid' WHEN state = 'open' THEN 'Open' WHEN state ='cancel' THEN 'Cancelled' END as S,amount_total as OA,residual as B 
from account_invoice as ai, res_partner as p where  ai.type = 'in_refund' and ai.partner_id = p.id
UNION
select cast(100000000000 + ai.id as bigint) as id,'' as number, customer as IC, supplier as ISS, partner_id as P, p.name as PN, ai.id as IID, 0 as VID, 0 as MIDD,
to_char(ai.create_date,'MM-DD-YYYY') as E, to_char(date_invoice,'MM-DD-YYYY') as EF, date_invoice as efd, to_char(date_due,'MM-DD-YYYY') as D,  ai.internal_number as DOC, number as R, 
'Customer Invoice' as T,
CASE WHEN state ='draft' THEN 'Draft' WHEN state ='proforma2' THEN 'Pro-forma' WHEN state ='proforma' THEN 'Pro-forma'
WHEN state ='paid' THEN 'Paid' WHEN state = 'open' THEN 'Open' WHEN state ='cancel' THEN 'Cancelled' END as S,amount_total as OA,residual as B 
from account_invoice as ai,res_partner as p where  ai.type = 'out_invoice' and ai.partner_id = p.id
UNION
select cast(100000000000 + ai.id as bigint) as id,'' as number, customer as IC, supplier as ISS, partner_id as P, p.name as PN, ai.id as IID, 0 as VID, 0 as MIDD,
to_char(ai.create_date,'MM-DD-YYYY') as E, to_char(date_invoice,'MM-DD-YYYY') as EF, date_invoice as efd, to_char(date_due,'MM-DD-YYYY') as D,  ai.name as DOC, number as R, 
'Customer Credit' as T,
CASE WHEN state ='draft' THEN 'Draft' WHEN state ='proforma2' THEN 'Pro-forma' WHEN state ='proforma' THEN 'Pro-forma'
WHEN state ='paid' THEN 'Paid' WHEN state = 'open' THEN 'Open' WHEN state ='cancel' THEN 'Cancelled' END as S,amount_total as OA, residual as B 
from account_invoice as ai, res_partner as p where  ai.type = 'out_refund' and  ai.partner_id = p.id
UNION
select av.id as id, '' as number, customer as IC, supplier as ISS, partner_id as P, p.name as PN,0  as IID, av.id as VID, 0 as MIDD,
to_char(av.create_date,'MM-DD-YYYY') as E, to_char(av.date,'MM-DD-YYYY') as EF, av.date as efd, '' as D, av.name as DOC, reference as R, 'Sales Receipt' as T,
CASE WHEN state='draft' THEN 'Draft' WHEN state='proforma' THEN 'Pro-forma' WHEN state='posted' THEN 'Posted'
WHEN state= 'cancel' THEN 'Cancelled' END as S, amount as OA,0 as B 
from account_voucher as av, res_partner as p
where av.type = 'sale' and  av.partner_id = p.id
UNION
select av.id as id,'' as number, customer as IC, supplier as ISS, partner_id as P, p.name as PN,  0 as IID, av.id as VID, 0 as MIDD,
to_char(av.create_date,'MM-DD-YYYY') as E, to_char(av.date,'MM-DD-YYYY') as EF, av.date as efd, '' as D, av.name as DOC, reference as R, 'Purchase Receipt' as T,
CASE WHEN state='draft' THEN 'Draft' WHEN state='proforma' THEN 'Pro-forma' WHEN state='posted' THEN 'Posted'
WHEN state= 'cancel' THEN 'Cancelled' END as S, amount as OA, 0 as B
from account_voucher as av, res_partner as p
where av.type = 'purchase' and  av.partner_id = p.id
UNION
select av.id as id,av.number,customer as IC, supplier as ISS, partner_id as P, p.name as PN,  0 as IID, av.id as VID, 0 as MIDD,
to_char(av.create_date,'MM-DD-YYYY') as E, to_char(av.date,'MM-DD-YYYY') as EF, av.date as efd, '' as D, av.name as DOC, number as R, 'Supplier Payment' as T,
CASE WHEN state='draft' THEN 'Draft' WHEN state='proforma' THEN 'Pro-forma' WHEN state='posted' THEN 'Posted'
WHEN state= 'cancel' THEN 'Cancelled' END as S, amount as OA,  CASE WHEN (select count(name) from account_move_line where name=number) 
> 1 THEN (select sum(debit) - sum(credit)
               from account_move_line where name =number) ELSE amount END as B
from account_voucher as av, res_partner as p
where av.type = 'payment' and  av.partner_id = p.id
UNION
select av.id as id,av.number,customer as IC, supplier as ISS, partner_id as P, p.name as PN,  0 as IID, av.id as VID, 0 as MIDD,
to_char(av.create_date,'MM-DD-YYYY') as E, to_char(av.date,'MM-DD-YYYY') as EF, av.date as efd, '' as D, av.name as DOC, number as R, 'Customer Payment' as T,
CASE WHEN state='draft' THEN 'Draft' WHEN state='proform' THEN 'Pro-forma' WHEN state='posted' THEN 'Posted'  WHEN state= 'cancel'
THEN 'Cancelled' END as S, amount as OA,  CASE WHEN (select count(name) from account_move_line where name=number) 
> 1 THEN (select sum(credit) - sum(debit)
               from account_move_line where name =number) ELSE amount END as B
from account_voucher as av, res_partner as p
where av.type = 'receipt' and  av.partner_id = p.id
UNION
select cast(500000000000 + am.id as bigint) as id,'' as number,p.customer as IC, p.supplier as ISS, am.partner_id as P, p.name as PN, 0 as IID, 0 as VID,am.id as MIDD,
to_char(am.create_date,'MM-DD-YYYY') as E, to_char(am.date,'MM-DD-YYYY')  as EF, am.date as efd, '' as D, am.name as DOC,  am.ref as R, 'Manual Journal' as T,
CASE WHEN am.state='draft' THEN 'Unposted' WHEN am.state='posted' THEN 'Posted' END as S,sum(aml.debit) as OA, 0 as B
from account_move am,account_move_line aml,res_partner as p
where am.id = aml.move_id and am.partner_id = p.id
and am.id NOT in (select DISTINCT move_id from account_invoice where move_id is not null)
and am.id NOT in (select DISTINCT move_id from account_voucher where move_id is not null)
GROUP BY am.id, ic, iss, p, pn, iid, vid, midd, e, ef, efd, d, doc, r, t, s, b
        """
        tools.drop_view_if_exists(cr, '%s' % (self._name.replace('.', '_')))
        cr.execute("""
                      CREATE OR REPLACE VIEW %s AS ( %s) 
        """ % (self._name.replace('.', '_'), query)) 

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: