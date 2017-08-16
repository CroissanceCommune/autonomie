webpackJsonp([1],[
/* 0 */
/*!********************************!*\
  !*** ./src/expense/expense.js ***!
  \********************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	var _jquery = __webpack_require__(/*! jquery */ 2);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _bootstrap = __webpack_require__(/*! bootstrap */ 4);
	
	var _bootstrap2 = _interopRequireDefault(_bootstrap);
	
	__webpack_require__(/*! jstree */ 16);
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _App = __webpack_require__(/*! ./components/App.js */ 20);
	
	var _App2 = _interopRequireDefault(_App);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	var _backboneTools = __webpack_require__(/*! ../backbone-tools.js */ 22);
	
	var _Router = __webpack_require__(/*! ./components/Router.js */ 23);
	
	var _Router2 = _interopRequireDefault(_Router);
	
	var _Controller = __webpack_require__(/*! ./components/Controller.js */ 24);
	
	var _Controller2 = _interopRequireDefault(_Controller);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 46);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	(0, _tools.setupAjaxCallbacks)(); /*
	                                   * File Name : expense.js
	                                   *
	                                   * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                   * Company : Majerti ( http://www.majerti.fr )
	                                   *
	                                   * This software is distributed under GPLV3
	                                   * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                   *
	                                   */
	
	
	_App2.default.on('start', function (app, options) {
	    console.log("  => Starting the expense app");
	    AppOption['form_config'] = options.form_config;
	    (0, _backboneTools.setupBbValidationCallbacks)(_backboneValidation2.default.callbacks);
	    (0, _backboneTools.setupBbValidationPatterns)(_backboneValidation2.default);
	    var controller = new _Controller2.default(options);
	    var router = new _Router2.default({ controller: controller });
	    _backbone2.default.history.start();
	    (0, _tools.hideLoader)();
	});
	
	(0, _jquery2.default)(function () {
	    (0, _tools.showLoader)();
	    console.log("# Retrieving datas from the server");
	    console.log(AppOption['form_config_url']);
	    var serverCall1 = (0, _tools.ajax_call)(AppOption['form_config_url']);
	    console.log(AppOption['context_url']);
	    var serverCall2 = (0, _tools.ajax_call)(AppOption['context_url']);
	
	    _jquery2.default.when(serverCall1, serverCall2).done(function (result1, result2) {
	        console.log("  => Datas retrieved");
	        _App2.default.start({
	            form_config: result1[0],
	            form_datas: result2[0]
	        });
	    });
	});

/***/ }),
/* 1 */,
/* 2 */,
/* 3 */,
/* 4 */,
/* 5 */,
/* 6 */,
/* 7 */,
/* 8 */,
/* 9 */,
/* 10 */,
/* 11 */,
/* 12 */,
/* 13 */,
/* 14 */,
/* 15 */,
/* 16 */,
/* 17 */,
/* 18 */,
/* 19 */,
/* 20 */
/*!***************************************!*\
  !*** ./src/expense/components/App.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var AppClass = _backbone2.default.Application.extend({
	  region: '#js-main-area'
	}); /*
	     * File Name : App.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	
	var App = new AppClass();
	exports.default = App;

/***/ }),
/* 21 */,
/* 22 */
/*!*******************************!*\
  !*** ./src/backbone-tools.js ***!
  \*******************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {"use strict";
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	/*
	 * * Copyright (C) 2012-2017 Croissance Commune
	 * * Authors:
	 *       * Arezki Feth <f.a@majerti.fr>;
	 *       * Miotte Julien <j.m@majerti.fr>;
	 *       * TJEBBES Gaston <g.t@majerti.fr>
	 *
	 * This file is part of Autonomie : Progiciel de gestion de CAE.
	 *
	 *    Autonomie is free software: you can redistribute it and/or modify
	 *    it under the terms of the GNU General Public License as published by
	 *    the Free Software Foundation, either version 3 of the License, or
	 *    (at your option) any later version.
	 *
	 *    Autonomie is distributed in the hope that it will be useful,
	 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
	 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	 *    GNU General Public License for more details.
	 *
	 *    You should have received a copy of the GNU General Public License
	 *    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
	 */
	
	var showError = function showError(control, error) {
	    /*"""
	     * shows error 'message' to the group group in a twitter bootstrap
	     * friendly manner
	     */
	    var group = control.parents(".form-group");
	    group.addClass("has-error");
	    if (group.find(".help-block").length === 0) {
	        group.append("<span class=\"help-block error-message\"></span>");
	    }
	    var target = group.find(".help-block");
	    return target.text(error);
	};
	var hideFormError = function hideFormError(form) {
	    /*"""
	     * Remove bootstrap style errors from the whole form
	     */
	    form.find(".alert").remove();
	    var groups = form.find(".form-group");
	    groups.removeClass("has-error");
	    groups.find(".error-message").remove();
	    return form;
	};
	var hideFieldError = function hideFieldError(control) {
	    /*"""
	     */
	    var group = control.parents(".form-group");
	    group.removeClass("has-error");
	    group.find(".error-message").remove();
	    return control;
	};
	var BootstrapOnValidForm = exports.BootstrapOnValidForm = function BootstrapOnValidForm(view, attr, selector) {
	    var control, group;
	    control = view.$('[' + selector + '=' + attr + ']');
	    hideFieldError(control);
	};
	var BootstrapOnInvalidForm = exports.BootstrapOnInvalidForm = function BootstrapOnInvalidForm(view, attr, error, selector) {
	    var control, group, position, target;
	    control = view.$('[' + selector + '=' + attr + ']');
	    showError(control, error);
	};
	var setupBbValidationCallbacks = exports.setupBbValidationCallbacks = function setupBbValidationCallbacks(bb_module) {
	    _.extend(bb_module, {
	        valid: BootstrapOnValidForm,
	        invalid: BootstrapOnInvalidForm
	    });
	};
	var _displayServerMessage = function _displayServerMessage(options) {
	    /*
	     * """ Display a message from the server
	     */
	    //   var msgdiv = require('../handlebars/serverMessage.mustache');
	    //   $(msgdiv).prependTo("#messageboxes").fadeIn('slow').delay(8000).fadeOut(
	    //   'fast', function() { $(this).remove(); });
	};
	var displayServerError = exports.displayServerError = function displayServerError(msg) {
	    /*
	     *  Show errors in a message box
	     */
	    _displayServerMessage({ msg: msg, error: true });
	};
	var displayServerSuccess = exports.displayServerSuccess = function displayServerSuccess(msg) {
	    /*
	     *  Show errors in a message box
	     */
	    _displayServerMessage({ msg: msg });
	};
	
	var setupBbValidationPatterns = exports.setupBbValidationPatterns = function setupBbValidationPatterns(bb_module) {
	    _.extend(bb_module.patterns, {
	        amount: /^(\d+(?:[\.\,]\d{1,5})?)$/,
	        amount2: /^(\d+(?:[\.\,]\d{1,2})?)$/
	    });
	    _.extend(bb_module.messages, {
	        amount: "Doit être un nombre avec au maximum 5 chiffres après la virgule",
	        amount2: "Doit être un nombre avec au maximum 2 chiffres après la virgule"
	    });
	};
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 23 */
/*!******************************************!*\
  !*** ./src/expense/components/Router.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var Router = _backbone2.default.AppRouter.extend({
	  appRoutes: {
	    'login': 'login'
	  }
	}); /*
	     * File Name : Router.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = Router;

/***/ }),
/* 24 */
/*!**********************************************!*\
  !*** ./src/expense/components/Controller.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _MainView = __webpack_require__(/*! ../views/MainView.js */ 25);
	
	var _MainView2 = _interopRequireDefault(_MainView);
	
	var _App = __webpack_require__(/*! ./App.js */ 20);
	
	var _App2 = _interopRequireDefault(_App);
	
	var _Facade = __webpack_require__(/*! ./Facade.js */ 38);
	
	var _Facade2 = _interopRequireDefault(_Facade);
	
	var _AuthBus = __webpack_require__(/*! ../../base/components/AuthBus.js */ 45);
	
	var _AuthBus2 = _interopRequireDefault(_AuthBus);
	
	var _MessageBus = __webpack_require__(/*! ../../base/components/MessageBus.js */ 51);
	
	var _MessageBus2 = _interopRequireDefault(_MessageBus);
	
	var _ConfigBus = __webpack_require__(/*! ../../base/components/ConfigBus.js */ 52);
	
	var _ConfigBus2 = _interopRequireDefault(_ConfigBus);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var Controller = _backbone2.default.Object.extend({
	    initialize: function initialize(options) {
	        _ConfigBus2.default.setFormConfig(options.form_config);
	        _Facade2.default.loadModels(options.form_datas);
	        AppOption.facade = _Facade2.default;
	
	        this.mainView = new _MainView2.default();
	        _App2.default.showView(this.mainView);
	    },
	    status: function status(_status) {
	        this.mainView.showBox(_status);
	    },
	
	    login: function login() {
	        /*
	         * Login view : show the login form
	         */
	        this.mainView.showLogin();
	    }
	}); /*
	     * File Name : Controller.js
	     *
	     * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = Controller;

/***/ }),
/* 25 */
/*!***************************************!*\
  !*** ./src/expense/views/MainView.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _ExpenseTableView = __webpack_require__(/*! ./ExpenseTableView.js */ 26);
	
	var _ExpenseTableView2 = _interopRequireDefault(_ExpenseTableView);
	
	var _ExpenseKmTableView = __webpack_require__(/*! ./ExpenseKmTableView.js */ 35);
	
	var _ExpenseKmTableView2 = _interopRequireDefault(_ExpenseKmTableView);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : MainView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var MainView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/MainView.mustache */ 37),
	    regions: {
	        modalRegion: '#modalregion',
	        internalLines: '.internal-lines',
	        internalKmLines: '.internal-kmlines',
	        activityLines: '.activity-lines',
	        activityKmLines: '.activity-kmlines',
	        totals: '.totals'
	    },
	    ui: {
	        internal: '#internal-container',
	        activity: '#activity-container'
	    },
	    initialize: function initialize() {
	        this.facade = _backbone4.default.channel('facade');
	        this.config = _backbone4.default.channel('config');
	        this.categories = this.config.requests('get:option', 'categories');
	    },
	    showInternalTab: function showInternalTab() {
	        var collection = this.facade.requests('get:collection', 'internal_lines');
	        var view = new _ExpenseTableView2.default({
	            collection: collection,
	            category: this.categories[0]
	        });
	        this.showChildView('internalLines', view);
	
	        collection = this.facade.requests('get:collection', 'internal_kmlines');
	        view = new _ExpenseKmTableView2.default({
	            collection: collection,
	            category: this.categories[0]
	        });
	        this.showChildView('internalKmLines', view);
	    },
	    showActitityTab: function showActitityTab() {
	        var collection = this.facade.requests('get:collection', 'activity_lines');
	        var view = new _ExpenseTableView2.default({
	            collection: collection,
	            category: this.categories[1]
	        });
	        this.showChildView('activityLines', view);
	
	        collection = this.facade.requests('get:collection', 'activity_kmlines');
	        view = new _ExpenseKmTableView2.default({
	            collection: collection,
	            category: this.categories[1]
	        });
	        this.showChildView('activityKmLines', view);
	    },
	    onRender: function onRender() {
	        this.showInternalTab();
	        this.showActitityTab();
	    }
	});
	exports.default = MainView;

/***/ }),
/* 26 */
/*!***********************************************!*\
  !*** ./src/expense/views/ExpenseTableView.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseTableView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/ExpenseTableView.mustache */ 27),
	    templateContext: function templateContext() {
	        return {};
	    }
	}); /*
	     * File Name : ExpenseTableView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseTableView;

/***/ }),
/* 27 */
/*!***************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseTableView.mustache ***!
  \***************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 28);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "        <div>\n        <a href=\"#lines/add/1\" class='btn btn-info' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n        <a href=\"#tel/add\" class='btn btn-info' title=\"Ajouter une ligne de dépense téléphonique\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter des dépenses téléphoniques</a>\n        </div>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "        <th class=\"hidden-print\">Actions</th>\n";
	  },"5":function(depth0,helpers,partials,data) {
	  return "            <td class=\"hidden-print\"></td>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class=\"row\">\n    <div class=\"col-xs-4\">\n        <h3 style=\"margin-top:0px\">\n            Frais\n        </h3>\n        <span class=\"help-block\">\n            Dépenses liées au fonctionnement de l'entreprise\n        </span>\n    </div>\n    <div class=\"col-xs-8\">\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </div>\n</div>\n<table class=\"opa table table-bordered table-condensed\">\n    <thead>\n        <th>Date</th>\n        <th>Type de dépense</th>\n        <th>Description</th>\n        <th>Montant HT</th>\n        <th>Tva</th>\n        <th>Total TTC</th>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </thead>\n    <tbody class='internal'>\n    </tbody>\n    <tfoot>\n        <tr>\n            <td colspan='3'>Total</td>\n            <td id='internal_total_ht'></td>\n            <td id='internal_total_tva'></td>\n            <td id='internal_total'></td>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "        </tr>\n    </tfoot>\n</table>\n";
	},"useData":true});

/***/ }),
/* 28 */
/*!*********************************!*\
  !*** ./~/handlebars/runtime.js ***!
  \*********************************/
/***/ (function(module, exports, __webpack_require__) {

	// Create a simple path alias to allow browserify to resolve
	// the runtime on a supported path.
	module.exports = __webpack_require__(/*! ./dist/cjs/handlebars.runtime */ 29);


/***/ }),
/* 29 */
/*!*****************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars.runtime.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	/*globals Handlebars: true */
	var base = __webpack_require__(/*! ./handlebars/base */ 30);
	
	// Each of these augment the Handlebars object. No need to setup here.
	// (This is done to easily share code between commonjs and browse envs)
	var SafeString = __webpack_require__(/*! ./handlebars/safe-string */ 32)["default"];
	var Exception = __webpack_require__(/*! ./handlebars/exception */ 33)["default"];
	var Utils = __webpack_require__(/*! ./handlebars/utils */ 31);
	var runtime = __webpack_require__(/*! ./handlebars/runtime */ 34);
	
	// For compatibility and usage outside of module systems, make the Handlebars object a namespace
	var create = function() {
	  var hb = new base.HandlebarsEnvironment();
	
	  Utils.extend(hb, base);
	  hb.SafeString = SafeString;
	  hb.Exception = Exception;
	  hb.Utils = Utils;
	  hb.escapeExpression = Utils.escapeExpression;
	
	  hb.VM = runtime;
	  hb.template = function(spec) {
	    return runtime.template(spec, hb);
	  };
	
	  return hb;
	};
	
	var Handlebars = create();
	Handlebars.create = create;
	
	Handlebars['default'] = Handlebars;
	
	exports["default"] = Handlebars;

/***/ }),
/* 30 */
/*!**************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/base.js ***!
  \**************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	var Utils = __webpack_require__(/*! ./utils */ 31);
	var Exception = __webpack_require__(/*! ./exception */ 33)["default"];
	
	var VERSION = "2.0.0";
	exports.VERSION = VERSION;var COMPILER_REVISION = 6;
	exports.COMPILER_REVISION = COMPILER_REVISION;
	var REVISION_CHANGES = {
	  1: '<= 1.0.rc.2', // 1.0.rc.2 is actually rev2 but doesn't report it
	  2: '== 1.0.0-rc.3',
	  3: '== 1.0.0-rc.4',
	  4: '== 1.x.x',
	  5: '== 2.0.0-alpha.x',
	  6: '>= 2.0.0-beta.1'
	};
	exports.REVISION_CHANGES = REVISION_CHANGES;
	var isArray = Utils.isArray,
	    isFunction = Utils.isFunction,
	    toString = Utils.toString,
	    objectType = '[object Object]';
	
	function HandlebarsEnvironment(helpers, partials) {
	  this.helpers = helpers || {};
	  this.partials = partials || {};
	
	  registerDefaultHelpers(this);
	}
	
	exports.HandlebarsEnvironment = HandlebarsEnvironment;HandlebarsEnvironment.prototype = {
	  constructor: HandlebarsEnvironment,
	
	  logger: logger,
	  log: log,
	
	  registerHelper: function(name, fn) {
	    if (toString.call(name) === objectType) {
	      if (fn) { throw new Exception('Arg not supported with multiple helpers'); }
	      Utils.extend(this.helpers, name);
	    } else {
	      this.helpers[name] = fn;
	    }
	  },
	  unregisterHelper: function(name) {
	    delete this.helpers[name];
	  },
	
	  registerPartial: function(name, partial) {
	    if (toString.call(name) === objectType) {
	      Utils.extend(this.partials,  name);
	    } else {
	      this.partials[name] = partial;
	    }
	  },
	  unregisterPartial: function(name) {
	    delete this.partials[name];
	  }
	};
	
	function registerDefaultHelpers(instance) {
	  instance.registerHelper('helperMissing', function(/* [args, ]options */) {
	    if(arguments.length === 1) {
	      // A missing field in a {{foo}} constuct.
	      return undefined;
	    } else {
	      // Someone is actually trying to call something, blow up.
	      throw new Exception("Missing helper: '" + arguments[arguments.length-1].name + "'");
	    }
	  });
	
	  instance.registerHelper('blockHelperMissing', function(context, options) {
	    var inverse = options.inverse,
	        fn = options.fn;
	
	    if(context === true) {
	      return fn(this);
	    } else if(context === false || context == null) {
	      return inverse(this);
	    } else if (isArray(context)) {
	      if(context.length > 0) {
	        if (options.ids) {
	          options.ids = [options.name];
	        }
	
	        return instance.helpers.each(context, options);
	      } else {
	        return inverse(this);
	      }
	    } else {
	      if (options.data && options.ids) {
	        var data = createFrame(options.data);
	        data.contextPath = Utils.appendContextPath(options.data.contextPath, options.name);
	        options = {data: data};
	      }
	
	      return fn(context, options);
	    }
	  });
	
	  instance.registerHelper('each', function(context, options) {
	    if (!options) {
	      throw new Exception('Must pass iterator to #each');
	    }
	
	    var fn = options.fn, inverse = options.inverse;
	    var i = 0, ret = "", data;
	
	    var contextPath;
	    if (options.data && options.ids) {
	      contextPath = Utils.appendContextPath(options.data.contextPath, options.ids[0]) + '.';
	    }
	
	    if (isFunction(context)) { context = context.call(this); }
	
	    if (options.data) {
	      data = createFrame(options.data);
	    }
	
	    if(context && typeof context === 'object') {
	      if (isArray(context)) {
	        for(var j = context.length; i<j; i++) {
	          if (data) {
	            data.index = i;
	            data.first = (i === 0);
	            data.last  = (i === (context.length-1));
	
	            if (contextPath) {
	              data.contextPath = contextPath + i;
	            }
	          }
	          ret = ret + fn(context[i], { data: data });
	        }
	      } else {
	        for(var key in context) {
	          if(context.hasOwnProperty(key)) {
	            if(data) {
	              data.key = key;
	              data.index = i;
	              data.first = (i === 0);
	
	              if (contextPath) {
	                data.contextPath = contextPath + key;
	              }
	            }
	            ret = ret + fn(context[key], {data: data});
	            i++;
	          }
	        }
	      }
	    }
	
	    if(i === 0){
	      ret = inverse(this);
	    }
	
	    return ret;
	  });
	
	  instance.registerHelper('if', function(conditional, options) {
	    if (isFunction(conditional)) { conditional = conditional.call(this); }
	
	    // Default behavior is to render the positive path if the value is truthy and not empty.
	    // The `includeZero` option may be set to treat the condtional as purely not empty based on the
	    // behavior of isEmpty. Effectively this determines if 0 is handled by the positive path or negative.
	    if ((!options.hash.includeZero && !conditional) || Utils.isEmpty(conditional)) {
	      return options.inverse(this);
	    } else {
	      return options.fn(this);
	    }
	  });
	
	  instance.registerHelper('unless', function(conditional, options) {
	    return instance.helpers['if'].call(this, conditional, {fn: options.inverse, inverse: options.fn, hash: options.hash});
	  });
	
	  instance.registerHelper('with', function(context, options) {
	    if (isFunction(context)) { context = context.call(this); }
	
	    var fn = options.fn;
	
	    if (!Utils.isEmpty(context)) {
	      if (options.data && options.ids) {
	        var data = createFrame(options.data);
	        data.contextPath = Utils.appendContextPath(options.data.contextPath, options.ids[0]);
	        options = {data:data};
	      }
	
	      return fn(context, options);
	    } else {
	      return options.inverse(this);
	    }
	  });
	
	  instance.registerHelper('log', function(message, options) {
	    var level = options.data && options.data.level != null ? parseInt(options.data.level, 10) : 1;
	    instance.log(level, message);
	  });
	
	  instance.registerHelper('lookup', function(obj, field) {
	    return obj && obj[field];
	  });
	}
	
	var logger = {
	  methodMap: { 0: 'debug', 1: 'info', 2: 'warn', 3: 'error' },
	
	  // State enum
	  DEBUG: 0,
	  INFO: 1,
	  WARN: 2,
	  ERROR: 3,
	  level: 3,
	
	  // can be overridden in the host environment
	  log: function(level, message) {
	    if (logger.level <= level) {
	      var method = logger.methodMap[level];
	      if (typeof console !== 'undefined' && console[method]) {
	        console[method].call(console, message);
	      }
	    }
	  }
	};
	exports.logger = logger;
	var log = logger.log;
	exports.log = log;
	var createFrame = function(object) {
	  var frame = Utils.extend({}, object);
	  frame._parent = object;
	  return frame;
	};
	exports.createFrame = createFrame;

