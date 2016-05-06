# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
"""
Description
-----------
This script intends to be used to reclassify consumables that are
held with real-time inventory valuation to periodical.

Dependencies
------------
None

"""
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

# Identify consumable products that have real-time inventory valuation
args = [('type', '=', 'consu')]
product_ids = sock.execute(dbname, uid, pwd, 'product.template', 'search',
                           args)

sock.execute(dbname, uid, pwd, 'product.template', 'write',
             product_ids, {'valuation': 'real_time',
                           'type': 'product'})

print '%s Consumables reclassified to stockables with real time inventory ' \
      'valuation' % len(product_ids)

if product_ids:
    # Identify consumable products that have real-time inventory valuation
    args = [('type', '=', 'consu')]
    updated_product_ids = sock.execute(dbname, uid, pwd, 'product.template',
                                       'search', args)

    if updated_product_ids:
        raise Exception('Still consumables exist.')
    else:
        print 'All consumables reclassified successfully stockable with ' \
              'real time inventory valuation'
