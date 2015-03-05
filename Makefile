JS_TEMPLATE_MAIN_FILE=autonomie/static/js/template.js
JS_TEMPLATE_DEST=autonomie/static/js/templates
JS_TEMPLATES_SOURCE=handlebars
DIRECTORIES=$(shell cd $(JS_TEMPLATES_SOURCE) && find *  -maxdepth 1 -type d)

js:
	handlebars $(JS_TEMPLATES_SOURCE)/*.mustache  -f $(JS_TEMPLATE_MAIN_FILE)
	for dir in $(DIRECTORIES);do \
		handlebars $(JS_TEMPLATES_SOURCE)/$$dir/*.mustache -f $(JS_TEMPLATE_DEST)/$$dir.js; \
	done


dev_serve:
	pserve --reload development.ini
