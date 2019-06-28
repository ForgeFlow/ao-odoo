.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

===================================
AO-specific customizations on stock
===================================

This module contains customizations specific to Aleph Objects.

* Pickings should show both the source and destination location zones
* Display picking creation date in picking list
* Show *Date* in stock moves to everyone.
* Show inventory location for stock inventories that exclude sublocations
  (this will show a location in zero-confirmations).
* Print the *Qty Available in Source* in the operations of stock pickings.
* New group *Modify Warehouses and Locations*. Only people in this group is
  able to modify the Warehouse and Location configuration.
* New report *Inventory (Blank Quantity)* which do not print the qty in each
  line so it could be filled up by pencil.
* Delivery Slip report sorted by source location.
* Able to access picking from stock move form view.
* Change generic PG/XXXXX for route name on origin due to module
  procurement_auto_create_group
* Report 'Inventory / Inventory by Location' should be allowed to Stock/User.
  (https://projects.alephobjects.com/projects/odoo-trouble-tickets/
  work_packages/21577)
* Kanbans related to Stock Requests should use a Letter format.
  (https://projects.alephobjects.com/projects/odoo-trouble-tickets/
  work_packages/21747)

Credits
=======

Contributors
------------

* Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
