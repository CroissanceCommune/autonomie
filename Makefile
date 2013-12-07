JS_TEMPLATE_FILE=autonomie/static/js/template.js
JS_TEMPLATE_SOURCES=$(wildcard handlebars/*.mustache)

js:
	handlebars $(JS_TEMPLATE_SOURCES) -f $(JS_TEMPLATE_FILE)

dev_serve:
	pserve --reload development.ini
