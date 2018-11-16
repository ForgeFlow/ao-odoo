.. image:: https://img.shields.io/badge/license-AGPLv3-blue.svg
   :target: https://www.gnu.org/licenses/agpl.html
   :alt: License: AGPL-3

===================================
MRP Production Update Product Price
===================================

This module updates the standard price (unit cost) field of the finished
product, considering the cost in the stock move resulting from production.

When a manufacturing order is processed, and a quantity of a finished
product is produced, if the finished product is managed under average price
costing method the field 'standard price' of the product template is updated
considering the cost that was associated to the stock move that is
associated to the production.

Other modules may be needed in order to allocate the cost of the finished
product to the stock move. For example, module
'MRP Production Calculate Cost Finished Product' will calculate the unit
cost of the finished product, based on the cost of the raw materials planned
in the manufacturing order.


Usage
=====

.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/129/8.0

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/Eficent/ao-odoo/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smash it by providing detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Eficent Business and IT Consulting Services S.L. <contact@eficent.com>


Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: http://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit http://odoo-community.org.
