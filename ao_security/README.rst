.. image:: https://img.shields.io/badge/license-AGPL--3-blue.png
   :target: https://www.gnu.org/licenses/agpl
   :alt: License: AGPL-3

=======================================
AO-specific customizations for Security
=======================================

This module contains customizations specific to Aleph Objects.

* Add UoM Maintainer group which will be the only one with CRUD permissions to UoM and UoM Category
* Add Stock Maintainer group which will be the only one with CRUD permission to Warehouse, Location, Location route, Procurement rule and Picking Type
* Add BoM Maintainer group which will be the only one with CRUD permissions to BoM and BoM Lines

All other groups have been left with only Reading capabilities to the previous models

Credits
=======

Contributors
------------

* Adria Gil Sorribes <adria.gil@eficent.com>
