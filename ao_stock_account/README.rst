.. image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL-3

===========================================
AO-specific customizations on stock account
===========================================

This module contains customizations specific to Aleph Objects:

* Introduce the field *Last moved date* in product to help finding obsolete
  ones.
* Add a Quant view that computes the standard cost valuation. Note here that:

  - It does not support multicompany environments.
  - It only works with standard cost valuation.
  - It is not the biggest source of truth. Real valuation looks at accounting.
    This view only aims to help management in a standard cost strategy.

* When reversing a transfer, set the field 'to refund' to true by
  default (#20925)

Credits
=======

Contributors
------------

* Eficent Business and IT Consulting Services S.L. <contact@eficent.com>
