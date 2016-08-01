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


with open('transform_files/product.stockable.latest.price.csv') \
        as extracted_csv:
    reader = csv.DictReader(extracted_csv)

    for row in reader:
        product_template_data = {
            'id': int(row['product_tmpl_id']),
            'standard_price': row['standard_price'],
            'cost_method': 'real',
            'valuation': 'real_time'
        }
        sock.execute(dbname, uid, pwd, 'product.template', 'write',
                     [int(row['product_tmpl_id'])], product_template_data)
        print 'Product [%s] %s cost updated to %s' %(row['default_code'],
                                                     row['name'],
                                                     row['standard_price'])

    extracted_csv.close()

