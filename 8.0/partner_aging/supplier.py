# -*- coding: utf-8 -*-



######################################################################
#
#  Note: Program metadata is available in /__init__.py
#
######################################################################

from openerp import fields, models, api, _
from openerp import tools

class partner_aging_supplier(models.Model):
    _name = 'partner.aging.supplier'
    _auto = False

    @api.multi
    def invopen(self):
        self.ensure_one()
        view = self.env.ref('account.invoice_form')
        view_id = view and view.id or False
        
        inv_id = self.invoice_id.id 
   
        return {
            'name': ('Supplier Invoices'),
            'view_type': 'form',
            'view_mode': 'form',
            'view_id': [view_id],
            'res_model': 'account.invoice',
            'context': "{'type':'out_invoice'}",
            'type': 'ir.actions.act_window',
            'nodestroy': True,
            'target': 'current',
            'res_id': inv_id,
        }

    partner_id = fields.Many2one('res.partner', string=u'Partner', readonly=True)
    partner_name = fields.Text(string='Name', readonly=True)
    max_days_overdue = fields.Integer(string=u'Days Overdue', readonly=True)
    avg_days_overdue = fields.Integer(string=u'Avg Days Overdue', readonly=True)
    oldest_invoice_date = fields.Date(string=u'Invoice Date', readonly=True)
    total = fields.Float(string=u'Total', readonly=True)
    current = fields.Float(string=u'Current', readonly=True)
    days_due_01to30 = fields.Float(string=u'01/30', readonly=True)
    days_due_31to60 = fields.Float(string=u'31/60', readonly=True)
    days_due_61to90 = fields.Float(string=u'61/90', readonly=True)
    days_due_91to120 = fields.Float(string=u'91/120', readonly=True)
    days_due_121togr = fields.Float(string=u'+121', readonly=True)
    invoice_ref = fields.Char(string='Reference', readonly=True)
    invoice_id = fields.Many2one('account.invoice', string='Invoice', readonly=True)
    comment = fields.Text(string='Notes', readonly=True)

    _order = 'partner_name'

    def init(self, cr):
        query = """
                SELECT * from (
                SELECT l.id as id, 
		    l.partner_id, res_partner.name as "partner_name", 
		    days_due as "avg_days_overdue",
		    l.date as "oldest_invoice_date",
                    l.debit-l.credit as "total",
                    CASE WHEN days_due BETWEEN 01 AND  30 THEN l.debit-l.credit ELSE 0 END  AS "days_due_01to30",
                    CASE WHEN days_due BETWEEN 31 AND  60 THEN l.debit-l.credit ELSE 0 END  AS "days_due_31to60",
                    CASE WHEN days_due BETWEEN 61 AND  90 THEN l.debit-l.credit ELSE 0 END  AS "days_due_61to90",
                    CASE WHEN days_due BETWEEN 91 AND 120 THEN l.debit-l.credit ELSE 0 END  AS "days_due_91to120",
                    CASE WHEN days_due >=121              THEN l.debit-l.credit ELSE 0 END  AS "days_due_121togr",
		    CASE when days_due < 0 THEN 0 ELSE days_due END as "max_days_overdue",
                    CASE when days_due <= 0 THEN l.debit-l.credit ELSE 0 END as "current",
                    l.ref as "invoice_ref",
                    ai.id as "invoice_id", ai.comment
                    
                    FROM account_move_line as l
                INNER JOIN
                  (
                   SELECT id, EXTRACT(DAY FROM (now() - (lt.date + INTERVAL '30 days'))) AS days_due
                   FROM account_move_line lt
                ) DaysDue
                ON DaysDue.id = l.id

                INNER JOIN account_account
                   ON account_account.id = l.account_id
                INNER JOIN res_company
                   ON account_account.company_id = res_company.id
                INNER JOIN account_move
                   ON account_move.id = l.move_id
                LEFT JOIN account_invoice as ai
                   ON ai.move_id = l.move_id
                INNER JOIN res_partner
                   ON res_partner.id = l.partner_id
                WHERE account_account.active
                  AND (account_account.type IN ('payable'))
                  AND (l.reconcile_id IS NULL)
                  AND (l.reconcile_partial_id IS NULL)
                  AND account_move.state = 'posted'
               
                ) sq
              """
            
        tools.drop_view_if_exists(cr, '%s' % (self._name.replace('.', '_')))
        cr.execute("""
                      CREATE OR REPLACE VIEW %s AS ( %s) 
        """ % (self._name.replace('.', '_'), query)) 

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: