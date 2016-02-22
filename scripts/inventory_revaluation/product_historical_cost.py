# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
"""
Description
-----------
This script builds a file that contains the list of stockable products,
updated with the latest purchase price. The resulting file is then
used by other scripts to revaluate the inventory and update the product data.

Dependencies
------------
None

"""

import csv
import xmlrpclib
import unicodedata
# Query to be run on the server, to produce the file
q = """Copy(SELECT DISTINCT ON (ail.product_id)
ai.number as invoice_number, ai.date_invoice as invoice_date,
ail.product_id, pr.default_code, pt.name as product_name, ail.quantity,
ail.uos_id, uom.name as invoice_uom_name, ail.price_unit, pr_uom.name as product_uom_name
FROM account_invoice_line AS ail
INNER JOIN account_invoice AS ai
ON ail.invoice_id = ai.id
INNER JOIN product_product AS pr
ON ail.product_id = pr.id
INNER JOIN product_template AS pt
ON pr.product_tmpl_id = pt.id
INNER JOIN product_uom AS uom
ON ail.uos_id = uom.id
INNER JOIN product_uom as pr_uom
ON pt.uom_id = pr_uom.id
WHERE ai.state in ('open', 'paid')
AND ai.type = 'in_invoice'
AND pt.type = 'product'
AND ail.quantity > 0
ORDER BY ail.product_id, ai.date_invoice DESC) To '/tmp/products_historical_prices.csv' With CSV HEADER FORCE QUOTE *;
"""

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


# Loaded products
prod = {}
prod_int = {}
args = [('type', '=', 'product')]
product_ids = sock.execute(dbname, uid, pwd, 'product.product', 'search', args)

args = [('model', '=', 'product.product'), ('res_id', 'in',
                                            tuple(product_ids))]
external_ident_ids = sock.execute(dbname, uid, pwd, 'ir.model.data', 'search',
                                  args)
external_ident_data = sock.execute(dbname, uid, pwd, 'ir.model.data', 'read',
                                   external_ident_ids,
                                   ['res_id', 'complete_name'])
ext_ident = {}
for od in external_ident_data:
    ext_ident[od['res_id']] = od['complete_name']

# Read products
args = [('type', '=', 'product')]
odoo_ids = sock.execute(dbname, uid, pwd, 'product.product', 'search', args)
odoo_data = sock.execute(dbname, uid, pwd, 'product.product', 'read',
                         odoo_ids, ['qty_available', 'default_code', 'name',
                                    'standard_price', 'type', 'uom_id',
                                    'product_tmpl_id'])
product_data = {}
for od in odoo_data:
    if type(od['name']) == unicode:
        name = unicodedata.normalize('NFKD', od['name']).encode('ascii',
                                                                'ignore')
    else:
        name = od['name']
    product_data[str(od['id'])] = {
        'qty_available': od['qty_available'],
        'default_code': od['default_code'],
        'name': name,
        'standard_price': od['standard_price'],
        'type': od['type'],
        'uom': od['uom_id'][1],
        'product_tmpl_id': od['product_tmpl_id'][0]
    }


err_list = []
err_log_list = []

uom = {}
with open('extract_files/product.uom.csv') \
        as extracted_csv:
    reader = csv.DictReader(extracted_csv)
    for row in reader:
        uom[row['name']] = {
            'uom_type': row['uom_type'],
            'factor': row['factor'],
            'category_id': row['category_id/id']
        }
    extracted_csv.close()

with open('extract_files/products_historical_prices.csv') \
        as extracted_csv:
    reader = csv.DictReader(extracted_csv)
    i = 1
    product_val = {}
    product_qty = {}
    product_name = {}
    for row in reader:
        err_log = {}
        err_log['row'] = i
        i += 1

        # Check that the uom in the invoice and in the product belong to the
        #  same category
        inv_uom_cat_id = False
        prod_uom_cat_id = False
        if row['invoice_uom_name'] in uom.keys():
            inv_uom_cat_id = uom[row['invoice_uom_name']]['category_id']
        if row['product_uom_name'] in uom.keys():
            prod_uom_cat_id = uom[row['product_uom_name']]['category_id']
        if inv_uom_cat_id != prod_uom_cat_id:
            err_log['msg'] = "Invoice %s. UoM %s has different category in " \
                             "than the UoM %s of product %s." \
                             % (row['invoice_number'], row['invoice_uom_name'],
                                row['product_uom_name'], row['default_code'])
            err_log_list.append(err_log)
            err_list.append(row)
            print err_log
            continue

        # Convert qty to the reference UoM
        reference_qty = 0.0
        if row['invoice_uom_name'] in uom.keys():
            uom_type = uom[row['invoice_uom_name']]['uom_type']
            factor = float(uom[row['invoice_uom_name']]['factor'])
            if factor:
                reference_qty = float(row['quantity']) / factor
            else:
                reference_qty = float(row['quantity'])
        # Convert qty to the product UoM
        qty = 0.0
        if row['product_uom_name'] in uom.keys():
            uom_type = uom[row['product_uom_name']]['uom_type']
            factor = float(uom[row['product_uom_name']]['factor'])
            if factor:
                qty = reference_qty * factor
            else:
                qty = reference_qty

        product_qty[row['product_id']] = qty
        if qty <= 0.0:
            print qty

        try:
            product_val[row['product_id']] = float(row['quantity']) * \
                                              float(row['price_unit'])
        except TypeError as err:
            err_log['msg'] = "%s" \
                             % err.message
            print err_log
            continue

        if row['product_id'] not in product_name.keys():
            product_name[row['product_id']] = {
                'default_code': row['default_code'],
                'name': row['product_name'],
                'uom': row['product_uom_name']
        }

    extracted_csv.close()

product_avg = {}
out_list = []
for product_id in product_data.keys():
    out = {}
    out['qty_available'] = product_data[product_id]['qty_available']
    out['type'] = product_data[product_id]['type']
    out['product_id'] = product_id
    out['default_code'] = product_data[product_id]['default_code']
    out['name'] = product_data[product_id]['name']
    out['uom'] = product_data[product_id]['uom']
    out['id'] = ext_ident.get(product_id, False)
    out['product_tmpl_id'] = product_data[product_id]['product_tmpl_id']

    if product_id in product_val.keys():
        try:
            product_avg[product_id] = product_val[product_id] / product_qty[
                product_id]
        except ZeroDivisionError as err:
            err_log['msg'] = "Product [%s] %s has 0 quantity: %s" \
                             % (product_name[product_id]['default_code'],
                                product_name[product_id]['name'],
                                err.message)
            print err_log
            continue

    if product_id in product_avg.keys():
        out['standard_price'] = str('{:.6f}'.format(product_avg[product_id]))
        out['previous_standard_price'] = \
            product_data[product_id]['standard_price']
    else:
        out['standard_price'] = product_data[product_id]['standard_price']
        out['previous_standard_price'] = \
            product_data[product_id]['standard_price']
    if out['standard_price'] != out['previous_standard_price']:
        out['price_change'] = 'True'
    else:
        out['price_change'] = 'False'

    out_list.append(out)

if out_list:
    with open('transform_files/product.stockable.latest.price.csv', 'w') \
            as output_csv:

        fieldnames = out_list[0].keys()
        writer = csv.DictWriter(output_csv,
                                quoting=csv.QUOTE_ALL, doublequote=True,
                                delimiter=',', fieldnames=fieldnames)
        writer.writeheader()
        for output in out_list:
            try:
                writer.writerow(output)
            except UnicodeEncodeError as err:
                err_log['msg'] = "Decide error with %s." \
                                 % output
                print output
        output_csv.close()
