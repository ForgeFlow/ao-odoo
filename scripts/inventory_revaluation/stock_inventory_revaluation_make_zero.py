# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>

import csv
import xmlrpclib

username = raw_input("User name: ")
pwd = raw_input("Password: ")
dbname = raw_input("Database name: ")
server_url = raw_input("Server URL: ")

server_xmlrpc_common = '%s/xmlrpc/common' % server_url
server_xmlrpc_object = '%s/xmlrpc/object' % server_url

# Get the uid
sock_common = xmlrpclib.ServerProxy(server_xmlrpc_common)

uid = sock_common.login(dbname, username, pwd)

# replace localhost with the address of the server
sock = xmlrpclib.ServerProxy(server_xmlrpc_object)

# Journal
args = [('name', '=', 'General Journal')]
journal_ids = sock.execute(dbname, uid, pwd, 'account.journal', 'search', args)
if not journal_ids:
    raise Exception('No Journal found with name General Journal')
journal_id = journal_ids[0]

# Inventory valuation account
prod = {}
prod_int = {}
args = [('code', '=', '59200')]
account_ids = sock.execute(dbname, uid, pwd, 'account.account', 'search', args)
if not account_ids:
    raise Exception('No Inventory valuation account found with code 59200')

account_id = account_ids[0]

with open('transform_files/product.stockable.latest.price.csv') \
        as extracted_csv:
    reader = csv.DictReader(extracted_csv)

    sir_lines = []

    for row in reader:
        sir_data = {
            'journal_id': journal_id,
            'revaluation_type': 'price_change',
            'decrease_account_id': account_id,
            'increase_account_id': account_id,
            'new_cost': 0.0,
            'product_template_id': int(row['product_tmpl_id']),
        }
        sir_line_id = sock.execute(dbname, uid, pwd,
                                   'stock.inventory.revaluation',
                                   'create', sir_data)
        print sir_line_id

    extracted_csv.close()

