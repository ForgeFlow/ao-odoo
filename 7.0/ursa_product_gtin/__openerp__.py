# -*- coding: utf-8 -*-
{
	"name" : "Product GTIN EAN8 EAN13 UPC JPC Support",
	"version" : "1.2",
	"author" : ["ChriCar Beteiligungs- und Beratungs- GmbH","Ursa Information Systems"],
	"website" : ["http://www.chricar.at/ChriCar", "http://www.ursainfosystems.com"],
	"category" : "Generic Modules/Others",
	"depends" : ["product"],
	"description" : """Replaces the EAN13 code completion with a checkroutine for EAN13, EAN8, JPC, UPC and GTIN
    makes EAN visible in simplified view
    YOU MUST comment constraints in product/product.py manually 
    #_constraints = [(_check_ean_key, 'Error: Invalid ean code', ['ean13'])]
    or apply the patch  provided in
    https://bugs.launchpad.net/openobject-server/+bug/700451
    Verified with OpenERP 7.0, added additional functions for each type of code to restrict use of code in fields
    which will allow user to have multiple codes associated with the product.
    By default view adds EAN13 and UPC fields to product form
        """,
	"init_xml" : [],
	"demo_xml" : [],
	"update_xml" : ["ursa_product_gtin_view.xml"],
	"active": False,
	"installable": True
}
