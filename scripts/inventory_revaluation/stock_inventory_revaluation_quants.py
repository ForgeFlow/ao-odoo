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


# Inventory valuation account
prod = {}
prod_int = {}
args = [('code', '=', '59200')]
account_ids = sock.execute(dbname, uid, pwd, 'account.account', 'search', args)
if not account_ids:
    raise Exception('No Inventory valuation account found with code 59200')

account_id = account_ids[0]

# Internal locations
args = [('usage', '=', 'internal')]
location_ids = sock.execute(dbname, uid, pwd, 'stock.location', 'search', args)

# Quants in internal locations
args = [('location_id', 'in', location_ids)]
quant_ids = sock.execute(dbname, uid, pwd, 'stock.quant', 'search', args)
quants_data = sock.execute(dbname, uid, pwd, 'stock.quant', 'read',
                           quant_ids, ['product_id'])

product_quants = {}
for quant in quants_data:
    product_id = quant['product_id'][0]
    if product_id not in product_quants.keys():
        product_quants[product_id] = []
    product_quants[product_id].append(quant['id'])

with open('transform_files/product.stockable.latest.price.csv') \
        as extracted_csv:
    reader = csv.DictReader(extracted_csv)

    for row in reader:
        product_id = int(row['product_id'])
        if not product_id in product_quants.keys():
            continue
        sir_data = {
            'journal_id': False,
            'revaluation_type': 'price_change',
            'decrease_account_id': account_id,
            'increase_account_id': account_id,
            'product_template_id': int(row['product_tmpl_id'])
        }
        sir_id = sock.execute(dbname, uid, pwd,
                                   'stock.inventory.revaluation',
                                   'create', sir_data)
        print 'Revaluation %s' % sir_id

        for quant_id in product_quants[product_id]:
            reval_quant_data = {
                'revaluation_id': sir_id,
                'quant_id': quant_id,
                'new_cost': row['standard_price']
            }
            sir_reval_quant_id = sock.execute(
                dbname, uid, pwd, 'stock.inventory.revaluation.quant',
                'create', reval_quant_data)
            print 'Revaluation %s - Quant %s' % (sir_id, sir_reval_quant_id)
        
    extracted_csv.close()

