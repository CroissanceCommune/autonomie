Compiling my templates with handlebars.js
=========================================

Handlebars.js is a javascript templating engine. It allows server-side template compilation.
Since we don't use nodejs as webserver, we need to precompile our templates.

For that, we need :

* Install nodejs : https://github.com/joyent/node/wiki/Installing-Node.js-via-package-manager
* npm install handlebars
* make js

Add your template in the handlebars directory. all the templates in this folder
are compiled to the same js file : template.js.
Maybe it should be splitted in several files one day.

It can be imported this way:

.. code-block:: python

    from autonomie.resources import templates

    def myview(request):
        templates.need()

Fanstatic will handle the import (and the requirements) for you.
Most of the time, the templates requirement is done through the declaration of a
new js ressource.
