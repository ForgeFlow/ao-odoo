# -*- coding: utf-8 -*-
##############################################################################
#
#
##############################################################################


{
    "name" : "Sale Margin Percent",
    "version" : "1.0",
    "author" : "Paul Thiry, Balaji Kannan",
    'category': 'Sales Management',
    "depends" : ["sale_margin"],
    "init_xml" : [],
    "demo_xml" : [],
    "description": """
        
        Margin Percent Calculation = 1 - Cost / Price
        
        Adds the margin as a percentage to the Sales Order Line. 
                
        Adds margin percent to the sale order.
    """,
    'update_xml': [
        "ursa_sale_margin_percent_view.xml",
    ],
    'test': [],
    'installable': True,
    'auto_install': False,
    'images': [],
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
