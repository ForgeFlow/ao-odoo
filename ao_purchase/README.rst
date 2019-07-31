.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

======================================
AO-specific customizations on purchase
======================================

This module contains customizations specific to Aleph Objects.

* Adds a button to the purchase variants to purchases. (out-of-the-box in v12)
* Always show the *Source Document*, even if empty.
* Purchase form shows name of the warehouse partner, not warehouse name
* Request for quotations can only be printed if they are not in state *To
  Approve*.
* Purchase Orders cannot be printed if they are not Approved.
* Add a *Unread Messages* filter to bypass a
  `bug <https://github.com/odoo/odoo/issues/16763>`_ with *New Mail* filter of
  odoo standard. (**removed - fixed in upstream**).
* Purchase Product Usage custom workflow:
    * Usage is required if Product is Consumible or a Service

Credits
=======

Contributors
------------

* Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