/***/ }),
/* 31 */
/*!***************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/utils.js ***!
  \***************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	/*jshint -W004 */
	var SafeString = __webpack_require__(/*! ./safe-string */ 32)["default"];
	
	var escape = {
	  "&": "&amp;",
	  "<": "&lt;",
	  ">": "&gt;",
	  '"': "&quot;",
	  "'": "&#x27;",
	  "`": "&#x60;"
	};
	
	var badChars = /[&<>"'`]/g;
	var possible = /[&<>"'`]/;
	
	function escapeChar(chr) {
	  return escape[chr];
	}
	
	function extend(obj /* , ...source */) {
	  for (var i = 1; i < arguments.length; i++) {
	    for (var key in arguments[i]) {
	      if (Object.prototype.hasOwnProperty.call(arguments[i], key)) {
	        obj[key] = arguments[i][key];
	      }
	    }
	  }
	
	  return obj;
	}
	
	exports.extend = extend;var toString = Object.prototype.toString;
	exports.toString = toString;
	// Sourced from lodash
	// https://github.com/bestiejs/lodash/blob/master/LICENSE.txt
	var isFunction = function(value) {
	  return typeof value === 'function';
	};
	// fallback for older versions of Chrome and Safari
	/* istanbul ignore next */
	if (isFunction(/x/)) {
	  isFunction = function(value) {
	    return typeof value === 'function' && toString.call(value) === '[object Function]';
	  };
	}
	var isFunction;
	exports.isFunction = isFunction;
	/* istanbul ignore next */
	var isArray = Array.isArray || function(value) {
	  return (value && typeof value === 'object') ? toString.call(value) === '[object Array]' : false;
	};
	exports.isArray = isArray;
	
	function escapeExpression(string) {
	  // don't escape SafeStrings, since they're already safe
	  if (string instanceof SafeString) {
	    return string.toString();
	  } else if (string == null) {
	    return "";
	  } else if (!string) {
	    return string + '';
	  }
	
	  // Force a string conversion as this will be done by the append regardless and
	  // the regex test will do this transparently behind the scenes, causing issues if
	  // an object's to string has escaped characters in it.
	  string = "" + string;
	
	  if(!possible.test(string)) { return string; }
	  return string.replace(badChars, escapeChar);
	}
	
	exports.escapeExpression = escapeExpression;function isEmpty(value) {
	  if (!value && value !== 0) {
	    return true;
	  } else if (isArray(value) && value.length === 0) {
	    return true;
	  } else {
	    return false;
	  }
	}
	
	exports.isEmpty = isEmpty;function appendContextPath(contextPath, id) {
	  return (contextPath ? contextPath + '.' : '') + id;
	}
	
	exports.appendContextPath = appendContextPath;

/***/ }),
/* 32 */
/*!*********************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/safe-string.js ***!
  \*********************************************************/
/***/ (function(module, exports) {

	"use strict";
	// Build out our basic SafeString type
	function SafeString(string) {
	  this.string = string;
	}
	
	SafeString.prototype.toString = function() {
	  return "" + this.string;
	};
	
	exports["default"] = SafeString;

/***/ }),
/* 33 */
/*!*******************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/exception.js ***!
  \*******************************************************/
/***/ (function(module, exports) {

	"use strict";
	
	var errorProps = ['description', 'fileName', 'lineNumber', 'message', 'name', 'number', 'stack'];
	
	function Exception(message, node) {
	  var line;
	  if (node && node.firstLine) {
	    line = node.firstLine;
	
	    message += ' - ' + line + ':' + node.firstColumn;
	  }
	
	  var tmp = Error.prototype.constructor.call(this, message);
	
	  // Unfortunately errors are not enumerable in Chrome (at least), so `for prop in tmp` doesn't work.
	  for (var idx = 0; idx < errorProps.length; idx++) {
	    this[errorProps[idx]] = tmp[errorProps[idx]];
	  }
	
	  if (line) {
	    this.lineNumber = line;
	    this.column = node.firstColumn;
	  }
	}
	
	Exception.prototype = new Error();
	
	exports["default"] = Exception;

/***/ }),
/* 34 */
/*!*****************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/runtime.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	var Utils = __webpack_require__(/*! ./utils */ 31);
	var Exception = __webpack_require__(/*! ./exception */ 33)["default"];
	var COMPILER_REVISION = __webpack_require__(/*! ./base */ 30).COMPILER_REVISION;
	var REVISION_CHANGES = __webpack_require__(/*! ./base */ 30).REVISION_CHANGES;
	var createFrame = __webpack_require__(/*! ./base */ 30).createFrame;
	
	function checkRevision(compilerInfo) {
	  var compilerRevision = compilerInfo && compilerInfo[0] || 1,
	      currentRevision = COMPILER_REVISION;
	
	  if (compilerRevision !== currentRevision) {
	    if (compilerRevision < currentRevision) {
	      var runtimeVersions = REVISION_CHANGES[currentRevision],
	          compilerVersions = REVISION_CHANGES[compilerRevision];
	      throw new Exception("Template was precompiled with an older version of Handlebars than the current runtime. "+
	            "Please update your precompiler to a newer version ("+runtimeVersions+") or downgrade your runtime to an older version ("+compilerVersions+").");
	    } else {
	      // Use the embedded version info since the runtime doesn't know about this revision yet
	      throw new Exception("Template was precompiled with a newer version of Handlebars than the current runtime. "+
	            "Please update your runtime to a newer version ("+compilerInfo[1]+").");
	    }
	  }
	}
	
	exports.checkRevision = checkRevision;// TODO: Remove this line and break up compilePartial
	
	function template(templateSpec, env) {
	  /* istanbul ignore next */
	  if (!env) {
	    throw new Exception("No environment passed to template");
	  }
	  if (!templateSpec || !templateSpec.main) {
	    throw new Exception('Unknown template object: ' + typeof templateSpec);
	  }
	
	  // Note: Using env.VM references rather than local var references throughout this section to allow
	  // for external users to override these as psuedo-supported APIs.
	  env.VM.checkRevision(templateSpec.compiler);
	
	  var invokePartialWrapper = function(partial, indent, name, context, hash, helpers, partials, data, depths) {
	    if (hash) {
	      context = Utils.extend({}, context, hash);
	    }
	
	    var result = env.VM.invokePartial.call(this, partial, name, context, helpers, partials, data, depths);
	
	    if (result == null && env.compile) {
	      var options = { helpers: helpers, partials: partials, data: data, depths: depths };
	      partials[name] = env.compile(partial, { data: data !== undefined, compat: templateSpec.compat }, env);
	      result = partials[name](context, options);
	    }
	    if (result != null) {
	      if (indent) {
	        var lines = result.split('\n');
	        for (var i = 0, l = lines.length; i < l; i++) {
	          if (!lines[i] && i + 1 === l) {
	            break;
	          }
	
	          lines[i] = indent + lines[i];
	        }
	        result = lines.join('\n');
	      }
	      return result;
	    } else {
	      throw new Exception("The partial " + name + " could not be compiled when running in runtime-only mode");
	    }
	  };
	
	  // Just add water
	  var container = {
	    lookup: function(depths, name) {
	      var len = depths.length;
	      for (var i = 0; i < len; i++) {
	        if (depths[i] && depths[i][name] != null) {
	          return depths[i][name];
	        }
	      }
	    },
	    lambda: function(current, context) {
	      return typeof current === 'function' ? current.call(context) : current;
	    },
	
	    escapeExpression: Utils.escapeExpression,
	    invokePartial: invokePartialWrapper,
	
	    fn: function(i) {
	      return templateSpec[i];
	    },
	
	    programs: [],
	    program: function(i, data, depths) {
	      var programWrapper = this.programs[i],
	          fn = this.fn(i);
	      if (data || depths) {
	        programWrapper = program(this, i, fn, data, depths);
	      } else if (!programWrapper) {
	        programWrapper = this.programs[i] = program(this, i, fn);
	      }
	      return programWrapper;
	    },
	
	    data: function(data, depth) {
	      while (data && depth--) {
	        data = data._parent;
	      }
	      return data;
	    },
	    merge: function(param, common) {
	      var ret = param || common;
	
	      if (param && common && (param !== common)) {
	        ret = Utils.extend({}, common, param);
	      }
	
	      return ret;
	    },
	
	    noop: env.VM.noop,
	    compilerInfo: templateSpec.compiler
	  };
	
	  var ret = function(context, options) {
	    options = options || {};
	    var data = options.data;
	
	    ret._setup(options);
	    if (!options.partial && templateSpec.useData) {
	      data = initData(context, data);
	    }
	    var depths;
	    if (templateSpec.useDepths) {
	      depths = options.depths ? [context].concat(options.depths) : [context];
	    }
	
	    return templateSpec.main.call(container, context, container.helpers, container.partials, data, depths);
	  };
	  ret.isTop = true;
	
	  ret._setup = function(options) {
	    if (!options.partial) {
	      container.helpers = container.merge(options.helpers, env.helpers);
	
	      if (templateSpec.usePartial) {
	        container.partials = container.merge(options.partials, env.partials);
	      }
	    } else {
	      container.helpers = options.helpers;
	      container.partials = options.partials;
	    }
	  };
	
	  ret._child = function(i, data, depths) {
	    if (templateSpec.useDepths && !depths) {
	      throw new Exception('must pass parent depths');
	    }
	
	    return program(container, i, templateSpec[i], data, depths);
	  };
	  return ret;
	}
	
	exports.template = template;function program(container, i, fn, data, depths) {
	  var prog = function(context, options) {
	    options = options || {};
	
	    return fn.call(container, context, container.helpers, container.partials, options.data || data, depths && [context].concat(depths));
	  };
	  prog.program = i;
	  prog.depth = depths ? depths.length : 0;
	  return prog;
	}
	
	exports.program = program;function invokePartial(partial, name, context, helpers, partials, data, depths) {
	  var options = { partial: true, helpers: helpers, partials: partials, data: data, depths: depths };
	
	  if(partial === undefined) {
	    throw new Exception("The partial " + name + " could not be found");
	  } else if(partial instanceof Function) {
	    return partial(context, options);
	  }
	}
	
	exports.invokePartial = invokePartial;function noop() { return ""; }
	
	exports.noop = noop;function initData(context, data) {
	  if (!data || !('root' in data)) {
	    data = data ? createFrame(data) : {};
	    data.root = context;
	  }
	  return data;
	}

/***/ }),
/* 35 */
/*!*************************************************!*\
  !*** ./src/expense/views/ExpenseKmTableView.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseKmTableView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/ExpenseKmTableView.mustache */ 36),
	    templateContext: function templateContext() {
	        return {};
	    }
	}); /*
	     * File Name : ExpenseKmTableView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseKmTableView;

/***/ }),
/* 36 */
/*!*****************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseKmTableView.mustache ***!
  \*****************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 28);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "        <div>\n            <a href=\"#kmlines/add/1\" class='btn btn-info visible-desktop hidden-tablet' title=\"Ajouter une ligne\"><i class='icon icon-plus-sign'></i>&nbsp;Ajouter</a>\n        </div>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "        <th class=\"hidden-print\">Actions</th>\n";
	  },"5":function(depth0,helpers,partials,data) {
	  return "            <td class=\"hidden-print\"></td>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class=\"row\">\n    <div class=\"col-xs-4\">\n        <h3 style=\"margin-top:0px\">\n            Dépenses kilométriques\n        </h3>\n    </div>\n    <div class=\"col-xs-8\">\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </div>\n</div>\n\n<table class=\"opa table table-striped table-bordered table-condensed\">\n    <thead>\n        <th>Date</th>\n        <th>Type</th>\n        <th>Prestation</th>\n        <th>Point de départ</th>\n        <th>Point d'arrivée</th>\n        <th>Kms</th>\n        <th>Indemnités</th>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </thead>\n    <tbody class='internal'>\n    </tbody>\n    <tfoot>\n        <tr>\n            <td colspan='5'>Total</td>\n            <td id='km_internal_total_km'></td>\n            <td id='km_internal_total'></td>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "        </tr>\n    </tfoot>\n</table>\n\n";
	},"useData":true});

/***/ }),
/* 37 */
/*!*******************************************************!*\
  !*** ./src/expense/views/templates/MainView.mustache ***!
  \*******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 28);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div>\n<div class='modalRegion'></div>\n<div class='totals'></div>\n<ul class=\"nav nav-tabs\" role=\"tablist\">\n    <li role=\"presentation\" class=\"active\">\n        <a href=\"#internal-container\"\n            aria-controls=\"internal-container\"\n            role=\"tab\"\n            data-toggle=\"tab\">\n            Frais\n        </a>\n    </li>\n    <li role=\"presentation\">\n        <a href=\"#activity-container\"\n            aria-controls=\"activity-container\"\n            role=\"tab\"\n            data-toggle=\"tab\">\n            Achats\n        </a>\n    </li>\n</ul>\n<div class='tab-content'>\n    <div\n        role=\"tabpanel\"\n        class=\"tab-pane fade in active\"\n        id=\"internal-container\">\n        <div class='internal-lines'>\n        </div>\n        <div class='internal-kmlines'>\n        </div>\n    </div>\n    <div\n        role=\"tabpanel\"\n        class=\"tab-pane fade\"\n        id=\"activity-container\">\n        <div class='activity-lines'>\n        </div>\n        <div class='activity-kmlines'>\n        </div>\n    </div>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 38 */
/*!******************************************!*\
  !*** ./src/expense/components/Facade.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TotalModel = __webpack_require__(/*! ../models/TotalModel.js */ 39);
	
	var _TotalModel2 = _interopRequireDefault(_TotalModel);
	
	var _ExpenseCollection = __webpack_require__(/*! ../models/ExpenseCollection.js */ 40);
	
	var _ExpenseCollection2 = _interopRequireDefault(_ExpenseCollection);
	
	var _ExpenseKmCollection = __webpack_require__(/*! ../models/ExpenseKmCollection.js */ 43);
	
	var _ExpenseKmCollection2 = _interopRequireDefault(_ExpenseKmCollection);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : Facade.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var FacadeClass = _backbone2.default.Object.extend({
	    channelName: 'facade',
	    radioEvents: {},
	    radioRequests: {
	        'get:collection': 'getCollectionRequest',
	        'get:totalmodel': 'getTotalModelRequest'
	        // 'get:paymentcollection': 'getPaymentCollectionRequest',
	        // 'get:totalmodel': 'getTotalModelRequest',
	        // 'get:status_history_collection': 'getStatusHistory',
	        // 'is:valid': "isDataValid",
	        // 'get:attachments': 'getAttachments',
	    },
	    loadModels: function loadModels(form_datas) {
	        this.datas = form_datas;
	        this.models = {};
	        this.collections = {};
	        this.totalmodel = new _TotalModel2.default();
	
	        var internal = form_datas['internal'];
	
	        var lines = internal['lines'];
	        this.collections['internal_lines'] = new _ExpenseCollection2.default(lines);
	        var kmlines = internal['kmlines'];
	        this.collections['internal_kmlines'] = new _ExpenseKmCollection2.default(lines);
	
	        var activity = form_datas['activity'];
	        var lines = activity['lines'];
	        this.collections['activity_lines'] = new _ExpenseCollection2.default(lines);
	        var kmlines = activity['kmlines'];
	        this.collections['activity_kmlines'] = new _ExpenseKmCollection2.default(lines);
	
	        this.computeTotals();
	    },
	    computeTotals: function computeTotals() {
	        var internal_ht = this.collections['internal_lines'].total_ht();
	        var internal_tva = this.collections['internal_lines'].total_tva();
	        var internal_total = this.collections['internal_lines'].total_ttc();
	        var internal_km = this.collections['internal_kmlines'].total_km();
	        var internal_km_total = this.collections['internal_kmlines'].total();
	        var internal_ttc = internal_total + internal_km_total;
	
	        var activity_ht = this.collections['activity_lines'].total_ht();
	        var activity_tva = this.collections['activity_lines'].total_tva();
	        var activity_total = this.collections['activity_lines'].total_ttc();
	        var activity_km = this.collections['activity_kmlines'].total_km();
	        var activity_km_total = this.collections['activity_kmlines'].total();
	        var activity_ttc = activity_total + activity_km_total;
	
	        this.totalmodel.set({
	            internal_ht: internal_ht,
	            internal_tva: internal_tva,
	            internal_total: internal_total,
	            internal_km: internal_km,
	            internal_km_total: internal_km_total,
	            internal_ttc: internal_ttc,
	            activity_ht: activity_ht,
	            activity_tva: activity_tva,
	            activity_total: activity_total,
	            activity_km: activity_km,
	            activity_ttc: activity_ttc
	        });
	    },
	    getCollectionRequest: function getCollectionRequest(label) {
	        return this.collections[label];
	    },
	    getTotalModelRequest: function getTotalModelRequest() {
	        return this.totalmodel;
	    }
	});
	var Facade = new FacadeClass();
	exports.default = Facade;

