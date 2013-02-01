Notes on computing
==================

Accounts
-------

There are some errors in the way datas are computed :

    When we compute the amount of intermediary invoices, we generate HT lines.
    Those HT lines are substracted in the sold invoice.
    The problem is that tvas are rounded after suming them.
    In the intermediary invoice the tvas are not summed with others but they are
    in the sold one, so the results may be a bit different (a few cents).

Epsilons
--------

When computing, sometimes numbers aren't very precise like 1.999999999 in place
of 2.0.

In Python, we floor numbers with int that handles that special case.
In Javascript the math.floor function doesn't handle this case.
The solution :

.. code-block:: javascript

    var passed_to_cents = price * 100;
    var epsilon = Math.round(passed_to_cents) - passed_to_cents;
    if (epsilon < 0.000001){
      passed_to_cents = Math.round(passed_to_cents);
    }else{
      passed_to_cents = Math.floor(passed_to_cents);
    }

