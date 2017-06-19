.. image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL-3

======================================
AO-specific customizations on purchase
======================================

This module contains customizations specific to Aleph Objects.

* Add a menu entry 'Product Variant' to the 'Purchases' menu.
* Adds a button to the purchase variants to purchases
* Purchase form shows name of the warehouse partner, not warehouse name
* Request for quotations can only be printed if they are not in state *To
  Approve*.
* Purchase Orders cannot be printed if they are not Approved.
* Add a *Unread Messages* filter to bypass a
  `bug <https://github.com/odoo/odoo/issues/16763>`_ with *New Mail* filter of
  odoo standard. (**removed - fixed in upstream**).

Credits
=======

Contributors
------------

* Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