/***/ }),
/* 39 */
/*!******************************************!*\
  !*** ./src/expense/models/TotalModel.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TotalModel = _backbone2.default.Model.extend({
	    initialize: function initialize() {
	        TotalModel.__super__.initialize.apply(this, arguments);
	    }
	}); /*
	     * File Name : TotalModel.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = TotalModel;

/***/ }),
/* 40 */
/*!*************************************************!*\
  !*** ./src/expense/models/ExpenseCollection.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ExpenseModel = __webpack_require__(/*! ./ExpenseModel.js */ 41);
	
	var _ExpenseModel2 = _interopRequireDefault(_ExpenseModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseCollection.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ExpenseCollection = _backbone2.default.Collection.extend({
	  /*
	   *  Collection of expense lines
	   */
	  model: _ExpenseModel2.default,
	  url: "/expenses/lines",
	  comparator: function comparator(a, b) {
	    /*
	     * Sort the collection and place special lines at the end
	     */
	    var res = 0;
	    if (b.isSpecial()) {
	      res = -1;
	    } else if (a.isSpecial()) {
	      res = 1;
	    } else {
	      var acat = a.get('category');
	      var bcat = b.get('category');
	      if (acat < bcat) {
	        res = -1;
	      } else if (acat > bcat) {
	        res = 1;
	      }
	      if (res === 0) {
	        var adate = a.get('altdate');
	        var bdate = a.get('altdate');
	        if (adate < bdate) {
	          res = -1;
	        } else if (acat > bcat) {
	          res = 1;
	        }
	      }
	    }
	    return res;
	  },
	  total_ht: function total_ht(category) {
	    /*
	     * Return the total value
	     */
	    var result = 0;
	    this.each(function (model) {
	      if (category != undefined) {
	        if (model.get('category') != category) {
	          return;
	        }
	      }
	      result += model.getHT();
	    });
	    return result;
	  },
	  total_tva: function total_tva(category) {
	    /*
	     * Return the total value
	     */
	    var result = 0;
	    this.each(function (model) {
	      if (category != undefined) {
	        if (model.get('category') != category) {
	          return;
	        }
	      }
	      result += model.getTva();
	    });
	    return result;
	  },
	  total: function total(category) {
	    /*
	     * Return the total value
	     */
	    var result = 0;
	    this.each(function (model) {
	      if (category != undefined) {
	        if (model.get('category') != category) {
	          return;
	        }
	      }
	      result += model.total();
	    });
	    return result;
	  }
	});
	exports.default = ExpenseCollection;

/***/ }),
/* 41 */
/*!********************************************!*\
  !*** ./src/expense/models/ExpenseModel.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _BaseModel = __webpack_require__(/*! ./BaseModel.js */ 42);
	
	var _BaseModel2 = _interopRequireDefault(_BaseModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseModel = _BaseModel2.default.extend({
	  defaults: {
	    category: null,
	    description: "",
	    ht: null,
	    tva: null
	  },
	  // Constructor dynamically add a altdate if missing
	  // (altdate is used in views for jquery datepicker)
	  initialize: function initialize(options) {
	    if (options['altdate'] === undefined && options['date'] !== undefined) {
	      this.set('altdate', formatPaymentDate(options['date']));
	    }
	  },
	
	  // Validation rules for our model's attributes
	  validation: {
	    category: {
	      required: true,
	      msg: "est requise"
	    },
	    type_id: {
	      required: true,
	      msg: "est requis"
	    },
	    date: {
	      required: true,
	      pattern: /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
	      msg: "est requise"
	    },
	    ht: {
	      required: true,
	      // Match"es 19,6 19.65 but not 19.654"
	      pattern: /^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
	      msg: "doit être un nombre"
	    },
	    tva: {
	      required: true,
	      pattern: /^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
	      msg: "doit être un nombre"
	    }
	  },
	  total: function total() {
	    var total = this.getHT() + this.getTva();
	    return total;
	  },
	  getTva: function getTva() {
	    var result = parseFloat(this.get('tva'));
	    if (this.isSpecial()) {
	      var percentage = this.getTypeOption(AppOptions['expensetel_types']).percentage;
	      result = getPercent(result, percentage);
	    }
	    return result;
	  },
	  getHT: function getHT() {
	    var result = parseFloat(this.get('ht'));
	    if (this.isSpecial()) {
	      var percentage = this.getTypeOption(AppOptions['expensetel_types']).percentage;
	      result = getPercent(result, percentage);
	    }
	    return result;
	  },
	  isSpecial: function isSpecial() {
	    /*
	     * return True if this expense is a special one (related to phone)
	     */
	    return this.getTypeOption(AppOptions['expensetel_types']) !== undefined;
	  },
	  hasNoType: function hasNoType() {
	    var isnottel = _.isUndefined(this.getTypeOption(AppOptions['expensetel_types']));
	    var isnotexp = _.isUndefined(this.getTypeOption(AppOptions['expense_types']));
	    if (isnottel && isnotexp) {
	      return true;
	    } else {
	      return false;
	    }
	  },
	  getTypeOptions: function getTypeOptions() {
	    var arr;
	    if (this.isSpecial()) {
	      arr = AppOptions['expensetel_types'];
	    } else {
	      arr = AppOptions['expense_types'];
	    }
	    return arr;
	  }
	}); /*
	     * File Name : ExpenseModel.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseModel;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 42 */
/*!*****************************************!*\
  !*** ./src/expense/models/BaseModel.js ***!
  \*****************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var BaseModel = _backbone2.default.Model.extend({
	    /*
	     * BaseModel for expenses, provides tools to access main options
	     */
	    getTypeOption: function getTypeOption(arr) {
	        /*
	         * Retrieve the element from arr where its type_id is the same as the model's
	         * current one
	         */
	        var type_id = this.get('type_id');
	        return _.find(arr, function (type) {
	            return type['value'] == type_id;
	        });
	    },
	    getTypeOptions: function getTypeOptions() {
	        /*
	         * Return an array of options for types ( should be overriden )
	         */
	        return [];
	    },
	    getType: function getType() {
	        /*
	         * return the type object associated to the current model
	         */
	        var options = this.getTypeOptions();
	        return this.getTypeOption(options);
	    },
	    getTypeLabel: function getTypeLabel() {
	        /*
	         * Return the Label of the current type
	         */
	        var current_type = this.getType();
	        var options = this.getTypeOptions();
	        if (current_type === undefined) {
	            return "";
	        } else {
	            return current_type.label;
	        }
	    }
	}); /*
	     * File Name : BaseModel.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = BaseModel;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 43 */
/*!***************************************************!*\
  !*** ./src/expense/models/ExpenseKmCollection.js ***!
  \***************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ExpenseKmModel = __webpack_require__(/*! ./ExpenseKmModel.js */ 44);
	
	var _ExpenseKmModel2 = _interopRequireDefault(_ExpenseKmModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseKmCollection.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ExpenseKmCollection = _backbone2.default.Collection.extend({
	  /*
	   * Collection for expenses related to km fees
	   */
	  model: _ExpenseKmModel2.default,
	  total_km: function total_km(category) {
	    /*
	     * Return the total value
	     */
	    var result = 0;
	    this.each(function (model) {
	      if (category != undefined) {
	        if (model.get('category') != category) {
	          return;
	        }
	      }
	      result += model.getKm();
	    });
	    return result;
	  },
	  total: function total(category) {
	    var result = 0;
	    this.each(function (model) {
	      if (category != undefined) {
	        if (model.get('category') != category) {
	          return;
	        }
	      }
	      result += model.total();
	    });
	    return result;
	  }
	});
	exports.default = ExpenseKmCollection;

/***/ }),
/* 44 */
/*!**********************************************!*\
  !*** ./src/expense/models/ExpenseKmModel.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {"use strict";
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _BaseModel = __webpack_require__(/*! ./BaseModel.js */ 42);
	
	var _BaseModel2 = _interopRequireDefault(_BaseModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseKmModel = _BaseModel2.default.extend({
	  defaults: {
	    category: null,
	    start: "",
	    end: "",
	    description: ""
	  },
	  initialize: function initialize(options) {
	    if (options['altdate'] === undefined && options['date'] !== undefined) {
	      this.set('altdate', formatPaymentDate(options['date']));
	    }
	  },
	
	  validation: {
	    category: {
	      required: true,
	      msg: "est requise"
	    },
	    type_id: {
	      required: true,
	      msg: "est requis"
	    },
	    date: {
	      required: true,
	      pattern: /^[0-9]{4}-[0-9]{2}-[0-9]{2}$/,
	      msg: "est requise"
	    },
	    km: {
	      required: true,
	      // Match"es 19,6 19.65 but not 19.654"
	      pattern: /^[\+\-]?[0-9]+(([\.\,][0-9]{1})|([\.\,][0-9]{2}))?$/,
	      msg: "doit être un nombre"
	    }
	  },
	  getIndice: function getIndice() {
	    /*
	     *  Return the reference used for compensation of km fees
	     */
	    var elem = _.where(AppOptions['expensekm_types'], { value: this.get('type_id') })[0];
	    if (elem === undefined) {
	      return 0;
	    }
	    return parseFloat(elem.amount);
	  },
	  total: function total() {
	    var km = this.getKm();
	    var amount = this.getIndice();
	    return km * amount;
	  },
	  getKm: function getKm() {
	    return parseFloat(this.get('km'));
	  },
	  getTypeOptions: function getTypeOptions() {
	    return AppOptions['expensekm_types'];
	  }
	}); /*
	     * File Name : ExpenseKmModel.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseKmModel;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 45 */
/*!****************************************!*\
  !*** ./src/base/components/AuthBus.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 46);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : AuthBus.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var AuthBusClass = _backbone2.default.Object.extend({
	    channelName: 'auth',
	    url: '/api/v1/login',
	    radioEvents: {
	        'login': 'onLogin'
	    },
	    initialize: function initialize() {
	        this.ok_callback = null;
	        this.error_callback = null;
	    },
	    setAuthCallbacks: function setAuthCallbacks(callbacks) {
	        /*
	         * Define authentication callbacks that should be fired
	         * on successfull authentication
	         */
	        this.callbacks = callbacks;
	    },
	    onLogin: function onLogin(datas, onAuthOk, onAuthFailed) {
	        var callbacks = this.callbacks;
	        this.ok_callback = onAuthOk;
	        this.error_callback = onAuthFailed;
	        (0, _tools.ajax_call)(this.url, datas, 'POST', {
	            success: this.onAuthSuccess.bind(this),
	            error: this.onAuthError.bind(this)
	        });
	    },
	    onAuthSuccess: function onAuthSuccess(result) {
	        if (result['status'] == 'success') {
	            _.each(this.callbacks, function (callback) {
	                callback();
	            });
	            this.ok_callback(result);
	        } else {
	            this.error_callback(result);
	        }
	    },
	    onAuthError: function onAuthError(xhr) {
	        if (xhr.status == 400) {
	            if (_.has(xhr.responseJSON, 'errors')) {
	                this.error_callback(xhr.responseJSON.errors);
	            } else {
	                this.error_callback();
	            }
	        } else {
	            alert('Erreur serveur : contactez votre administrateur');
	        }
	    }
	});
	var AuthBus = new AuthBusClass();
	exports.default = AuthBus;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 46 */
/*!**********************!*\
  !*** ./src/tools.js ***!
  \**********************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	exports.hideLoader = exports.showLoader = exports.setupAjaxCallbacks = exports.serializeForm = exports.getOpt = exports.findCurrentSelected = exports.getDefaultItem = exports.updateSelectOptions = exports.ajax_call = exports.setDatePicker = undefined;
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _jquery = __webpack_require__(/*! jquery */ 2);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _date = __webpack_require__(/*! ./date.js */ 47);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	__webpack_require__(/*! jquery */ 2);
	
	
	var datepicker = __webpack_require__(/*! jquery-ui/ui/widgets/datepicker */ 48);
	
	var setDatePicker = exports.setDatePicker = function setDatePicker(input_tag, altfield_selector, value, kwargs) {
	    /*
	        * Set a datepicker
	        * Input tag is the visible field
	        * altfield_selector is the real world field
	        * value : The value to set
	        * kwargs: additional options to pass to the datepicker call
	        */
	    var options = {
	        altFormat: "yy-mm-dd",
	        dateFormat: "dd/mm/yy",
	        altField: altfield_selector
	    };
	    _underscore2.default.extend(options, kwargs);
	    input_tag.datepicker(options);
	
	    if (value !== null && !_underscore2.default.isUndefined(value)) {
	        value = (0, _date.parseDate)(value);
	        input_tag.datepicker('setDate', value);
	    } else {
	        if (!_underscore2.default.isUndefined(default_value)) {
	            value = (0, _date.parseDate)(default_value);
	            input_tag.datepicker('setDate', value);
	        }
	    }
	};
	
	var ajax_call = exports.ajax_call = function ajax_call(url, data, method, extra_options) {
	    var data = data || {};
	    var method = method || 'GET';
	
	    var options = {
	        url: url,
	        data: data,
	        method: method,
	        dataType: 'json',
	        cache: false
	    };
	    if (method == 'POST') {
	        options.data = JSON.stringify(data);
	        options.contentType = "application/json; charset=UTF-8";
	        options.processData = false;
	    }
	
	    _underscore2.default.extend(options, extra_options);
	
	    return _jquery2.default.ajax(options);
	};
	
	var updateSelectOptions = exports.updateSelectOptions = function updateSelectOptions(options, val, key) {
	    /*
	     * Add the selected attr to the option with value 'val'
	     *
	     * :param list options: list of js objects
	     * :param list val: list of values or single value
	     * :param str key: the key used to identifiy items ('value' by default)
	     * :returns: True if a default or an existing value has been found
	     * :rtype: bool
	     */
	    if (!_underscore2.default.isArray(val)) {
	        val = [val];
	    }
	    if (_underscore2.default.isUndefined(key)) {
	        key = 'value';
	    }
	    var has_selected = false;
	    _underscore2.default.each(options, function (option) {
	        delete option['selected'];
	        if (_underscore2.default.contains(val, option[key])) {
	            option['selected'] = 'true';
	            has_selected = true;
	        }
	    });
	    if (!has_selected) {
	        var option = getDefaultItem(options);
	        if (!_underscore2.default.isUndefined(option)) {
	            option['selected'] = true;
	            has_selected = true;
	        }
	    }
	    return has_selected;
	};
	var getDefaultItem = exports.getDefaultItem = function getDefaultItem(items) {
	    /*
	     * Get The default item from an array of items looking for a default key
	     *
	     * :param list items: list of objects
	     * :rtype: obj or undefined
	     */
	    var result = _underscore2.default.find(items, function (item) {
	        return item.default == true;
	    });
	    return result;
	};
	var findCurrentSelected = exports.findCurrentSelected = function findCurrentSelected(options, current_value, key) {
	    /*
	     * Return the full object definition from options matching the current value
	     *
	     * :param list options: List of objects
	     * :param str current_value: The current value in int or str
	     * :param str key: The key used to identify objects (value by default)
	     * :returns: The object matching the current_value
	     */
	    return _underscore2.default.find(options, function (item) {
	        return item[key] == current_value;
	    });
	};
	var getOpt = exports.getOpt = function getOpt(obj, key, default_val) {
	    /*
	     * Helper to get a default option
	     *
	     * :param obj obj: The object with the getOption func
	     * :param str key: The key we're looking for
	     * :param default_val: the default value
	     *
	     * :returns: The value matching key or default
	     */
	    var val = obj.getOption(key);
	    if (_underscore2.default.isUndefined(val)) {
	        val = default_val;
	    }
	    return val;
	};
	
	var serializeForm = exports.serializeForm = function serializeForm(form_object) {
	    /*
	     * Return the form datas as an object
	     * :param obj form_object: A jquery instance wrapping the form
	     */
	    var result = {};
	    var serial = form_object.serializeArray();
	    _jquery2.default.each(serial, function () {
	        if (result[this.name]) {
	            if (!result[this.name].push) {
	                result[this.name] = [result[this.name]];
	            }
	            result[this.name].push(this.value || '');
	        } else {
	            result[this.name] = this.value || '';
	        }
	    });
	    return result;
	};
	
	var setupAjaxCallbacks = exports.setupAjaxCallbacks = function setupAjaxCallbacks() {
	    /*
	     * Setup ajax calls callbacks
	     *
	     * if 'redirect' is found in the json resp, we go there
	     *
	     * if status code is 401 : we redirect to #login
	     */
	    (0, _jquery2.default)(document).ajaxComplete(function (event, xhr, settings) {
	        if (xhr.status == 401) {
	            window.location.replace('#login');
	        } else {
	            var json_resp = xhr.responseJSON;
	            if (!_underscore2.default.isUndefined(json_resp) && json_resp.redirect) {
	                window.location.href = json_resp.redirect;
	            }
	        }
	    });
	};
	var showLoader = exports.showLoader = function showLoader() {
	    /*
	     * Show a loading box
	     */
	    (0, _jquery2.default)('#loading-box').show();
	};
	var hideLoader = exports.hideLoader = function hideLoader() {
	    /*
	     * Show a loading box
	     */
	    (0, _jquery2.default)('#loading-box').hide();
	};

/***/ }),
/* 47 */
/*!*********************!*\
  !*** ./src/date.js ***!
  \*********************/
