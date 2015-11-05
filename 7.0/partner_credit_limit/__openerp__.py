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
{
    'name':'Partner Credit Limit',
    'version':'1.7',
    'depends':["base","account","sale"],
    "author" : "Tiny / Ursa",
    "summary": 'Enforce Customer Credit Limit',
    "description": """
Prevents users from confirming sales orders that would put Customers above their Credit Limit
based on open Invoices.  Adds a new group that allows certain users to relax the credit limit
and approve orders or also permanently stop checking the credit limit for all future orders.

OpenERP Version: 7.0 Ursa Dev Team: RC
Contact: contact@ursainfosystems.com

 """,
    'maintainer': 'Ursa Information Systems',
    'website': 'http://www.openerp.com; http://www.ursinfosystems.com',
    'category': "Sales",
    'data': [
        'security/credit_limit.xml',
        'partner_view.xml',
        'sale_workflow.xml',
    ],
    'installable': True,
}
