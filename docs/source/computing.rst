Notes on computing
==================

Amounts compilation
--------------------

There are some errors in the way datas are computed :

    When we compute the amount of intermediary invoices, we generate HT lines.
    Those HT lines are substracted in the sold invoice.
    The problem is that tvas are rounded after suming them.
    In the intermediary invoice the tvas are not summed with others but they are
    in the sold one, so the results may be a bit different (a few cents).

See the tests for more information (look for skipped tests).