/***/ (function(module, exports) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	/*
	 * * Copyright (C) 2012-2013 Croissance Commune
	 * * Authors:
	 *       * Arezki Feth <f.a@majerti.fr>;
	 *       * Miotte Julien <j.m@majerti.fr>;
	 *       * Pettier Gabriel;
	 *       * TJEBBES Gaston <g.t@majerti.fr>
	 *
	 * This file is part of Autonomie : Progiciel de gestion de CAE.
	 *
	 *    Autonomie is free software: you can redistribute it and/or modify
	 *    it under the terms of the GNU General Public License as published by
	 *    the Free Software Foundation, either version 3 of the License, or
	 *    (at your option) any later version.
	 *
	 *    Autonomie is distributed in the hope that it will be useful,
	 *    but WITHOUT ANY WARRANTY; without even the implied warranty of
	 *    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
	 *    GNU General Public License for more details.
	 *
	 *    You should have received a copy of the GNU General Public License
	 *    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
	 */
	
	var getOneMonthAgo = exports.getOneMonthAgo = function getOneMonthAgo() {
	    var today = new Date();
	    var year = today.getUTCFullYear();
	    var month = today.getUTCMonth() - 1;
	    var day = today.getUTCDate();
	    return new Date(year, month, day);
	};
	
	var parseDate = exports.parseDate = function parseDate(isoDate) {
	    /*
	     * Returns a js Date object from an iso formatted string
	     */
	    var splitted = isoDate.split('-');
	    var year = parseInt(splitted[0], 10);
	    var month = parseInt(splitted[1], 10) - 1;
	    var day = parseInt(splitted[2], 10);
	    return new Date(year, month, day);
	};
	var getDateFromIso = exports.getDateFromIso = parseDate;
	var formatPaymentDate = exports.formatPaymentDate = function formatPaymentDate(isoDate) {
	    /*
	     *  format a date from iso to display format
	     */
	    if (isoDate !== '' && isoDate !== null) {
	        var dateObject = parseDate(isoDate);
	        return dateToLocaleFormat(dateObject);
	    } else {
	        return "";
	    }
	};
	var formatDate = exports.formatDate = formatPaymentDate;
	
	var dateToIso = exports.dateToIso = function dateToIso(dateObject) {
	    var year = dateObject.getFullYear();
	    var month = dateObject.getMonth() + 1;
	    var dt = dateObject.getDate();
	
	    if (dt < 10) {
	        dt = '0' + dt;
	    }
	    if (month < 10) {
	        month = '0' + month;
	    }
	    return year + "-" + month + "-" + dt;
	};
	var dateToLocaleFormat = exports.dateToLocaleFormat = function dateToLocaleFormat(dateObject) {
	    var year = dateObject.getFullYear();
	    var month = dateObject.getMonth() + 1;
	    var dt = dateObject.getDate();
	
	    if (dt < 10) {
	        dt = '0' + dt;
	    }
	    if (month < 10) {
	        month = '0' + month;
	    }
	    return dt + '-' + month + '-' + year;
	};

/***/ }),
/* 48 */
/*!**********************************************!*\
  !*** ./~/jquery-ui/ui/widgets/datepicker.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;// jscs:disable maximumLineLength
	/* jscs:disable requireCamelCaseOrUpperCaseIdentifiers */
	/*!
	 * jQuery UI Datepicker 1.12.1
	 * http://jqueryui.com
	 *
	 * Copyright jQuery Foundation and other contributors
	 * Released under the MIT license.
	 * http://jquery.org/license
	 */
	
	//>>label: Datepicker
	//>>group: Widgets
	//>>description: Displays a calendar from an input or inline for selecting dates.
	//>>docs: http://api.jqueryui.com/datepicker/
	//>>demos: http://jqueryui.com/datepicker/
	//>>css.structure: ../../themes/base/core.css
	//>>css.structure: ../../themes/base/datepicker.css
	//>>css.theme: ../../themes/base/theme.css
	
	( function( factory ) {
		if ( true ) {
	
			// AMD. Register as an anonymous module.
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [
				__webpack_require__(/*! jquery */ 2),
				__webpack_require__(/*! ../version */ 49),
				__webpack_require__(/*! ../keycode */ 50)
			], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
		} else {
	
			// Browser globals
			factory( jQuery );
		}
	}( function( $ ) {
	
	$.extend( $.ui, { datepicker: { version: "1.12.1" } } );
	
	var datepicker_instActive;
	
	function datepicker_getZindex( elem ) {
		var position, value;
		while ( elem.length && elem[ 0 ] !== document ) {
	
			// Ignore z-index if position is set to a value where z-index is ignored by the browser
			// This makes behavior of this function consistent across browsers
			// WebKit always returns auto if the element is positioned
			position = elem.css( "position" );
			if ( position === "absolute" || position === "relative" || position === "fixed" ) {
	
				// IE returns 0 when zIndex is not specified
				// other browsers return a string
				// we ignore the case of nested elements with an explicit value of 0
				// <div style="z-index: -10;"><div style="z-index: 0;"></div></div>
				value = parseInt( elem.css( "zIndex" ), 10 );
				if ( !isNaN( value ) && value !== 0 ) {
					return value;
				}
			}
			elem = elem.parent();
		}
	
		return 0;
	}
	/* Date picker manager.
	   Use the singleton instance of this class, $.datepicker, to interact with the date picker.
	   Settings for (groups of) date pickers are maintained in an instance object,
	   allowing multiple different settings on the same page. */
	
	function Datepicker() {
		this._curInst = null; // The current instance in use
		this._keyEvent = false; // If the last event was a key event
		this._disabledInputs = []; // List of date picker inputs that have been disabled
		this._datepickerShowing = false; // True if the popup picker is showing , false if not
		this._inDialog = false; // True if showing within a "dialog", false if not
		this._mainDivId = "ui-datepicker-div"; // The ID of the main datepicker division
		this._inlineClass = "ui-datepicker-inline"; // The name of the inline marker class
		this._appendClass = "ui-datepicker-append"; // The name of the append marker class
		this._triggerClass = "ui-datepicker-trigger"; // The name of the trigger marker class
		this._dialogClass = "ui-datepicker-dialog"; // The name of the dialog marker class
		this._disableClass = "ui-datepicker-disabled"; // The name of the disabled covering marker class
		this._unselectableClass = "ui-datepicker-unselectable"; // The name of the unselectable cell marker class
		this._currentClass = "ui-datepicker-current-day"; // The name of the current day marker class
		this._dayOverClass = "ui-datepicker-days-cell-over"; // The name of the day hover marker class
		this.regional = []; // Available regional settings, indexed by language code
		this.regional[ "" ] = { // Default regional settings
			closeText: "Done", // Display text for close link
			prevText: "Prev", // Display text for previous month link
			nextText: "Next", // Display text for next month link
			currentText: "Today", // Display text for current month link
			monthNames: [ "January","February","March","April","May","June",
				"July","August","September","October","November","December" ], // Names of months for drop-down and formatting
			monthNamesShort: [ "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec" ], // For formatting
			dayNames: [ "Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday" ], // For formatting
			dayNamesShort: [ "Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat" ], // For formatting
			dayNamesMin: [ "Su","Mo","Tu","We","Th","Fr","Sa" ], // Column headings for days starting at Sunday
			weekHeader: "Wk", // Column header for week of the year
			dateFormat: "mm/dd/yy", // See format options on parseDate
			firstDay: 0, // The first day of the week, Sun = 0, Mon = 1, ...
			isRTL: false, // True if right-to-left language, false if left-to-right
			showMonthAfterYear: false, // True if the year select precedes month, false for month then year
			yearSuffix: "" // Additional text to append to the year in the month headers
		};
		this._defaults = { // Global defaults for all the date picker instances
			showOn: "focus", // "focus" for popup on focus,
				// "button" for trigger button, or "both" for either
			showAnim: "fadeIn", // Name of jQuery animation for popup
			showOptions: {}, // Options for enhanced animations
			defaultDate: null, // Used when field is blank: actual date,
				// +/-number for offset from today, null for today
			appendText: "", // Display text following the input box, e.g. showing the format
			buttonText: "...", // Text for trigger button
			buttonImage: "", // URL for trigger button image
			buttonImageOnly: false, // True if the image appears alone, false if it appears on a button
			hideIfNoPrevNext: false, // True to hide next/previous month links
				// if not applicable, false to just disable them
			navigationAsDateFormat: false, // True if date formatting applied to prev/today/next links
			gotoCurrent: false, // True if today link goes back to current selection instead
			changeMonth: false, // True if month can be selected directly, false if only prev/next
			changeYear: false, // True if year can be selected directly, false if only prev/next
			yearRange: "c-10:c+10", // Range of years to display in drop-down,
				// either relative to today's year (-nn:+nn), relative to currently displayed year
				// (c-nn:c+nn), absolute (nnnn:nnnn), or a combination of the above (nnnn:-n)
			showOtherMonths: false, // True to show dates in other months, false to leave blank
			selectOtherMonths: false, // True to allow selection of dates in other months, false for unselectable
			showWeek: false, // True to show week of the year, false to not show it
			calculateWeek: this.iso8601Week, // How to calculate the week of the year,
				// takes a Date and returns the number of the week for it
			shortYearCutoff: "+10", // Short year values < this are in the current century,
				// > this are in the previous century,
				// string value starting with "+" for current year + value
			minDate: null, // The earliest selectable date, or null for no limit
			maxDate: null, // The latest selectable date, or null for no limit
			duration: "fast", // Duration of display/closure
			beforeShowDay: null, // Function that takes a date and returns an array with
				// [0] = true if selectable, false if not, [1] = custom CSS class name(s) or "",
				// [2] = cell title (optional), e.g. $.datepicker.noWeekends
			beforeShow: null, // Function that takes an input field and
				// returns a set of custom settings for the date picker
			onSelect: null, // Define a callback function when a date is selected
			onChangeMonthYear: null, // Define a callback function when the month or year is changed
			onClose: null, // Define a callback function when the datepicker is closed
			numberOfMonths: 1, // Number of months to show at a time
			showCurrentAtPos: 0, // The position in multipe months at which to show the current month (starting at 0)
			stepMonths: 1, // Number of months to step back/forward
			stepBigMonths: 12, // Number of months to step back/forward for the big links
			altField: "", // Selector for an alternate field to store selected dates into
			altFormat: "", // The date format to use for the alternate field
			constrainInput: true, // The input is constrained by the current date format
			showButtonPanel: false, // True to show button panel, false to not show it
			autoSize: false, // True to size the input for the date format, false to leave as is
			disabled: false // The initial disabled state
		};
		$.extend( this._defaults, this.regional[ "" ] );
		this.regional.en = $.extend( true, {}, this.regional[ "" ] );
		this.regional[ "en-US" ] = $.extend( true, {}, this.regional.en );
		this.dpDiv = datepicker_bindHover( $( "<div id='" + this._mainDivId + "' class='ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all'></div>" ) );
	}
	
	$.extend( Datepicker.prototype, {
		/* Class name added to elements to indicate already configured with a date picker. */
		markerClassName: "hasDatepicker",
	
		//Keep track of the maximum number of rows displayed (see #7043)
		maxRows: 4,
	
		// TODO rename to "widget" when switching to widget factory
		_widgetDatepicker: function() {
			return this.dpDiv;
		},
	
		/* Override the default settings for all instances of the date picker.
		 * @param  settings  object - the new settings to use as defaults (anonymous object)
		 * @return the manager object
		 */
		setDefaults: function( settings ) {
			datepicker_extendRemove( this._defaults, settings || {} );
			return this;
		},
	
		/* Attach the date picker to a jQuery selection.
		 * @param  target	element - the target input field or division or span
		 * @param  settings  object - the new settings to use for this date picker instance (anonymous)
		 */
		_attachDatepicker: function( target, settings ) {
			var nodeName, inline, inst;
			nodeName = target.nodeName.toLowerCase();
			inline = ( nodeName === "div" || nodeName === "span" );
			if ( !target.id ) {
				this.uuid += 1;
				target.id = "dp" + this.uuid;
			}
			inst = this._newInst( $( target ), inline );
			inst.settings = $.extend( {}, settings || {} );
			if ( nodeName === "input" ) {
				this._connectDatepicker( target, inst );
			} else if ( inline ) {
				this._inlineDatepicker( target, inst );
			}
		},
	
		/* Create a new instance object. */
		_newInst: function( target, inline ) {
			var id = target[ 0 ].id.replace( /([^A-Za-z0-9_\-])/g, "\\\\$1" ); // escape jQuery meta chars
			return { id: id, input: target, // associated target
				selectedDay: 0, selectedMonth: 0, selectedYear: 0, // current selection
				drawMonth: 0, drawYear: 0, // month being drawn
				inline: inline, // is datepicker inline or not
				dpDiv: ( !inline ? this.dpDiv : // presentation div
				datepicker_bindHover( $( "<div class='" + this._inlineClass + " ui-datepicker ui-widget ui-widget-content ui-helper-clearfix ui-corner-all'></div>" ) ) ) };
		},
	
		/* Attach the date picker to an input field. */
		_connectDatepicker: function( target, inst ) {
			var input = $( target );
			inst.append = $( [] );
			inst.trigger = $( [] );
			if ( input.hasClass( this.markerClassName ) ) {
				return;
			}
			this._attachments( input, inst );
			input.addClass( this.markerClassName ).on( "keydown", this._doKeyDown ).
				on( "keypress", this._doKeyPress ).on( "keyup", this._doKeyUp );
			this._autoSize( inst );
			$.data( target, "datepicker", inst );
	
			//If disabled option is true, disable the datepicker once it has been attached to the input (see ticket #5665)
			if ( inst.settings.disabled ) {
				this._disableDatepicker( target );
			}
		},
	
		/* Make attachments based on settings. */
		_attachments: function( input, inst ) {
			var showOn, buttonText, buttonImage,
				appendText = this._get( inst, "appendText" ),
				isRTL = this._get( inst, "isRTL" );
	
			if ( inst.append ) {
				inst.append.remove();
			}
			if ( appendText ) {
				inst.append = $( "<span class='" + this._appendClass + "'>" + appendText + "</span>" );
				input[ isRTL ? "before" : "after" ]( inst.append );
			}
	
			input.off( "focus", this._showDatepicker );
	
			if ( inst.trigger ) {
				inst.trigger.remove();
			}
	
			showOn = this._get( inst, "showOn" );
			if ( showOn === "focus" || showOn === "both" ) { // pop-up date picker when in the marked field
				input.on( "focus", this._showDatepicker );
			}
			if ( showOn === "button" || showOn === "both" ) { // pop-up date picker when button clicked
				buttonText = this._get( inst, "buttonText" );
				buttonImage = this._get( inst, "buttonImage" );
				inst.trigger = $( this._get( inst, "buttonImageOnly" ) ?
					$( "<img/>" ).addClass( this._triggerClass ).
						attr( { src: buttonImage, alt: buttonText, title: buttonText } ) :
					$( "<button type='button'></button>" ).addClass( this._triggerClass ).
						html( !buttonImage ? buttonText : $( "<img/>" ).attr(
						{ src:buttonImage, alt:buttonText, title:buttonText } ) ) );
				input[ isRTL ? "before" : "after" ]( inst.trigger );
				inst.trigger.on( "click", function() {
					if ( $.datepicker._datepickerShowing && $.datepicker._lastInput === input[ 0 ] ) {
						$.datepicker._hideDatepicker();
					} else if ( $.datepicker._datepickerShowing && $.datepicker._lastInput !== input[ 0 ] ) {
						$.datepicker._hideDatepicker();
						$.datepicker._showDatepicker( input[ 0 ] );
					} else {
						$.datepicker._showDatepicker( input[ 0 ] );
					}
					return false;
				} );
			}
		},
	
		/* Apply the maximum length for the date format. */
		_autoSize: function( inst ) {
			if ( this._get( inst, "autoSize" ) && !inst.inline ) {
				var findMax, max, maxI, i,
					date = new Date( 2009, 12 - 1, 20 ), // Ensure double digits
					dateFormat = this._get( inst, "dateFormat" );
	
				if ( dateFormat.match( /[DM]/ ) ) {
					findMax = function( names ) {
						max = 0;
						maxI = 0;
						for ( i = 0; i < names.length; i++ ) {
							if ( names[ i ].length > max ) {
								max = names[ i ].length;
								maxI = i;
							}
						}
						return maxI;
					};
					date.setMonth( findMax( this._get( inst, ( dateFormat.match( /MM/ ) ?
						"monthNames" : "monthNamesShort" ) ) ) );
					date.setDate( findMax( this._get( inst, ( dateFormat.match( /DD/ ) ?
						"dayNames" : "dayNamesShort" ) ) ) + 20 - date.getDay() );
				}
				inst.input.attr( "size", this._formatDate( inst, date ).length );
			}
		},
	
		/* Attach an inline date picker to a div. */
		_inlineDatepicker: function( target, inst ) {
			var divSpan = $( target );
			if ( divSpan.hasClass( this.markerClassName ) ) {
				return;
			}
			divSpan.addClass( this.markerClassName ).append( inst.dpDiv );
			$.data( target, "datepicker", inst );
			this._setDate( inst, this._getDefaultDate( inst ), true );
			this._updateDatepicker( inst );
			this._updateAlternate( inst );
	
			//If disabled option is true, disable the datepicker before showing it (see ticket #5665)
			if ( inst.settings.disabled ) {
				this._disableDatepicker( target );
			}
	
			// Set display:block in place of inst.dpDiv.show() which won't work on disconnected elements
			// http://bugs.jqueryui.com/ticket/7552 - A Datepicker created on a detached div has zero height
			inst.dpDiv.css( "display", "block" );
		},
	
		/* Pop-up the date picker in a "dialog" box.
		 * @param  input element - ignored
		 * @param  date	string or Date - the initial date to display
		 * @param  onSelect  function - the function to call when a date is selected
		 * @param  settings  object - update the dialog date picker instance's settings (anonymous object)
		 * @param  pos int[2] - coordinates for the dialog's position within the screen or
		 *					event - with x/y coordinates or
		 *					leave empty for default (screen centre)
		 * @return the manager object
		 */
		_dialogDatepicker: function( input, date, onSelect, settings, pos ) {
			var id, browserWidth, browserHeight, scrollX, scrollY,
				inst = this._dialogInst; // internal instance
	
			if ( !inst ) {
				this.uuid += 1;
				id = "dp" + this.uuid;
				this._dialogInput = $( "<input type='text' id='" + id +
					"' style='position: absolute; top: -100px; width: 0px;'/>" );
				this._dialogInput.on( "keydown", this._doKeyDown );
				$( "body" ).append( this._dialogInput );
				inst = this._dialogInst = this._newInst( this._dialogInput, false );
				inst.settings = {};
				$.data( this._dialogInput[ 0 ], "datepicker", inst );
			}
			datepicker_extendRemove( inst.settings, settings || {} );
			date = ( date && date.constructor === Date ? this._formatDate( inst, date ) : date );
			this._dialogInput.val( date );
	
			this._pos = ( pos ? ( pos.length ? pos : [ pos.pageX, pos.pageY ] ) : null );
			if ( !this._pos ) {
				browserWidth = document.documentElement.clientWidth;
				browserHeight = document.documentElement.clientHeight;
				scrollX = document.documentElement.scrollLeft || document.body.scrollLeft;
				scrollY = document.documentElement.scrollTop || document.body.scrollTop;
				this._pos = // should use actual width/height below
					[ ( browserWidth / 2 ) - 100 + scrollX, ( browserHeight / 2 ) - 150 + scrollY ];
			}
	
			// Move input on screen for focus, but hidden behind dialog
			this._dialogInput.css( "left", ( this._pos[ 0 ] + 20 ) + "px" ).css( "top", this._pos[ 1 ] + "px" );
			inst.settings.onSelect = onSelect;
			this._inDialog = true;
			this.dpDiv.addClass( this._dialogClass );
			this._showDatepicker( this._dialogInput[ 0 ] );
			if ( $.blockUI ) {
				$.blockUI( this.dpDiv );
			}
			$.data( this._dialogInput[ 0 ], "datepicker", inst );
			return this;
		},
	
		/* Detach a datepicker from its control.
		 * @param  target	element - the target input field or division or span
		 */
		_destroyDatepicker: function( target ) {
			var nodeName,
				$target = $( target ),
				inst = $.data( target, "datepicker" );
	
			if ( !$target.hasClass( this.markerClassName ) ) {
				return;
			}
	
			nodeName = target.nodeName.toLowerCase();
			$.removeData( target, "datepicker" );
			if ( nodeName === "input" ) {
				inst.append.remove();
				inst.trigger.remove();
				$target.removeClass( this.markerClassName ).
					off( "focus", this._showDatepicker ).
					off( "keydown", this._doKeyDown ).
					off( "keypress", this._doKeyPress ).
					off( "keyup", this._doKeyUp );
			} else if ( nodeName === "div" || nodeName === "span" ) {
				$target.removeClass( this.markerClassName ).empty();
			}
	
			if ( datepicker_instActive === inst ) {
				datepicker_instActive = null;
			}
		},
	
		/* Enable the date picker to a jQuery selection.
		 * @param  target	element - the target input field or division or span
		 */
		_enableDatepicker: function( target ) {
			var nodeName, inline,
				$target = $( target ),
				inst = $.data( target, "datepicker" );
	
			if ( !$target.hasClass( this.markerClassName ) ) {
				return;
			}
	
			nodeName = target.nodeName.toLowerCase();
			if ( nodeName === "input" ) {
				target.disabled = false;
				inst.trigger.filter( "button" ).
					each( function() { this.disabled = false; } ).end().
					filter( "img" ).css( { opacity: "1.0", cursor: "" } );
			} else if ( nodeName === "div" || nodeName === "span" ) {
				inline = $target.children( "." + this._inlineClass );
				inline.children().removeClass( "ui-state-disabled" );
				inline.find( "select.ui-datepicker-month, select.ui-datepicker-year" ).
					prop( "disabled", false );
			}
			this._disabledInputs = $.map( this._disabledInputs,
				function( value ) { return ( value === target ? null : value ); } ); // delete entry
		},
	
		/* Disable the date picker to a jQuery selection.
		 * @param  target	element - the target input field or division or span
		 */
		_disableDatepicker: function( target ) {
			var nodeName, inline,
				$target = $( target ),
				inst = $.data( target, "datepicker" );
	
			if ( !$target.hasClass( this.markerClassName ) ) {
				return;
			}
	
			nodeName = target.nodeName.toLowerCase();
			if ( nodeName === "input" ) {
				target.disabled = true;
				inst.trigger.filter( "button" ).
					each( function() { this.disabled = true; } ).end().
					filter( "img" ).css( { opacity: "0.5", cursor: "default" } );
			} else if ( nodeName === "div" || nodeName === "span" ) {
				inline = $target.children( "." + this._inlineClass );
				inline.children().addClass( "ui-state-disabled" );
				inline.find( "select.ui-datepicker-month, select.ui-datepicker-year" ).
					prop( "disabled", true );
			}
			this._disabledInputs = $.map( this._disabledInputs,
				function( value ) { return ( value === target ? null : value ); } ); // delete entry
			this._disabledInputs[ this._disabledInputs.length ] = target;
		},
	
		/* Is the first field in a jQuery collection disabled as a datepicker?
		 * @param  target	element - the target input field or division or span
		 * @return boolean - true if disabled, false if enabled
		 */
		_isDisabledDatepicker: function( target ) {
			if ( !target ) {
				return false;
			}
			for ( var i = 0; i < this._disabledInputs.length; i++ ) {
				if ( this._disabledInputs[ i ] === target ) {
					return true;
				}
			}
			return false;
		},
	
		/* Retrieve the instance data for the target control.
		 * @param  target  element - the target input field or division or span
		 * @return  object - the associated instance data
		 * @throws  error if a jQuery problem getting data
		 */
		_getInst: function( target ) {
			try {
				return $.data( target, "datepicker" );
			}
			catch ( err ) {
				throw "Missing instance data for this datepicker";
			}
		},
	
		/* Update or retrieve the settings for a date picker attached to an input field or division.
		 * @param  target  element - the target input field or division or span
		 * @param  name	object - the new settings to update or
		 *				string - the name of the setting to change or retrieve,
		 *				when retrieving also "all" for all instance settings or
		 *				"defaults" for all global defaults
		 * @param  value   any - the new value for the setting
		 *				(omit if above is an object or to retrieve a value)
		 */
		_optionDatepicker: function( target, name, value ) {
			var settings, date, minDate, maxDate,
				inst = this._getInst( target );
	
			if ( arguments.length === 2 && typeof name === "string" ) {
				return ( name === "defaults" ? $.extend( {}, $.datepicker._defaults ) :
					( inst ? ( name === "all" ? $.extend( {}, inst.settings ) :
					this._get( inst, name ) ) : null ) );
			}
	
			settings = name || {};
			if ( typeof name === "string" ) {
				settings = {};
				settings[ name ] = value;
			}
	
			if ( inst ) {
				if ( this._curInst === inst ) {
					this._hideDatepicker();
				}
	
				date = this._getDateDatepicker( target, true );
				minDate = this._getMinMaxDate( inst, "min" );
				maxDate = this._getMinMaxDate( inst, "max" );
				datepicker_extendRemove( inst.settings, settings );
	
				// reformat the old minDate/maxDate values if dateFormat changes and a new minDate/maxDate isn't provided
				if ( minDate !== null && settings.dateFormat !== undefined && settings.minDate === undefined ) {
					inst.settings.minDate = this._formatDate( inst, minDate );
				}
				if ( maxDate !== null && settings.dateFormat !== undefined && settings.maxDate === undefined ) {
					inst.settings.maxDate = this._formatDate( inst, maxDate );
				}
				if ( "disabled" in settings ) {
					if ( settings.disabled ) {
						this._disableDatepicker( target );
					} else {
						this._enableDatepicker( target );
					}
				}
				this._attachments( $( target ), inst );
				this._autoSize( inst );
				this._setDate( inst, date );
				this._updateAlternate( inst );
				this._updateDatepicker( inst );
			}
		},
	
		// Change method deprecated
		_changeDatepicker: function( target, name, value ) {
			this._optionDatepicker( target, name, value );
		},
	
		/* Redraw the date picker attached to an input field or division.
		 * @param  target  element - the target input field or division or span
		 */
		_refreshDatepicker: function( target ) {
			var inst = this._getInst( target );
			if ( inst ) {
				this._updateDatepicker( inst );
			}
		},
	
		/* Set the dates for a jQuery selection.
		 * @param  target element - the target input field or division or span
		 * @param  date	Date - the new date
		 */
		_setDateDatepicker: function( target, date ) {
			var inst = this._getInst( target );
			if ( inst ) {
				this._setDate( inst, date );
				this._updateDatepicker( inst );
				this._updateAlternate( inst );
			}
		},
	
		/* Get the date(s) for the first entry in a jQuery selection.
		 * @param  target element - the target input field or division or span
		 * @param  noDefault boolean - true if no default date is to be used
		 * @return Date - the current date
		 */
		_getDateDatepicker: function( target, noDefault ) {
			var inst = this._getInst( target );
			if ( inst && !inst.inline ) {
				this._setDateFromField( inst, noDefault );
			}
			return ( inst ? this._getDate( inst ) : null );
		},
	
		/* Handle keystrokes. */
		_doKeyDown: function( event ) {
			var onSelect, dateStr, sel,
				inst = $.datepicker._getInst( event.target ),
				handled = true,
				isRTL = inst.dpDiv.is( ".ui-datepicker-rtl" );
	
			inst._keyEvent = true;
			if ( $.datepicker._datepickerShowing ) {
				switch ( event.keyCode ) {
					case 9: $.datepicker._hideDatepicker();
							handled = false;
							break; // hide on tab out
					case 13: sel = $( "td." + $.datepicker._dayOverClass + ":not(." +
										$.datepicker._currentClass + ")", inst.dpDiv );
							if ( sel[ 0 ] ) {
								$.datepicker._selectDay( event.target, inst.selectedMonth, inst.selectedYear, sel[ 0 ] );
							}
	
							onSelect = $.datepicker._get( inst, "onSelect" );
							if ( onSelect ) {
								dateStr = $.datepicker._formatDate( inst );
	
								// Trigger custom callback
								onSelect.apply( ( inst.input ? inst.input[ 0 ] : null ), [ dateStr, inst ] );
							} else {
								$.datepicker._hideDatepicker();
							}
	
							return false; // don't submit the form
					case 27: $.datepicker._hideDatepicker();
							break; // hide on escape
					case 33: $.datepicker._adjustDate( event.target, ( event.ctrlKey ?
								-$.datepicker._get( inst, "stepBigMonths" ) :
								-$.datepicker._get( inst, "stepMonths" ) ), "M" );
							break; // previous month/year on page up/+ ctrl
					case 34: $.datepicker._adjustDate( event.target, ( event.ctrlKey ?
								+$.datepicker._get( inst, "stepBigMonths" ) :
								+$.datepicker._get( inst, "stepMonths" ) ), "M" );
							break; // next month/year on page down/+ ctrl
					case 35: if ( event.ctrlKey || event.metaKey ) {
								$.datepicker._clearDate( event.target );
							}
							handled = event.ctrlKey || event.metaKey;
							break; // clear on ctrl or command +end
					case 36: if ( event.ctrlKey || event.metaKey ) {
								$.datepicker._gotoToday( event.target );
							}
							handled = event.ctrlKey || event.metaKey;
							break; // current on ctrl or command +home
					case 37: if ( event.ctrlKey || event.metaKey ) {
								$.datepicker._adjustDate( event.target, ( isRTL ? +1 : -1 ), "D" );
							}
							handled = event.ctrlKey || event.metaKey;
	
							// -1 day on ctrl or command +left
							if ( event.originalEvent.altKey ) {
								$.datepicker._adjustDate( event.target, ( event.ctrlKey ?
									-$.datepicker._get( inst, "stepBigMonths" ) :
									-$.datepicker._get( inst, "stepMonths" ) ), "M" );
							}
	
							// next month/year on alt +left on Mac
							break;
					case 38: if ( event.ctrlKey || event.metaKey ) {
								$.datepicker._adjustDate( event.target, -7, "D" );
							}
							handled = event.ctrlKey || event.metaKey;
							break; // -1 week on ctrl or command +up
					case 39: if ( event.ctrlKey || event.metaKey ) {
								$.datepicker._adjustDate( event.target, ( isRTL ? -1 : +1 ), "D" );
							}
							handled = event.ctrlKey || event.metaKey;
	
							// +1 day on ctrl or command +right
							if ( event.originalEvent.altKey ) {
								$.datepicker._adjustDate( event.target, ( event.ctrlKey ?
									+$.datepicker._get( inst, "stepBigMonths" ) :
									+$.datepicker._get( inst, "stepMonths" ) ), "M" );
							}
	
							// next month/year on alt +right
							break;
					case 40: if ( event.ctrlKey || event.metaKey ) {
								$.datepicker._adjustDate( event.target, +7, "D" );
							}
							handled = event.ctrlKey || event.metaKey;
							break; // +1 week on ctrl or command +down
					default: handled = false;
				}
			} else if ( event.keyCode === 36 && event.ctrlKey ) { // display the date picker on ctrl+home
				$.datepicker._showDatepicker( this );
			} else {
				handled = false;
			}
	
			if ( handled ) {
				event.preventDefault();
				event.stopPropagation();
			}
		},
	
		/* Filter entered characters - based on date format. */
		_doKeyPress: function( event ) {
			var chars, chr,
				inst = $.datepicker._getInst( event.target );
	
			if ( $.datepicker._get( inst, "constrainInput" ) ) {
				chars = $.datepicker._possibleChars( $.datepicker._get( inst, "dateFormat" ) );
				chr = String.fromCharCode( event.charCode == null ? event.keyCode : event.charCode );
				return event.ctrlKey || event.metaKey || ( chr < " " || !chars || chars.indexOf( chr ) > -1 );
			}
		},
	
		/* Synchronise manual entry and field/alternate field. */
		_doKeyUp: function( event ) {
			var date,
				inst = $.datepicker._getInst( event.target );
	
			if ( inst.input.val() !== inst.lastVal ) {
				try {
					date = $.datepicker.parseDate( $.datepicker._get( inst, "dateFormat" ),
						( inst.input ? inst.input.val() : null ),
						$.datepicker._getFormatConfig( inst ) );
	
					if ( date ) { // only if valid
						$.datepicker._setDateFromField( inst );
						$.datepicker._updateAlternate( inst );
						$.datepicker._updateDatepicker( inst );
					}
				}
				catch ( err ) {
				}
			}
			return true;
		},
	
		/* Pop-up the date picker for a given input field.
		 * If false returned from beforeShow event handler do not show.
		 * @param  input  element - the input field attached to the date picker or
		 *					event - if triggered by focus
		 */
		_showDatepicker: function( input ) {
			input = input.target || input;
			if ( input.nodeName.toLowerCase() !== "input" ) { // find from button/image trigger
				input = $( "input", input.parentNode )[ 0 ];
			}
	
			if ( $.datepicker._isDisabledDatepicker( input ) || $.datepicker._lastInput === input ) { // already here
				return;
			}
	
			var inst, beforeShow, beforeShowSettings, isFixed,
				offset, showAnim, duration;
	
			inst = $.datepicker._getInst( input );
			if ( $.datepicker._curInst && $.datepicker._curInst !== inst ) {
				$.datepicker._curInst.dpDiv.stop( true, true );
				if ( inst && $.datepicker._datepickerShowing ) {
					$.datepicker._hideDatepicker( $.datepicker._curInst.input[ 0 ] );
				}
			}
	
			beforeShow = $.datepicker._get( inst, "beforeShow" );
			beforeShowSettings = beforeShow ? beforeShow.apply( input, [ input, inst ] ) : {};
			if ( beforeShowSettings === false ) {
				return;
			}
			datepicker_extendRemove( inst.settings, beforeShowSettings );
	
			inst.lastVal = null;
			$.datepicker._lastInput = input;
			$.datepicker._setDateFromField( inst );
	
			if ( $.datepicker._inDialog ) { // hide cursor
				input.value = "";
			}
			if ( !$.datepicker._pos ) { // position below input
				$.datepicker._pos = $.datepicker._findPos( input );
				$.datepicker._pos[ 1 ] += input.offsetHeight; // add the height
			}
	
			isFixed = false;
			$( input ).parents().each( function() {
				isFixed |= $( this ).css( "position" ) === "fixed";
				return !isFixed;
			} );
	
			offset = { left: $.datepicker._pos[ 0 ], top: $.datepicker._pos[ 1 ] };
			$.datepicker._pos = null;
	
			//to avoid flashes on Firefox
			inst.dpDiv.empty();
	
			// determine sizing offscreen
			inst.dpDiv.css( { position: "absolute", display: "block", top: "-1000px" } );
			$.datepicker._updateDatepicker( inst );
	
			// fix width for dynamic number of date pickers
			// and adjust position before showing
			offset = $.datepicker._checkOffset( inst, offset, isFixed );
			inst.dpDiv.css( { position: ( $.datepicker._inDialog && $.blockUI ?
				"static" : ( isFixed ? "fixed" : "absolute" ) ), display: "none",
				left: offset.left + "px", top: offset.top + "px" } );
	
			if ( !inst.inline ) {
				showAnim = $.datepicker._get( inst, "showAnim" );
				duration = $.datepicker._get( inst, "duration" );
				inst.dpDiv.css( "z-index", datepicker_getZindex( $( input ) ) + 1 );
				$.datepicker._datepickerShowing = true;
	
				if ( $.effects && $.effects.effect[ showAnim ] ) {
					inst.dpDiv.show( showAnim, $.datepicker._get( inst, "showOptions" ), duration );
				} else {
					inst.dpDiv[ showAnim || "show" ]( showAnim ? duration : null );
				}
	
				if ( $.datepicker._shouldFocusInput( inst ) ) {
					inst.input.trigger( "focus" );
				}
	
				$.datepicker._curInst = inst;
			}
		},
	
		/* Generate the date picker content. */
		_updateDatepicker: function( inst ) {
			this.maxRows = 4; //Reset the max number of rows being displayed (see #7043)
			datepicker_instActive = inst; // for delegate hover events
			inst.dpDiv.empty().append( this._generateHTML( inst ) );
			this._attachHandlers( inst );
	
			var origyearshtml,
				numMonths = this._getNumberOfMonths( inst ),
				cols = numMonths[ 1 ],
				width = 17,
				activeCell = inst.dpDiv.find( "." + this._dayOverClass + " a" );
	
			if ( activeCell.length > 0 ) {
				datepicker_handleMouseover.apply( activeCell.get( 0 ) );
			}
	
			inst.dpDiv.removeClass( "ui-datepicker-multi-2 ui-datepicker-multi-3 ui-datepicker-multi-4" ).width( "" );
			if ( cols > 1 ) {
				inst.dpDiv.addClass( "ui-datepicker-multi-" + cols ).css( "width", ( width * cols ) + "em" );
			}
			inst.dpDiv[ ( numMonths[ 0 ] !== 1 || numMonths[ 1 ] !== 1 ? "add" : "remove" ) +
				"Class" ]( "ui-datepicker-multi" );
			inst.dpDiv[ ( this._get( inst, "isRTL" ) ? "add" : "remove" ) +
				"Class" ]( "ui-datepicker-rtl" );
	
			if ( inst === $.datepicker._curInst && $.datepicker._datepickerShowing && $.datepicker._shouldFocusInput( inst ) ) {
				inst.input.trigger( "focus" );
			}
	
			// Deffered render of the years select (to avoid flashes on Firefox)
			if ( inst.yearshtml ) {
				origyearshtml = inst.yearshtml;
				setTimeout( function() {
	
					//assure that inst.yearshtml didn't change.
					if ( origyearshtml === inst.yearshtml && inst.yearshtml ) {
						inst.dpDiv.find( "select.ui-datepicker-year:first" ).replaceWith( inst.yearshtml );
					}
					origyearshtml = inst.yearshtml = null;
				}, 0 );
			}
		},
	
		// #6694 - don't focus the input if it's already focused
		// this breaks the change event in IE
		// Support: IE and jQuery <1.9
		_shouldFocusInput: function( inst ) {
			return inst.input && inst.input.is( ":visible" ) && !inst.input.is( ":disabled" ) && !inst.input.is( ":focus" );
		},
	
		/* Check positioning to remain on screen. */
		_checkOffset: function( inst, offset, isFixed ) {
			var dpWidth = inst.dpDiv.outerWidth(),
				dpHeight = inst.dpDiv.outerHeight(),
				inputWidth = inst.input ? inst.input.outerWidth() : 0,
				inputHeight = inst.input ? inst.input.outerHeight() : 0,
				viewWidth = document.documentElement.clientWidth + ( isFixed ? 0 : $( document ).scrollLeft() ),
				viewHeight = document.documentElement.clientHeight + ( isFixed ? 0 : $( document ).scrollTop() );
	
			offset.left -= ( this._get( inst, "isRTL" ) ? ( dpWidth - inputWidth ) : 0 );
			offset.left -= ( isFixed && offset.left === inst.input.offset().left ) ? $( document ).scrollLeft() : 0;
			offset.top -= ( isFixed && offset.top === ( inst.input.offset().top + inputHeight ) ) ? $( document ).scrollTop() : 0;
	
			// Now check if datepicker is showing outside window viewport - move to a better place if so.
			offset.left -= Math.min( offset.left, ( offset.left + dpWidth > viewWidth && viewWidth > dpWidth ) ?
				Math.abs( offset.left + dpWidth - viewWidth ) : 0 );
			offset.top -= Math.min( offset.top, ( offset.top + dpHeight > viewHeight && viewHeight > dpHeight ) ?
				Math.abs( dpHeight + inputHeight ) : 0 );
	
			return offset;
		},
	
		/* Find an object's position on the screen. */
		_findPos: function( obj ) {
			var position,
				inst = this._getInst( obj ),
				isRTL = this._get( inst, "isRTL" );
	
			while ( obj && ( obj.type === "hidden" || obj.nodeType !== 1 || $.expr.filters.hidden( obj ) ) ) {
				obj = obj[ isRTL ? "previousSibling" : "nextSibling" ];
			}
	
			position = $( obj ).offset();
			return [ position.left, position.top ];
		},
	
		/* Hide the date picker from view.
		 * @param  input  element - the input field attached to the date picker
		 */
		_hideDatepicker: function( input ) {
			var showAnim, duration, postProcess, onClose,
				inst = this._curInst;
	
			if ( !inst || ( input && inst !== $.data( input, "datepicker" ) ) ) {
				return;
			}
	
			if ( this._datepickerShowing ) {
				showAnim = this._get( inst, "showAnim" );
				duration = this._get( inst, "duration" );
				postProcess = function() {
					$.datepicker._tidyDialog( inst );
				};
	
				// DEPRECATED: after BC for 1.8.x $.effects[ showAnim ] is not needed
				if ( $.effects && ( $.effects.effect[ showAnim ] || $.effects[ showAnim ] ) ) {
					inst.dpDiv.hide( showAnim, $.datepicker._get( inst, "showOptions" ), duration, postProcess );
				} else {
					inst.dpDiv[ ( showAnim === "slideDown" ? "slideUp" :
						( showAnim === "fadeIn" ? "fadeOut" : "hide" ) ) ]( ( showAnim ? duration : null ), postProcess );
				}
	
				if ( !showAnim ) {
					postProcess();
				}
				this._datepickerShowing = false;
	
				onClose = this._get( inst, "onClose" );
				if ( onClose ) {
					onClose.apply( ( inst.input ? inst.input[ 0 ] : null ), [ ( inst.input ? inst.input.val() : "" ), inst ] );
				}
	
				this._lastInput = null;
				if ( this._inDialog ) {
					this._dialogInput.css( { position: "absolute", left: "0", top: "-100px" } );
					if ( $.blockUI ) {
						$.unblockUI();
						$( "body" ).append( this.dpDiv );
					}
				}
				this._inDialog = false;
			}
		},
	
		/* Tidy up after a dialog display. */
		_tidyDialog: function( inst ) {
			inst.dpDiv.removeClass( this._dialogClass ).off( ".ui-datepicker-calendar" );
		},
	
		/* Close date picker if clicked elsewhere. */
		_checkExternalClick: function( event ) {
			if ( !$.datepicker._curInst ) {
				return;
			}
	
			var $target = $( event.target ),
				inst = $.datepicker._getInst( $target[ 0 ] );
	
			if ( ( ( $target[ 0 ].id !== $.datepicker._mainDivId &&
					$target.parents( "#" + $.datepicker._mainDivId ).length === 0 &&
					!$target.hasClass( $.datepicker.markerClassName ) &&
					!$target.closest( "." + $.datepicker._triggerClass ).length &&
					$.datepicker._datepickerShowing && !( $.datepicker._inDialog && $.blockUI ) ) ) ||
				( $target.hasClass( $.datepicker.markerClassName ) && $.datepicker._curInst !== inst ) ) {
					$.datepicker._hideDatepicker();
			}
		},
	
		/* Adjust one of the date sub-fields. */
		_adjustDate: function( id, offset, period ) {
			var target = $( id ),
				inst = this._getInst( target[ 0 ] );
	
			if ( this._isDisabledDatepicker( target[ 0 ] ) ) {
				return;
			}
			this._adjustInstDate( inst, offset +
				( period === "M" ? this._get( inst, "showCurrentAtPos" ) : 0 ), // undo positioning
				period );
			this._updateDatepicker( inst );
		},
	
		/* Action for current link. */
		_gotoToday: function( id ) {
			var date,
				target = $( id ),
				inst = this._getInst( target[ 0 ] );
	
			if ( this._get( inst, "gotoCurrent" ) && inst.currentDay ) {
				inst.selectedDay = inst.currentDay;
				inst.drawMonth = inst.selectedMonth = inst.currentMonth;
				inst.drawYear = inst.selectedYear = inst.currentYear;
			} else {
				date = new Date();
				inst.selectedDay = date.getDate();
				inst.drawMonth = inst.selectedMonth = date.getMonth();
				inst.drawYear = inst.selectedYear = date.getFullYear();
			}
			this._notifyChange( inst );
			this._adjustDate( target );
		},
	
		/* Action for selecting a new month/year. */
		_selectMonthYear: function( id, select, period ) {
			var target = $( id ),
				inst = this._getInst( target[ 0 ] );
	
			inst[ "selected" + ( period === "M" ? "Month" : "Year" ) ] =
			inst[ "draw" + ( period === "M" ? "Month" : "Year" ) ] =
				parseInt( select.options[ select.selectedIndex ].value, 10 );
	
			this._notifyChange( inst );
			this._adjustDate( target );
		},
	
		/* Action for selecting a day. */
		_selectDay: function( id, month, year, td ) {
			var inst,
				target = $( id );
	
			if ( $( td ).hasClass( this._unselectableClass ) || this._isDisabledDatepicker( target[ 0 ] ) ) {
				return;
			}
	
			inst = this._getInst( target[ 0 ] );
			inst.selectedDay = inst.currentDay = $( "a", td ).html();
			inst.selectedMonth = inst.currentMonth = month;
			inst.selectedYear = inst.currentYear = year;
			this._selectDate( id, this._formatDate( inst,
				inst.currentDay, inst.currentMonth, inst.currentYear ) );
		},
	
		/* Erase the input field and hide the date picker. */
		_clearDate: function( id ) {
			var target = $( id );
			this._selectDate( target, "" );
		},
	
		/* Update the input field with the selected date. */
		_selectDate: function( id, dateStr ) {
			var onSelect,
				target = $( id ),
				inst = this._getInst( target[ 0 ] );
	
			dateStr = ( dateStr != null ? dateStr : this._formatDate( inst ) );
			if ( inst.input ) {
				inst.input.val( dateStr );
			}
			this._updateAlternate( inst );
	
			onSelect = this._get( inst, "onSelect" );
			if ( onSelect ) {
				onSelect.apply( ( inst.input ? inst.input[ 0 ] : null ), [ dateStr, inst ] );  // trigger custom callback
			} else if ( inst.input ) {
				inst.input.trigger( "change" ); // fire the change event
			}
	
			if ( inst.inline ) {
				this._updateDatepicker( inst );
			} else {
				this._hideDatepicker();
				this._lastInput = inst.input[ 0 ];
				if ( typeof( inst.input[ 0 ] ) !== "object" ) {
					inst.input.trigger( "focus" ); // restore focus
				}
				this._lastInput = null;
			}
		},
	
		/* Update any alternate field to synchronise with the main field. */
		_updateAlternate: function( inst ) {
			var altFormat, date, dateStr,
				altField = this._get( inst, "altField" );
	
			if ( altField ) { // update alternate field too
				altFormat = this._get( inst, "altFormat" ) || this._get( inst, "dateFormat" );
				date = this._getDate( inst );
				dateStr = this.formatDate( altFormat, date, this._getFormatConfig( inst ) );
				$( altField ).val( dateStr );
			}
		},
	
		/* Set as beforeShowDay function to prevent selection of weekends.
		 * @param  date  Date - the date to customise
		 * @return [boolean, string] - is this date selectable?, what is its CSS class?
		 */
		noWeekends: function( date ) {
			var day = date.getDay();
			return [ ( day > 0 && day < 6 ), "" ];
		},
	
		/* Set as calculateWeek to determine the week of the year based on the ISO 8601 definition.
		 * @param  date  Date - the date to get the week for
		 * @return  number - the number of the week within the year that contains this date
		 */
		iso8601Week: function( date ) {
			var time,
				checkDate = new Date( date.getTime() );
	
			// Find Thursday of this week starting on Monday
			checkDate.setDate( checkDate.getDate() + 4 - ( checkDate.getDay() || 7 ) );
	
			time = checkDate.getTime();
			checkDate.setMonth( 0 ); // Compare with Jan 1
			checkDate.setDate( 1 );
			return Math.floor( Math.round( ( time - checkDate ) / 86400000 ) / 7 ) + 1;
		},
	
		/* Parse a string value into a date object.
		 * See formatDate below for the possible formats.
		 *
		 * @param  format string - the expected format of the date
		 * @param  value string - the date in the above format
		 * @param  settings Object - attributes include:
		 *					shortYearCutoff  number - the cutoff year for determining the century (optional)
		 *					dayNamesShort	string[7] - abbreviated names of the days from Sunday (optional)
		 *					dayNames		string[7] - names of the days from Sunday (optional)
		 *					monthNamesShort string[12] - abbreviated names of the months (optional)
		 *					monthNames		string[12] - names of the months (optional)
		 * @return  Date - the extracted date value or null if value is blank
		 */
		parseDate: function( format, value, settings ) {
			if ( format == null || value == null ) {
				throw "Invalid arguments";
			}
	
			value = ( typeof value === "object" ? value.toString() : value + "" );
			if ( value === "" ) {
				return null;
			}
	
			var iFormat, dim, extra,
				iValue = 0,
				shortYearCutoffTemp = ( settings ? settings.shortYearCutoff : null ) || this._defaults.shortYearCutoff,
				shortYearCutoff = ( typeof shortYearCutoffTemp !== "string" ? shortYearCutoffTemp :
					new Date().getFullYear() % 100 + parseInt( shortYearCutoffTemp, 10 ) ),
				dayNamesShort = ( settings ? settings.dayNamesShort : null ) || this._defaults.dayNamesShort,
				dayNames = ( settings ? settings.dayNames : null ) || this._defaults.dayNames,
				monthNamesShort = ( settings ? settings.monthNamesShort : null ) || this._defaults.monthNamesShort,
				monthNames = ( settings ? settings.monthNames : null ) || this._defaults.monthNames,
				year = -1,
				month = -1,
				day = -1,
				doy = -1,
				literal = false,
				date,
	
				// Check whether a format character is doubled
				lookAhead = function( match ) {
					var matches = ( iFormat + 1 < format.length && format.charAt( iFormat + 1 ) === match );
					if ( matches ) {
						iFormat++;
					}
					return matches;
				},
	
				// Extract a number from the string value
				getNumber = function( match ) {
					var isDoubled = lookAhead( match ),
						size = ( match === "@" ? 14 : ( match === "!" ? 20 :
						( match === "y" && isDoubled ? 4 : ( match === "o" ? 3 : 2 ) ) ) ),
						minSize = ( match === "y" ? size : 1 ),
						digits = new RegExp( "^\\d{" + minSize + "," + size + "}" ),
						num = value.substring( iValue ).match( digits );
					if ( !num ) {
						throw "Missing number at position " + iValue;
					}
					iValue += num[ 0 ].length;
					return parseInt( num[ 0 ], 10 );
				},
	
				// Extract a name from the string value and convert to an index
				getName = function( match, shortNames, longNames ) {
					var index = -1,
						names = $.map( lookAhead( match ) ? longNames : shortNames, function( v, k ) {
							return [ [ k, v ] ];
						} ).sort( function( a, b ) {
							return -( a[ 1 ].length - b[ 1 ].length );
						} );
	
					$.each( names, function( i, pair ) {
						var name = pair[ 1 ];
						if ( value.substr( iValue, name.length ).toLowerCase() === name.toLowerCase() ) {
							index = pair[ 0 ];
							iValue += name.length;
							return false;
						}
					} );
					if ( index !== -1 ) {
						return index + 1;
					} else {
						throw "Unknown name at position " + iValue;
					}
				},
	
				// Confirm that a literal character matches the string value
				checkLiteral = function() {
					if ( value.charAt( iValue ) !== format.charAt( iFormat ) ) {
						throw "Unexpected literal at position " + iValue;
					}
					iValue++;
				};
	
			for ( iFormat = 0; iFormat < format.length; iFormat++ ) {
				if ( literal ) {
					if ( format.charAt( iFormat ) === "'" && !lookAhead( "'" ) ) {
						literal = false;
					} else {
						checkLiteral();
					}
				} else {
					switch ( format.charAt( iFormat ) ) {
						case "d":
							day = getNumber( "d" );
							break;
						case "D":
							getName( "D", dayNamesShort, dayNames );
							break;
						case "o":
							doy = getNumber( "o" );
							break;
						case "m":
							month = getNumber( "m" );
							break;
						case "M":
							month = getName( "M", monthNamesShort, monthNames );
							break;
						case "y":
							year = getNumber( "y" );
							break;
						case "@":
							date = new Date( getNumber( "@" ) );
							year = date.getFullYear();
							month = date.getMonth() + 1;
							day = date.getDate();
							break;
						case "!":
							date = new Date( ( getNumber( "!" ) - this._ticksTo1970 ) / 10000 );
							year = date.getFullYear();
							month = date.getMonth() + 1;
							day = date.getDate();
							break;
						case "'":
							if ( lookAhead( "'" ) ) {
								checkLiteral();
							} else {
								literal = true;
							}
							break;
						default:
							checkLiteral();
					}
				}
			}
	
			if ( iValue < value.length ) {
				extra = value.substr( iValue );
				if ( !/^\s+/.test( extra ) ) {
					throw "Extra/unparsed characters found in date: " + extra;
				}
			}
	
			if ( year === -1 ) {
				year = new Date().getFullYear();
			} else if ( year < 100 ) {
				year += new Date().getFullYear() - new Date().getFullYear() % 100 +
					( year <= shortYearCutoff ? 0 : -100 );
			}
	
			if ( doy > -1 ) {
				month = 1;
				day = doy;
				do {
					dim = this._getDaysInMonth( year, month - 1 );
					if ( day <= dim ) {
						break;
					}
					month++;
					day -= dim;
				} while ( true );
			}
	
			date = this._daylightSavingAdjust( new Date( year, month - 1, day ) );
			if ( date.getFullYear() !== year || date.getMonth() + 1 !== month || date.getDate() !== day ) {
				throw "Invalid date"; // E.g. 31/02/00
			}
			return date;
		},
	
		/* Standard date formats. */
		ATOM: "yy-mm-dd", // RFC 3339 (ISO 8601)
		COOKIE: "D, dd M yy",
		ISO_8601: "yy-mm-dd",
		RFC_822: "D, d M y",
		RFC_850: "DD, dd-M-y",
		RFC_1036: "D, d M y",
		RFC_1123: "D, d M yy",
		RFC_2822: "D, d M yy",
		RSS: "D, d M y", // RFC 822
		TICKS: "!",
		TIMESTAMP: "@",
		W3C: "yy-mm-dd", // ISO 8601
	
		_ticksTo1970: ( ( ( 1970 - 1 ) * 365 + Math.floor( 1970 / 4 ) - Math.floor( 1970 / 100 ) +
			Math.floor( 1970 / 400 ) ) * 24 * 60 * 60 * 10000000 ),
	
		/* Format a date object into a string value.
		 * The format can be combinations of the following:
		 * d  - day of month (no leading zero)
		 * dd - day of month (two digit)
		 * o  - day of year (no leading zeros)
		 * oo - day of year (three digit)
		 * D  - day name short
		 * DD - day name long
		 * m  - month of year (no leading zero)
		 * mm - month of year (two digit)
		 * M  - month name short
		 * MM - month name long
		 * y  - year (two digit)
		 * yy - year (four digit)
		 * @ - Unix timestamp (ms since 01/01/1970)
		 * ! - Windows ticks (100ns since 01/01/0001)
		 * "..." - literal text
		 * '' - single quote
		 *
		 * @param  format string - the desired format of the date
		 * @param  date Date - the date value to format
		 * @param  settings Object - attributes include:
		 *					dayNamesShort	string[7] - abbreviated names of the days from Sunday (optional)
		 *					dayNames		string[7] - names of the days from Sunday (optional)
		 *					monthNamesShort string[12] - abbreviated names of the months (optional)
		 *					monthNames		string[12] - names of the months (optional)
		 * @return  string - the date in the above format
		 */
		formatDate: function( format, date, settings ) {
			if ( !date ) {
				return "";
			}
	
			var iFormat,
				dayNamesShort = ( settings ? settings.dayNamesShort : null ) || this._defaults.dayNamesShort,
				dayNames = ( settings ? settings.dayNames : null ) || this._defaults.dayNames,
				monthNamesShort = ( settings ? settings.monthNamesShort : null ) || this._defaults.monthNamesShort,
				monthNames = ( settings ? settings.monthNames : null ) || this._defaults.monthNames,
	
				// Check whether a format character is doubled
				lookAhead = function( match ) {
					var matches = ( iFormat + 1 < format.length && format.charAt( iFormat + 1 ) === match );
					if ( matches ) {
						iFormat++;
					}
					return matches;
				},
	
				// Format a number, with leading zero if necessary
				formatNumber = function( match, value, len ) {
					var num = "" + value;
					if ( lookAhead( match ) ) {
						while ( num.length < len ) {
							num = "0" + num;
						}
					}
					return num;
				},
	
				// Format a name, short or long as requested
				formatName = function( match, value, shortNames, longNames ) {
					return ( lookAhead( match ) ? longNames[ value ] : shortNames[ value ] );
				},
				output = "",
				literal = false;
	
			if ( date ) {
				for ( iFormat = 0; iFormat < format.length; iFormat++ ) {
					if ( literal ) {
						if ( format.charAt( iFormat ) === "'" && !lookAhead( "'" ) ) {
							literal = false;
						} else {
							output += format.charAt( iFormat );
						}
					} else {
						switch ( format.charAt( iFormat ) ) {
							case "d":
								output += formatNumber( "d", date.getDate(), 2 );
								break;
							case "D":
								output += formatName( "D", date.getDay(), dayNamesShort, dayNames );
								break;
							case "o":
								output += formatNumber( "o",
									Math.round( ( new Date( date.getFullYear(), date.getMonth(), date.getDate() ).getTime() - new Date( date.getFullYear(), 0, 0 ).getTime() ) / 86400000 ), 3 );
								break;
							case "m":
								output += formatNumber( "m", date.getMonth() + 1, 2 );
								break;
							case "M":
								output += formatName( "M", date.getMonth(), monthNamesShort, monthNames );
								break;
							case "y":
								output += ( lookAhead( "y" ) ? date.getFullYear() :
									( date.getFullYear() % 100 < 10 ? "0" : "" ) + date.getFullYear() % 100 );
								break;
							case "@":
								output += date.getTime();
								break;
							case "!":
								output += date.getTime() * 10000 + this._ticksTo1970;
								break;
							case "'":
								if ( lookAhead( "'" ) ) {
									output += "'";
								} else {
									literal = true;
								}
								break;
							default:
								output += format.charAt( iFormat );
						}
					}
				}
			}
			return output;
		},
	
		/* Extract all possible characters from the date format. */
		_possibleChars: function( format ) {
			var iFormat,
				chars = "",
				literal = false,
	
				// Check whether a format character is doubled
				lookAhead = function( match ) {
					var matches = ( iFormat + 1 < format.length && format.charAt( iFormat + 1 ) === match );
					if ( matches ) {
						iFormat++;
					}
					return matches;
				};
	
			for ( iFormat = 0; iFormat < format.length; iFormat++ ) {
				if ( literal ) {
					if ( format.charAt( iFormat ) === "'" && !lookAhead( "'" ) ) {
						literal = false;
					} else {
						chars += format.charAt( iFormat );
					}
				} else {
					switch ( format.charAt( iFormat ) ) {
						case "d": case "m": case "y": case "@":
							chars += "0123456789";
							break;
						case "D": case "M":
							return null; // Accept anything
						case "'":
							if ( lookAhead( "'" ) ) {
								chars += "'";
							} else {
								literal = true;
							}
							break;
						default:
							chars += format.charAt( iFormat );
					}
				}
			}
			return chars;
		},
	
		/* Get a setting value, defaulting if necessary. */
		_get: function( inst, name ) {
			return inst.settings[ name ] !== undefined ?
				inst.settings[ name ] : this._defaults[ name ];
		},
	
		/* Parse existing date and initialise date picker. */
		_setDateFromField: function( inst, noDefault ) {
			if ( inst.input.val() === inst.lastVal ) {
				return;
			}
	
			var dateFormat = this._get( inst, "dateFormat" ),
				dates = inst.lastVal = inst.input ? inst.input.val() : null,
				defaultDate = this._getDefaultDate( inst ),
				date = defaultDate,
				settings = this._getFormatConfig( inst );
	
			try {
				date = this.parseDate( dateFormat, dates, settings ) || defaultDate;
			} catch ( event ) {
				dates = ( noDefault ? "" : dates );
			}
			inst.selectedDay = date.getDate();
			inst.drawMonth = inst.selectedMonth = date.getMonth();
			inst.drawYear = inst.selectedYear = date.getFullYear();
			inst.currentDay = ( dates ? date.getDate() : 0 );
			inst.currentMonth = ( dates ? date.getMonth() : 0 );
			inst.currentYear = ( dates ? date.getFullYear() : 0 );
			this._adjustInstDate( inst );
		},
	
		/* Retrieve the default date shown on opening. */
		_getDefaultDate: function( inst ) {
			return this._restrictMinMax( inst,
				this._determineDate( inst, this._get( inst, "defaultDate" ), new Date() ) );
		},
	
		/* A date may be specified as an exact value or a relative one. */
		_determineDate: function( inst, date, defaultDate ) {
			var offsetNumeric = function( offset ) {
					var date = new Date();
					date.setDate( date.getDate() + offset );
					return date;
				},
				offsetString = function( offset ) {
					try {
						return $.datepicker.parseDate( $.datepicker._get( inst, "dateFormat" ),
							offset, $.datepicker._getFormatConfig( inst ) );
					}
					catch ( e ) {
	
						// Ignore
					}
	
					var date = ( offset.toLowerCase().match( /^c/ ) ?
						$.datepicker._getDate( inst ) : null ) || new Date(),
						year = date.getFullYear(),
						month = date.getMonth(),
						day = date.getDate(),
						pattern = /([+\-]?[0-9]+)\s*(d|D|w|W|m|M|y|Y)?/g,
						matches = pattern.exec( offset );
	
					while ( matches ) {
						switch ( matches[ 2 ] || "d" ) {
							case "d" : case "D" :
								day += parseInt( matches[ 1 ], 10 ); break;
							case "w" : case "W" :
								day += parseInt( matches[ 1 ], 10 ) * 7; break;
							case "m" : case "M" :
								month += parseInt( matches[ 1 ], 10 );
								day = Math.min( day, $.datepicker._getDaysInMonth( year, month ) );
								break;
							case "y": case "Y" :
								year += parseInt( matches[ 1 ], 10 );
								day = Math.min( day, $.datepicker._getDaysInMonth( year, month ) );
								break;
						}
						matches = pattern.exec( offset );
					}
					return new Date( year, month, day );
				},
				newDate = ( date == null || date === "" ? defaultDate : ( typeof date === "string" ? offsetString( date ) :
					( typeof date === "number" ? ( isNaN( date ) ? defaultDate : offsetNumeric( date ) ) : new Date( date.getTime() ) ) ) );
	
			newDate = ( newDate && newDate.toString() === "Invalid Date" ? defaultDate : newDate );
			if ( newDate ) {
				newDate.setHours( 0 );
				newDate.setMinutes( 0 );
				newDate.setSeconds( 0 );
				newDate.setMilliseconds( 0 );
			}
			return this._daylightSavingAdjust( newDate );
		},
	
		/* Handle switch to/from daylight saving.
		 * Hours may be non-zero on daylight saving cut-over:
		 * > 12 when midnight changeover, but then cannot generate
		 * midnight datetime, so jump to 1AM, otherwise reset.
		 * @param  date  (Date) the date to check
		 * @return  (Date) the corrected date
		 */
		_daylightSavingAdjust: function( date ) {
			if ( !date ) {
				return null;
			}
			date.setHours( date.getHours() > 12 ? date.getHours() + 2 : 0 );
			return date;
		},
	
		/* Set the date(s) directly. */
		_setDate: function( inst, date, noChange ) {
			var clear = !date,
				origMonth = inst.selectedMonth,
				origYear = inst.selectedYear,
				newDate = this._restrictMinMax( inst, this._determineDate( inst, date, new Date() ) );
	
			inst.selectedDay = inst.currentDay = newDate.getDate();
			inst.drawMonth = inst.selectedMonth = inst.currentMonth = newDate.getMonth();
			inst.drawYear = inst.selectedYear = inst.currentYear = newDate.getFullYear();
			if ( ( origMonth !== inst.selectedMonth || origYear !== inst.selectedYear ) && !noChange ) {
				this._notifyChange( inst );
			}
			this._adjustInstDate( inst );
			if ( inst.input ) {
				inst.input.val( clear ? "" : this._formatDate( inst ) );
			}
		},
	
		/* Retrieve the date(s) directly. */
		_getDate: function( inst ) {
			var startDate = ( !inst.currentYear || ( inst.input && inst.input.val() === "" ) ? null :
				this._daylightSavingAdjust( new Date(
				inst.currentYear, inst.currentMonth, inst.currentDay ) ) );
				return startDate;
		},
	
		/* Attach the onxxx handlers.  These are declared statically so
		 * they work with static code transformers like Caja.
		 */
		_attachHandlers: function( inst ) {
			var stepMonths = this._get( inst, "stepMonths" ),
				id = "#" + inst.id.replace( /\\\\/g, "\\" );
			inst.dpDiv.find( "[data-handler]" ).map( function() {
				var handler = {
					prev: function() {
						$.datepicker._adjustDate( id, -stepMonths, "M" );
					},
					next: function() {
						$.datepicker._adjustDate( id, +stepMonths, "M" );
					},
					hide: function() {
						$.datepicker._hideDatepicker();
					},
					today: function() {
						$.datepicker._gotoToday( id );
					},
					selectDay: function() {
						$.datepicker._selectDay( id, +this.getAttribute( "data-month" ), +this.getAttribute( "data-year" ), this );
						return false;
					},
					selectMonth: function() {
						$.datepicker._selectMonthYear( id, this, "M" );
						return false;
					},
					selectYear: function() {
						$.datepicker._selectMonthYear( id, this, "Y" );
						return false;
					}
				};
				$( this ).on( this.getAttribute( "data-event" ), handler[ this.getAttribute( "data-handler" ) ] );
			} );
		},
	
		/* Generate the HTML for the current state of the date picker. */
		_generateHTML: function( inst ) {
			var maxDraw, prevText, prev, nextText, next, currentText, gotoDate,
				controls, buttonPanel, firstDay, showWeek, dayNames, dayNamesMin,
				monthNames, monthNamesShort, beforeShowDay, showOtherMonths,
				selectOtherMonths, defaultDate, html, dow, row, group, col, selectedDate,
				cornerClass, calender, thead, day, daysInMonth, leadDays, curRows, numRows,
				printDate, dRow, tbody, daySettings, otherMonth, unselectable,
				tempDate = new Date(),
				today = this._daylightSavingAdjust(
					new Date( tempDate.getFullYear(), tempDate.getMonth(), tempDate.getDate() ) ), // clear time
				isRTL = this._get( inst, "isRTL" ),
				showButtonPanel = this._get( inst, "showButtonPanel" ),
				hideIfNoPrevNext = this._get( inst, "hideIfNoPrevNext" ),
				navigationAsDateFormat = this._get( inst, "navigationAsDateFormat" ),
				numMonths = this._getNumberOfMonths( inst ),
				showCurrentAtPos = this._get( inst, "showCurrentAtPos" ),
				stepMonths = this._get( inst, "stepMonths" ),
				isMultiMonth = ( numMonths[ 0 ] !== 1 || numMonths[ 1 ] !== 1 ),
				currentDate = this._daylightSavingAdjust( ( !inst.currentDay ? new Date( 9999, 9, 9 ) :
					new Date( inst.currentYear, inst.currentMonth, inst.currentDay ) ) ),
				minDate = this._getMinMaxDate( inst, "min" ),
				maxDate = this._getMinMaxDate( inst, "max" ),
				drawMonth = inst.drawMonth - showCurrentAtPos,
				drawYear = inst.drawYear;
	
			if ( drawMonth < 0 ) {
				drawMonth += 12;
				drawYear--;
			}
			if ( maxDate ) {
				maxDraw = this._daylightSavingAdjust( new Date( maxDate.getFullYear(),
					maxDate.getMonth() - ( numMonths[ 0 ] * numMonths[ 1 ] ) + 1, maxDate.getDate() ) );
				maxDraw = ( minDate && maxDraw < minDate ? minDate : maxDraw );
				while ( this._daylightSavingAdjust( new Date( drawYear, drawMonth, 1 ) ) > maxDraw ) {
					drawMonth--;
					if ( drawMonth < 0 ) {
						drawMonth = 11;
						drawYear--;
					}
				}
			}
			inst.drawMonth = drawMonth;
			inst.drawYear = drawYear;
	
			prevText = this._get( inst, "prevText" );
			prevText = ( !navigationAsDateFormat ? prevText : this.formatDate( prevText,
				this._daylightSavingAdjust( new Date( drawYear, drawMonth - stepMonths, 1 ) ),
				this._getFormatConfig( inst ) ) );
	
			prev = ( this._canAdjustMonth( inst, -1, drawYear, drawMonth ) ?
				"<a class='ui-datepicker-prev ui-corner-all' data-handler='prev' data-event='click'" +
				" title='" + prevText + "'><span class='ui-icon ui-icon-circle-triangle-" + ( isRTL ? "e" : "w" ) + "'>" + prevText + "</span></a>" :
				( hideIfNoPrevNext ? "" : "<a class='ui-datepicker-prev ui-corner-all ui-state-disabled' title='" + prevText + "'><span class='ui-icon ui-icon-circle-triangle-" + ( isRTL ? "e" : "w" ) + "'>" + prevText + "</span></a>" ) );
	
			nextText = this._get( inst, "nextText" );
			nextText = ( !navigationAsDateFormat ? nextText : this.formatDate( nextText,
				this._daylightSavingAdjust( new Date( drawYear, drawMonth + stepMonths, 1 ) ),
				this._getFormatConfig( inst ) ) );
	
			next = ( this._canAdjustMonth( inst, +1, drawYear, drawMonth ) ?
				"<a class='ui-datepicker-next ui-corner-all' data-handler='next' data-event='click'" +
				" title='" + nextText + "'><span class='ui-icon ui-icon-circle-triangle-" + ( isRTL ? "w" : "e" ) + "'>" + nextText + "</span></a>" :
				( hideIfNoPrevNext ? "" : "<a class='ui-datepicker-next ui-corner-all ui-state-disabled' title='" + nextText + "'><span class='ui-icon ui-icon-circle-triangle-" + ( isRTL ? "w" : "e" ) + "'>" + nextText + "</span></a>" ) );
	
			currentText = this._get( inst, "currentText" );
			gotoDate = ( this._get( inst, "gotoCurrent" ) && inst.currentDay ? currentDate : today );
			currentText = ( !navigationAsDateFormat ? currentText :
				this.formatDate( currentText, gotoDate, this._getFormatConfig( inst ) ) );
	
			controls = ( !inst.inline ? "<button type='button' class='ui-datepicker-close ui-state-default ui-priority-primary ui-corner-all' data-handler='hide' data-event='click'>" +
				this._get( inst, "closeText" ) + "</button>" : "" );
	
			buttonPanel = ( showButtonPanel ) ? "<div class='ui-datepicker-buttonpane ui-widget-content'>" + ( isRTL ? controls : "" ) +
				( this._isInRange( inst, gotoDate ) ? "<button type='button' class='ui-datepicker-current ui-state-default ui-priority-secondary ui-corner-all' data-handler='today' data-event='click'" +
				">" + currentText + "</button>" : "" ) + ( isRTL ? "" : controls ) + "</div>" : "";
	
			firstDay = parseInt( this._get( inst, "firstDay" ), 10 );
			firstDay = ( isNaN( firstDay ) ? 0 : firstDay );
	
			showWeek = this._get( inst, "showWeek" );
			dayNames = this._get( inst, "dayNames" );
			dayNamesMin = this._get( inst, "dayNamesMin" );
			monthNames = this._get( inst, "monthNames" );
			monthNamesShort = this._get( inst, "monthNamesShort" );
			beforeShowDay = this._get( inst, "beforeShowDay" );
			showOtherMonths = this._get( inst, "showOtherMonths" );
			selectOtherMonths = this._get( inst, "selectOtherMonths" );
			defaultDate = this._getDefaultDate( inst );
			html = "";
	
			for ( row = 0; row < numMonths[ 0 ]; row++ ) {
				group = "";
				this.maxRows = 4;
				for ( col = 0; col < numMonths[ 1 ]; col++ ) {
					selectedDate = this._daylightSavingAdjust( new Date( drawYear, drawMonth, inst.selectedDay ) );
					cornerClass = " ui-corner-all";
					calender = "";
					if ( isMultiMonth ) {
						calender += "<div class='ui-datepicker-group";
						if ( numMonths[ 1 ] > 1 ) {
							switch ( col ) {
								case 0: calender += " ui-datepicker-group-first";
									cornerClass = " ui-corner-" + ( isRTL ? "right" : "left" ); break;
								case numMonths[ 1 ] - 1: calender += " ui-datepicker-group-last";
									cornerClass = " ui-corner-" + ( isRTL ? "left" : "right" ); break;
								default: calender += " ui-datepicker-group-middle"; cornerClass = ""; break;
							}
						}
						calender += "'>";
					}
					calender += "<div class='ui-datepicker-header ui-widget-header ui-helper-clearfix" + cornerClass + "'>" +
						( /all|left/.test( cornerClass ) && row === 0 ? ( isRTL ? next : prev ) : "" ) +
						( /all|right/.test( cornerClass ) && row === 0 ? ( isRTL ? prev : next ) : "" ) +
						this._generateMonthYearHeader( inst, drawMonth, drawYear, minDate, maxDate,
						row > 0 || col > 0, monthNames, monthNamesShort ) + // draw month headers
						"</div><table class='ui-datepicker-calendar'><thead>" +
						"<tr>";
					thead = ( showWeek ? "<th class='ui-datepicker-week-col'>" + this._get( inst, "weekHeader" ) + "</th>" : "" );
					for ( dow = 0; dow < 7; dow++ ) { // days of the week
						day = ( dow + firstDay ) % 7;
						thead += "<th scope='col'" + ( ( dow + firstDay + 6 ) % 7 >= 5 ? " class='ui-datepicker-week-end'" : "" ) + ">" +
							"<span title='" + dayNames[ day ] + "'>" + dayNamesMin[ day ] + "</span></th>";
					}
					calender += thead + "</tr></thead><tbody>";
					daysInMonth = this._getDaysInMonth( drawYear, drawMonth );
					if ( drawYear === inst.selectedYear && drawMonth === inst.selectedMonth ) {
						inst.selectedDay = Math.min( inst.selectedDay, daysInMonth );
					}
					leadDays = ( this._getFirstDayOfMonth( drawYear, drawMonth ) - firstDay + 7 ) % 7;
					curRows = Math.ceil( ( leadDays + daysInMonth ) / 7 ); // calculate the number of rows to generate
					numRows = ( isMultiMonth ? this.maxRows > curRows ? this.maxRows : curRows : curRows ); //If multiple months, use the higher number of rows (see #7043)
					this.maxRows = numRows;
					printDate = this._daylightSavingAdjust( new Date( drawYear, drawMonth, 1 - leadDays ) );
					for ( dRow = 0; dRow < numRows; dRow++ ) { // create date picker rows
						calender += "<tr>";
						tbody = ( !showWeek ? "" : "<td class='ui-datepicker-week-col'>" +
							this._get( inst, "calculateWeek" )( printDate ) + "</td>" );
						for ( dow = 0; dow < 7; dow++ ) { // create date picker days
							daySettings = ( beforeShowDay ?
								beforeShowDay.apply( ( inst.input ? inst.input[ 0 ] : null ), [ printDate ] ) : [ true, "" ] );
							otherMonth = ( printDate.getMonth() !== drawMonth );
							unselectable = ( otherMonth && !selectOtherMonths ) || !daySettings[ 0 ] ||
								( minDate && printDate < minDate ) || ( maxDate && printDate > maxDate );
							tbody += "<td class='" +
								( ( dow + firstDay + 6 ) % 7 >= 5 ? " ui-datepicker-week-end" : "" ) + // highlight weekends
								( otherMonth ? " ui-datepicker-other-month" : "" ) + // highlight days from other months
								( ( printDate.getTime() === selectedDate.getTime() && drawMonth === inst.selectedMonth && inst._keyEvent ) || // user pressed key
								( defaultDate.getTime() === printDate.getTime() && defaultDate.getTime() === selectedDate.getTime() ) ?
	
								// or defaultDate is current printedDate and defaultDate is selectedDate
								" " + this._dayOverClass : "" ) + // highlight selected day
								( unselectable ? " " + this._unselectableClass + " ui-state-disabled" : "" ) +  // highlight unselectable days
								( otherMonth && !showOtherMonths ? "" : " " + daySettings[ 1 ] + // highlight custom dates
								( printDate.getTime() === currentDate.getTime() ? " " + this._currentClass : "" ) + // highlight selected day
								( printDate.getTime() === today.getTime() ? " ui-datepicker-today" : "" ) ) + "'" + // highlight today (if different)
								( ( !otherMonth || showOtherMonths ) && daySettings[ 2 ] ? " title='" + daySettings[ 2 ].replace( /'/g, "&#39;" ) + "'" : "" ) + // cell title
								( unselectable ? "" : " data-handler='selectDay' data-event='click' data-month='" + printDate.getMonth() + "' data-year='" + printDate.getFullYear() + "'" ) + ">" + // actions
								( otherMonth && !showOtherMonths ? "&#xa0;" : // display for other months
								( unselectable ? "<span class='ui-state-default'>" + printDate.getDate() + "</span>" : "<a class='ui-state-default" +
								( printDate.getTime() === today.getTime() ? " ui-state-highlight" : "" ) +
								( printDate.getTime() === currentDate.getTime() ? " ui-state-active" : "" ) + // highlight selected day
								( otherMonth ? " ui-priority-secondary" : "" ) + // distinguish dates from other months
								"' href='#'>" + printDate.getDate() + "</a>" ) ) + "</td>"; // display selectable date
							printDate.setDate( printDate.getDate() + 1 );
							printDate = this._daylightSavingAdjust( printDate );
						}
						calender += tbody + "</tr>";
					}
					drawMonth++;
					if ( drawMonth > 11 ) {
						drawMonth = 0;
						drawYear++;
					}
					calender += "</tbody></table>" + ( isMultiMonth ? "</div>" +
								( ( numMonths[ 0 ] > 0 && col === numMonths[ 1 ] - 1 ) ? "<div class='ui-datepicker-row-break'></div>" : "" ) : "" );
					group += calender;
				}
				html += group;
			}
			html += buttonPanel;
			inst._keyEvent = false;
			return html;
		},
	
		/* Generate the month and year header. */
		_generateMonthYearHeader: function( inst, drawMonth, drawYear, minDate, maxDate,
				secondary, monthNames, monthNamesShort ) {
	
			var inMinYear, inMaxYear, month, years, thisYear, determineYear, year, endYear,
				changeMonth = this._get( inst, "changeMonth" ),
				changeYear = this._get( inst, "changeYear" ),
				showMonthAfterYear = this._get( inst, "showMonthAfterYear" ),
				html = "<div class='ui-datepicker-title'>",
				monthHtml = "";
	
			// Month selection
			if ( secondary || !changeMonth ) {
				monthHtml += "<span class='ui-datepicker-month'>" + monthNames[ drawMonth ] + "</span>";
			} else {
				inMinYear = ( minDate && minDate.getFullYear() === drawYear );
				inMaxYear = ( maxDate && maxDate.getFullYear() === drawYear );
				monthHtml += "<select class='ui-datepicker-month' data-handler='selectMonth' data-event='change'>";
				for ( month = 0; month < 12; month++ ) {
					if ( ( !inMinYear || month >= minDate.getMonth() ) && ( !inMaxYear || month <= maxDate.getMonth() ) ) {
						monthHtml += "<option value='" + month + "'" +
							( month === drawMonth ? " selected='selected'" : "" ) +
							">" + monthNamesShort[ month ] + "</option>";
					}
				}
				monthHtml += "</select>";
			}
	
			if ( !showMonthAfterYear ) {
				html += monthHtml + ( secondary || !( changeMonth && changeYear ) ? "&#xa0;" : "" );
			}
	
			// Year selection
			if ( !inst.yearshtml ) {
				inst.yearshtml = "";
				if ( secondary || !changeYear ) {
					html += "<span class='ui-datepicker-year'>" + drawYear + "</span>";
				} else {
	
					// determine range of years to display
					years = this._get( inst, "yearRange" ).split( ":" );
					thisYear = new Date().getFullYear();
					determineYear = function( value ) {
						var year = ( value.match( /c[+\-].*/ ) ? drawYear + parseInt( value.substring( 1 ), 10 ) :
							( value.match( /[+\-].*/ ) ? thisYear + parseInt( value, 10 ) :
							parseInt( value, 10 ) ) );
						return ( isNaN( year ) ? thisYear : year );
					};
					year = determineYear( years[ 0 ] );
					endYear = Math.max( year, determineYear( years[ 1 ] || "" ) );
					year = ( minDate ? Math.max( year, minDate.getFullYear() ) : year );
					endYear = ( maxDate ? Math.min( endYear, maxDate.getFullYear() ) : endYear );
					inst.yearshtml += "<select class='ui-datepicker-year' data-handler='selectYear' data-event='change'>";
					for ( ; year <= endYear; year++ ) {
						inst.yearshtml += "<option value='" + year + "'" +
							( year === drawYear ? " selected='selected'" : "" ) +
							">" + year + "</option>";
					}
					inst.yearshtml += "</select>";
	
					html += inst.yearshtml;
					inst.yearshtml = null;
				}
			}
	
			html += this._get( inst, "yearSuffix" );
			if ( showMonthAfterYear ) {
				html += ( secondary || !( changeMonth && changeYear ) ? "&#xa0;" : "" ) + monthHtml;
			}
			html += "</div>"; // Close datepicker_header
			return html;
		},
	
		/* Adjust one of the date sub-fields. */
		_adjustInstDate: function( inst, offset, period ) {
			var year = inst.selectedYear + ( period === "Y" ? offset : 0 ),
				month = inst.selectedMonth + ( period === "M" ? offset : 0 ),
				day = Math.min( inst.selectedDay, this._getDaysInMonth( year, month ) ) + ( period === "D" ? offset : 0 ),
				date = this._restrictMinMax( inst, this._daylightSavingAdjust( new Date( year, month, day ) ) );
	
			inst.selectedDay = date.getDate();
			inst.drawMonth = inst.selectedMonth = date.getMonth();
			inst.drawYear = inst.selectedYear = date.getFullYear();
			if ( period === "M" || period === "Y" ) {
				this._notifyChange( inst );
			}
		},
	
		/* Ensure a date is within any min/max bounds. */
		_restrictMinMax: function( inst, date ) {
			var minDate = this._getMinMaxDate( inst, "min" ),
				maxDate = this._getMinMaxDate( inst, "max" ),
				newDate = ( minDate && date < minDate ? minDate : date );
			return ( maxDate && newDate > maxDate ? maxDate : newDate );
		},
	
		/* Notify change of month/year. */
		_notifyChange: function( inst ) {
			var onChange = this._get( inst, "onChangeMonthYear" );
			if ( onChange ) {
				onChange.apply( ( inst.input ? inst.input[ 0 ] : null ),
					[ inst.selectedYear, inst.selectedMonth + 1, inst ] );
			}
		},
	
		/* Determine the number of months to show. */
		_getNumberOfMonths: function( inst ) {
			var numMonths = this._get( inst, "numberOfMonths" );
			return ( numMonths == null ? [ 1, 1 ] : ( typeof numMonths === "number" ? [ 1, numMonths ] : numMonths ) );
		},
	
		/* Determine the current maximum date - ensure no time components are set. */
		_getMinMaxDate: function( inst, minMax ) {
			return this._determineDate( inst, this._get( inst, minMax + "Date" ), null );
		},
	
		/* Find the number of days in a given month. */
		_getDaysInMonth: function( year, month ) {
			return 32 - this._daylightSavingAdjust( new Date( year, month, 32 ) ).getDate();
		},
	
		/* Find the day of the week of the first of a month. */
		_getFirstDayOfMonth: function( year, month ) {
			return new Date( year, month, 1 ).getDay();
		},
	
		/* Determines if we should allow a "next/prev" month display change. */
		_canAdjustMonth: function( inst, offset, curYear, curMonth ) {
			var numMonths = this._getNumberOfMonths( inst ),
				date = this._daylightSavingAdjust( new Date( curYear,
				curMonth + ( offset < 0 ? offset : numMonths[ 0 ] * numMonths[ 1 ] ), 1 ) );
	
			if ( offset < 0 ) {
				date.setDate( this._getDaysInMonth( date.getFullYear(), date.getMonth() ) );
			}
			return this._isInRange( inst, date );
		},
	
		/* Is the given date in the accepted range? */
		_isInRange: function( inst, date ) {
			var yearSplit, currentYear,
				minDate = this._getMinMaxDate( inst, "min" ),
				maxDate = this._getMinMaxDate( inst, "max" ),
				minYear = null,
				maxYear = null,
				years = this._get( inst, "yearRange" );
				if ( years ) {
					yearSplit = years.split( ":" );
					currentYear = new Date().getFullYear();
					minYear = parseInt( yearSplit[ 0 ], 10 );
					maxYear = parseInt( yearSplit[ 1 ], 10 );
					if ( yearSplit[ 0 ].match( /[+\-].*/ ) ) {
						minYear += currentYear;
					}
					if ( yearSplit[ 1 ].match( /[+\-].*/ ) ) {
						maxYear += currentYear;
					}
				}
	
			return ( ( !minDate || date.getTime() >= minDate.getTime() ) &&
				( !maxDate || date.getTime() <= maxDate.getTime() ) &&
				( !minYear || date.getFullYear() >= minYear ) &&
				( !maxYear || date.getFullYear() <= maxYear ) );
		},
	
		/* Provide the configuration settings for formatting/parsing. */
		_getFormatConfig: function( inst ) {
			var shortYearCutoff = this._get( inst, "shortYearCutoff" );
			shortYearCutoff = ( typeof shortYearCutoff !== "string" ? shortYearCutoff :
				new Date().getFullYear() % 100 + parseInt( shortYearCutoff, 10 ) );
			return { shortYearCutoff: shortYearCutoff,
				dayNamesShort: this._get( inst, "dayNamesShort" ), dayNames: this._get( inst, "dayNames" ),
				monthNamesShort: this._get( inst, "monthNamesShort" ), monthNames: this._get( inst, "monthNames" ) };
		},
	
		/* Format the given date for display. */
		_formatDate: function( inst, day, month, year ) {
			if ( !day ) {
				inst.currentDay = inst.selectedDay;
				inst.currentMonth = inst.selectedMonth;
				inst.currentYear = inst.selectedYear;
			}
			var date = ( day ? ( typeof day === "object" ? day :
				this._daylightSavingAdjust( new Date( year, month, day ) ) ) :
				this._daylightSavingAdjust( new Date( inst.currentYear, inst.currentMonth, inst.currentDay ) ) );
			return this.formatDate( this._get( inst, "dateFormat" ), date, this._getFormatConfig( inst ) );
		}
	} );
	
	/*
	 * Bind hover events for datepicker elements.
	 * Done via delegate so the binding only occurs once in the lifetime of the parent div.
	 * Global datepicker_instActive, set by _updateDatepicker allows the handlers to find their way back to the active picker.
	 */
	function datepicker_bindHover( dpDiv ) {
		var selector = "button, .ui-datepicker-prev, .ui-datepicker-next, .ui-datepicker-calendar td a";
		return dpDiv.on( "mouseout", selector, function() {
				$( this ).removeClass( "ui-state-hover" );
				if ( this.className.indexOf( "ui-datepicker-prev" ) !== -1 ) {
					$( this ).removeClass( "ui-datepicker-prev-hover" );
				}
				if ( this.className.indexOf( "ui-datepicker-next" ) !== -1 ) {
					$( this ).removeClass( "ui-datepicker-next-hover" );
				}
			} )
			.on( "mouseover", selector, datepicker_handleMouseover );
	}
	
	function datepicker_handleMouseover() {
		if ( !$.datepicker._isDisabledDatepicker( datepicker_instActive.inline ? datepicker_instActive.dpDiv.parent()[ 0 ] : datepicker_instActive.input[ 0 ] ) ) {
			$( this ).parents( ".ui-datepicker-calendar" ).find( "a" ).removeClass( "ui-state-hover" );
			$( this ).addClass( "ui-state-hover" );
			if ( this.className.indexOf( "ui-datepicker-prev" ) !== -1 ) {
				$( this ).addClass( "ui-datepicker-prev-hover" );
			}
			if ( this.className.indexOf( "ui-datepicker-next" ) !== -1 ) {
				$( this ).addClass( "ui-datepicker-next-hover" );
			}
		}
	}
	
	/* jQuery extend now ignores nulls! */
	function datepicker_extendRemove( target, props ) {
		$.extend( target, props );
		for ( var name in props ) {
			if ( props[ name ] == null ) {
				target[ name ] = props[ name ];
			}
		}
		return target;
	}
	
	/* Invoke the datepicker functionality.
	   @param  options  string - a command, optionally followed by additional parameters or
						Object - settings for attaching new datepicker functionality
	   @return  jQuery object */
	$.fn.datepicker = function( options ) {
	
		/* Verify an empty collection wasn't passed - Fixes #6976 */
		if ( !this.length ) {
			return this;
		}
	
		/* Initialise the date picker. */
		if ( !$.datepicker.initialized ) {
			$( document ).on( "mousedown", $.datepicker._checkExternalClick );
			$.datepicker.initialized = true;
		}
	
		/* Append datepicker main container to body if not exist. */
		if ( $( "#" + $.datepicker._mainDivId ).length === 0 ) {
			$( "body" ).append( $.datepicker.dpDiv );
		}
	
		var otherArgs = Array.prototype.slice.call( arguments, 1 );
		if ( typeof options === "string" && ( options === "isDisabled" || options === "getDate" || options === "widget" ) ) {
			return $.datepicker[ "_" + options + "Datepicker" ].
				apply( $.datepicker, [ this[ 0 ] ].concat( otherArgs ) );
		}
		if ( options === "option" && arguments.length === 2 && typeof arguments[ 1 ] === "string" ) {
			return $.datepicker[ "_" + options + "Datepicker" ].
				apply( $.datepicker, [ this[ 0 ] ].concat( otherArgs ) );
		}
		return this.each( function() {
			typeof options === "string" ?
				$.datepicker[ "_" + options + "Datepicker" ].
					apply( $.datepicker, [ this ].concat( otherArgs ) ) :
				$.datepicker._attachDatepicker( this, options );
		} );
	};
	
	$.datepicker = new Datepicker(); // singleton instance
	$.datepicker.initialized = false;
	$.datepicker.uuid = new Date().getTime();
	$.datepicker.version = "1.12.1";
	
	return $.datepicker;
	
	} ) );


/***/ }),
/* 49 */
/*!***********************************!*\
  !*** ./~/jquery-ui/ui/version.js ***!
  \***********************************/
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;( function( factory ) {
		if ( true ) {
	
			// AMD. Register as an anonymous module.
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [ __webpack_require__(/*! jquery */ 2) ], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
		} else {
	
			// Browser globals
			factory( jQuery );
		}
	} ( function( $ ) {
	
	$.ui = $.ui || {};
	
	return $.ui.version = "1.12.1";
	
	} ) );


