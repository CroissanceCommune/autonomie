Notes on computing
==================

Accounts
-------

There are some errors in the way datas are computed :

    * When you use manualDeliverables TVA is added to the intermediate
      payments misleading to differences beetween estimation and generated
      invoices
    * If there are multiple tvas in the document, the first retrieved one is
      used for intermediate invoice generation (may lead to tva errors)
