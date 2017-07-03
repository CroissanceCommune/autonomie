Javascript code
===============

Js code is split in two way of coding :

1- Old way is directly coding js files using fanstatic to handle dependencies and import libs in the appropriate order
2- New way is using webpack to build js files written in es2015 syntax

Old way
-------

Old style coded js files can be found in autononmie/static/js/.
Downloaded libs are in the vendors directory.
Tests are stored in the tests directory.
Templates built with handlebars are stored in the templates directory.

Other libs used in the 'old fashioned' js stuff are installed through pip (see js.* packages in the requirements.txt file).

Templates
..........

Build templates with the following command ::

    make js


New way
-------

'New fashionned' js stuff sources are stored in the js_sources/src directory.
They are compiled through webpack.

Their built version can be found in autononmie/static/js/build/.

Build the dev js files (and wait for changes)::

    make devjs

Build the prod js files ::

    make prodjs


Libraries
----------

autonomie's js code mostly rely on :

* Backbone (http://backbonejs.org/)
* Marionette (http://marionettejs.com)
* Backbone.Validation (http://thedersen.com/projects/backbone-validation/)
* Jquery
* JqueryUi.datepicker