/***/ }),
/* 50 */
/*!***********************************!*\
  !*** ./~/jquery-ui/ui/keycode.js ***!
  \***********************************/
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!
	 * jQuery UI Keycode 1.12.1
	 * http://jqueryui.com
	 *
	 * Copyright jQuery Foundation and other contributors
	 * Released under the MIT license.
	 * http://jquery.org/license
	 */
	
	//>>label: Keycode
	//>>group: Core
	//>>description: Provide keycodes as keynames
	//>>docs: http://api.jqueryui.com/jQuery.ui.keyCode/
	
	( function( factory ) {
		if ( true ) {
	
			// AMD. Register as an anonymous module.
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [ __webpack_require__(/*! jquery */ 2), __webpack_require__(/*! ./version */ 49) ], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
		} else {
	
			// Browser globals
			factory( jQuery );
		}
	} ( function( $ ) {
	return $.ui.keyCode = {
		BACKSPACE: 8,
		COMMA: 188,
		DELETE: 46,
		DOWN: 40,
		END: 35,
		ENTER: 13,
		ESCAPE: 27,
		HOME: 36,
		LEFT: 37,
		PAGE_DOWN: 34,
		PAGE_UP: 33,
		PERIOD: 190,
		RIGHT: 39,
		SPACE: 32,
		TAB: 9,
		UP: 38
	};
	
	} ) );


