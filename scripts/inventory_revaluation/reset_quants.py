# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
"""
Description
-----------
This script resets the cost of the internal quants to 0

Dependencies
------------
None

"""

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

# Internal locations
args = [('usage', '=', 'internal')]
location_ids = sock.execute(dbname, uid, pwd, 'stock.location', 'search', args)

# Quants in internal locations
args = [('location_id', 'in', location_ids)]
quant_ids = sock.execute(dbname, uid, pwd, 'stock.quant', 'search', args)

sock.execute(dbname, uid, pwd, 'stock.quant', 'write',
             quant_ids, {'cost': 0.0})

