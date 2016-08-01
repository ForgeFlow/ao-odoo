import os
import csv
import xmlrpclib
import time
#import paramiko
import re
import ftplib
import oerphelper
import logging
import array
import string
import sys
from datetime import datetime, timedelta, date
from random import randint


# FILE PATHS

# OERP Constants
USERNAME = 'fedexapi'
PWD = 'fedexapi'
DBNAME = 'ao_1213'
ERP_WWW = 'http://develerp.alephobjects.com:8069'

def connect_oerp():
    '''
    Function that will make a connection to OpenERP using XML-RPC.
    @return1: socket that is connected to OpenERP
    @return2: An id that shows that you have been validated
    '''	
    sock = xmlrpclib.ServerProxy(ERP_WWW +'/xmlrpc/object', allow_none=True) 
    sock_common = xmlrpclib.ServerProxy(ERP_WWW + '/xmlrpc/common')
    uid = sock_common.login(DBNAME, USERNAME, PWD)

    print "INFO: ***** SUCCESS - SERVER HAS AUTHENTICATED A LOGIN *****"

    print sock, uid
    return sock, uid

def search_outgoing(sock, uid, do_names):

    ids = sock.execute(DBNAME, uid, PWD, 'stock.picking.out', 'search', do_names)

    try:
        os_ids = ids
    except Exception:
        "There are no outgoing shipments to process"
        pass
    return os_ids

def fedex_get_deliveries(sock, uid, ids):

    result = sock.execute(DBNAME, uid, PWD, 'stock.picking.out', 'fedex_get', ids)
    
    try:
        os_ids = ids
    except Exception:
        "There are no outgoing shipments to process"
        pass
    return result

def fedex_put_tracking_nums(sock, uid, delivery_ids, tracking, desc):

    tracking_num = {
    'tracking': tracking,
    'desc': desc,
    }
    try:
        sock.execute(DBNAME, uid, PWD, 'tracking.numbers', 'write', delivery_ids, tracking_num)

    except Exception:
        "cannot update these records"
        pass

def main():
    #Connect to OpenERP
    sock, uid = connect_oerp()
    #do_names = [('name', '=', 'OUT/06919')] 
    #do_ids = search_outgoing(sock, uid, do_names)
    #print do_ids
    result = fedex_get_deliveries(sock, uid, 'OUT/06919')
    print result


            
if __name__ == '__main__':
    print 'Starting'
    main()
    print 'Done'
