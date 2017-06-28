JS_SOURCES_DIR=js_sources/
JS_TEMPLATE_MAIN_FILE=autonomie/static/js/template.js
JS_TEMPLATE_DEST=autonomie/static/js/templates
JS_TEMPLATES_SOURCE=$(JS_SOURCES_DIR)src/handlebars
DIRECTORIES=$(shell cd $(JS_TEMPLATES_SOURCE) && find *  -maxdepth 1 -type d)

SASSC=$(shell which sassc)
CSS_SOURCES=css_sources/main.scss
CSS_DEST=autonomie/static/css/main.css

# Used to build templates used in inline javascript stuff (not webpacked)
js:
	handlebars $(JS_TEMPLATES_SOURCE)/*.mustache  -f $(JS_TEMPLATE_MAIN_FILE)
	for dir in $(DIRECTORIES);do \
		handlebars $(JS_TEMPLATES_SOURCE)/$$dir/*.mustache -f $(JS_TEMPLATE_DEST)/$$dir.js; \
	done

# build js with webpack
prodjs:
	cd $(JS_SOURCES_DIR) && npm run prod

devjs:
	cd $(JS_SOURCES_DIR) && npm run dev

# build css with libsassc
css:
	$(SASSC) $(CSS_SOURCES) $(CSS_DEST)
	

dev_serve:
	pserve --reload development.ini
