# -*- coding: utf-8 -*-
# © 2015 Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
"""
Description
-----------
This script sets the company in property fields where it's not set. This is
required in order to be able to reclassify consumables.

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

# Identify company
args = []
company_ids = sock.execute(dbname, uid, pwd, 'res.company', 'search',
                           args)
if not company_ids:
    raise Exception('No active company was found')

company_id = company_ids[0]

# Identify consumable products that have real-time inventory valuation
args = [('company_id', '=', False)]
ir_property_ids = sock.execute(dbname, uid, pwd, 'ir.property', 'search',
                               args)

sock.execute(dbname, uid, pwd, 'ir.property', 'write',
             ir_property_ids, {'company_id': company_id})

print '%s ir.property records updated' % len(ir_property_ids)
