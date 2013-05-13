JS_TEMPLATE_FILE=autonomie/static/js/template.js
JS_TEMPLATE_SOURCES=$(wildcard hogan/*.mustache)

js:
	hulk $(JS_TEMPLATE_SOURCES) > $(JS_TEMPLATE_FILE)

dev_serve:
	pserve --reload development.ini
