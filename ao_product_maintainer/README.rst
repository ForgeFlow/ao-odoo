.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

==================
Product Maintainer
==================

This module overrides standard security and adds a new security group,
*Product maintainer*. Only members of this group can modify, create or delete
products and variants.

Involved models:
----------------

This module restrict the write, create and unlink actions for the following 
models:

* ``product.product``
* ``product.template``
* ``product.packaging``
* ``product.category``

Following involved models keep they access configuration unchanged:

* ``product.supplierinfo``
* ``product.uom.categ``
* ``product.uom``
* ``product.supplierinfo``
* ``product.pricelist``
* ``product.pricelist.item``
* ``product.price.history``
* ``product.attribute*``

Credits
=======

Contributors
------------

* Jordi Ballester <jordi.ballester@eficent.com>
* Lois Rilo <lois.rilo@eficent.com>
