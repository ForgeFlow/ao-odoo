This module includes the concept of Labor and Overhead costs to the Bill of Materials in the
manufacture context.

Under the BOM scope the module adds the following fields:
* Total cost: Total cost of the manufactured product
* Materials cost: Aggregate cost taking into account child bom's labor and overhead costs
* Only materials cost: Aggregate cost taking into account only the cost of the materials
* Total labor cost: Aggregate cost of all labor costs inside the bom
* Labor cost: Cost of the labor at the top bom level
* Total overhead cost: Aggregate cost of all overhead costs inside the bom
* Overhead cost: Cost of the overhead at the top bom level
* BoM Costs: Used to define the labor and overhead costs associated to the BoM

Under the product category scope the module adds the following fields:
* Labor account id: Account for the labor products
* Overhead account id: Account for the overhead products

The module also includes two additional features:
* When a manufacture order is created and a production is done, account move lines will be created for the labor and overhead products defined in the BoM specified in the MO.
* When an unbuild order is created and unbuild is performed, account move lines will be created to revert the ones that had been created when the product was manufactured in the first place.
