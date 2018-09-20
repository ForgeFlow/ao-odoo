.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=====================================
AO MRP Flattened BOM Cost Report XLSX
=====================================

This module extends the functionality of the MRP capabilities of Odoo,
and allows you to export the flattened BOM Cost to MS Excel .XLSX format.

A list of the sum of lowest levels will be shown for every
BoM you export using this method. Plus, the unit cost and total cost for
every component will be shown.

It also maintains units correctly across all nested BOM's and take units
that have been defined in product Unit of Measure field.

Usage
=====

To use this module, you need to:

#. Go to 'Manufacturing / Products / Bill of Materials'
#. Select a BOM or more
#. Go to 'Action / Export Flattened BOM Cost Excel'.

Credits
=======

Contributors
------------

* Héctor Villarreal <hector.villarreal@eficent.com>
* Lois Rilo <lois.rilo@eficent.com>
