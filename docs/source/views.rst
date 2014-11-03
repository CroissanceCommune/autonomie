Views
=====

Configuration
-------------

Views are imported statically, avoiding whole view module scanning.

.. code-block:: python

    def includeme(config):
        """
            Add auth related routes/views
        """
        config.add_route('login', '/login')
        config.add_view(forbidden_view,
                        context=HTTPForbidden,
                        permission=NO_PERMISSION_REQUIRED,
                        xhr=True,
                        renderer='json')

The BaseFormView object
-----------------------

The BaseFormView object allows easy configuration of form views.
It's based on pyramid_deform FormView and extends a little bit its
functionnalities.

