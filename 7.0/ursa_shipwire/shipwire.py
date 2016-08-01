#!/usr/bin/python

import httplib
import xmltodict
import logging
_logger = logging.getLogger(__name__)

from xml.dom.minidom import parse, parseString
target = "api.shipwire.com"
url = "/exec/InventoryServices.php"

# Sample XML Request for Real-time Inventory for all warehouses
#xml_request = """<?xml version="1.0" ?>
#<InventoryUpdate>
# <Username>apiuser</Username>
# <Password>password</Password>
# <Server>Production</Server>
# <Warehouse></Warehouse>
# <ProductCode></ProductCode>
# <IncludeEmpty/>
#</InventoryUpdate>
#"""

# function to get xml response for the request (for each location)
def get_shipwire_data(xml_request):

    # initialize return dictionary
    dic_xml = {}
    
    ''' sends xml request to url with parameter request '''
    webservice = httplib.HTTPS(target)
    webservice.putrequest("POST", url)
    webservice.putheader("Host", target)
    webservice.putheader("User-Agent", "Python post")
    webservice.putheader("Content-type", "text/xml; charset=\"UTF-8\"")
    webservice.putheader("Content-length", "%d" % len(xml_request))
    webservice.endheaders()
    webservice.send(xml_request)
    statuscode, statusmessage, header = webservice.getreply()
    result = webservice.getfile().read()
    
    # success
    if statuscode == 200:

        _logger.debug("API Response", result) 
        
        # parse result to dictionary for return
        dic_xml = xmltodict.parse(result)

    # failure
    else:
        _logger.debug("Error API Response", (statuscode, statusmessage, result))
    
    # return to caller
    return dic_xml, statuscode, statusmessage, header    

# main function to process     
def process(location, product, server, username, passw):
    
    # construct xml request
    xml_req="<?xml version=\"1.0\" ?><InventoryUpdate><Username>%s</Username><Password>%s</Password><Server>%s</Server><Warehouse>%s</Warehouse><ProductCode>%s</ProductCode></InventoryUpdate>" %(username, passw, server, location,product)
    
    #initialize
    proddict={}
    statuscode=200
    statusmessage="Success"
    header=""
    
    # get data through Shipwire API
    (locd, statuscode, statusmessage, header) = get_shipwire_data(xml_req)
    
    # if no error
    if statuscode == 200:
        
        # status, product, total product, processing time list
        locvlist = locd.values()
        
        # dictionary subset
        fieldd = locvlist[0]
        
        #get status
        status = fieldd.values()[0]
        
        # initialize counter
        counter = 0

        # No error in response
        if status <> 'Error':
            
            n = -1
            
            # walk through the keys
            for key in fieldd.keys():
            
                n = n + 1
                
                # if we are on product key
                if key == "Product":
                
                    # get values corresponding to key:Product
                    prodlist = fieldd.values()[n]
        
                    # more than one product returned
                    if type(prodlist).__name__=="list":
            
                        # for each product dictionary
                        for pd in prodlist:
            
                            # get values for each product
                            code = pd['@code']
                            qty=pd['@quantity']
                            
                            proddict[code] = qty
                            
                            counter = counter + 1
                
                            _logger.debug("Product: ",  (counter, '. ', code,':', qty))
                    
                    # only one product returned
                    else:
                        code=prodlist['@code']
                        qty=prodlist['@quantity']
                        
                        proddict[code] = qty
                        
                        counter = counter + 1
                
                        _logger.debug("Product: ",  (counter, '. ', code,':', qty))
                
            _logger.debug("Success. No. of Products Imported :",  counter)
        
        # error in response
        else:
            _logger.debug("API Response Error: ",fieldd.values()[1])
        
    # failure    
    else:
        _logger.debug("API Response Error:", (statuscode, statusmessage, header))
    
    return (statuscode, proddict)

if __name__ == "__process__":
    process()