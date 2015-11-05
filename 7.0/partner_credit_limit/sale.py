#!/usr/bin/env python
#-*- coding:utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution    
#    Copyright (C) 2004-2009 Tiny SPRL (<http://tiny.be>). All Rights Reserved
#    d$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import time
import netsvc
from osv import fields, osv
from mx import DateTime
from tools import config
from tools.translate import _
import logging

class sale_order(osv.osv):
    _inherit = "sale.order"

    def check_limit(self, cr, uid, ids, context={}):
        so = self.browse(cr, uid, ids[0], context)
        partner = so.partner_invoice_id
        user = self.pool.get('res.users').browse(cr, uid, uid)
        order_ids = self.search(cr, uid, [('partner_invoice_id','=',partner.id),('state','in',['progress','manual','invoice_except'])], context=None)
        orders = self.browse(cr, uid, order_ids, context)

        existing_order_balance = 0.0
        for order in orders:
            existing_order_balance = existing_order_balance + order.amount_total

        #don't perform credit check if sales order payment term doesn't exist or credit card.  this means SO will be paid prior to shipping
        if not so.payment_term or so.payment_term.name == 'Immediate Payment':
            return True

        if (partner.credit + existing_order_balance + so.amount_total) > partner.credit_limit:
            allowed = False
            for group in user.groups_id:
                if group.name == 'Relax Customer Credit Limit':
                    allowed = True
            if partner.enforce_credit and not allowed:
                msg = "This Customer has a balance due of $%0.2f and existing orders for $%0.2f.\n\n They have a Credit Limit of $%0.2f !\n\nPlease SAVE this order and contact Accounting.\n\n Change Payment Term to Immediate Payment to process the order." % (partner.credit, existing_order_balance, partner.credit_limit)
                raise osv.except_osv(_('Cannot confirm this sales order!'), _(msg))
                return False
            else:
                #self.pool.get('res.partner').write(cr, uid, [partner.id], {'credit_limit':credit - debit + so.amount_total})
                return True
        else:
            return True
sale_order()