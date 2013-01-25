Compiling my templates with hogan.js
====================================

Hogan.js is a javascript templating engine. It allows server-side template compilation.
Since we don't use nodejs as webserver, we need to precompile our templates.

For that, you need :

* Install nodejs : https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager
* npm install hogan.js
* find the hogan/<version>/bin/hulk command
* hulk autonomie/hogan/\*.mustache > autonomie/static/js/templates/template.js

template.js is the js librarie containing all the templates, maybe it should be
splitted one day. It can be imported this way:

.. code-block:: python

    from autonomie.resources import hogan_template

    def myview(request):
        hogan_template.need()

Fanstatic will handle the import (and the requirements) for you.