/***/ }),
/* 51 */
/*!*******************************************!*\
  !*** ./src/base/components/MessageBus.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : MessageBus.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var MessageBusClass = _backbone2.default.Object.extend({
	    channelName: 'message',
	    radioEvents: {
	        'success': 'logSuccess',
	        'error': 'logError'
	    },
	    logSuccess: function logSuccess(view, message) {
	        console.log("MessageBus : " + message);
	    },
	    logError: function logError(view, message) {
	        console.error("MessageBus : " + message);
	    }
	});
	var MessageBus = new MessageBusClass();
	exports.default = MessageBus;

/***/ }),
/* 52 */
/*!******************************************!*\
  !*** ./src/base/components/ConfigBus.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ConfigBus.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ConfigBusClass = _backbone2.default.Object.extend({
	    channelName: 'config',
	    radioRequests: {
	        'get:form_options': 'getFormOptions',
	        'has:form_section': 'hasFormSection',
	        'get:form_section': 'getFormSection',
	        'get:form_actions': 'getFormActions'
	    },
	    setFormConfig: function setFormConfig(form_config) {
	        this.form_config = form_config;
	    },
	    getFormOptions: function getFormOptions(option_name) {
	        /*
	         * Return the form options for option_name
	         *
	         * :param str option_name: The name of the option
	         * :returns: A list of dict with options (for building selects)
	         */
	        console.log("FacadeClass.getFormOptions");
	        return this.form_config['options'][option_name];
	    },
	    hasFormSection: function hasFormSection(section_name) {
	        /*
	         *
	         * :param str section_name: The name of the section
	         * :rtype: bool
	         */
	        return _.has(this.form_config['sections'], section_name);
	    },
	    getFormSection: function getFormSection(section_name) {
	        /*
	         *
	         * Return the form section description
	         * :param str section_name: The name of the section
	         * :returns: The section definition
	         * :rtype: Object
	         */
	        return this.form_config['sections'][section_name];
	    },
	    getFormActions: function getFormActions() {
	        /*
	         * Return available form action config
	         */
	        return this.form_config['actions'];
	    }
	});
	var ConfigBus = new ConfigBusClass();
	exports.default = ConfigBus;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ })
]);
//# sourceMappingURL=expense.js.map