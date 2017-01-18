.. image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL-3

=================
URSA Product GTIN
=================
This module contains customizations specific to Aleph Objects.

Replaces the EAN13 code completion with a checkroutine for EAN13, EAN8, JPC,
 UPC and GTIN makes EAN visible in simplified view YOU MUST comment
 constraints in product/product.py manually

#_constraints = [(_check_ean_key, 'Error: Invalid ean code', ['ean13'])] or
apply the patch  provided in https://bugs.launchpad
.net/openobject-server/+bug/700451

Verified with OpenERP 7.0, added additional functions for each type of code
to restrict use of code in fields which will allow user to have multiple
codes associated with the product.
By default view adds EAN13 and UPC fields to product form

Credits
=======

Contributors
------------

* URSA
