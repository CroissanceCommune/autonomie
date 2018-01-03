webpackJsonp([2],[
/* 0 */
/*!**************************!*\
  !*** ./src/task/task.js ***!
  \**************************/
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
	
	var _App = __webpack_require__(/*! ./components/App.js */ 105);
	
	var _App2 = _interopRequireDefault(_App);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	var _backboneTools = __webpack_require__(/*! ../backbone-tools.js */ 22);
	
	var _Router = __webpack_require__(/*! ./components/Router.js */ 106);
	
	var _Router2 = _interopRequireDefault(_Router);
	
	var _Controller = __webpack_require__(/*! ./components/Controller.js */ 107);
	
	var _Controller2 = _interopRequireDefault(_Controller);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	// import 'bootstrap/dist/js/bootstrap';
	(0, _tools.setupAjaxCallbacks)(); /* global AppOption; */
	/*
	 * File Name :
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	
	
	_App2.default.on('start', function (app, options) {
	    console.log("  => Starting the app");
	    AppOption['form_config'] = options.form_config;
	    (0, _backboneTools.setupBbValidationCallbacks)(_backboneValidation2.default.callbacks);
	    (0, _backboneTools.setupBbValidationPatterns)(_backboneValidation2.default);
	    var controller = new _Controller2.default(options);
	    var router = new _Router2.default({ controller: controller });
	    _backbone2.default.history.start();
	    (0, _tools.hideLoader)();
	});
	
	(0, _jquery2.default)(function () {
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
/* 20 */,
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
	        amount: /^-?(\d+(?:[\.\,]\d{1,5})?)$/,
	        amount2: /^-?(\d+(?:[\.\,]\d{1,2})?)$/
	    });
	    _.extend(bb_module.messages, {
	        amount: "Doit être un nombre avec au maximum 5 chiffres après la virgule",
	        amount2: "Doit être un nombre avec au maximum 2 chiffres après la virgule"
	    });
	};
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 23 */,
/* 24 */,
/* 25 */,
/* 26 */,
/* 27 */,
/* 28 */,
/* 29 */,
/* 30 */
/*!*************************************!*\
  !*** ./src/widgets/AnchorWidget.js ***!
  \*************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	var _math = __webpack_require__(/*! ../math.js */ 36);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var AnchorWidget = _backbone2.default.View.extend({
	    tagName: 'div',
	    template: __webpack_require__(/*! ./templates/AnchorWidget.mustache */ 37),
	    ui: {
	        anchor: 'a'
	    },
	    events: {
	        'click @ui.anchor': "onClick"
	    },
	    onClick: function onClick() {
	        console.log("Clicked");
	        console.log(this.model);
	        var options = this.model.get('option');
	        if (options.popup) {
	            var screen_width = screen.width;
	            var screen_height = screen.height;
	
	            var width = (0, _math.getPercent)(screen_width, 60);
	            var height = (0, _math.getPercent)(screen_height, 60);
	            var url = options.url;
	            var title = options.title;
	            window.open(url + "?popup=true", title, "width=" + width + ",height=" + height);
	        }
	    }
	}); /*
	     * File Name : AnchorWidget.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = AnchorWidget;

/***/ }),
/* 31 */
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
	
	var _date = __webpack_require__(/*! ./date.js */ 32);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	__webpack_require__(/*! jquery */ 2);
	
	
	var datepicker = __webpack_require__(/*! jquery-ui/ui/widgets/datepicker */ 33);
	
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
	        if (!_underscore2.default.isUndefined(options.default_value)) {
	            value = (0, _date.parseDate)(options.default_value);
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
/* 32 */
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
/* 33 */
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
				__webpack_require__(/*! ../version */ 34),
				__webpack_require__(/*! ../keycode */ 35)
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
/* 34 */
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
/* 35 */
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
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [ __webpack_require__(/*! jquery */ 2), __webpack_require__(/*! ./version */ 34) ], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
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
/* 36 */
/*!*********************!*\
  !*** ./src/math.js ***!
  \*********************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	exports.getPercent = exports.getTvaPart = exports.trailingZeros = exports.formatAmount = exports.isNotFormattable = exports.formatPrice = exports.round = exports.strToFloat = undefined;
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function getEpsilon() {
	  /*
	   * Return the epsilon needed to test if the value is a float error
	   * computation result
	   */
	  if ("EPSILON" in Number) {
	    return Number.EPSILON;
	  }
	  var eps = 1.0;
	  do {
	    eps /= 2.0;
	  } while (1.0 + eps / 2.0 != 1.0);
	  return eps;
	} /*
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
	
	
	function removeEpsilon(value) {
	  /*
	   * Remove epsilons (75.599999999 -> 75.6 )from the value if needed
	   *
	   * :param int value: The value to test if it's a string, we convert it to
	   * float before
	   */
	  if (_underscore2.default.isUndefined(value.toPrecision)) {
	    return value;
	  }
	  var epsilon = getEpsilon();
	  var delta = value.toPrecision(6) - value;
	  delta = delta * delta;
	  if (delta === 0) {
	    return value;
	  }
	  if (delta < epsilon) {
	    return value.toPrecision(6);
	  } else {
	    return value;
	  }
	}
	
	var strToFloat = exports.strToFloat = function strToFloat(value) {
	  /*
	   * Transform the value to a float
	   *
	   * :param str value: A string value representing a number
	   */
	  var result;
	
	  if (_underscore2.default.isNumber(value)) {
	    return value;
	  }
	
	  if (_underscore2.default.isUndefined(value) || _underscore2.default.isNull(value)) {
	    value = "0.00";
	  }
	  value = value.replace(",", ".");
	  result = parseFloat(value);
	  if (isNaN(result)) {
	    return 0.0;
	  } else {
	    return result;
	  }
	};
	var round = exports.round = function round(price) {
	  /*
	   *  Round the price (in our comptability model, round_half_up, 1.5->2)
	   *
	   *  :param float price: The price to round
	   */
	  var passed_to_cents = price * 100;
	  passed_to_cents = Math.round(passed_to_cents);
	  return passed_to_cents / 100;
	};
	
	var formatPrice = exports.formatPrice = function formatPrice(price, rounded) {
	  /*
	   * Return a formatted price for display
	   * @price : compute-formatted price
	   */
	  price = removeEpsilon(price);
	  var dots, splitted, cents, ret_string;
	  if (rounded) {
	    price = round(price);
	  }
	
	  splitted = String(price).split('.');
	  if (splitted[1] != undefined) {
	    cents = splitted[1];
	    if (cents.length > 4) {
	      dots = true;
	    }
	    cents = cents.substr(0, 4);
	    cents = trailingZeros(cents, rounded);
	  } else {
	    cents = '00';
	  }
	  ret_string = splitted[0] + "," + cents;
	  if (dots) {
	    ret_string += "...";
	  }
	  return ret_string;
	};
	var isNotFormattable = exports.isNotFormattable = function isNotFormattable(amount) {
	  /*
	   * Verify if the amount is already formatted (with the euros sign)
	   */
	  var test = " " + amount;
	  if (test.indexOf("€") >= 0 || test.indexOf("&nbsp;&euro;") >= 0) {
	    return true;
	  }
	  return false;
	};
	var formatAmount = exports.formatAmount = function formatAmount(amount, rounded) {
	  /*
	   * return a formatted user-friendly amount
	   */
	  if (rounded === undefined) {
	    rounded = true;
	  }
	  if (isNotFormattable(amount)) {
	    return amount;
	  }
	  return formatPrice(amount, rounded) + "&nbsp;&euro;";
	};
	var trailingZeros = exports.trailingZeros = function trailingZeros(cents, rounded) {
	  /*
	   * Remove trailing zeros in an amount
	   *
	   * :param str cents: A string value representing cents (14010)
	   * :param bool rounded: Should we round the value ?
	   */
	  if (cents.length === 1) {
	    cents += 0;
	  }
	  var last_value;
	  if (!rounded) {
	    last_value = cents.substr(cents.length - 1);
	    while (cents.length > 2 && last_value == '0') {
	      cents = cents.substr(0, cents.length - 1);
	      last_value = cents.substr(cents.length - 1);
	    }
	  }
	  return cents;
	};
	
	var getTvaPart = exports.getTvaPart = function getTvaPart(total, tva) {
	  /*
	   *  Compute the given tva from total
	   */
	  return total * tva / 100;
	};
	
	var getPercent = exports.getPercent = function getPercent(amount, percent) {
	  /*
	   * Compute a percentage
	   */
	  return round(amount * percent / 100);
	};

/***/ }),
/* 37 */
/*!*****************************************************!*\
  !*** ./src/widgets/templates/AnchorWidget.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "#";
	  },"3":function(depth0,helpers,partials,data) {
	  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.url : stack1), depth0));
	  },"5":function(depth0,helpers,partials,data) {
	  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "onclick=\""
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.onclick : stack1), depth0))
	    + "\"";
	},"7":function(depth0,helpers,partials,data) {
	  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return " "
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.attrs : stack1), depth0));
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression, buffer = "<a\n    class='"
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.css : stack1), depth0))
	    + " btn-block'\n    href='";
	  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.popup : stack1), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "'\n    title=\""
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.title : stack1), depth0))
	    + "\"\n    ";
	  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.onclick : stack1), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "\n    ";
	  stack1 = helpers['if'].call(depth0, ((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.attrs : stack1), {"name":"if","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + ">\n    <i class='"
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.icon : stack1), depth0))
	    + "'></i> "
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.label : stack1), depth0))
	    + "\n</a>\n";
	},"useData":true});

/***/ }),
/* 38 */
/*!*********************************!*\
  !*** ./~/handlebars/runtime.js ***!
  \*********************************/
/***/ (function(module, exports, __webpack_require__) {

	// Create a simple path alias to allow browserify to resolve
	// the runtime on a supported path.
	module.exports = __webpack_require__(/*! ./dist/cjs/handlebars.runtime */ 39);


/***/ }),
/* 39 */
/*!*****************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars.runtime.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	/*globals Handlebars: true */
	var base = __webpack_require__(/*! ./handlebars/base */ 40);
	
	// Each of these augment the Handlebars object. No need to setup here.
	// (This is done to easily share code between commonjs and browse envs)
	var SafeString = __webpack_require__(/*! ./handlebars/safe-string */ 42)["default"];
	var Exception = __webpack_require__(/*! ./handlebars/exception */ 43)["default"];
	var Utils = __webpack_require__(/*! ./handlebars/utils */ 41);
	var runtime = __webpack_require__(/*! ./handlebars/runtime */ 44);
	
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
/* 40 */
/*!**************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/base.js ***!
  \**************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	var Utils = __webpack_require__(/*! ./utils */ 41);
	var Exception = __webpack_require__(/*! ./exception */ 43)["default"];
	
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
/* 41 */
/*!***************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/utils.js ***!
  \***************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	/*jshint -W004 */
	var SafeString = __webpack_require__(/*! ./safe-string */ 42)["default"];
	
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
/* 42 */
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
/* 43 */
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
/* 44 */
/*!*****************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/runtime.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	var Utils = __webpack_require__(/*! ./utils */ 41);
	var Exception = __webpack_require__(/*! ./exception */ 43)["default"];
	var COMPILER_REVISION = __webpack_require__(/*! ./base */ 40).COMPILER_REVISION;
	var REVISION_CHANGES = __webpack_require__(/*! ./base */ 40).REVISION_CHANGES;
	var createFrame = __webpack_require__(/*! ./base */ 40).createFrame;
	
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
/* 45 */
/*!*************************************!*\
  !*** ./src/widgets/ToggleWidget.js ***!
  \*************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function($) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ToggleWidget.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/ToggleWidget.mustache */ 46);
	
	var ToggleWidget = _backbone2.default.View.extend({
	    template: template,
	    ui: {
	        buttons: '.btn'
	    },
	    events: {
	        'click @ui.buttons': 'onClick'
	    },
	    onClick: function onClick(event) {
	        var url = this.model.get('options').url;
	        var value = $(event.target).find('input').val();
	        (0, _tools.ajax_call)(url, { 'submit': value }, 'POST', { success: this.refresh });
	    },
	
	    refresh: function refresh() {
	        window.location.reload();
	    },
	    templateContext: function templateContext() {
	        var buttons = this.model.get('options').buttons;
	
	        var current_value = this.model.get('options').current_value;
	        var found_one = (0, _tools.updateSelectOptions)(buttons, current_value, "status");
	        console.log(buttons);
	        console.log(current_value);
	
	        return {
	            name: this.model.get('options').name,
	            buttons: buttons
	        };
	    }
	});
	
	exports.default = ToggleWidget;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 2)))

/***/ }),
/* 46 */
/*!*****************************************************!*\
  !*** ./src/widgets/templates/ToggleWidget.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data,depths) {
	  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression, buffer = "    <label class=\""
	    + escapeExpression(lambda((depth0 != null ? depth0.css : depth0), depth0))
	    + " ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.selected : depth0), {"name":"if","hash":{},"fn":this.program(2, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "\">\n        <input\n            type=\"radio\"\n            name=\""
	    + escapeExpression(lambda((depths[1] != null ? depths[1].field_name : depths[1]), depth0))
	    + "\"\n            value=\""
	    + escapeExpression(lambda((depth0 != null ? depth0.value : depth0), depth0))
	    + "\"\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.selected : depth0), {"name":"if","hash":{},"fn":this.program(4, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "            autocomplete=\"off\"\n            >\n            <i class='"
	    + escapeExpression(lambda((depth0 != null ? depth0.icon : depth0), depth0))
	    + "'></i> "
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "\n\n    </label>\n";
	},"2":function(depth0,helpers,partials,data) {
	  return "active";
	  },"4":function(depth0,helpers,partials,data) {
	  return "            checked\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data,depths) {
	  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression, buffer = "<h4 class='text-center'>"
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.options : depth0)) != null ? stack1.label : stack1), depth0))
	    + "</h4>\n<hr />\n<div class='btn-group' data-toggle=\"buttons\">\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.buttons : depth0), {"name":"each","hash":{},"fn":this.program(1, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>\n";
	},"useData":true,"useDepths":true});

/***/ }),
/* 47 */,
/* 48 */,
/* 49 */
/*!*********************************************!*\
  !*** ./src/base/behaviors/ModalBehavior.js ***!
  \*********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ModalBehavior = _backbone2.default.Behavior.extend({
	  defaults: {
	    modalClasses: '',
	    modalOptions: {
	      'keyboard': 'false',
	      'backdrop': 'static'
	    }
	  },
	  ui: {
	    close: '.close'
	  },
	  events: {
	    'hidden.bs.modal': 'triggerFinish',
	    'click @ui.close': 'onClose'
	  },
	  onRender: function onRender() {
	    this.view.$el.addClass('modal ' + this.getOption('modalClasses'));
	  },
	  onAttach: function onAttach() {
	    this.view.$el.modal(this.getOption('modalOptions') || {});
	  },
	  onClose: function onClose() {
	    console.log("Trigger modal:beforeClose from ModalBehavior");
	    this.view.triggerMethod('modal:beforeClose');
	    console.log("Trigger modal:close from ModalBehavior");
	    this.view.triggerMethod('modal:close');
	  },
	  onModalClose: function onModalClose() {
	    console.log("ModalBehavior.onModalClose");
	    this.view.$el.modal('hide');
	  },
	  triggerFinish: function triggerFinish() {
	    console.log("Trigger destroy:modal from ModalBehavior");
	    this.view.triggerMethod('destroy:modal');
	  }
	}); /*
	     * File Name : ModalBehavior.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ModalBehavior;

/***/ }),
/* 50 */,
/* 51 */,
/* 52 */,
/* 53 */,
/* 54 */,
/* 55 */,
/* 56 */,
/* 57 */,
/* 58 */,
/* 59 */,
/* 60 */,
/* 61 */,
/* 62 */,
/* 63 */,
/* 64 */,
/* 65 */,
/* 66 */,
/* 67 */,
/* 68 */,
/* 69 */,
/* 70 */,
/* 71 */,
/* 72 */,
/* 73 */
/*!********************************************!*\
  !*** ./src/base/behaviors/FormBehavior.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _BaseFormBehavior = __webpack_require__(/*! ./BaseFormBehavior.js */ 74);
	
	var _BaseFormBehavior2 = _interopRequireDefault(_BaseFormBehavior);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var FormBehavior = _backbone2.default.Behavior.extend({
	    behaviors: [_BaseFormBehavior2.default],
	    ui: {
	        form: "form",
	        submit: "button[type=submit]",
	        reset: "button[type=reset]"
	    },
	    events: {
	        'submit @ui.form': 'onSubmitForm',
	        'click @ui.reset': 'onCancelClick'
	    },
	    defaults: {
	        errorMessage: "Une erreur est survenue"
	    },
	    serializeForm: function serializeForm() {
	        return (0, _tools.serializeForm)(this.getUI('form'));
	    },
	    onSyncError: function onSyncError(datas, status, result) {
	        var channel = _backbone4.default.channel("message");
	        channel.trigger('error:backbone', result);
	        _backboneValidation2.default.unbind(this.view);
	    },
	    onSyncSuccess: function onSyncSuccess(datas, status, result) {
	        var channel = _backbone4.default.channel("message");
	        channel.trigger('success:backbone', result);
	        _backboneValidation2.default.unbind(this.view);
	        console.log("Trigger success:sync from FormBehavior");
	        this.view.triggerMethod('success:sync');
	    },
	    syncServer: function syncServer(datas, bound) {
	        var bound = bound || false;
	        var datas = datas || this.view.model.toJSON();
	
	        if (!bound) {
	            _backboneValidation2.default.bind(this.view, {
	                attributes: function attributes(view) {
	                    return _.keys(datas);
	                }
	            });
	        }
	
	        if (this.view.model.isValid(_.keys(datas))) {
	            var request = void 0;
	            if (!this.view.model.get('id')) {
	                request = this.addSubmit(datas);
	            } else {
	                request = this.editSubmit(datas);
	            }
	            console.log(request);
	            request.done(this.onSyncSuccess.bind(this)).fail(this.onSyncError.bind(this));
	        }
	    },
	    addSubmit: function addSubmit(datas) {
	        /*
	         *
	         * Since collection.create doesn't return a jquery promise, we need to
	         * re-implement the destcollection create stuff and return the expected
	         * promise
	         *
	         * See sources : (Collection.create)
	         * http://backbonejs.org/docs/backbone.html
	         *
	         */
	        console.log("FormBehavior.addSubmit");
	        var destCollection = this.view.getOption('destCollection');
	        var model = destCollection._prepareModel(datas);
	
	        var request = model.save(null, { wait: true, sort: true });
	        request = request.done(function (model, resp, callbackOpts) {
	            destCollection.add(model, callbackOpts);
	            return model, 'success', resp;
	        });
	        return request;
	    },
	    editSubmit: function editSubmit(datas) {
	        console.log("FormBehavior.editSubmit");
	        return this.view.model.save(datas, { wait: true, patch: true });
	    },
	    onSubmitForm: function onSubmitForm(event) {
	        console.log("FormBehavior.onSubmitForm");
	        event.preventDefault();
	        var datas = this.serializeForm();
	        this.view.model.set(datas, { validate: true });
	        this.syncServer(datas);
	    },
	    onDataPersisted: function onDataPersisted(datas) {
	        console.log("FormBehavior.onDataPersisted");
	        this.syncServer(datas, true);
	    },
	    onCancelClick: function onCancelClick() {
	        console.log("FormBehavior.onCancelClick");
	        console.log("Trigger reset:model from FormBehavior");
	        this.view.triggerMethod('reset:model');
	        console.log("Trigger cancel:form from FormBehavior");
	        this.view.triggerMethod('cancel:form');
	    },
	    onResetModel: function onResetModel() {
	        console.log("FormBehavior.onResetModel");
	        this.view.model.rollback();
	    }
	}); /*
	     * File Name : FormBehavior.js
	     *
	     * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = FormBehavior;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 74 */
/*!************************************************!*\
  !*** ./src/base/behaviors/BaseFormBehavior.js ***!
  \************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : FormValidationBehavior.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var BaseFormBehavior = _backbone2.default.Behavior.extend({
	    onDataPersist: function onDataPersist(attribute, value) {
	        console.log("BaseFormBehavior.onDataPersist");
	        _backboneValidation2.default.unbind(this.view);
	        _backboneValidation2.default.bind(this.view, {
	            attributes: function attributes(view) {
	                return [attribute];
	            }
	        });
	
	        var datas = {};
	        datas[attribute] = value;
	        this.view.model.set(datas);
	        this.view.triggerMethod('data:persisted', datas);
	    },
	    onDataModified: function onDataModified(attribute, value) {
	        _backboneValidation2.default.unbind(this.view);
	        _backboneValidation2.default.bind(this.view, {
	            attributes: function attributes(view) {
	                return [attribute];
	            }
	        });
	        var datas = {};
	        datas[attribute] = value;
	        this.view.model.set(datas);
	        this.view.model.isValid();
	    }
	});
	exports.default = BaseFormBehavior;

/***/ }),
/* 75 */
/*!*****************************************!*\
  !*** ./src/widgets/DatePickerWidget.js ***!
  \*****************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function($) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	var _date = __webpack_require__(/*! ../date.js */ 32);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : DatePickerWidget.js
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/DatePickerWidget.mustache */ 76);
	
	var DatePickerWidget = _backbone2.default.View.extend({
	    template: template,
	    ui: {
	        altdate: "input[name=altdate]"
	    },
	    onDateSelect: function onDateSelect() {
	        /* On date select trigger a change event */
	        var value = $(this.getSelector()).val();
	        this.triggerMethod('finish', this.getOption('field_name'), value);
	    },
	    getSelector: function getSelector() {
	        /* Return the selector for the date input */
	        return "input[name=" + (0, _tools.getOpt)(this, 'field_name', 'date') + "]";
	    },
	    onAttach: function onAttach() {
	        /* On attachement in case of edit, we setup the datepicker */
	        if ((0, _tools.getOpt)(this, 'editable', true)) {
	            var today = (0, _date.dateToIso)(new Date());
	            var kwargs = {
	                // Bind the method to access view through the 'this' param
	                onSelect: this.onDateSelect.bind(this),
	                default_value: (0, _tools.getOpt)(this, 'default_value', today)
	            };
	            if ((0, _tools.getOpt)(this, 'current_year', false)) {
	                kwargs['changeYear'] = false;
	                kwargs['yearRange'] = '-0:+0';
	            }
	
	            var date = this.getOption('date');
	            var selector = this.getSelector();
	            (0, _tools.setDatePicker)(this.getUI('altdate'), selector, date, kwargs);
	        }
	    },
	    templateContext: function templateContext() {
	        /*
	         * Give parameters for the templating context
	         */
	        var ctx = {
	            editable: (0, _tools.getOpt)(this, 'editable', true),
	            title: (0, _tools.getOpt)(this, 'title', 'Date'),
	            description: (0, _tools.getOpt)(this, 'description', ''),
	            field_name: (0, _tools.getOpt)(this, 'field_name', 'date')
	        };
	        if (!(0, _tools.getOpt)(this, 'editable', true)) {
	            ctx['date'] = (0, _date.formatDate)(this.getOption('date'));
	        }
	        return ctx;
	    }
	});
	exports.default = DatePickerWidget;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 2)))

/***/ }),
/* 76 */
/*!*********************************************************!*\
  !*** ./src/widgets/templates/DatePickerWidget.mustache ***!
  \*********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "    <div class='form-group date'>\n        <label for='altdate'>"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</label>\n        <input class=\"form-control\" name=\"altdate\" type=\"text\" autocomplete=\"off\" />\n        <input class=\"form-control\" name=\""
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "\" type=\"hidden\" />\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.description : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "    </div>\n";
	},"2":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "        <span class='help-block'>"
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + "</span>\n";
	},"4":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "    <div class='form-group date'>\n        <label>Date</label>\n        <div class='form-control'>\n            "
	    + escapeExpression(((helper = (helper = helpers.date || (depth0 != null ? depth0.date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"date","hash":{},"data":data}) : helper)))
	    + "\n        </div>\n    </div>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.editable : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(4, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 77 */
/*!************************************!*\
  !*** ./src/widgets/InputWidget.js ***!
  \************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : InputWidget.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var InputWidget = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'form-group',
	    template: __webpack_require__(/*! ./templates/InputWidget.mustache */ 78),
	    ui: {
	        input: 'input'
	    },
	    events: {
	        'keyup @ui.input': 'onKeyUp',
	        'blur @ui.input': 'onBlur'
	    },
	    onKeyUp: function onKeyUp() {
	        this.triggerMethod('change', this.getOption('field_name'), this.getUI('input').val());
	    },
	    onBlur: function onBlur() {
	        this.triggerMethod('finish', this.getOption('field_name'), this.getUI('input').val());
	    },
	    templateContext: function templateContext() {
	        return {
	            value: this.getOption('value'),
	            title: (0, _tools.getOpt)(this, 'title', ''),
	            field_name: this.getOption('field_name'),
	            description: (0, _tools.getOpt)(this, 'description', false),
	            type: (0, _tools.getOpt)(this, 'type', 'text'),
	            addon: (0, _tools.getOpt)(this, 'addon', ''),
	            css_class: (0, _tools.getOpt)(this, 'css', '')
	        };
	    }
	});
	
	exports.default = InputWidget;

/***/ }),
/* 78 */
/*!****************************************************!*\
  !*** ./src/widgets/templates/InputWidget.mustache ***!
  \****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<label for="
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + ">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</label>";
	},"3":function(depth0,helpers,partials,data) {
	  return "<div class='input-group'>";
	  },"5":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class=\"input-group-addon\">";
	  stack1 = ((helper = (helper = helpers.addon || (depth0 != null ? depth0.addon : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"addon","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>";
	},"7":function(depth0,helpers,partials,data) {
	  return "</div>";
	  },"9":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<span class='help-block'><small>"
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + "</small></span>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.addon : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "<input class='form-control "
	    + escapeExpression(((helper = (helper = helpers.css_class || (depth0 != null ? depth0.css_class : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"css_class","hash":{},"data":data}) : helper)))
	    + "' type='"
	    + escapeExpression(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"type","hash":{},"data":data}) : helper)))
	    + "' value='"
	    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
	    + "' name=\""
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "\"></input>";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.addon : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.addon : depth0), {"name":"if","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.description : depth0), {"name":"if","hash":{},"fn":this.program(9, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 79 */
/*!*************************************!*\
  !*** ./src/widgets/SelectWidget.js ***!
  \*************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : SelectWidget.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/SelectWidget.mustache */ 80);
	
	var SelectWidget = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'form-group',
	    template: template,
	    ui: {
	        select: 'select'
	    },
	    events: {
	        'change @ui.select': "onChange"
	    },
	    onChange: function onChange(event) {
	        this.triggerMethod("finish", this.getOption('field_name'), this.getUI('select').val());
	    },
	    hasVoid: function hasVoid(options) {
	        return !_underscore2.default.isUndefined(_underscore2.default.find(options, function (option) {
	            return option.label == '';
	        }));
	    },
	
	    templateContext: function templateContext() {
	        var id_key = (0, _tools.getOpt)(this, 'id_key', 'value');
	        var options = this.getOption('options');
	        var current_value = this.getOption('value');
	        var add_default = (0, _tools.getOpt)(this, 'add_default', false);
	        var found_one = (0, _tools.updateSelectOptions)(options, current_value, id_key);
	        if (!found_one && add_default && !this.hasVoid(options)) {
	            var void_option = {};
	            void_option['value'] = '';
	            void_option['label'] = '';
	            options.unshift(void_option);
	        }
	
	        var title = this.getOption('title');
	        var field_name = this.getOption('field_name');
	        var multiple = (0, _tools.getOpt)(this, 'multiple', false);
	        return {
	            options: options,
	            title: title,
	            field_name: field_name,
	            id_key: id_key,
	            multiple: multiple
	        };
	    }
	});
	exports.default = SelectWidget;

/***/ }),
/* 80 */
/*!*****************************************************!*\
  !*** ./src/widgets/templates/SelectWidget.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<label for='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "'>"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</label>\n";
	},"3":function(depth0,helpers,partials,data) {
	  return "multiple";
	  },"5":function(depth0,helpers,partials,data,depths) {
	  var stack1, escapeExpression=this.escapeExpression, lambda=this.lambda, buffer = "    <option value='"
	    + escapeExpression(helpers.lookup.call(depth0, depth0, (depths[1] != null ? depths[1].id_key : depths[1]), {"name":"lookup","hash":{},"data":data}))
	    + "' ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.selected : depth0), {"name":"if","hash":{},"fn":this.program(6, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + ">"
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "</option>\n";
	},"6":function(depth0,helpers,partials,data) {
	  return "selected";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data,depths) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(1, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "<select class='form-control' ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.multiple : depth0), {"name":"if","hash":{},"fn":this.program(3, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += " name='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "'>\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.options : depth0), {"name":"each","hash":{},"fn":this.program(5, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</select>\n";
	},"useData":true,"useDepths":true});

/***/ }),
/* 81 */,
/* 82 */,
/* 83 */,
/* 84 */,
/* 85 */,
/* 86 */
/*!*************************************************!*\
  !*** ./src/base/behaviors/ModalFormBehavior.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 22);
	
	var _ModalBehavior = __webpack_require__(/*! ./ModalBehavior.js */ 49);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	var _FormBehavior = __webpack_require__(/*! ./FormBehavior.js */ 73);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ModalFormBehavior.js
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ModalFormBehavior = _backbone2.default.Behavior.extend({
	    behaviors: [_ModalBehavior2.default, _FormBehavior2.default],
	    onSuccessSync: function onSuccessSync() {
	        console.log("ModalFormBehavior.onSuccessSync");
	        console.log("Trigger modal:close from ModalFormBehavior");
	        this.view.triggerMethod('modal:close');
	    },
	    onModalBeforeClose: function onModalBeforeClose() {
	        console.log("Trigger reset:model from ModalFormBehavior");
	        this.view.triggerMethod('reset:model');
	    },
	    onCancelForm: function onCancelForm() {
	        console.log("ModalFormBehavior.onCancelForm");
	        console.log("Trigger modal:close from ModalFormBehavior");
	        this.view.triggerMethod('modal:close');
	    },
	    onModalClose: function onModalClose() {
	        console.log("ModalFormBehavior.onModalClose");
	    }
	});
	
	exports.default = ModalFormBehavior;

/***/ }),
/* 87 */,
/* 88 */,
/* 89 */,
/* 90 */,
/* 91 */,
/* 92 */,
/* 93 */,
/* 94 */,
/* 95 */,
/* 96 */,
/* 97 */,
/* 98 */,
/* 99 */,
/* 100 */,
/* 101 */,
/* 102 */
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
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
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
/* 103 */
/*!*******************************************!*\
  !*** ./src/base/components/MessageBus.js ***!
  \*******************************************/
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
	        'error': 'logError',
	        'error:ajax': 'onAjaxError',
	        'success:ajax': 'onAjaxSuccess',
	        'error:backbone': 'onAjaxError',
	        'success:backbone': 'onAjaxSuccess'
	    },
	    logSuccess: function logSuccess(view, message) {
	        console.log("MessageBus : " + message);
	        this.getChannel().request('notify:success', message);
	    },
	    logError: function logError(view, message) {
	        console.error("MessageBus : " + message);
	        this.getChannel().request('notify:error', message);
	    },
	    extractJsonMessage: function extractJsonMessage(xhr) {
	        var json_resp = xhr.responseJSON;
	        var result = null;
	        if (!_.isUndefined(json_resp)) {
	            if (!_.isUndefined(json_resp.message)) {
	                result = json_resp.message;
	            } else if (!_.isUndefined(json_resp.messages)) {
	                result = json_resp.messages.join("<br />");
	            } else if (!_.isUndefined(json_resp.errors)) {
	                result = json_resp.errors.join("<br />");
	            } else if (!_.isUndefined(json_resp.error)) {
	                result = json_resp.error;
	            } else if (json_resp.status == 'success') {
	                result = "Opération réussie";
	            } else if (xhr.status == 200) {
	                result = "Opération réussie";
	            }
	        } else if (xhr.status == 403) {
	            result = "Opération non permise";
	        } else if (xhr.status == 501) {
	            result = "Une erreur inconnue est survenue, contactez votre administrateur";
	        }
	        return result;
	    },
	    onAjaxError: function onAjaxError(xhr) {
	        var message = this.extractJsonMessage(xhr);
	        if (!_.isNull(message)) {
	            this.getChannel().request('notify:error', message);
	        }
	    },
	    onAjaxSuccess: function onAjaxSuccess(xhr) {
	        // let message = this.extractJsonMessage(xhr);
	        // if (!_.isNull(message)){
	        //     this.getChannel().request('notify:success', message);
	        // }
	    }
	});
	var MessageBus = new MessageBusClass();
	exports.default = MessageBus;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 104 */
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
	        'get:options': 'getFormOptions',
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

/***/ }),
/* 105 */
/*!************************************!*\
  !*** ./src/task/components/App.js ***!
  \************************************/
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
	     * File Name : app.js
	     *
	     * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	
	var App = new AppClass();
	exports.default = App;

/***/ }),
/* 106 */
/*!***************************************!*\
  !*** ./src/task/components/Router.js ***!
  \***************************************/
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
	     * File Name : router.js
	     *
	     * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	
	exports.default = Router;

/***/ }),
/* 107 */
/*!*******************************************!*\
  !*** ./src/task/components/Controller.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _MainView = __webpack_require__(/*! ../views/MainView.js */ 108);
	
	var _MainView2 = _interopRequireDefault(_MainView);
	
	var _App = __webpack_require__(/*! ./App.js */ 105);
	
	var _App2 = _interopRequireDefault(_App);
	
	var _Facade = __webpack_require__(/*! ./Facade.js */ 203);
	
	var _Facade2 = _interopRequireDefault(_Facade);
	
	var _AuthBus = __webpack_require__(/*! ../../base/components/AuthBus.js */ 102);
	
	var _AuthBus2 = _interopRequireDefault(_AuthBus);
	
	var _MessageBus = __webpack_require__(/*! ../../base/components/MessageBus.js */ 103);
	
	var _MessageBus2 = _interopRequireDefault(_MessageBus);
	
	var _ConfigBus = __webpack_require__(/*! ../../base/components/ConfigBus.js */ 104);
	
	var _ConfigBus2 = _interopRequireDefault(_ConfigBus);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var Controller = _backbone2.default.Object.extend({
	    initialize: function initialize(options) {
	        _ConfigBus2.default.setFormConfig(options.form_config);
	        _Facade2.default.loadModels(options.form_datas);
	        AppOption.facade = _Facade2.default;
	
	        _AuthBus2.default.setAuthCallbacks([_Facade2.default.syncModel]);
	
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
/* 108 */
/*!************************************!*\
  !*** ./src/task/views/MainView.js ***!
  \************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _GeneralView = __webpack_require__(/*! ./GeneralView.js */ 109);
	
	var _GeneralView2 = _interopRequireDefault(_GeneralView);
	
	var _CommonView = __webpack_require__(/*! ./CommonView.js */ 126);
	
	var _CommonView2 = _interopRequireDefault(_CommonView);
	
	var _TaskBlockView = __webpack_require__(/*! ./TaskBlockView.js */ 128);
	
	var _TaskBlockView2 = _interopRequireDefault(_TaskBlockView);
	
	var _HtBeforeDiscountsView = __webpack_require__(/*! ./HtBeforeDiscountsView.js */ 157);
	
	var _HtBeforeDiscountsView2 = _interopRequireDefault(_HtBeforeDiscountsView);
	
	var _DiscountBlockView = __webpack_require__(/*! ./DiscountBlockView.js */ 158);
	
	var _DiscountBlockView2 = _interopRequireDefault(_DiscountBlockView);
	
	var _ExpenseHtBlockView = __webpack_require__(/*! ./ExpenseHtBlockView.js */ 171);
	
	var _ExpenseHtBlockView2 = _interopRequireDefault(_ExpenseHtBlockView);
	
	var _TotalView = __webpack_require__(/*! ./TotalView.js */ 173);
	
	var _TotalView2 = _interopRequireDefault(_TotalView);
	
	var _NotesBlockView = __webpack_require__(/*! ./NotesBlockView.js */ 175);
	
	var _NotesBlockView2 = _interopRequireDefault(_NotesBlockView);
	
	var _PaymentConditionBlockView = __webpack_require__(/*! ./PaymentConditionBlockView.js */ 177);
	
	var _PaymentConditionBlockView2 = _interopRequireDefault(_PaymentConditionBlockView);
	
	var _PaymentBlockView = __webpack_require__(/*! ./PaymentBlockView.js */ 179);
	
	var _PaymentBlockView2 = _interopRequireDefault(_PaymentBlockView);
	
	var _RightBarView = __webpack_require__(/*! ./RightBarView.js */ 191);
	
	var _RightBarView2 = _interopRequireDefault(_RightBarView);
	
	var _StatusView = __webpack_require__(/*! ./StatusView.js */ 196);
	
	var _StatusView2 = _interopRequireDefault(_StatusView);
	
	var _BootomActionView = __webpack_require__(/*! ./BootomActionView.js */ 198);
	
	var _BootomActionView2 = _interopRequireDefault(_BootomActionView);
	
	var _LoginView = __webpack_require__(/*! ../../base/views/LoginView.js */ 200);
	
	var _LoginView2 = _interopRequireDefault(_LoginView);
	
	var _ErrorView = __webpack_require__(/*! ./ErrorView.js */ 152);
	
	var _ErrorView2 = _interopRequireDefault(_ErrorView);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : MainView.js
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/MainView.mustache */ 202);
	
	var MainView = _backbone2.default.View.extend({
	    template: template,
	    regions: {
	        errors: '.errors',
	        modalRegion: '#modalregion',
	        general: '#general',
	        common: '#common',
	        tasklines: '#tasklines',
	        discounts: '#discounts',
	        expenses_ht: '#expenses_ht',
	        rightbar: "#rightbar",
	        ht_before_discounts: '.ht_before_discounts',
	        totals: '.totals',
	        notes: '.notes',
	        payment_conditions: '.payment-conditions',
	        payments: '.payments',
	        footer: {
	            el: '.footer-actions',
	            replaceElement: true
	        }
	    },
	    childViewEvents: {
	        'status:change': 'onStatusChange'
	    },
	    initialize: function initialize(options) {
	        this.config = _backbone4.default.channel('config');
	        this.facade = _backbone4.default.channel('facade');
	    },
	    showGeneralBlock: function showGeneralBlock() {
	        var section = this.config.request('get:form_section', 'general');
	        var model = this.facade.request('get:model', 'common');
	        var view = new _GeneralView2.default({ model: model, section: section });
	        this.showChildView('general', view);
	    },
	    showCommonBlock: function showCommonBlock() {
	        var section = this.config.request('get:form_section', 'common');
	        var model = this.facade.request('get:model', 'common');
	        var view = new _CommonView2.default({ model: model, section: section });
	        this.showChildView('common', view);
	    },
	    showTaskGroupBlock: function showTaskGroupBlock() {
	        var section = this.config.request('get:form_section', 'tasklines');
	        var model = this.facade.request('get:model', 'common');
	        var collection = this.facade.request('get:collection', 'task_groups');
	        var view = new _TaskBlockView2.default({ collection: collection, section: section, model: model });
	        this.showChildView('tasklines', view);
	    },
	    showDiscountBlock: function showDiscountBlock() {
	        var section = this.config.request('get:form_section', 'discounts');
	        var collection = this.facade.request('get:collection', 'discounts');
	        var model = this.facade.request('get:model', 'common');
	        var view = new _DiscountBlockView2.default({ collection: collection, model: model, section: section });
	        this.showChildView('discounts', view);
	    },
	    showExpenseHtBlock: function showExpenseHtBlock() {
	        var section = this.config.request('get:form_section', 'expenses_ht');
	        var model = this.facade.request('get:model', 'common');
	        var view = new _ExpenseHtBlockView2.default({ model: model, section: section });
	        this.showChildView('expenses_ht', view);
	    },
	    showNotesBlock: function showNotesBlock() {
	        var section = this.config.request('get:form_section', 'notes');
	        var model = this.facade.request('get:model', 'common');
	        var view = new _NotesBlockView2.default({ model: model, section: section });
	        this.showChildView('notes', view);
	    },
	    showPaymentConditionsBlock: function showPaymentConditionsBlock() {
	        var section = this.config.request('get:form_section', 'payment_conditions');
	        var model = this.facade.request('get:model', 'common');
	        var view = new _PaymentConditionBlockView2.default({ model: model });
	        this.showChildView('payment_conditions', view);
	    },
	    showPaymentBlock: function showPaymentBlock() {
	        var section = this.config.request('get:form_section', 'payments');
	        var model = this.facade.request('get:model', 'common');
	        var collection = this.facade.request('get:paymentcollection');
	        var view = new _PaymentBlockView2.default({ model: model, collection: collection, section: section });
	        this.showChildView('payments', view);
	    },
	    showLogin: function showLogin() {
	        var view = new _LoginView2.default({});
	        this.showChildView('modalRegion', view);
	    },
	    onRender: function onRender() {
	        var totalmodel = this.facade.request('get:totalmodel');
	        var view;
	        if (this.config.request('has:form_section', 'general')) {
	            this.showGeneralBlock();
	        }
	        if (this.config.request('has:form_section', 'common')) {
	            this.showCommonBlock();
	        }
	        if (this.config.request('has:form_section', "tasklines")) {
	            this.showTaskGroupBlock();
	        }
	        if (this.config.request('has:form_section', "discounts")) {
	            view = new _HtBeforeDiscountsView2.default({ model: totalmodel });
	            this.showChildView('ht_before_discounts', view);
	            this.showDiscountBlock();
	        }
	        if (this.config.request('has:form_section', "expenses_ht")) {
	            this.showExpenseHtBlock();
	        }
	
	        view = new _TotalView2.default({ model: totalmodel });
	        this.showChildView('totals', view);
	
	        if (this.config.request('has:form_section', "notes")) {
	            this.showNotesBlock();
	        }
	        if (this.config.request('has:form_section', "payment_conditions")) {
	            this.showPaymentConditionsBlock();
	        }
	        if (this.config.request('has:form_section', "payments")) {
	            this.showPaymentBlock();
	        }
	
	        view = new _RightBarView2.default({
	            actions: this.config.request('get:form_actions'),
	            model: totalmodel
	        });
	        this.showChildView('rightbar', view);
	        view = new _BootomActionView2.default({ actions: this.config.request('get:form_actions') });
	        this.showChildView('footer', view);
	    },
	    showStatusView: function showStatusView(status, title, label, url) {
	        var model = this.facade.request('get:model', 'common');
	        var view = new _StatusView2.default({
	            status: status,
	            title: title,
	            label: label,
	            model: model,
	            url: url
	        });
	        this.showChildView('modalRegion', view);
	    },
	    formOk: function formOk() {
	        var result = true;
	        var errors = this.facade.request('is:valid');
	        if (!_.isEmpty(errors)) {
	            this.showChildView('errors', new _ErrorView2.default({ errors: errors }));
	            result = false;
	        } else {
	            this.detachChildView('errors');
	        }
	        return result;
	    },
	
	    onStatusChange: function onStatusChange(status, title, label, url) {
	        (0, _tools.showLoader)();
	        if (status != 'draft') {
	            if (!this.formOk()) {
	                document.body.scrollTop = document.documentElement.scrollTop = 0;
	                (0, _tools.hideLoader)();
	                return;
	            }
	        }
	        (0, _tools.hideLoader)();
	        var common_model = this.facade.request('get:model', 'common');
	        var this_ = this;
	        // We ensure the common_model get saved before changing the status
	        common_model.save(null, {
	            patch: true,
	            success: function success() {
	                this_.showStatusView(status, title, label, url);
	            },
	            error: function error() {
	                (0, _tools.hideLoader)();
	            }
	        });
	    },
	    onChildviewDestroyModal: function onChildviewDestroyModal() {
	        this.getRegion('modalRegion').empty();
	    }
	});
	exports.default = MainView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 109 */
/*!***************************************!*\
  !*** ./src/task/views/GeneralView.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _jquery = __webpack_require__(/*! jquery */ 2);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _FormBehavior = __webpack_require__(/*! ../../base/behaviors/FormBehavior.js */ 73);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _CheckboxListWidget = __webpack_require__(/*! ../../widgets/CheckboxListWidget.js */ 110);
	
	var _CheckboxListWidget2 = _interopRequireDefault(_CheckboxListWidget);
	
	var _CheckboxWidget = __webpack_require__(/*! ../../widgets/CheckboxWidget.js */ 112);
	
	var _CheckboxWidget2 = _interopRequireDefault(_CheckboxWidget);
	
	var _DatePickerWidget = __webpack_require__(/*! ../../widgets/DatePickerWidget.js */ 75);
	
	var _DatePickerWidget2 = _interopRequireDefault(_DatePickerWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 77);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _StatusHistoryView = __webpack_require__(/*! ./StatusHistoryView.js */ 121);
	
	var _StatusHistoryView2 = _interopRequireDefault(_StatusHistoryView);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/GeneralView.mustache */ 125); /*
	                                                             * File Name : GeneralView.js
	                                                             *
	                                                             * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	                                                             * Company : Majerti ( http://www.majerti.fr )
	                                                             *
	                                                             * This software is distributed under GPLV3
	                                                             * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                             *
	                                                             */
	
	
	var GeneralView = _backbone2.default.View.extend({
	    /*
	     * Wrapper around the component making part of the 'common'
	     * invoice/estimation form, provide a main layout with regions for each
	     * field
	     */
	    behaviors: [{
	        behaviorClass: _FormBehavior2.default,
	        errorMessage: "Vérifiez votre saisie"
	    }],
	    tagName: 'div',
	    className: 'form-section',
	    template: template,
	    regions: {
	        status_history: '.status_history',
	        name: '.name',
	        course: '.course',
	        prefix: '.prefix',
	        financial_year: '.financial_year'
	    },
	    childViewTriggers: {
	        'change': 'data:modified',
	        'finish': 'data:persist'
	    },
	    initialize: function initialize(options) {
	        this.section = options['section'];
	        this.attachments = _backbone4.default.channel('facade').request('get:attachments');
	    },
	
	    templateContext: function templateContext() {
	        return { attachments: this.attachments };
	    },
	    showStatusHistory: function showStatusHistory() {
	        var collection = _backbone4.default.channel('facade').request('get:status_history_collection');
	        if (collection.models.length > 0) {
	            var view = new _StatusHistoryView2.default({ collection: collection });
	            this.showChildView('status_history', view);
	        }
	    },
	
	    onRender: function onRender() {
	        this.showStatusHistory();
	        this.showChildView('name', new _InputWidget2.default({
	            title: "Nom du document",
	            value: this.model.get('name'),
	            field_name: 'name'
	        }));
	        this.showChildView('course', new _CheckboxWidget2.default({
	            label: "Ce document concerne-t-il une formation professionelle continue ?",
	            title: "Formation professionnelle",
	            value: this.model.get('course'),
	            field_name: 'course'
	        }));
	        if (_.has(this.section, 'prefix')) {
	            this.showChildView('prefix', new _InputWidget2.default({
	                title: "Préfixe du numéro de facture",
	                value: this.model.get('prefix'),
	                field_name: 'prefix'
	            }));
	        }
	        if (_.has(this.section, 'financial_year')) {
	            this.showChildView('financial_year', new _InputWidget2.default({
	                title: "Année comptable de référence",
	                value: this.model.get('financial_year'),
	                field_name: 'financial_year'
	            }));
	        }
	    }
	});
	exports.default = GeneralView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 110 */
/*!*******************************************!*\
  !*** ./src/widgets/CheckboxListWidget.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _jquery = __webpack_require__(/*! jquery */ 2);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : CheckboxListWidget.js
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/CheckboxListWidget.mustache */ 111);
	
	var CheckboxListWidget = _backbone2.default.View.extend({
	    template: template,
	    ui: {
	        checkboxes: 'input[type=checkbox]'
	    },
	    events: {
	        'click @ui.checkboxes': 'onClick'
	    },
	    getCurrentValues: function getCurrentValues() {
	        var checkboxes = this.$el.find('input[type=checkbox]:checked');
	        var res = [];
	        _.each(checkboxes, function (checkbox) {
	            res.push((0, _jquery2.default)(checkbox).attr('value'));
	        });
	        return res;
	    },
	    onClick: function onClick(event) {
	        this.triggerMethod('finish', this.getOption('field_name'), this.getCurrentValues());
	    },
	    templateContext: function templateContext() {
	        var id_key = (0, _tools.getOpt)(this, 'id_key', 'id');
	        var options = this.getOption('options');
	        var current_values = this.getOption('value');
	        (0, _tools.updateSelectOptions)(options, current_values, id_key);
	
	        return {
	            title: this.getOption('title'),
	            description: this.getOption('description'),
	            field_name: this.getOption('field_name'),
	            options: options,
	            editable: (0, _tools.getOpt)(this, 'editable', true)
	        };
	    }
	});
	exports.default = CheckboxListWidget;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 111 */
/*!***********************************************************!*\
  !*** ./src/widgets/templates/CheckboxListWidget.mustache ***!
  \***********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "    <label>"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</label>\n";
	},"3":function(depth0,helpers,partials,data,depths) {
	  var stack1, buffer = "";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.options : depth0), {"name":"each","hash":{},"fn":this.program(4, data, depths),"inverse":this.program(9, data, depths),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"4":function(depth0,helpers,partials,data,depths) {
	  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression, buffer = "        <div class='checkbox'>\n            <label>\n            <input type='checkbox'\n                name='"
	    + escapeExpression(lambda((depths[1] != null ? depths[1].field_name : depths[1]), depth0))
	    + "'\n                value='"
	    + escapeExpression(lambda((depth0 != null ? depth0.id : depth0), depth0))
	    + "'\n                ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.selected : depth0), {"name":"if","hash":{},"fn":this.program(5, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += " /> "
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "\n            </label>\n        </div>\n";
	  stack1 = helpers['if'].call(depth0, (depths[1] != null ? depths[1].description : depths[1]), {"name":"if","hash":{},"fn":this.program(7, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"5":function(depth0,helpers,partials,data) {
	  return "checked";
	  },"7":function(depth0,helpers,partials,data,depths) {
	  var lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "        <span class='help-block'>"
	    + escapeExpression(lambda((depths[1] != null ? depths[1].description : depths[1]), depth0))
	    + "</span>\n";
	},"9":function(depth0,helpers,partials,data) {
	  return "        <div></div>\n";
	  },"11":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "        <ul>\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.options : depth0), {"name":"each","hash":{},"fn":this.program(12, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "        </ul>\n";
	},"12":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.selected : depth0), {"name":"if","hash":{},"fn":this.program(13, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"13":function(depth0,helpers,partials,data) {
	  var lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "            <li>"
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "</li>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data,depths) {
	  var stack1, buffer = "<div class='form-group'>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(1, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.editable : depth0), {"name":"if","hash":{},"fn":this.program(3, data, depths),"inverse":this.program(11, data, depths),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>\n";
	},"useData":true,"useDepths":true});

/***/ }),
/* 112 */
/*!***************************************!*\
  !*** ./src/widgets/CheckboxWidget.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _jquery = __webpack_require__(/*! jquery */ 2);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : CheckboxWidget.js
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/CheckboxWidget.mustache */ 113);
	
	var CheckboxWidget = _backbone2.default.View.extend({
	    template: template,
	    ui: {
	        checkbox: 'input[type=checkbox]'
	    },
	    events: {
	        'click @ui.checkbox': 'onClick'
	    },
	    getCurrentValue: function getCurrentValue() {
	        var checked = this.getUI('checkbox').prop('checked');
	        if (checked) {
	            return (0, _tools.getOpt)(this, 'true_val', '1');
	        } else {
	            return (0, _tools.getOpt)(this, 'false_val', '0');
	        }
	    },
	    onClick: function onClick(event) {
	        this.triggerMethod('finish', this.getOption('field_name'), this.getCurrentValue());
	    },
	    templateContext: function templateContext() {
	        var true_val = (0, _tools.getOpt)(this, 'true_val', '1');
	        var checked = this.getOption('value') == true_val;
	        return {
	            title: this.getOption('title'),
	            label: this.getOption('label'),
	            description: this.getOption('description'),
	            field_name: this.getOption('field_name'),
	            checked: checked,
	            editable: (0, _tools.getOpt)(this, 'editable', true)
	        };
	    }
	});
	exports.default = CheckboxWidget;

/***/ }),
/* 113 */
/*!*******************************************************!*\
  !*** ./src/widgets/templates/CheckboxWidget.mustache ***!
  \*******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "    <label>"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</label>\n";
	},"3":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "        <div class='checkbox'>\n            <label>\n            <input type='checkbox'\n                name='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "'\n                value='true'\n                ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.checked : depth0), {"name":"if","hash":{},"fn":this.program(4, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += " /> "
	    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
	    + "\n            </label>\n        </div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.description : depth0), {"name":"if","hash":{},"fn":this.program(6, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"4":function(depth0,helpers,partials,data) {
	  return "checked";
	  },"6":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "        <span class='help-block'>"
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + "</span>\n";
	},"8":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "        <div>"
	    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
	    + "</div>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<div class='form-group'>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.editable : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.program(8, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>\n";
	},"useData":true});

/***/ }),
/* 114 */
/*!***************************************!*\
  !*** ./src/widgets/TextAreaWidget.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	var _tinymce = __webpack_require__(/*! ../tinymce.js */ 115);
	
	var _tinymce2 = _interopRequireDefault(_tinymce);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/TextAreaWidget.mustache */ 120); /*
	                                                                * File Name : TextAreaWidget.js
	                                                                *
	                                                                * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                                * Company : Majerti ( http://www.majerti.fr )
	                                                                *
	                                                                * This software is distributed under GPLV3
	                                                                * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                *
	                                                                */
	
	var TextAreaWidget = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'form-group',
	    template: template,
	    ui: {
	        textarea: 'textarea'
	    },
	    events: {
	        'keyup @ui.textarea': 'onKeyUp',
	        'blur @ui.textarea': 'onBlur'
	    },
	    onKeyUp: function onKeyUp() {
	        this.triggerMethod('change', this.getOption('field_name'), this.getUI('textarea').val());
	    },
	    onBlur: function onBlur() {
	        this.triggerMethod('finish', this.getOption('field_name'), this.getUI('textarea').val());
	    },
	    getTagId: function getTagId() {
	        /*
	         * Return an id for the current textarea
	         */
	        var cid = (0, _tools.getOpt)(this, 'cid', '');
	        if (cid === '') {
	            return false;
	        }
	        var field_name = this.getOption('field_name');
	        return field_name + "-" + cid;
	    },
	    templateContext: function templateContext() {
	        return {
	            title: this.getOption('title'),
	            description: this.getOption('description'),
	            field_name: this.getOption('field_name'),
	            value: (0, _tools.getOpt)(this, 'value', ''),
	            rows: (0, _tools.getOpt)(this, 'rows', 3),
	            editable: (0, _tools.getOpt)(this, 'editable', true),
	            tagId: this.getTagId(),
	            placeholder: (0, _tools.getOpt)(this, "placeholder", false)
	        };
	    },
	    onAttach: function onAttach() {
	        var tiny = (0, _tools.getOpt)(this, 'tinymce', false);
	        if (tiny) {
	            var onblur = this.onBlur.bind(this);
	            var onkeyup = this.onKeyUp.bind(this);
	            (0, _tinymce2.default)({
	                selector: "#" + this.getTagId(),
	                init_instance_callback: function init_instance_callback(editor) {
	                    editor.on('blur', onblur);
	                    editor.on('keyup', onkeyup);
	                    editor.on('change', function () {
	                        tinymce.triggerSave();
	                    });
	                }
	            });
	        }
	    }
	});
	exports.default = TextAreaWidget;

/***/ }),
/* 115 */,
/* 116 */,
/* 117 */,
/* 118 */,
/* 119 */,
/* 120 */
/*!*******************************************************!*\
  !*** ./src/widgets/templates/TextAreaWidget.mustache ***!
  \*******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    <textarea name='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "' ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.tagId : depth0), {"name":"if","hash":{},"fn":this.program(4, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += " class='form-control' rows='"
	    + escapeExpression(((helper = (helper = helpers.rows || (depth0 != null ? depth0.rows : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"rows","hash":{},"data":data}) : helper)))
	    + "' ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.placeholder : depth0), {"name":"if","hash":{},"fn":this.program(6, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + ">"
	    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
	    + "</textarea>\n";
	},"2":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "    <label for='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "'>"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</label>\n";
	},"4":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "id=\""
	    + escapeExpression(((helper = (helper = helpers.tagId || (depth0 != null ? depth0.tagId : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tagId","hash":{},"data":data}) : helper)))
	    + "\"";
	},"6":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "placeholde=\""
	    + escapeExpression(((helper = (helper = helpers.placeholder || (depth0 != null ? depth0.placeholder : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"placeholder","hash":{},"data":data}) : helper)))
	    + "\"";
	},"8":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "    "
	    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
	    + "\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.editable : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(8, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 121 */
/*!*********************************************!*\
  !*** ./src/task/views/StatusHistoryView.js ***!
  \*********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _StatusHistoryCollectionView = __webpack_require__(/*! ./StatusHistoryCollectionView.js */ 122);
	
	var _StatusHistoryCollectionView2 = _interopRequireDefault(_StatusHistoryCollectionView);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var StatusHistoryView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/StatusHistoryView.mustache */ 124),
	    regions: {
	        comments: '.comments'
	    },
	    onRender: function onRender() {
	        var collection = this.getOption('collection');
	        this.showChildView("comments", new _StatusHistoryCollectionView2.default({ collection: collection }));
	    }
	}); /*
	     * File Name : StatusHistoryView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = StatusHistoryView;

/***/ }),
/* 122 */
/*!*******************************************************!*\
  !*** ./src/task/views/StatusHistoryCollectionView.js ***!
  \*******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _date = __webpack_require__(/*! ../../date.js */ 32);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : StatusHistoryCollectionView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var StatusHistoryItemView = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'row',
	    template: __webpack_require__(/*! ./templates/StatusHistoryItemView.mustache */ 123),
	    templateContext: function templateContext() {
	        return {
	            date: (0, _date.formatDate)(this.model.get('date'))
	        };
	    }
	});
	
	var StatusHistoryCollectionView = _backbone2.default.CollectionView.extend({
	    tagName: 'div',
	    className: 'col-xs-12',
	    childView: StatusHistoryItemView
	});
	exports.default = StatusHistoryCollectionView;

/***/ }),
/* 123 */
/*!*****************************************************************!*\
  !*** ./src/task/views/templates/StatusHistoryItemView.mustache ***!
  \*****************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<p>"
	    + escapeExpression(((helper = (helper = helpers.comment || (depth0 != null ? depth0.comment : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"comment","hash":{},"data":data}) : helper)))
	    + "</p>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class='col-xs-12'>\n<blockquote class='status_history_item'>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.comment : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "<footer>Statut : "
	    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
	    + " -  Le "
	    + escapeExpression(((helper = (helper = helpers.date || (depth0 != null ? depth0.date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"date","hash":{},"data":data}) : helper)))
	    + " par "
	    + escapeExpression(((helper = (helper = helpers.account || (depth0 != null ? depth0.account : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"account","hash":{},"data":data}) : helper)))
	    + "</footer>\n</blockquote>\n</div>\n";
	},"useData":true});

/***/ }),
/* 124 */
/*!*************************************************************!*\
  !*** ./src/task/views/templates/StatusHistoryView.mustache ***!
  \*************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<a\n    data-target='#comments-more'\n    data-toggle='collapse'\n    aria-expanded=\"false\"\n    aria-controls=\"comments-more\"\n    >\n    <i class='glyphicon glyphicon-plus-sign'></i>\nHistorique des commentaires et changements de statut\n</a>\n<div id='comments-more' class='collapse row comments'>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 125 */
/*!*******************************************************!*\
  !*** ./src/task/views/templates/GeneralView.mustache ***!
  \*******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "        <a\n                data-target='#files-more'\n                data-toggle='collapse'\n                aria-expanded=\"false\"\n                aria-controls=\"files-more\"\n                >\n                <i class='glyphicon glyphicon-plus-sign'></i>\n            Fichiers attachés\n        </a>\n        <div id=\"files-more\" class='collapse row'>\n        <div class='col-xs-12'>\n        <ul>\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.attachments : depth0), {"name":"each","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "        </ul>\n        </div>\n        </div>\n";
	},"2":function(depth0,helpers,partials,data) {
	  var lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "            <li>\n                <a href='/files/"
	    + escapeExpression(lambda((depth0 != null ? depth0.id : depth0), depth0))
	    + "' target='_blank'>\n                <i class='fa fa-file'></i> "
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "\n                </a>\n            </li>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<h2>Informations générales <small>Ces informations n'apparaissent pas dans le PDF</small></h2>\n<div class='content'>\n    <form class='form' name='common' action=\"#\" onSubmit=\"return false;\">\n        <div class='row'>\n            <div class='col-md-6 col-xs-12'>\n                <div class='name'></div>\n            </div>\n            <div class='col-md-6 col-xs-12'>\n                <div class='course'></div>\n            </div>\n        </div>\n        <div class='row'>\n            <div class='col-md-6 col-xs-12'>\n                <div class='prefix'></div>\n            </div>\n            <div class='col-md-6 col-xs-12'>\n                <div class='financial_year'></div>\n            </div>\n        </div>\n    </form>\n    <div class='status_history'>\n    </div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.attachments : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>\n";
	},"useData":true});

/***/ }),
/* 126 */
/*!**************************************!*\
  !*** ./src/task/views/CommonView.js ***!
  \**************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _jquery = __webpack_require__(/*! jquery */ 2);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _FormBehavior = __webpack_require__(/*! ../../base/behaviors/FormBehavior.js */ 73);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _CheckboxListWidget = __webpack_require__(/*! ../../widgets/CheckboxListWidget.js */ 110);
	
	var _CheckboxListWidget2 = _interopRequireDefault(_CheckboxListWidget);
	
	var _DatePickerWidget = __webpack_require__(/*! ../../widgets/DatePickerWidget.js */ 75);
	
	var _DatePickerWidget2 = _interopRequireDefault(_DatePickerWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 77);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : CommonView.js
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/CommonView.mustache */ 127);
	
	var CommonView = _backbone2.default.View.extend({
	    /*
	     * Wrapper around the component making part of the 'common'
	     * invoice/estimation form, provide a main layout with regions for each
	     * field
	     */
	    behaviors: [{
	        behaviorClass: _FormBehavior2.default,
	        errorMessage: "Vérifiez votre saisie"
	    }],
	    tagName: 'div',
	    className: 'form-section',
	    template: template,
	    fields: ['date', 'address', 'description', 'workplace', 'mentions'],
	    regions: {
	        errors: '.errors',
	        date: '.date',
	        description: '.description',
	        address: '.address',
	        workplace: '.workplace',
	        mentions: '.mentions'
	    },
	    childViewTriggers: {
	        'change': 'data:modified',
	        'finish': 'data:persist'
	    },
	    modelEvents: {
	        'validated:invalid': 'showErrors',
	        'validated:valid': 'hideErrors'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('facade');
	        this.listenTo(channel, 'bind:validation', this.bindValidation);
	        this.listenTo(channel, 'unbind:validation', this.unbindValidation);
	        this.mentions_options = _backbone4.default.channel('config').request('get:options', 'mentions');
	    },
	    showErrors: function showErrors(model, errors) {
	        this.$el.addClass('error');
	    },
	    hideErrors: function hideErrors(model) {
	        this.$el.removeClass('error');
	    },
	    bindValidation: function bindValidation() {
	        _backboneValidation2.default.bind(this);
	    },
	    unbindValidation: function unbindValidation() {
	        _backboneValidation2.default.unbind(this);
	    },
	    getMentionIds: function getMentionIds() {
	        var mention_ids = this.model.get('mentions');
	        return mention_ids;
	    },
	    isMoreSet: function isMoreSet() {
	        var mention_ids = this.getMentionIds();
	        if (mention_ids.length > 0) {
	            return true;
	        }
	        if (this.model.get('workplace')) {
	            return true;
	        }
	        return false;
	    },
	    templateContext: function templateContext() {
	        return { is_more_set: this.isMoreSet() };
	    },
	    onRender: function onRender() {
	        this.showChildView('date', new _DatePickerWidget2.default({
	            date: this.model.get('date'),
	            title: "Date",
	            field_name: "date"
	        }));
	
	        this.showChildView('address', new _TextAreaWidget2.default({
	            title: 'Adresse du client',
	            value: this.model.get('address'),
	            field_name: 'address',
	            rows: 5
	        }));
	
	        this.showChildView('description', new _TextAreaWidget2.default({
	            title: 'Objet du document',
	            value: this.model.get('description'),
	            field_name: 'description',
	            rows: 3
	        }));
	
	        this.showChildView('workplace', new _TextAreaWidget2.default({
	            title: 'Lieu des travaux',
	            value: this.model.get('workplace'),
	            field_name: 'workplace',
	            rows: 3
	        }));
	        var mention_list = new _CheckboxListWidget2.default({
	            options: this.mentions_options,
	            value: this.getMentionIds(),
	            title: "Mentions facultatives",
	            description: "Choisissez les mentions à ajouter au document",
	            field_name: "mentions"
	        });
	        this.showChildView('mentions', mention_list);
	    }
	});
	exports.default = CommonView;

/***/ }),
/* 127 */
/*!******************************************************!*\
  !*** ./src/task/views/templates/CommonView.mustache ***!
  \******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "in";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<h2>Entêtes du document</h2>\n<div class='content'>\n    <div class='errors'></div>\n    <form class='form' name='common' action=\"#\" onSubmit=\"return false;\">\n        <div class='row'>\n            <div class='col-md-6 col-xs-12'>\n                <div class='date'></div>\n                <div class='description'></div>\n            </div>\n            <div class='col-md-6 col-xs-12'>\n                <div class='address'></div>\n            </div>\n        </div>\n        <a\n            data-target='#common-more'\n            data-toggle='collapse'\n            aria-expanded=\"false\"\n            aria-controls=\"common-more\"\n            >\n            <i class='glyphicon glyphicon-plus-sign'></i> Plus d'options (Lieu des travaux, mentions facultatives ...)\n        </a>\n        <div class='collapse row ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_more_set : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "' id=\"common-more\">\n            <div class='col-md-6 col-xs-12'>\n                <div class='workplace'></div>\n            </div>\n            <div class='col-md-6 col-xs-12'>\n                <div class='mentions'>\n                </div>\n            </div>\n        </div>\n    </form>\n</div>\n";
	},"useData":true});

/***/ }),
/* 128 */
/*!*****************************************!*\
  !*** ./src/task/views/TaskBlockView.js ***!
  \*****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TaskGroupModel = __webpack_require__(/*! ../models/TaskGroupModel.js */ 129);
	
	var _TaskGroupModel2 = _interopRequireDefault(_TaskGroupModel);
	
	var _TaskGroupCollectionView = __webpack_require__(/*! ./TaskGroupCollectionView.js */ 134);
	
	var _TaskGroupCollectionView2 = _interopRequireDefault(_TaskGroupCollectionView);
	
	var _TaskGroupFormView = __webpack_require__(/*! ./TaskGroupFormView.js */ 150);
	
	var _TaskGroupFormView2 = _interopRequireDefault(_TaskGroupFormView);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 22);
	
	var _ErrorView = __webpack_require__(/*! ./ErrorView.js */ 152);
	
	var _ErrorView2 = _interopRequireDefault(_ErrorView);
	
	var _DisplayUnitsView = __webpack_require__(/*! ./DisplayUnitsView.js */ 154);
	
	var _DisplayUnitsView2 = _interopRequireDefault(_DisplayUnitsView);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TaskBlockView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/TaskBlockView.mustache */ 156),
	    tagName: 'div',
	    className: 'form-section',
	    regions: {
	        errors: '.group-errors',
	        container: '.group-container',
	        modalRegion: ".group-modalregion",
	        display_units_container: '.display-units-container'
	    },
	    ui: {
	        add_button: 'button.add'
	    },
	    triggers: {
	        "click @ui.add_button": "group:add"
	    },
	    childViewEvents: {
	        'group:edit': 'onGroupEdit',
	        'group:delete': 'onGroupDelete',
	        'catalog:insert': 'onCatalogInsert'
	    },
	    collectionEvents: {
	        'change': 'hideErrors'
	    },
	    initialize: function initialize(options) {
	        this.collection = options['collection'];
	        this.listenTo(this.collection, 'validated:invalid', this.showErrors);
	        this.listenTo(this.collection, 'validated:valid', this.hideErrors.bind(this));
	    },
	    showErrors: function showErrors(model, errors) {
	        this.detachChildView('errors');
	        this.showChildView('errors', new _ErrorView2.default({ errors: errors }));
	        this.$el.addClass('error');
	    },
	    hideErrors: function hideErrors(model) {
	        this.detachChildView('errors');
	        this.$el.removeClass('error');
	    },
	
	    onDeleteSuccess: function onDeleteSuccess() {
	        (0, _backboneTools.displayServerSuccess)("Vos données ont bien été supprimées");
	    },
	    onDeleteError: function onDeleteError() {
	        (0, _backboneTools.displayServerError)("Une erreur a été rencontrée lors de la " + "suppression de cet élément");
	    },
	    onGroupDelete: function onGroupDelete(childView) {
	        var result = window.confirm("Êtes-vous sûr de vouloir supprimer cet ouvrage ?");
	        if (result) {
	            childView.model.destroy({
	                success: this.onDeleteSuccess,
	                error: this.onDeleteError
	            });
	        }
	    },
	    onGroupEdit: function onGroupEdit(childView) {
	        this.showTaskGroupForm(childView.model, "Modifier cet ouvrage");
	    },
	    onGroupAdd: function onGroupAdd() {
	        var model = new _TaskGroupModel2.default({
	            order: this.collection.getMaxOrder() + 1
	        });
	        this.showTaskGroupForm(model, "Ajouter un ouvrage");
	    },
	    onEditGroup: function onEditGroup(childView) {
	        var model = childView.model;
	        this.showTaskGroupForm(model, "Modifier cet ouvrage");
	    },
	    showTaskGroupForm: function showTaskGroupForm(model, title) {
	        var form = new _TaskGroupFormView2.default({
	            model: model,
	            title: title,
	            destCollection: this.collection
	        });
	        this.showChildView('modalRegion', form);
	    },
	    onCatalogInsert: function onCatalogInsert(sale_product_group_ids) {
	        this.collection.load_from_catalog(sale_product_group_ids);
	        this.getChildView('modalRegion').triggerMethod('modal:close');
	    },
	    onChildviewDestroyModal: function onChildviewDestroyModal() {
	        this.detachChildView('modalRegion');
	        this.getRegion('modalRegion').empty();
	    },
	    onRender: function onRender() {
	        this.showChildView('display_units_container', new _DisplayUnitsView2.default({ model: this.model }));
	        this.showChildView('container', new _TaskGroupCollectionView2.default({ collection: this.collection }));
	    }
	}); /*
	     * File Name : TaskBlockView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = TaskBlockView;

/***/ }),
/* 129 */
/*!*******************************************!*\
  !*** ./src/task/models/TaskGroupModel.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _TaskLineCollection = __webpack_require__(/*! ./TaskLineCollection.js */ 130);
	
	var _TaskLineCollection2 = _interopRequireDefault(_TaskLineCollection);
	
	var _BaseModel = __webpack_require__(/*! ./BaseModel.js */ 132);
	
	var _BaseModel2 = _interopRequireDefault(_BaseModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TaskGroupModel = _BaseModel2.default.extend({
	    props: ['id', 'order', 'title', 'description', 'lines', 'task_id'],
	    validation: {
	        lines: function lines(value) {
	            if (value.length === 0) {
	                return "Veuillez saisir au moins une prestation";
	            }
	        }
	    },
	    initialize: function initialize() {
	        this.populate();
	        this.on('change:id', this.populate.bind(this));
	        this.listenTo(this.lines, 'add', this.updateLines);
	        this.listenTo(this.lines, 'sync', this.updateLines);
	        this.listenTo(this.lines, 'remove', this.updateLines);
	    },
	    populate: function populate() {
	        if (this.get('id')) {
	            this.lines = new _TaskLineCollection2.default(this.get('lines'));
	            this.lines.url = this.url() + '/task_lines';
	        }
	    },
	    updateLines: function updateLines() {
	        this.set('lines', this.lines.toJSON());
	    },
	
	    loadProductGroup: function loadProductGroup(sale_product_group_datas) {
	        this.set('title', sale_product_group_datas.title);
	        this.set('description', sale_product_group_datas.description);
	        this.trigger('set:product_group');
	    },
	    ht: function ht() {
	        return this.lines.ht();
	    },
	    tvaParts: function tvaParts() {
	        return this.lines.tvaParts();
	    },
	    ttc: function ttc() {
	        return this.lines.ttc();
	    }
	}); /*
	     * File Name : TaskGroupModel.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = TaskGroupModel;

/***/ }),
/* 130 */
/*!***********************************************!*\
  !*** ./src/task/models/TaskLineCollection.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _TaskLineModel = __webpack_require__(/*! ./TaskLineModel.js */ 131);
	
	var _TaskLineModel2 = _interopRequireDefault(_TaskLineModel);
	
	var _backbone = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _OrderableCollection = __webpack_require__(/*! ./OrderableCollection.js */ 133);
	
	var _OrderableCollection2 = _interopRequireDefault(_OrderableCollection);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TaskLineCollection = _OrderableCollection2.default.extend({
	    model: _TaskLineModel2.default,
	    initialize: function initialize(options) {
	        TaskLineCollection.__super__.initialize.apply(this, options);
	        this.on('remove', this.channelCall);
	        this.on('sync', this.channelCall);
	        this.on('reset', this.channelCall);
	        this.on('add', this.channelCall);
	    },
	    channelCall: function channelCall() {
	        var channel = _backbone2.default.channel('facade');
	        channel.trigger('changed:task');
	    },
	    load_from_catalog: function load_from_catalog(sale_product_ids) {
	        var serverRequest = (0, _tools.ajax_call)(this.url + '?action=load_from_catalog', { sale_product_ids: sale_product_ids }, 'POST');
	        serverRequest.then(this.fetch.bind(this));
	    },
	    ht: function ht() {
	        var result = 0;
	        this.each(function (model) {
	            result += model.ht();
	        });
	        return result;
	    },
	    tvaParts: function tvaParts() {
	        var result = {};
	        this.each(function (model) {
	            var tva_amount = model.tva();
	            var tva = model.get('tva');
	            if (tva in result) {
	                tva_amount += result[tva];
	            }
	            result[tva] = tva_amount;
	        });
	        return result;
	    },
	    ttc: function ttc() {
	        var result = 0;
	        this.each(function (model) {
	            result += model.ttc();
	        });
	        return result;
	    },
	    validate: function validate() {
	        var result = {};
	        this.each(function (model) {
	            var res = model.validate();
	            if (res) {
	                _underscore2.default.extend(result, res);
	            }
	        });
	        return result;
	    }
	}); /*
	     * File Name : TaskLineCollection.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = TaskLineCollection;

/***/ }),
/* 131 */
/*!******************************************!*\
  !*** ./src/task/models/TaskLineModel.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _BaseModel = __webpack_require__(/*! ./BaseModel.js */ 132);
	
	var _BaseModel2 = _interopRequireDefault(_BaseModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : TaskLineModel.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var TaskLineModel = _BaseModel2.default.extend({
	    props: ['id', 'order', 'description', 'cost', 'quantity', 'unity', 'tva', 'product_id', 'task_id'],
	    validation: {
	        description: {
	            required: true,
	            msg: "Veuillez saisir un objet"
	        },
	        cost: {
	            required: true,
	            pattern: "amount",
	            msg: "Veuillez saisir un coup unitaire, dans la limite de 5 chiffres après la virgule"
	        },
	        quantity: {
	            required: true,
	            pattern: "amount",
	            msg: "Veuillez saisir une quantité, dans la limite de 5 chiffres après la virgule"
	        },
	        tva: {
	            required: true,
	            pattern: "number",
	            msg: "Veuillez sélectionner une TVA"
	        }
	    },
	    ht: function ht() {
	        return (0, _math.strToFloat)(this.get('cost')) * (0, _math.strToFloat)(this.get('quantity'));
	    },
	    tva_value: function tva_value() {
	        var tva = this.get('tva');
	        if (tva < 0) {
	            tva = 0;
	        }
	        return tva;
	    },
	    tva: function tva() {
	        var val = (0, _math.getTvaPart)(this.ht(), this.tva_value());
	        return val;
	    },
	    ttc: function ttc() {
	        return this.ht() + this.tva();
	    },
	    loadProduct: function loadProduct(product_datas) {
	        this.set('description', product_datas.label);
	        this.set('cost', product_datas.value);
	        this.set('quantity', 1);
	        this.set('tva', product_datas.tva);
	        this.trigger('set:product');
	    }
	});
	
	exports.default = TaskLineModel;

/***/ }),
/* 132 */
/*!**************************************!*\
  !*** ./src/task/models/BaseModel.js ***!
  \**************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : BaseModel.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var BaseModel = _backbone2.default.Model.extend({
	    props: null,
	    constructor: function constructor() {
	        if (!_underscore2.default.isNull(this.props)) {
	            arguments[0] = _underscore2.default.pick(arguments[0], this.props);
	            arguments[0] = _underscore2.default.omit(arguments[0], function (value) {
	                return _underscore2.default.isNull(value) || _underscore2.default.isUndefined(value);
	            });
	        }
	        _backbone2.default.Model.apply(this, arguments);
	    },
	    toJSON: function toJSON(options) {
	        var attributes = _underscore2.default.clone(this.attributes);
	        if (!_underscore2.default.isNull(this.props)) {
	            attributes = _underscore2.default.pick(attributes, this.props);
	            attributes = _underscore2.default.omit(attributes, function (value) {
	                return _underscore2.default.isNull(value) || _underscore2.default.isUndefined(value);
	            });
	        }
	        return attributes;
	    },
	    rollback: function rollback() {
	        if (this.get('id')) {
	            this.fetch();
	        }
	    }
	});
	exports.default = BaseModel;

/***/ }),
/* 133 */
/*!************************************************!*\
  !*** ./src/task/models/OrderableCollection.js ***!
  \************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : OrderableCollection.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var OrderableCollection = _backbone2.default.Collection.extend({
	    comparator: 'order',
	    initialize: function initialize(options) {
	        this.on('change:reorder', this.updateModelOrder);
	        this.updateModelOrder(false);
	    },
	    updateModelOrder: function updateModelOrder(sync) {
	        /*
	         * Update the model's order
	         *
	         * :param bool sync: Should we synchronize the change ?
	         */
	        if (_underscore2.default.isUndefined(sync)) {
	            sync = true;
	        }
	        this.each(function (model, index) {
	            model.set('order', index);
	            if (sync) {
	                model.save({ 'order': index }, { patch: true });
	            }
	        });
	    },
	    getMinOrder: function getMinOrder() {
	        if (this.models.length == 0) {
	            return 0;
	        }
	        var first_model = _underscore2.default.min(this.models, function (model) {
	            return model.get('order');
	        });
	        return first_model.get('order');
	    },
	    getMaxOrder: function getMaxOrder() {
	        if (this.models.length == 0) {
	            return 0;
	        }
	        var last_model = _underscore2.default.max(this.models, function (model) {
	            return model.get('order');
	        });
	        return last_model.get('order');
	    },
	    moveUp: function moveUp(model) {
	        // I see move up as the -1
	        var index = this.indexOf(model);
	        if (index > 0) {
	            this.models.splice(index - 1, 0, this.models.splice(index, 1)[0]);
	            this.trigger('change:reorder');
	        }
	    },
	    moveDown: function moveDown(model) {
	        // I see move up as the -1
	        var index = this.indexOf(model);
	        if (index < this.models.length) {
	            this.models.splice(index + 1, 0, this.models.splice(index, 1)[0]);
	            this.trigger('change:reorder');
	        }
	    }
	});
	exports.default = OrderableCollection;

/***/ }),
/* 134 */
/*!***************************************************!*\
  !*** ./src/task/views/TaskGroupCollectionView.js ***!
  \***************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TaskGroupView = __webpack_require__(/*! ./TaskGroupView.js */ 135);
	
	var _TaskGroupView2 = _interopRequireDefault(_TaskGroupView);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : TaskGroupCollectionView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var TaskGroupCollectionView = _backbone2.default.CollectionView.extend({
	    tagName: 'div',
	    childView: _TaskGroupView2.default,
	    collectionEvents: {
	        'change:reorder': 'render',
	        'sync': 'render'
	    },
	    // Bubble up child view events
	    childViewTriggers: {
	        'edit': 'group:edit',
	        'delete': 'group:delete',
	        'catalog:insert': 'catalog:insert'
	    },
	    onChildviewOrderUp: function onChildviewOrderUp(childView) {
	        this.collection.moveUp(childView.model);
	    },
	    onChildviewOrderDown: function onChildviewOrderDown(childView) {
	        this.collection.moveDown(childView.model);
	    }
	});
	
	exports.default = TaskGroupCollectionView;

/***/ }),
/* 135 */
/*!*****************************************!*\
  !*** ./src/task/views/TaskGroupView.js ***!
  \*****************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TaskLineCollectionView = __webpack_require__(/*! ./TaskLineCollectionView.js */ 136);
	
	var _TaskLineCollectionView2 = _interopRequireDefault(_TaskLineCollectionView);
	
	var _TaskLineFormView = __webpack_require__(/*! ./TaskLineFormView.js */ 139);
	
	var _TaskLineFormView2 = _interopRequireDefault(_TaskLineFormView);
	
	var _TaskLineModel = __webpack_require__(/*! ../models/TaskLineModel.js */ 131);
	
	var _TaskLineModel2 = _interopRequireDefault(_TaskLineModel);
	
	var _TaskGroupTotalView = __webpack_require__(/*! ./TaskGroupTotalView.js */ 145);
	
	var _TaskGroupTotalView2 = _interopRequireDefault(_TaskGroupTotalView);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 22);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/TaskGroupView.mustache */ 149); /*
	                                                               * File Name : TaskGroupView.js
	                                                               *
	                                                               * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                               * Company : Majerti ( http://www.majerti.fr )
	                                                               *
	                                                               * This software is distributed under GPLV3
	                                                               * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                               *
	                                                               */
	
	
	var TaskGroupView = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'taskline-group row',
	    template: template,
	    regions: {
	        errors: '.errors',
	        lines: '.lines',
	        modalRegion: ".modalregion",
	        subtotal: '.subtotal'
	    },
	    ui: {
	        btn_add: ".btn-add",
	        up_button: 'button.up',
	        down_button: 'button.down',
	        edit_button: 'button.edit',
	        delete_button: 'button.delete'
	    },
	    triggers: {
	        'click @ui.up_button': 'order:up',
	        'click @ui.down_button': 'order:down',
	        'click @ui.edit_button': 'edit',
	        'click @ui.delete_button': 'delete'
	    },
	    events: {
	        "click @ui.btn_add": "onLineAdd"
	    },
	    childViewEvents: {
	        'line:edit': 'onLineEdit',
	        'line:delete': 'onLineDelete',
	        'catalog:insert': 'onCatalogInsert',
	        'destroy:modal': 'render'
	    },
	    initialize: function initialize(options) {
	        // Collection of task lines
	        this.collection = this.model.lines;
	        this.listenTo(this.collection, 'sync', this.showLines.bind(this));
	
	        var channel = _backbone4.default.channel('facade');
	        this.listenTo(channel, 'bind:validation', this.bindValidation);
	        this.listenTo(channel, 'unbind:validation', this.unbindValidation);
	        this.listenTo(this.model, 'validated:invalid', this.showErrors);
	        this.listenTo(this.model, 'validated:valid', this.hideErrors.bind(this));
	    },
	    isEmpty: function isEmpty() {
	        return this.model.lines.length === 0;
	    },
	    showErrors: function showErrors(model, errors) {
	        this.$el.addClass('error');
	    },
	    hideErrors: function hideErrors(model) {
	        this.$el.removeClass('error');
	    },
	    bindValidation: function bindValidation() {
	        _backboneValidation2.default.bind(this);
	    },
	    unbindValidation: function unbindValidation() {
	        _backboneValidation2.default.unbind(this);
	    },
	    showLines: function showLines() {
	        /*
	         * Show lines if it's not done yet
	         */
	        if (!_.isNull(this.getChildView('lines'))) {
	            this.showChildView('lines', new _TaskLineCollectionView2.default({ collection: this.collection }));
	        }
	    },
	
	    onRender: function onRender() {
	        if (!this.isEmpty()) {
	            this.showLines();
	        }
	        this.showChildView('subtotal', new _TaskGroupTotalView2.default({ collection: this.collection }));
	    },
	    onLineEdit: function onLineEdit(childView) {
	        this.showTaskLineForm(childView.model, "Modifier la prestation", true);
	    },
	    onLineAdd: function onLineAdd() {
	        var model = new _TaskLineModel2.default({
	            task_id: this.model.get('id'),
	            order: this.collection.getMaxOrder() + 1
	        });
	        this.showTaskLineForm(model, "Définir une prestation", false);
	    },
	    showTaskLineForm: function showTaskLineForm(model, title, edit) {
	        var form = new _TaskLineFormView2.default({
	            model: model,
	            title: title,
	            destCollection: this.collection,
	            edit: edit
	        });
	        this.showChildView('modalRegion', form);
	    },
	    onDeleteSuccess: function onDeleteSuccess() {
	        (0, _backboneTools.displayServerSuccess)("Vos données ont bien été supprimées");
	    },
	    onDeleteError: function onDeleteError() {
	        (0, _backboneTools.displayServerError)("Une erreur a été rencontrée lors de la " + "suppression de cet élément");
	    },
	    onLineDelete: function onLineDelete(childView) {
	        var result = window.confirm("Êtes-vous sûr de vouloir supprimer cette prestation ?");
	        if (result) {
	            childView.model.destroy({
	                success: this.onDeleteSuccess,
	                error: this.onDeleteError
	            });
	        }
	    },
	    onCatalogInsert: function onCatalogInsert(sale_product_ids) {
	        this.collection.load_from_catalog(sale_product_ids);
	        this.getChildView('modalRegion').triggerMethod('modal:close');
	    },
	    onChildviewDestroyModal: function onChildviewDestroyModal() {
	        this.getRegion('modalRegion').empty();
	    },
	    templateContext: function templateContext() {
	        var min_order = this.model.collection.getMinOrder();
	        var max_order = this.model.collection.getMaxOrder();
	        var order = this.model.get('order');
	        return {
	            not_is_empty: !this.isEmpty(),
	            total_ht: (0, _math.formatAmount)(this.model.ht(), false),
	            is_not_first: order != min_order,
	            is_not_last: order != max_order
	        };
	    }
	});
	exports.default = TaskGroupView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 136 */
/*!**************************************************!*\
  !*** ./src/task/views/TaskLineCollectionView.js ***!
  \**************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TaskLineView = __webpack_require__(/*! ./TaskLineView.js */ 137);
	
	var _TaskLineView2 = _interopRequireDefault(_TaskLineView);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : TaskLineCollectionView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var TaskLineCollectionView = _backbone2.default.CollectionView.extend({
	    tagName: 'div',
	    className: 'col-xs-12',
	    childView: _TaskLineView2.default,
	    sort: true,
	    collectionEvents: {
	        'change:reorder': 'render'
	    },
	    // Bubble up child view events
	    childViewTriggers: {
	        'edit': 'line:edit',
	        'delete': 'line:delete'
	    },
	    onChildviewOrderUp: function onChildviewOrderUp(childView) {
	        this.collection.moveUp(childView.model);
	    },
	    onChildviewOrderDown: function onChildviewOrderDown(childView) {
	        this.collection.moveDown(childView.model);
	    }
	});
	exports.default = TaskLineCollectionView;

/***/ }),
/* 137 */
/*!****************************************!*\
  !*** ./src/task/views/TaskLineView.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : TaskLineView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/TaskLineView.mustache */ 138);
	
	var TaskLineView = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'row taskline',
	    template: template,
	    ui: {
	        up_button: 'button.up',
	        down_button: 'button.down',
	        edit_button: 'button.edit',
	        delete_button: 'button.delete'
	    },
	    triggers: {
	        'click @ui.up_button': 'order:up',
	        'click @ui.down_button': 'order:down',
	        'click @ui.edit_button': 'edit',
	        'click @ui.delete_button': 'delete'
	    },
	    modelEvents: {
	        'change': 'render'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('config');
	        this.tva_options = channel.request('get:options', 'tvas');
	        this.product_options = channel.request('get:options', 'products');
	    },
	    getTvaLabel: function getTvaLabel() {
	        var res = "";
	        var current_value = this.model.get('tva');
	        _underscore2.default.each(this.tva_options, function (tva) {
	            if (tva.value == current_value) {
	                res = tva.name;
	            }
	        });
	        return res;
	    },
	    getProductLabel: function getProductLabel() {
	        var res = "";
	        var current_value = this.model.get('product_id');
	        _underscore2.default.each(this.product_options, function (product) {
	            if (product.id == current_value) {
	                res = product.label;
	            }
	        });
	        return res;
	    },
	    templateContext: function templateContext() {
	        var min_order = this.model.collection.getMinOrder();
	        var max_order = this.model.collection.getMaxOrder();
	        var order = this.model.get('order');
	        return {
	            ht: (0, _math.formatAmount)(this.model.ht(), false),
	            product: this.getProductLabel(),
	            tva_label: this.getTvaLabel(),
	            is_not_first: order != min_order,
	            is_not_last: order != max_order
	        };
	    }
	});
	exports.default = TaskLineView;

/***/ }),
/* 138 */
/*!********************************************************!*\
  !*** ./src/task/views/templates/TaskLineView.mustache ***!
  \********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "    <button type='button' class='btn btn-default btn-small up'>\n        <i class='glyphicon glyphicon-arrow-up'></i>\n    </button>\n    <br />\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "    <button type='button' class='btn btn-default btn-small down'>\n        <i class='glyphicon glyphicon-arrow-down'></i>\n    </button>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class='col-md-3 col-sm-4 col-xs-12 description'>";
	  stack1 = ((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n<div class='col-md-1 hidden-sm hidden-xs text-center'>"
	    + escapeExpression(((helper = (helper = helpers.cost || (depth0 != null ? depth0.cost : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"cost","hash":{},"data":data}) : helper)))
	    + "</div>\n<div class='col-md-1 hidden-sm hidden-xs text-center'>"
	    + escapeExpression(((helper = (helper = helpers.quantity || (depth0 != null ? depth0.quantity : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"quantity","hash":{},"data":data}) : helper)))
	    + "</div>\n<div class='col-lg-1 hidden-sm hidden-xs hidden-md text-center'>"
	    + escapeExpression(((helper = (helper = helpers.unity || (depth0 != null ? depth0.unity : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"unity","hash":{},"data":data}) : helper)))
	    + "</div>\n<div class='col-md-1 hidden-sm hidden-xs text-center'>"
	    + escapeExpression(((helper = (helper = helpers.tva_label || (depth0 != null ? depth0.tva_label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva_label","hash":{},"data":data}) : helper)))
	    + "</div>\n<div class='col-md-1 col-sm-1 col-xs-12 text-center'><b class='visible-xs text-left'>HT : ";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</b><span class='hidden-xs'>";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</span></div>\n<div class='col-lg-1 hidden-sm hidden-xs hidden-md text-center'>";
	  stack1 = ((helper = (helper = helpers.product || (depth0 != null ? depth0.product : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"product","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n<div class='col-md-5 col-lg-3 col-sm-7 text-right'>\n    <button type='button' class='btn btn-default edit'>\n        <i class='glyphicon glyphicon-pencil'></i> <span class='hidden-xs'>Modifier</span>\n    </button>\n    <button type='button' class='btn btn-default delete'>\n        <i class='glyphicon glyphicon-trash'></i> <span class='hidden-xs'>Supprimer</span>\n    </button>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_not_first : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_not_last : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>\n";
	},"useData":true});

/***/ }),
/* 139 */
/*!********************************************!*\
  !*** ./src/task/views/TaskLineFormView.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 77);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _SelectWidget = __webpack_require__(/*! ../../widgets/SelectWidget.js */ 79);
	
	var _SelectWidget2 = _interopRequireDefault(_SelectWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _ModalFormBehavior = __webpack_require__(/*! ../../base/behaviors/ModalFormBehavior.js */ 86);
	
	var _ModalFormBehavior2 = _interopRequireDefault(_ModalFormBehavior);
	
	var _CatalogTreeView = __webpack_require__(/*! ./CatalogTreeView.js */ 140);
	
	var _CatalogTreeView2 = _interopRequireDefault(_CatalogTreeView);
	
	var _LoadingWidget = __webpack_require__(/*! ../../widgets/LoadingWidget.js */ 142);
	
	var _LoadingWidget2 = _interopRequireDefault(_LoadingWidget);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : TaskLineFormView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/TaskLineFormView.mustache */ 144);
	
	var TaskLineFormView = _backbone2.default.View.extend({
	    template: template,
	    behaviors: [_ModalFormBehavior2.default],
	    regions: {
	        'order': '.order',
	        'description': '.description',
	        'cost': '.cost',
	        'quantity': '.quantity',
	        'unity': '.unity',
	        'tva': '.tva',
	        'product_id': '.product_id',
	        'catalog_container': '#catalog-container'
	    },
	    ui: {
	        main_tab: 'ul.nav-tabs li:first a'
	    },
	    childViewEvents: {
	        'catalog:edit': 'onCatalogEdit'
	    },
	    // Bubble up child view events
	    //
	    childViewTriggers: {
	        'catalog:insert': 'catalog:insert',
	        'change': 'data:modified',
	        'finish': 'data:modified'
	    },
	    modelEvents: {
	        'set:product': 'refreshForm',
	        'change:tva': 'refreshProductSelect'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('config');
	        this.workunit_options = channel.request('get:options', 'workunits');
	        this.tva_options = channel.request('get:options', 'tvas');
	        this.product_options = channel.request('get:options', 'products');
	        this.section = channel.request('get:form_section', 'tasklines');
	    },
	
	    onCatalogEdit: function onCatalogEdit(product_datas) {
	        this.model.loadProduct(product_datas);
	    },
	    isAddView: function isAddView() {
	        return !(0, _tools.getOpt)(this, 'edit', false);
	    },
	    templateContext: function templateContext() {
	        return {
	            title: this.getOption('title'),
	            add: this.isAddView()
	        };
	    },
	    refreshForm: function refreshForm() {
	        this.showChildView('order', new _InputWidget2.default({
	            value: this.model.get('order'),
	            field_name: 'order',
	            type: 'hidden'
	        }));
	        this.showChildView('description', new _TextAreaWidget2.default({
	            value: this.model.get('description'),
	            title: "Intitulé des postes",
	            field_name: "description",
	            tinymce: true,
	            cid: this.model.cid
	        }));
	        this.showChildView('cost', new _InputWidget2.default({
	            value: this.model.get('cost'),
	            title: "Prix unitaire HT",
	            field_name: "cost",
	            addon: "€"
	        }));
	        this.showChildView('quantity', new _InputWidget2.default({
	            value: this.model.get('quantity'),
	            title: "Quantité",
	            field_name: "quantity"
	        }));
	        this.showChildView('unity', new _SelectWidget2.default({
	            options: this.workunit_options,
	            title: "Unité",
	            value: this.model.get('unity'),
	            field_name: 'unity',
	            id_key: 'value'
	        }));
	        this.showChildView('tva', new _SelectWidget2.default({
	            options: this.tva_options,
	            title: "TVA",
	            value: this.model.get('tva'),
	            field_name: 'tva',
	            id_key: 'value'
	        }));
	        this.refreshProductSelect();
	        if (this.isAddView()) {
	            this.getUI('main_tab').tab('show');
	        }
	    },
	    getTvaIdFromValue: function getTvaIdFromValue(value) {
	        return _.findWhere(this.tva_options, { value: (0, _math.strToFloat)(value) });
	    },
	    getDefaultTva: function getDefaultTva() {
	        return _.findWhere(this.tva_options, { selected: true });
	    },
	    refreshProductSelect: function refreshProductSelect() {
	        /*
	         * Show the product select tag
	         */
	        if (_.has(this.section, 'product')) {
	            var product_options = this.product_options;
	
	            var tva_value = this.model.get('tva');
	            var tva;
	            if (!_.isUndefined(tva_value)) {
	                tva = this.getTvaIdFromValue(tva_value);
	            }
	            if (!_.isUndefined(tva)) {
	                product_options = _.where(this.product_options, { tva_id: tva.id });
	            } else {
	                var default_tva = this.getDefaultTva();
	                if (!_.isUndefined(default_tva)) {
	                    product_options = _.where(this.product_options, { tva_id: default_tva.id });
	                }
	            }
	            this.showChildView('product_id', new _SelectWidget2.default({
	                options: product_options,
	                title: "Code produit",
	                value: this.model.get('product_id'),
	                field_name: 'product_id',
	                id_key: 'id'
	            }));
	        }
	    },
	
	    onRender: function onRender() {
	        this.refreshForm();
	        if (this.isAddView()) {
	            this.showChildView('catalog_container', new _LoadingWidget2.default());
	            var req = (0, _tools.ajax_call)(AppOption['load_catalog_url'], { type: 'sale_product' });
	            req.done(this.onCatalogLoaded.bind(this));
	        }
	    },
	    onCatalogLoaded: function onCatalogLoaded(result) {
	        this.showChildView('catalog_container', new _CatalogTreeView2.default({
	            catalog: result,
	            title: "Catalogue produit"
	        }));
	    }
	});
	exports.default = TaskLineFormView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 140 */
/*!*******************************************!*\
  !*** ./src/task/views/CatalogTreeView.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : CatalogTreeView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/CatalogTreeView.mustache */ 141);
	
	var CatalogTreeView = _backbone2.default.View.extend({
	    /*
	     *
	     * Display a jstree with the datas provided by the attribute jstree from
	     * the catalog option
	     *
	     * :emits: catalog:selected ( <Array of ids> ) when the user submit its
	     * selection
	     */
	    tree_options: {
	        plugins: ["checkbox", 'types', "search"],
	        types: {
	            "default": { icon: "glyphicon glyphicon-triangle-right" },
	            "product": { icon: "glyphicon glyphicon-file" },
	            "group": { icon: "glyphicon glyphicon-book" }
	        },
	        search: {
	            show_only_matches: true,
	            case_insensitive: true
	        },
	        core: {
	            multiple: true
	        }
	    },
	    template: template,
	    ui: {
	        tree: '.tree',
	        search: 'input[name=catalog_search]',
	        edit_btn: 'button.edit-catalog',
	        insert_btn: 'button.insert-catalog'
	    },
	    events: {
	        'keyup @ui.search': 'onSearch',
	        'click @ui.edit_btn': 'onEdit',
	        'click @ui.insert_btn': 'onInsert'
	    },
	    onSearch: function onSearch() {
	        var searchString = this.getUI('search').val();
	        this.getUI('tree').jstree('search', searchString);
	    },
	    onAttach: function onAttach() {
	        var catalog = this.getOption('catalog');
	        if (_.has(catalog, "void_message")) {
	            this.getUI('edit_btn').prop('disabled', true);
	            this.getUI('insert_btn').prop('disabled', true);
	            this.getUI('search').prop('disabled', true);
	            this.getUI('tree').html(catalog.void_message);
	        } else {
	            var tree_tag = this.getUI('tree');
	            this.tree_options['core']['data'] = catalog.jstree;
	            tree_tag.jstree(this.tree_options);
	        }
	    },
	    productLoadCallback: function productLoadCallback(result) {
	        this.triggerMethod("catalog:edit", result);
	    },
	    onEdit: function onEdit() {
	        var url = null;
	
	        var selected = this.getUI('tree').jstree('get_selected', true);
	        _.each(selected, function (node) {
	            if (_.has(node.original, 'url')) {
	                url = node.original.url;
	            }
	        });
	        if (url === null) {
	            alert("Veuillez sélectionner au moins un élément");
	        } else {
	            var serverRequest = (0, _tools.ajax_call)(url);
	            serverRequest.done(this.productLoadCallback.bind(this));
	        }
	    },
	    onInsert: function onInsert() {
	        var result = [];
	        var selected = this.getUI('tree').jstree('get_selected', true);
	        _.each(selected, function (node) {
	            if (_.has(node.original, 'id')) {
	                result.push(node.original.id);
	            }
	        });
	        if (result.length === 0) {
	            alert("Veuillez sélectionner au moins un élément");
	        } else {
	            this.triggerMethod('catalog:insert', result);
	        }
	    }
	});
	exports.default = CatalogTreeView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 141 */
/*!***********************************************************!*\
  !*** ./src/task/views/templates/CatalogTreeView.mustache ***!
  \***********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<input class=\"form-control\" name=\"catalog_search\" placeholder=\"Nom ou référence\" type=\"text\" />\n<div class='tree'>\n</div>\n<div class=\"form-group\">\n    <div class=\"text-right\">\n        <button class=\"btn btn-success primary-action edit-catalog\" type=\"button\">\n            Éditer comme un nouvel élément\n        </button>\n        <button class=\"btn btn-success secondary-action insert-catalog\" type=\"button\">\n            Insérer les éléments sélectionnés\n        </button>\n    </div>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 142 */
/*!**************************************!*\
  !*** ./src/widgets/LoadingWidget.js ***!
  \**************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/LoadingWidget.mustache */ 143); /*
	                                                               * File Name : LoadingWidget.js
	                                                               *
	                                                               * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                               * Company : Majerti ( http://www.majerti.fr )
	                                                               *
	                                                               * This software is distributed under GPLV3
	                                                               * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                               *
	                                                               */
	
	var LoadingWidget = _backbone2.default.View.extend({
	  template: template
	});
	exports.default = LoadingWidget;

/***/ }),
/* 143 */
/*!******************************************************!*\
  !*** ./src/widgets/templates/LoadingWidget.mustache ***!
  \******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div class='loader'>\n<i class=\"fa fa-spinner fa-spin fa-3x fa-fw\" aria-hidden=\"true\"></i>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 144 */
/*!************************************************************!*\
  !*** ./src/task/views/templates/TaskLineFormView.mustache ***!
  \************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "            <ul class=\"nav nav-tabs\" role=\"tablist\">\n                <li role=\"presentation\" class=\"active\">\n                    <a href=\"#form-container\"\n                        aria-controls=\"form-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\"\n                        tabindex='-1'\n                        >\n                        Saisie libre\n                    </a>\n                </li>\n                <li role=\"presentation\">\n                    <a href=\"#catalog-container\"\n                        aria-controls=\"catalog-container\"\n                        role=\"tab\"\n                        tabindex='-1'\n                        data-toggle=\"tab\">\n                        Depuis le catalogue\n                    </a>\n                </li>\n            </ul>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane\"\n                    id=\"catalog-container\">\n                </div>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\" role=\"document\">\n	<div class=\"modal-content\">\n        <div class=\"modal-header\">\n            <button tabindex='-1' type=\"button\" class=\"close\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n            <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n        </div>\n        <div class=\"modal-body\">\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "            <div class='tab-content'>\n                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane fade in active\"\n                    id=\"form-container\">\n                    <form class='form taskline-form'>\n                        <div class='order'></div>\n                        <div class='description required'></div>\n                        <div class='cost required'></div>\n                        <div class='quantity required'></div>\n                        <div class='unity'></div>\n                        <div class='tva required'></div>\n                        <div class='product_id'></div>\n                        <button\n                            class='btn btn-success primary-action'\n                            type='submit'\n                            value='submit'>\n                            "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n                        </button>\n                        <button\n                            class='btn btn-default secondary-action'\n                            type='reset'\n                            value='submit'>\n                            Annuler\n                        </button>\n                    </form>\n                </div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "            </div>\n        </div>\n        <div class=\"modal-footer\">\n        </div>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n";
	},"useData":true});

/***/ }),
/* 145 */
/*!**********************************************!*\
  !*** ./src/task/views/TaskGroupTotalView.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _LabelRowWidget = __webpack_require__(/*! ../../widgets/LabelRowWidget.js */ 146);
	
	var _LabelRowWidget2 = _interopRequireDefault(_LabelRowWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TaskGroupTotalView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/LineContainerView.mustache */ 148),
	    regions: {
	        line: {
	            el: '.line',
	            replaceElement: true
	        }
	    },
	    collectionEvents: {
	        'change': 'render',
	        'remove': 'render',
	        'add': 'render'
	    },
	    onRender: function onRender() {
	        var values = (0, _math.formatAmount)(this.collection.ht(), false);
	        var view = new _LabelRowWidget2.default({
	            label: 'Sous total HT',
	            values: values
	        });
	        this.showChildView('line', view);
	    }
	}); /*
	     * File Name : TaskGroupTotalView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = TaskGroupTotalView;

/***/ }),
/* 146 */
/*!***************************************!*\
  !*** ./src/widgets/LabelRowWidget.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : LabelRowWidget.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var LabelRowWidget = _backbone2.default.View.extend({
	    tagName: 'div',
	    template: __webpack_require__(/*! ./templates/LabelRowWidget.mustache */ 147),
	    templateContext: function templateContext() {
	        var values = this.getOption('values');
	        var label = (0, _tools.getOpt)(this, 'label', '');
	
	        if (!Array.isArray(values)) {
	            values = [{ 'label': label, 'value': values }];
	        }
	        return {
	            values: values
	        };
	    }
	});
	exports.default = LabelRowWidget;

/***/ }),
/* 147 */
/*!*******************************************************!*\
  !*** ./src/widgets/templates/LabelRowWidget.mustache ***!
  \*******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class='row'>\n<div class='col-md-10 col-xs-8 text-right'>\n    <b>";
	  stack1 = ((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</b>\n</div>\n<div class='col-md-2 col-xs-4 text-right'>\n    ";
	  stack1 = ((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\n</div>\n</div>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.values : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 148 */
/*!*************************************************************!*\
  !*** ./src/task/views/templates/LineContainerView.mustache ***!
  \*************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div class='line'></div>\n";
	  },"useData":true});

/***/ }),
/* 149 */
/*!*********************************************************!*\
  !*** ./src/task/views/templates/TaskGroupView.mustache ***!
  \*********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "                <button type='button' class='btn btn-default btn-small up' tabindex='-1'>\n                    <i class='glyphicon glyphicon-arrow-up'></i>\n                </button>\n                <br />\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "                <button type='button' class='btn btn-default btn-small down' tabindex='-1'>\n                    <i class='glyphicon glyphicon-arrow-down'></i>\n                </button>\n";
	  },"5":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "            "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n";
	},"7":function(depth0,helpers,partials,data) {
	  return "            <small>Aucun titre n'a été saisi pour cet ouvrage</small>\n";
	  },"9":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "            ";
	  stack1 = ((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\n";
	},"11":function(depth0,helpers,partials,data) {
	  return "            <i>Aucune description n'a été saisie</i>\n";
	  },"13":function(depth0,helpers,partials,data) {
	  return "    <div class='row lines-header hidden-xs'>\n        <div class='col-md-3 col-sm-4 '>Intitulé des postes</div>\n        <div class='col-md-1 hidden-sm hidden-xs text-center'>Prix unit. HT</div>\n        <div class='col-md-1 hidden-sm hidden-xs text-center'>Qté</div>\n        <div class='col-lg-1 hidden-sm hidden-xs hidden-md text-center'>Unité</div>\n        <div class='col-md-1 hidden-sm hidden-xs text-center'>Tva</div>\n        <div class='col-md-1 col-sm-1 text-center'>HT</div>\n        <div class='col-lg-1 hidden-sm hidden-xs hidden-md text-center'>Produit</div>\n        <div class='col-md-5 col-lg-3 col-sm-7 text-center'>Actions</div>\n    </div>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<div class='col-xs-12'>\n    <div class='row'>\n        <div class='col-xs-12'>\n        <div class='errors'></div>\n            <div class='btn-group pull-right'>\n                <button\n                    type='button'\n                    class='btn btn-danger delete btn-small'\n                    title='Supprimer cet ouvrage'\n                    tabindex='-1'\n                    >\n                    <i class='glyphicon glyphicon-trash'></i>\n                </button>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_not_first : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_not_last : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "            </div>\n        </div>\n        </div>\n        <div class='row'>\n        <div class='col-xs-12'>\n            <h4>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.program(7, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "            <button\n                type='button'\n                class='btn-nostyle edit btn-small'\n                title=\"Modifier cet ouvrage\"\n                tabindex='-1'\n                >\n                <i class='glyphicon glyphicon-pencil'></i>\n            </button>\n            </h4>\n            <p>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.description : depth0), {"name":"if","hash":{},"fn":this.program(9, data),"inverse":this.program(11, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "            </p>\n        </div>\n    </div>\n\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.not_is_empty : depth0), {"name":"if","hash":{},"fn":this.program(13, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "    <div class='row lines'>\n    </div>\n    <div class='row actions'>\n        <div class='col-xs-11 text-right'>\n            <button type='button' class='btn btn-info btn-add'>\n                <i class='glyphicon glyphicon-plus-sign'></i> Ajouter une prestation\n            </button>\n        </div>\n    </div>\n    <div class='subtotal'>\n    </div>\n    <div class='modalregion'></div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 150 */
/*!*********************************************!*\
  !*** ./src/task/views/TaskGroupFormView.js ***!
  \*********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 77);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _ModalFormBehavior = __webpack_require__(/*! ../../base/behaviors/ModalFormBehavior.js */ 86);
	
	var _ModalFormBehavior2 = _interopRequireDefault(_ModalFormBehavior);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _CatalogTreeView = __webpack_require__(/*! ./CatalogTreeView.js */ 140);
	
	var _CatalogTreeView2 = _interopRequireDefault(_CatalogTreeView);
	
	var _LoadingWidget = __webpack_require__(/*! ../../widgets/LoadingWidget.js */ 142);
	
	var _LoadingWidget2 = _interopRequireDefault(_LoadingWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/TaskGroupFormView.mustache */ 151); /*
	                                                                   * File Name : TaskGroupFormView.js
	                                                                   *
	                                                                   * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                                   * Company : Majerti ( http://www.majerti.fr )
	                                                                   *
	                                                                   * This software is distributed under GPLV3
	                                                                   * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                   *
	                                                                   */
	
	
	var TaskGroupFormView = _backbone2.default.View.extend({
	    template: template,
	    regions: {
	        'order': '.order',
	        'title': '.title',
	        'description': '.description',
	        'catalog_container': '#catalog-container'
	    },
	    ui: {
	        main_tab: 'ul.nav-tabs li:first a'
	    },
	    behaviors: [_ModalFormBehavior2.default],
	    childViewEvents: {
	        'catalog:edit': 'onCatalogEdit'
	    },
	    childViewTriggers: {
	        'catalog:insert': 'catalog:insert',
	        'change': 'data:modified'
	    },
	    modelEvents: {
	        'set:product_group': 'refreshForm'
	    },
	    onCatalogEdit: function onCatalogEdit(productgroup_datas) {
	        this.model.loadProductGroup(productgroup_datas);
	    },
	    isAddView: function isAddView() {
	        return !(0, _tools.getOpt)(this, 'edit', false);
	    },
	    templateContext: function templateContext() {
	        return {
	            title: this.getOption('title'),
	            add: this.isAddView()
	        };
	    },
	    refreshForm: function refreshForm() {
	        this.showChildView('order', new _InputWidget2.default({
	            value: this.model.get('order'),
	            field_name: 'order',
	            type: 'hidden'
	        }));
	        this.showChildView('title', new _InputWidget2.default({
	            value: this.model.get('title'),
	            title: "Titre (optionnel)",
	            description: "Titre de l'ouvrage tel qu'affiché dans la sortie pdf, laissez vide pour ne pas le faire apparaître",
	            field_name: "title"
	        }));
	        this.showChildView('description', new _TextAreaWidget2.default({
	            value: this.model.get('description'),
	            title: "Description (optionnel)",
	            field_name: "description",
	            tinymce: true,
	            cid: this.model.cid
	        }));
	        if (this.isAddView()) {
	            this.getUI('main_tab').tab('show');
	        }
	    },
	    onRender: function onRender() {
	        this.refreshForm();
	        if (this.isAddView()) {
	            this.showChildView('catalog_container', new _LoadingWidget2.default());
	            var req = (0, _tools.ajax_call)(AppOption['load_catalog_url'], { type: 'sale_product_group' });
	            req.done(this.onCatalogLoaded.bind(this));
	        }
	    },
	    onCatalogLoaded: function onCatalogLoaded(result) {
	        this.showChildView('catalog_container', new _CatalogTreeView2.default({
	            catalog: result,
	            title: "Catalogue produit"
	        }));
	    }
	});
	exports.default = TaskGroupFormView;

/***/ }),
/* 151 */
/*!*************************************************************!*\
  !*** ./src/task/views/templates/TaskGroupFormView.mustache ***!
  \*************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "            <ul class=\"nav nav-tabs\" role=\"tablist\">\n                <li role=\"presentation\" class=\"active\">\n                    <a href=\"#form-container\"\n                        aria-controls=\"form-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\">\n                        Saisie libre\n                    </a>\n                </li>\n                <li role=\"presentation\">\n                    <a href=\"#catalog-container\"\n                        aria-controls=\"catalog-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\">\n                        Depuis le catalogue\n                    </a>\n                </li>\n            </ul>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane\"\n                    id=\"catalog-container\">\n                </div>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\" role=\"document\">\n	<div class=\"modal-content\">\n          <div class=\"modal-header\">\n            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n            <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n          </div>\n          <div class=\"modal-body\">\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "            <div class='tab-content'>\n                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane fade in active\"\n                    id=\"form-container\">\n                    <form class='form taskgroup-form'>\n                        <div class='order'></div>\n                        <div class='title'></div>\n                        <div class='description'></div>\n                        <button class='btn btn-success primary-action' type='submit' value='submit'>\n                            "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n                        </button>\n                        <button class='btn btn-default secondary-action' type='reset' value='submit'>\n                            Annuler\n                        </button>\n                    </form>\n                </div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "            </div>\n          </div>\n          <div class=\"modal-footer\">\n          </div>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n\n";
	},"useData":true});

/***/ }),
/* 152 */
/*!*************************************!*\
  !*** ./src/task/views/ErrorView.js ***!
  \*************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ErrorView = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'alert alert-danger',
	    template: __webpack_require__(/*! ./templates/ErrorView.mustache */ 153),
	    initialize: function initialize() {
	        this.errors = this.getOption('errors');
	    },
	    templateContext: function templateContext() {
	        return { "errors": this.errors };
	    }
	}); /*
	     * File Name : ErrorView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ErrorView;

/***/ }),
/* 153 */
/*!*****************************************************!*\
  !*** ./src/task/views/templates/ErrorView.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "<li>"
	    + escapeExpression(lambda(depth0, depth0))
	    + "</li>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<ul>\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.errors : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</ul>\n";
	},"useData":true});

/***/ }),
/* 154 */
/*!********************************************!*\
  !*** ./src/task/views/DisplayUnitsView.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _FormBehavior = __webpack_require__(/*! ../../base/behaviors/FormBehavior.js */ 73);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _CheckboxWidget = __webpack_require__(/*! ../../widgets/CheckboxWidget.js */ 112);
	
	var _CheckboxWidget2 = _interopRequireDefault(_CheckboxWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var DisplayUnitsView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/DisplayUnitsView.mustache */ 155),
	    fields: ['display_units'],
	    behaviors: [_FormBehavior2.default],
	    regions: {
	        "content": "div"
	    },
	    childViewTriggers: {
	        'change': 'data:modified',
	        'finish': 'data:persist'
	    },
	    onRender: function onRender() {
	        var value = this.model.get('display_units');
	        var checked = false;
	        if (value == 1 || value == '1') {
	            checked = true;
	        }
	        console.log(this.model);
	
	        this.showChildView("content", new _CheckboxWidget2.default({
	            title: "",
	            label: "Afficher le détail des prestations dans le PDF",
	            description: "Le prix unitaire et la quantité seront affichés dans le PDF",
	            field_name: "display_units",
	            checked: checked,
	            value: this.model.get('display_units')
	        }));
	    }
	}); /*
	     * File Name : DisplayUnitsView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = DisplayUnitsView;

/***/ }),
/* 155 */
/*!************************************************************!*\
  !*** ./src/task/views/templates/DisplayUnitsView.mustache ***!
  \************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div></div>\n";
	  },"useData":true});

/***/ }),
/* 156 */
/*!*********************************************************!*\
  !*** ./src/task/views/templates/TaskBlockView.mustache ***!
  \*********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<h2>Description des prestations</h2>\n<div class='content'>\n    <div class='display-units-container'></div>\n    <div class='group-errors'></div>\n    <div class='group-container'></div>\n    <div class='group-modalregion'></div>\n    <div class='actions text-right'>\n        <button class='btn btn-default add' type='button'>\n            <i class='glyphicon glyphicon-plus-sign'></i> Ajouter un ouvrage\n        </button>\n    </div>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 157 */
/*!*************************************************!*\
  !*** ./src/task/views/HtBeforeDiscountsView.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _LabelRowWidget = __webpack_require__(/*! ../../widgets/LabelRowWidget.js */ 146);
	
	var _LabelRowWidget2 = _interopRequireDefault(_LabelRowWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var HtBeforeDiscountsView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/LineContainerView.mustache */ 148),
	    regions: {
	        line: {
	            el: '.line',
	            replaceElement: true
	        }
	    },
	    modelEvents: {
	        'change': 'render'
	    },
	    onRender: function onRender() {
	        var values = (0, _math.formatAmount)(this.model.get('ht_before_discounts'), false);
	        var view = new _LabelRowWidget2.default({
	            label: 'Total HT avant remise',
	            values: values
	        });
	        this.showChildView('line', view);
	    }
	}); /*
	     * File Name : HtBeforeDiscountsView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = HtBeforeDiscountsView;

/***/ }),
/* 158 */
/*!*********************************************!*\
  !*** ./src/task/views/DiscountBlockView.js ***!
  \*********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _DiscountModel = __webpack_require__(/*! ../models/DiscountModel.js */ 159);
	
	var _DiscountModel2 = _interopRequireDefault(_DiscountModel);
	
	var _DiscountCollectionView = __webpack_require__(/*! ./DiscountCollectionView.js */ 160);
	
	var _DiscountCollectionView2 = _interopRequireDefault(_DiscountCollectionView);
	
	var _DiscountFormPopupView = __webpack_require__(/*! ./DiscountFormPopupView.js */ 163);
	
	var _DiscountFormPopupView2 = _interopRequireDefault(_DiscountFormPopupView);
	
	var _ErrorView = __webpack_require__(/*! ./ErrorView.js */ 152);
	
	var _ErrorView2 = _interopRequireDefault(_ErrorView);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 22);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : DiscountBlockView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var DiscountBlockView = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'form-section discount-group',
	    template: __webpack_require__(/*! ./templates/DiscountBlockView.mustache */ 170),
	    regions: {
	        'lines': '.lines',
	        'modalRegion': '.modalregion',
	        'errors': ".block-errors"
	    },
	    ui: {
	        add_button: 'button.btn-add'
	    },
	    triggers: {
	        "click @ui.add_button": "line:add"
	    },
	    childViewEvents: {
	        'line:edit': 'onLineEdit',
	        'line:delete': 'onLineDelete',
	        'destroy:modal': 'render',
	        'insert:percent': 'onInsertPercent'
	    },
	    collectionEvents: {
	        'change': 'hideErrors'
	    },
	    initialize: function initialize(options) {
	        this.collection = options['collection'];
	        this.model = options['model'];
	        this.listenTo(this.collection, 'validated:invalid', this.showErrors);
	        this.listenTo(this.collection, 'validated:valid', this.hideErrors.bind(this));
	    },
	    showErrors: function showErrors(model, errors) {
	        this.detachChildView('errors');
	        this.showChildView('errors', new _ErrorView2.default({ errors: errors }));
	        this.$el.addClass('error');
	    },
	    hideErrors: function hideErrors(model) {
	        this.detachChildView('errors');
	        this.$el.removeClass('error');
	    },
	
	    isEmpty: function isEmpty() {
	        return this.collection.length === 0;
	    },
	    onLineAdd: function onLineAdd() {
	        var model = new _DiscountModel2.default();
	        this.showDiscountLineForm(model, "Ajouter la remise", false);
	    },
	    onLineEdit: function onLineEdit(childView) {
	        this.showDiscountLineForm(childView.model, "Modifier la remise", true);
	    },
	    showDiscountLineForm: function showDiscountLineForm(model, title, edit) {
	        var form = new _DiscountFormPopupView2.default({
	            model: model,
	            title: title,
	            destCollection: this.collection,
	            edit: edit
	        });
	        this.showChildView('modalRegion', form);
	    },
	    onDeleteSuccess: function onDeleteSuccess() {
	        (0, _backboneTools.displayServerSuccess)("Vos données ont bien été supprimées");
	    },
	    onDeleteError: function onDeleteError() {
	        (0, _backboneTools.displayServerError)("Une erreur a été rencontrée lors de la " + "suppression de cet élément");
	    },
	    onLineDelete: function onLineDelete(childView) {
	        var result = window.confirm("Êtes-vous sûr de vouloir supprimer cette remise ?");
	        if (result) {
	            childView.model.destroy({
	                success: this.onDeleteSuccess,
	                error: this.onDeleteError
	            });
	        }
	    },
	    onInsertPercent: function onInsertPercent(model) {
	        this.collection.insert_percent(model);
	        this.getChildView('modalRegion').triggerMethod('modal:close');
	    },
	    templateContext: function templateContext() {
	        return {
	            not_empty: !this.isEmpty()
	        };
	    },
	    onRender: function onRender() {
	        if (!this.isEmpty()) {
	            this.showChildView('lines', new _DiscountCollectionView2.default({ collection: this.collection }));
	        }
	    }
	});
	exports.default = DiscountBlockView;

/***/ }),
/* 159 */
/*!******************************************!*\
  !*** ./src/task/models/DiscountModel.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _BaseModel = __webpack_require__(/*! ./BaseModel.js */ 132);
	
	var _BaseModel2 = _interopRequireDefault(_BaseModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var DiscountModel = _BaseModel2.default.extend({
	    props: ['id', 'amount', 'tva', 'ht', 'description'],
	    validation: {
	        description: {
	            required: true,
	            msg: "Remise : Veuillez saisir un objet"
	        },
	        amount: {
	            required: true,
	            pattern: "amount",
	            msg: "Remise : Veuillez saisir un coup unitaire, dans la limite de 5 chiffres après la virgule"
	        },
	        tva: {
	            required: true,
	            pattern: "number",
	            msg: "Remise : Veuillez sélectionner une TVA"
	        }
	    },
	    ht: function ht() {
	        return -1 * (0, _math.strToFloat)(this.get('amount'));
	    },
	    tva_value: function tva_value() {
	        var tva = this.get('tva');
	        if (tva < 0) {
	            tva = 0;
	        }
	        return tva;
	    },
	    tva: function tva() {
	        return (0, _math.getTvaPart)(this.ht(), this.tva_value());
	    },
	    ttc: function ttc() {
	        return this.ht() + this.tva();
	    }
	}); /*
	     * File Name : DiscountModel.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = DiscountModel;

/***/ }),
/* 160 */
/*!**************************************************!*\
  !*** ./src/task/views/DiscountCollectionView.js ***!
  \**************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _DiscountView = __webpack_require__(/*! ./DiscountView.js */ 161);
	
	var _DiscountView2 = _interopRequireDefault(_DiscountView);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : DiscountCollectionView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var DiscountCollectionView = _backbone2.default.CollectionView.extend({
	    tagName: 'div',
	    className: 'col-xs-12',
	    childView: _DiscountView2.default,
	    // Bubble up child view events
	    childViewTriggers: {
	        'edit': 'line:edit',
	        'delete': 'line:delete'
	    },
	    initialize: function initialize(options) {
	        var channel = _backbone4.default.channel('facade');
	        this.listenTo(channel, 'bind:validation', this.bindValidation);
	        this.listenTo(channel, 'unbind:validation', this.unbindValidation);
	        this.listenTo(this.collection, 'validated:invalid', this.showErrors);
	        this.listenTo(this.collection, 'validated:valid', this.hideErrors.bind(this));
	    },
	    showErrors: function showErrors(model, errors) {
	        this.$el.addClass('error');
	    },
	    hideErrors: function hideErrors(model) {
	        this.$el.removeClass('error');
	    },
	    bindValidation: function bindValidation() {
	        _backboneValidation2.default.bind(this);
	    },
	    unbindValidation: function unbindValidation() {
	        _backboneValidation2.default.unbind(this);
	    }
	});
	exports.default = DiscountCollectionView;

/***/ }),
/* 161 */
/*!****************************************!*\
  !*** ./src/task/views/DiscountView.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : DiscountView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/DiscountView.mustache */ 162);
	
	var DiscountView = _backbone2.default.View.extend({
	    template: template,
	    ui: {
	        edit_button: 'button.edit',
	        delete_button: 'button.delete'
	    },
	    // Trigger to the parent
	    triggers: {
	        'click @ui.edit_button': 'edit',
	        'click @ui.delete_button': 'delete'
	    },
	    modelEvents: {
	        'change': 'render'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('config');
	        this.tva_options = channel.request('get:options', 'tvas');
	    },
	    getTvaLabel: function getTvaLabel() {
	        var res = "";
	        var current_value = this.model.get('tva');
	        _underscore2.default.each(this.tva_options, function (tva) {
	            if (tva.value == current_value) {
	                res = tva.name;
	            }
	        });
	        return res;
	    },
	    templateContext: function templateContext() {
	        return {
	            ht: (0, _math.formatAmount)(this.model.ht()),
	            tva_label: this.getTvaLabel()
	        };
	    }
	});
	exports.default = DiscountView;

/***/ }),
/* 162 */
/*!********************************************************!*\
  !*** ./src/task/views/templates/DiscountView.mustache ***!
  \********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class='col-md-3 col-sm-4 col-xs-12 description'>";
	  stack1 = ((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n<div class='col-md-3 col-sm-2 col-xs-12 amount'><b class='visible-xs text-left'>HT : ";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</b><span class='hidden-xs'>";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</span></div>\n<div class='col-md-1 hidden-sm hidden-xs text-center'>"
	    + escapeExpression(((helper = (helper = helpers.tva_label || (depth0 != null ? depth0.tva_label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva_label","hash":{},"data":data}) : helper)))
	    + "</div>\n<div class='col-md-5 col-sm-6 col-xs-12 text-right actions'>\n    <button type='button' class='btn btn-default edit'>\n        <i class='glyphicon glyphicon-pencil'></i> <span class='hidden-xs'>Modifier</span>\n    </button>\n    <button type='button' class='btn btn-default delete'>\n        <i class='glyphicon glyphicon-trash'></i> <span class='hidden-xs'>Supprimer</span>\n    </button>\n</div>\n";
	},"useData":true});

/***/ }),
/* 163 */
/*!*************************************************!*\
  !*** ./src/task/views/DiscountFormPopupView.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ModalBehavior = __webpack_require__(/*! ../../base/behaviors/ModalBehavior.js */ 49);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	var _DiscountFormView = __webpack_require__(/*! ./DiscountFormView.js */ 164);
	
	var _DiscountFormView2 = _interopRequireDefault(_DiscountFormView);
	
	var _DiscountPercentModel = __webpack_require__(/*! ../models/DiscountPercentModel.js */ 166);
	
	var _DiscountPercentModel2 = _interopRequireDefault(_DiscountPercentModel);
	
	var _DiscountPercentView = __webpack_require__(/*! ./DiscountPercentView.js */ 167);
	
	var _DiscountPercentView2 = _interopRequireDefault(_DiscountPercentView);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : DiscountFormPopupView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/DiscountFormPopupView.mustache */ 169);
	
	var DiscountFormPopupView = _backbone2.default.View.extend({
	    behaviors: [_ModalBehavior2.default],
	    template: template,
	    regions: {
	        'simple-form': '.simple-form',
	        'percent-form': '.percent-form'
	    },
	    // Here we bind the child FormBehavior with our ModalBehavior
	    // Like it's done in the ModalFormBehavior
	    childViewTriggers: {
	        'cancel:form': 'modal:close',
	        'success:sync': 'modal:close',
	        'insert:percent': 'insert:percent'
	    },
	    onModalBeforeClose: function onModalBeforeClose() {
	        this.model.rollback();
	    },
	
	    isAddView: function isAddView() {
	        return !(0, _tools.getOpt)(this, 'edit', false);
	    },
	    onRender: function onRender() {
	        this.showChildView('simple-form', new _DiscountFormView2.default({
	            model: this.model,
	            title: this.getOption('title'),
	            destCollection: this.getOption('destCollection')
	        }));
	
	        if (this.isAddView()) {
	            this.showChildView('percent-form', new _DiscountPercentView2.default({
	                title: this.getOption('title'),
	                model: new _DiscountPercentModel2.default(),
	                destCollection: this.getOption('destCollection')
	            }));
	        }
	    },
	    templateContext: function templateContext() {
	        return {
	            title: this.getOption('title'),
	            add: this.isAddView()
	        };
	    }
	});
	exports.default = DiscountFormPopupView;

/***/ }),
/* 164 */
/*!********************************************!*\
  !*** ./src/task/views/DiscountFormView.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 77);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _SelectWidget = __webpack_require__(/*! ../../widgets/SelectWidget.js */ 79);
	
	var _SelectWidget2 = _interopRequireDefault(_SelectWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _FormBehavior = __webpack_require__(/*! ../../base/behaviors/FormBehavior.js */ 73);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/DiscountFormView.mustache */ 165); /*
	                                                                  * File Name : DiscountFormView.js
	                                                                  *
	                                                                  * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                                  * Company : Majerti ( http://www.majerti.fr )
	                                                                  *
	                                                                  * This software is distributed under GPLV3
	                                                                  * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                  *
	                                                                  */
	
	
	var DiscountFormView = _backbone2.default.View.extend({
	    behaviors: [_FormBehavior2.default],
	    template: template,
	    regions: {
	        'order': '.order',
	        'description': '.description',
	        'amount': '.amount',
	        'tva': '.tva'
	    },
	    childViewTriggers: {
	        'change': 'data:modified'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('config');
	        this.tva_options = channel.request('get:options', 'tvas');
	    },
	
	    onRender: function onRender() {
	        this.showChildView('order', new _InputWidget2.default({
	            value: this.model.get('order'),
	            field_name: 'order',
	            type: 'hidden'
	        }));
	        this.showChildView('description', new _TextAreaWidget2.default({
	            value: this.model.get('description'),
	            title: "Description",
	            field_name: "description",
	            tinymce: true,
	            cid: this.model.cid
	        }));
	        this.showChildView('amount', new _InputWidget2.default({
	            value: this.model.get('amount'),
	            title: "Montant",
	            field_name: "amount",
	            addon: '€'
	        }));
	        this.showChildView('tva', new _SelectWidget2.default({
	            options: this.tva_options,
	            title: "TVA",
	            value: this.model.get('tva'),
	            id_key: 'value',
	            field_name: 'tva'
	        }));
	    },
	    templateContext: function templateContext() {
	        return {
	            title: this.getOption('title')
	        };
	    }
	});
	exports.default = DiscountFormView;

/***/ }),
/* 165 */
/*!************************************************************!*\
  !*** ./src/task/views/templates/DiscountFormView.mustache ***!
  \************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<form class='form'>\n    <div class='order'></div>\n    <div class='description'></div>\n    <div class='amount'></div>\n    <div class='tva'></div>\n    <button class='btn btn-success primary-action' type='submit' value='submit'>\n        "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n    </button>\n    <button class='btn btn-default secondary-action' type='reset' value='submit'>\n        Annuler\n    </button>\n</form>\n";
	},"useData":true});

/***/ }),
/* 166 */
/*!*************************************************!*\
  !*** ./src/task/models/DiscountPercentModel.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var DiscountPercentModel = _backbone2.default.Model.extend({
	    validation: {
	        description: {
	            required: true,
	            msg: "Veuillez saisir un objet"
	        },
	        percentage: {
	            required: true,
	            range: [1, 99],
	            msg: "Veuillez saisir un pourcentage"
	        },
	        tva: {
	            required: true,
	            pattern: "number",
	            msg: "Veuillez sélectionner une TVA"
	        }
	    }
	
	}); /*
	     * File Name : DiscountPercentModel.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = DiscountPercentModel;

/***/ }),
/* 167 */
/*!***********************************************!*\
  !*** ./src/task/views/DiscountPercentView.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 77);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _DiscountModel = __webpack_require__(/*! ../models/DiscountModel.js */ 159);
	
	var _DiscountModel2 = _interopRequireDefault(_DiscountModel);
	
	var _BaseFormBehavior = __webpack_require__(/*! ../../base/behaviors/BaseFormBehavior.js */ 74);
	
	var _BaseFormBehavior2 = _interopRequireDefault(_BaseFormBehavior);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var DiscountPercentView = _backbone2.default.View.extend({
	    behaviors: [_BaseFormBehavior2.default],
	    template: __webpack_require__(/*! ./templates/DiscountPercentView.mustache */ 168),
	    regions: {
	        'description': '.description',
	        'percentage': '.percentage'
	    },
	    ui: {
	        form: 'form',
	        submit: "button[type=submit]",
	        btn_cancel: "button[type=reset]"
	    },
	    triggers: {
	        'click @ui.btn_cancel': 'cancel:form'
	    },
	    childViewTriggers: {
	        'change': 'data:modified'
	    },
	    events: {
	        'submit @ui.form': "onSubmit"
	    },
	    onSubmit: function onSubmit(event) {
	        event.preventDefault();
	        this.triggerMethod('insert:percent', this.model);
	    },
	    onRender: function onRender() {
	        this.showChildView('description', new _TextAreaWidget2.default({
	            title: "Description",
	            field_name: "description",
	            tinymce: true,
	            cid: '11111'
	        }));
	        this.showChildView('percentage', new _InputWidget2.default({
	            title: "Pourcentage",
	            field_name: 'percentage',
	            addon: "%"
	        }));
	    },
	    templateContext: function templateContext() {
	        return {
	            title: this.getOption('title')
	        };
	    }
	
	}); /*
	     * File Name : DiscountPercentView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = DiscountPercentView;

/***/ }),
/* 168 */
/*!***************************************************************!*\
  !*** ./src/task/views/templates/DiscountPercentView.mustache ***!
  \***************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<form>\n    <div class='description'></div>\n    <div class='percentage'></div>\n    <button class='btn btn-success primary-action' type='submit' value='submit'>\n    "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n    </button>\n    <button class='btn btn-default secondary-action' type='reset' value='submit'>\n    Annuler\n    </button>\n</form>\n";
	},"useData":true});

/***/ }),
/* 169 */
/*!*****************************************************************!*\
  !*** ./src/task/views/templates/DiscountFormPopupView.mustache ***!
  \*****************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "            <ul class=\"nav nav-tabs\" role=\"tablist\">\n                <li role=\"presentation\" class=\"active\">\n                    <a href=\"#main-discount-container\"\n                        aria-controls=\"main-discount-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\">\n                        Saisie d'un montant\n                    </a>\n                </li>\n                <li role=\"presentation\">\n                    <a href=\"#percentage-container\"\n                        aria-controls=\"percentage-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\">\n                        Remise en pourcentage\n                    </a>\n                </li>\n            </ul>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\" role=\"document\">\n	<div class=\"modal-content\">\n          <div class=\"modal-header\">\n            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n            <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n          </div>\n          <div class=\"modal-body\">\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "            <div class='tab-content'>\n                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane fade in active simple-form\"\n                    id=\"main-discount-container\">\n                </div>\n                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane percent-form\"\n                    id=\"percentage-container\">\n                </div>\n            </div>\n          </div>\n          <div class=\"modal-footer\">\n          </div>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n";
	},"useData":true});

/***/ }),
/* 170 */
/*!*************************************************************!*\
  !*** ./src/task/views/templates/DiscountBlockView.mustache ***!
  \*************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "    <div class='row lines-header hidden-xs'>\n        <div class='col-md-3 col-sm-4'>Description</div>\n        <div class='col-md-3 ol-sm-2 col-xs-12'>Montant HT</div>\n        <div class='col-md-1 hidden-sm hidden-xs text-center'>TVA</div>\n        <div class='col-md-5 col-sm-6 col-xs-12 text-right'>Actions</div>\n    </div>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<h2>Remises</h2>\n<div class='modalregion'></div>\n<div class='content'>\n    <div class='block-errors'></div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.not_empty : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "    <div class='row lines'>\n    </div>\n    <div class='row'>\n        <div class='col-xs-11 text-right'>\n            <button type='button' class='btn btn-default btn-add'>\n                <i class='glyphicon glyphicon-plus-sign'></i> Ajouter une remise\n            </button>\n        </div>\n    </div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 171 */
/*!**********************************************!*\
  !*** ./src/task/views/ExpenseHtBlockView.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _Mn$View$extend;
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _FormBehavior = __webpack_require__(/*! ../../base/behaviors/FormBehavior.js */ 73);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 77);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; } /*
	                                                                                                                                                                                                                   * File Name : ExpenseHtBlockView.js
	                                                                                                                                                                                                                   *
	                                                                                                                                                                                                                   * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                                                                                                                                                                                   * Company : Majerti ( http://www.majerti.fr )
	                                                                                                                                                                                                                   *
	                                                                                                                                                                                                                   * This software is distributed under GPLV3
	                                                                                                                                                                                                                   * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                                                                                                                                                                   *
	                                                                                                                                                                                                                   */
	
	
	var template = __webpack_require__(/*! ./templates/ExpenseHtBlockView.mustache */ 172);
	
	var ExpenseHtBlockView = _backbone2.default.View.extend((_Mn$View$extend = {
	    template: template,
	    behaviors: [{
	        behaviorClass: _FormBehavior2.default,
	        errorMessage: "Vérifiez votre saisie"
	    }],
	    tagName: 'div',
	    className: 'form-section'
	}, _defineProperty(_Mn$View$extend, 'template', template), _defineProperty(_Mn$View$extend, 'regions', {
	    expenses_ht: ".expenses_ht"
	}), _defineProperty(_Mn$View$extend, 'childViewTriggers', {
	    'change': 'data:modified',
	    'finish': 'data:persist'
	}), _defineProperty(_Mn$View$extend, 'initialize', function initialize(options) {
	    this.section = options['section'];
	}), _defineProperty(_Mn$View$extend, 'onRender', function onRender() {
	    this.showChildView('expenses_ht', new _InputWidget2.default({
	        title: "Frais forfaitaires (HT)",
	        value: this.model.get('expenses_ht'),
	        field_name: 'expenses_ht'
	    }));
	}), _Mn$View$extend));
	exports.default = ExpenseHtBlockView;

/***/ }),
/* 172 */
/*!**************************************************************!*\
  !*** ./src/task/views/templates/ExpenseHtBlockView.mustache ***!
  \**************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<h2>Frais forfaitaires</h2>\n<div class='content'>\n    <div class='row'>\n        <form class='form-inline'>\n            <div class='col-xs-11 expenses_ht text-right'></div>\n        </form>\n    </div>\n</div>\n\n";
	  },"useData":true});

/***/ }),
/* 173 */
/*!*************************************!*\
  !*** ./src/task/views/TotalView.js ***!
  \*************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _LabelRowWidget = __webpack_require__(/*! ../../widgets/LabelRowWidget.js */ 146);
	
	var _LabelRowWidget2 = _interopRequireDefault(_LabelRowWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TotalView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/TotalView.mustache */ 174),
	    regions: {
	        ht: {
	            el: '.ht',
	            replaceElement: true
	        },
	        tvas: {
	            el: '.tvas',
	            replaceElement: true
	        },
	        ttc: {
	            el: '.ttc',
	            replaceElement: true
	        }
	    },
	    modelEvents: {
	        'change': 'render'
	    },
	    showHt: function showHt() {
	        var values = (0, _math.formatAmount)(this.model.get('ht'), true);
	        var view = new _LabelRowWidget2.default({
	            label: 'Total HT',
	            values: values
	        });
	        this.showChildView('ht', view);
	    },
	    showTvas: function showTvas() {
	        var view = new _LabelRowWidget2.default({ values: this.model.tva_labels() });
	        this.showChildView('tvas', view);
	    },
	    showTtc: function showTtc() {
	        var values = (0, _math.formatAmount)(this.model.get('ttc'), true);
	        var view = new _LabelRowWidget2.default({
	            label: 'Total TTC',
	            values: values
	        });
	        this.showChildView('ttc', view);
	    },
	    onRender: function onRender() {
	        this.showHt();
	        this.showTvas();
	        this.showTtc();
	    }
	}); /*
	     * File Name : TotalView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = TotalView;

/***/ }),
/* 174 */
/*!*****************************************************!*\
  !*** ./src/task/views/templates/TotalView.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div class='ht'></div>\n<div class='tvas'></div>\n<div class='ttc'></div>\n";
	  },"useData":true});

/***/ }),
/* 175 */
/*!******************************************!*\
  !*** ./src/task/views/NotesBlockView.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _FormBehavior = __webpack_require__(/*! ../../base/behaviors/FormBehavior.js */ 73);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/NotesBlockView.mustache */ 176); /*
	                                                                * File Name : NotesBlockView.js
	                                                                *
	                                                                * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                                * Company : Majerti ( http://www.majerti.fr )
	                                                                *
	                                                                * This software is distributed under GPLV3
	                                                                * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                *
	                                                                */
	
	
	var NotesBlockView = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'form-section',
	    template: template,
	    regions: {
	        exclusions: '.exclusions'
	    },
	    behaviors: [{
	        behaviorClass: _FormBehavior2.default,
	        errorMessage: "Vérifiez votre saisie"
	    }],
	    childViewTriggers: {
	        'change': 'data:modified',
	        'finish': 'data:persist'
	    },
	    isMoreSet: function isMoreSet() {
	        if (this.model.get('exclusions')) {
	            return true;
	        }
	        return false;
	    },
	    templateContext: function templateContext() {
	        return {
	            is_more_set: this.isMoreSet()
	        };
	    },
	    onRender: function onRender() {
	        var view = new _TextAreaWidget2.default({
	            title: 'Notes',
	            description: 'Notes complémentaires concernant les prestations décrites',
	            field_name: 'exclusions',
	            value: this.model.get('exclusions')
	        });
	        this.showChildView('exclusions', view);
	    }
	});
	exports.default = NotesBlockView;

/***/ }),
/* 176 */
/*!**********************************************************!*\
  !*** ./src/task/views/templates/NotesBlockView.mustache ***!
  \**********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "<i>\n        Note complémentaire\n        </i>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "        Note complémentaire\n";
	  },"5":function(depth0,helpers,partials,data) {
	  return "in";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<h3>\n    <a\n        data-target='#exclusions-more'\n        data-toggle='collapse'\n        aria-expanded=\"false\"\n        aria-controls=\"exclusions-more\"\n        >\n        <i class='glyphicon glyphicon-plus-sign'></i>\n            ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_more_set : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </a>\n</h3>\n<div class='content'>\n    <div\n        class='collapse row ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_more_set : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "'\n        id=\"exclusions-more\">\n        <hr />\n        <div class='exclusions'></div>\n    </div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 177 */
/*!*****************************************************!*\
  !*** ./src/task/views/PaymentConditionBlockView.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _SelectWidget = __webpack_require__(/*! ../../widgets/SelectWidget.js */ 79);
	
	var _SelectWidget2 = _interopRequireDefault(_SelectWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _FormBehavior = __webpack_require__(/*! ../../base/behaviors/FormBehavior.js */ 73);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/PaymentConditionBlockView.mustache */ 178); /*
	                                                                           * File Name : PaymentConditionBlockView.js
	                                                                           *
	                                                                           * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                                           * Company : Majerti ( http://www.majerti.fr )
	                                                                           *
	                                                                           * This software is distributed under GPLV3
	                                                                           * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                           *
	                                                                           */
	
	
	var PaymentConditionBlockView = _backbone2.default.View.extend({
	    behaviors: [_FormBehavior2.default],
	    tagName: 'div',
	    className: 'form-section',
	    template: template,
	    regions: {
	        errors: ".errors",
	        predefined_conditions: '.predefined-conditions',
	        conditions: '.conditions'
	    },
	    modelEvents: {
	        'change:payment_conditions': 'render',
	        'validated:invalid': 'showErrors',
	        'validated:valid': 'hideErrors'
	    },
	    childViewEvents: {
	        'finish': 'onFinish'
	    },
	    initialize: function initialize() {
	        this.payment_conditions_options = _backbone4.default.channel('config').request('get:options', 'payment_conditions');
	        this.lookupDefault();
	
	        var channel = _backbone4.default.channel('facade');
	        this.listenTo(channel, 'bind:validation', this.bindValidation);
	        this.listenTo(channel, 'unbind:validation', this.unbindValidation);
	    },
	    bindValidation: function bindValidation() {
	        _backboneValidation2.default.bind(this);
	    },
	    unbindValidation: function unbindValidation() {
	        _backboneValidation2.default.unbind(this);
	    },
	    showErrors: function showErrors(model, errors) {
	        this.$el.addClass('error');
	    },
	    hideErrors: function hideErrors(model) {
	        this.$el.removeClass('error');
	    },
	    onFinish: function onFinish(field_name, value) {
	        if (field_name == 'predefined_conditions') {
	            var condition_object = this.getCondition(value);
	
	            this.model.set('predefined_conditions', value);
	            if (!_.isUndefined(condition_object)) {
	                this.triggerMethod('data:persist', 'payment_conditions', condition_object.label);
	            }
	        } else {
	            this.triggerMethod('data:persist', 'payment_conditions', value);
	        }
	    },
	    getCondition: function getCondition(id) {
	        return _.find(this.payment_conditions_options, function (item) {
	            return item.id == id;
	        });
	    },
	    lookupDefault: function lookupDefault() {
	        /*
	         * Setup the default payment condition if none is set
	         */
	        var option = (0, _tools.getDefaultItem)(this.payment_conditions_options);
	        if (!_.isUndefined(option)) {
	            var payment_conditions = this.model.get('payment_conditions');
	            if (_.isUndefined(payment_conditions) || payment_conditions.trim() == '') {
	                this.model.set('payment_conditions', option.label);
	                this.model.save({ 'payment_conditions': option.label }, { patch: true });
	            }
	        }
	    },
	
	    onRender: function onRender() {
	        var val = this.model.get('predefined_conditions');
	        val = parseInt(val, 10);
	        this.showChildView('predefined_conditions', new _SelectWidget2.default({
	            options: this.payment_conditions_options,
	            title: "",
	            field_name: 'predefined_conditions',
	            id_key: 'id',
	            value: val,
	            add_default: true
	        }));
	        this.showChildView('conditions', new _TextAreaWidget2.default({
	            value: this.model.get('payment_conditions'),
	            placeholder: "Conditions de paiement applicables à ce document",
	            field_name: 'payment_conditions'
	        }));
	    }
	});
	exports.default = PaymentConditionBlockView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 178 */
/*!*********************************************************************!*\
  !*** ./src/task/views/templates/PaymentConditionBlockView.mustache ***!
  \*********************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<h2>Conditions de paiements</h2>\n<div class='content'>\n<div class='errors'>\n</div>\n    <div class='predefined-conditions'></div>\n    <div class='conditions'></div>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 179 */
/*!********************************************!*\
  !*** ./src/task/views/PaymentBlockView.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _SelectWidget = __webpack_require__(/*! ../../widgets/SelectWidget.js */ 79);
	
	var _SelectWidget2 = _interopRequireDefault(_SelectWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _FormBehavior = __webpack_require__(/*! ../../base/behaviors/FormBehavior.js */ 73);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _PaymentLineTableView = __webpack_require__(/*! ./PaymentLineTableView.js */ 180);
	
	var _PaymentLineTableView2 = _interopRequireDefault(_PaymentLineTableView);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : PaymentBlockView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/PaymentBlockView.mustache */ 190);
	
	var PaymentBlockView = _backbone2.default.View.extend({
	    behaviors: [_FormBehavior2.default],
	    tagName: 'div',
	    className: 'form-section',
	    template: template,
	    regions: {
	        payment_display: '.payment_display-container',
	        payment_times: '.payment_times-container',
	        deposit: '.payment-deposit-container',
	        lines: '.payment-lines-container'
	    },
	    modelEvents: {
	        //        'change:payment_conditions': 'render'
	    },
	    childViewEvents: {
	        'finish': 'onFinish'
	    },
	    initialize: function initialize(options) {
	        this.collection = options['collection'];
	        var channel = _backbone4.default.channel('config');
	        this.payment_display_options = channel.request('get:options', 'payment_displays');
	        this.deposit_options = channel.request('get:options', 'deposits');
	        this.payment_times_options = channel.request('get:options', 'payment_times');
	        channel = _backbone4.default.channel('facade');
	        this.listenTo(channel, 'bind:validation', this.bindValidation);
	        this.listenTo(channel, 'unbind:validation', this.unbindValidation);
	    },
	    bindValidation: function bindValidation() {
	        _backboneValidation2.default.bind(this);
	    },
	    unbindValidation: function unbindValidation() {
	        _backboneValidation2.default.unbind(this);
	    },
	    onFinish: function onFinish(field_name, value) {
	        /*
	         * Launch when a field has been modified
	         *
	         * Handles fields that impact the payment lines
	         *
	         *      payment_times
	         *
	         *              we generate the payment lines
	         *
	         *      paymentDisplay
	         *
	         *              we hide/show the date field
	         *
	         */
	        if (field_name == 'paymentDisplay') {
	            var old_value = this.model.get('paymentDisplay');
	            this.triggerMethod('data:persist', 'paymentDisplay', value);
	            // If it changed and it is or was ALL_NO_DATE we render the lines again
	            if (old_value != value && _.indexOf([value, old_value], 'ALL_NO_DATE') != -1) {
	                this.renderTable();
	            }
	        } else if (field_name == 'payment_times') {
	            var old_value = this.model.get('payment_times');
	            if (old_value != value) {
	                if (value != -1) {
	                    // We generate the payment lines (and delete old ones)
	                    var this_ = this;
	                    var deferred = this.collection.genPaymentLines(value, this.model.get('deposit'));
	
	                    // We set the datas after because setting it, we also sync
	                    // the model and payment_times attribute is compuated based
	                    // on the lines that are added/deleted in the given
	                    // deferred
	                    deferred.then(function () {
	                        this_.triggerMethod('data:persist', field_name, value);
	                    });
	                } else {
	                    this.triggerMethod('data:persist', field_name, value);
	                }
	                if (value == -1 || old_value == -1) {
	                    // If we set it on manual configuration we re-render the
	                    // table
	                    this.tableview.showLines();
	                }
	            }
	        } else if (field_name == 'deposit') {
	            var old_value = this.model.get('deposit');
	
	            if (old_value != value) {
	                this.triggerMethod('data:persist', field_name, value);
	            }
	        }
	    },
	
	    renderTable: function renderTable() {
	        var edit = false;
	        if (this.model.get('payment_times') == -1) {
	            edit = true;
	        }
	        var show_date = true;
	        if (this.model.get('paymentDisplay') == 'ALL_NO_DATE') {
	            show_date = false;
	        }
	        this.tableview = new _PaymentLineTableView2.default({
	            collection: this.collection,
	            model: this.model,
	            edit: edit,
	            show_date: show_date
	        });
	        this.showChildView('lines', this.tableview);
	    },
	    onRender: function onRender() {
	        this.showChildView('payment_display', new _SelectWidget2.default({
	            options: this.payment_display_options,
	            title: "Affichage des paiements",
	            field_name: 'paymentDisplay',
	            id_key: 'value',
	            value: this.model.get('paymentDisplay')
	        }));
	        this.showChildView('deposit', new _SelectWidget2.default({
	            options: this.deposit_options,
	            title: "Acompte à la commande",
	            field_name: 'deposit',
	            id_key: 'value',
	            value: this.model.get('deposit')
	        }));
	        this.showChildView('payment_times', new _SelectWidget2.default({
	            options: this.payment_times_options,
	            title: "Paiement en",
	            field_name: 'payment_times',
	            id_key: 'value',
	            value: this.model.get('payment_times')
	        }));
	        this.renderTable();
	    }
	});
	exports.default = PaymentBlockView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 180 */
/*!************************************************!*\
  !*** ./src/task/views/PaymentLineTableView.js ***!
  \************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _PaymentDepositView = __webpack_require__(/*! ./PaymentDepositView.js */ 181);
	
	var _PaymentDepositView2 = _interopRequireDefault(_PaymentDepositView);
	
	var _PaymentLineModel = __webpack_require__(/*! ../models/PaymentLineModel.js */ 183);
	
	var _PaymentLineModel2 = _interopRequireDefault(_PaymentLineModel);
	
	var _PaymentLineCollectionView = __webpack_require__(/*! ./PaymentLineCollectionView.js */ 184);
	
	var _PaymentLineCollectionView2 = _interopRequireDefault(_PaymentLineCollectionView);
	
	var _PaymentLineFormView = __webpack_require__(/*! ./PaymentLineFormView.js */ 187);
	
	var _PaymentLineFormView2 = _interopRequireDefault(_PaymentLineFormView);
	
	var _PaymentLineView = __webpack_require__(/*! ./PaymentLineView.js */ 185);
	
	var _PaymentLineView2 = _interopRequireDefault(_PaymentLineView);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : PaymentLineTableView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var PaymentLineTableView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/PaymentLineTableView.mustache */ 189),
	    regions: {
	        lines: '.paymentlines',
	        modalRegion: '.payment-line-modal-container',
	        deposit: ".deposit"
	    },
	    ui: {
	        btn_add: ".btn-add"
	    },
	    events: {
	        "click @ui.btn_add": "onLineAdd"
	    },
	    childViewEvents: {
	        'line:edit': 'onLineEdit',
	        'line:delete': 'onLineDelete',
	        'destroy:modal': 'render'
	
	    },
	    initialize: function initialize(options) {
	        this.collection = options['collection'];
	        this.message = _backbone4.default.channel('message');
	        this.facade = _backbone4.default.channel('facade');
	        this.totalmodel = this.facade.request('get:totalmodel');
	        this.depositmodel = new _PaymentLineModel2.default({
	            description: "Facture d'acompte",
	            date: "À la commande",
	            amount: this.collection.depositAmount(this.model.get('deposit'))
	        });
	        this.listenTo(this.totalmodel, 'change:ttc', this.updateDeposit.bind(this));
	        this.listenTo(this.facade, 'update:payment_lines', this.updateDeposit.bind(this));
	        this.listenTo(this.model, 'change:deposit', this.updateDeposit.bind(this));
	        this.edit = this.getOption('edit');
	    },
	    onLineAdd: function onLineAdd() {
	        var model = new _PaymentLineModel2.default({
	            task_id: this.model.get('id'),
	            order: this.collection.getMaxOrder() - 1
	        });
	        this.showPaymentLineForm(model, "Ajouter une échéance", false);
	    },
	    onLineEdit: function onLineEdit(childView) {
	        this.showPaymentLineForm(childView.model, "Modifier l'échéance", true);
	    },
	
	    showPaymentLineForm: function showPaymentLineForm(model, title, edit) {
	        var edit_amount = false;
	        if (this.edit) {
	            edit_amount = true;
	            if (edit) {
	                if (model.isLast()) {
	                    edit_amount = false;
	                }
	            }
	        }
	        var form = new _PaymentLineFormView2.default({
	            model: model,
	            title: title,
	            destCollection: this.collection,
	            edit: edit,
	            edit_amount: edit_amount,
	            show_date: this.getOption('show_date')
	        });
	        this.showChildView('modalRegion', form);
	    },
	    onDeleteSuccess: function onDeleteSuccess() {
	        this.message.trigger('success', "Vos données ont bien été supprimées");
	    },
	    onDeleteError: function onDeleteError() {
	        this.message.trigger('error', "Une erreur a été rencontrée lors de la suppression de cet élément");
	    },
	    onLineDelete: function onLineDelete(childView) {
	        var result = window.confirm("Êtes-vous sûr de vouloir supprimer cette échéance ?");
	        if (result) {
	            childView.model.destroy({
	                success: this.onDeleteSuccess.bind(this),
	                error: this.onDeleteError.bind(this)
	            });
	        }
	    },
	    templateContext: function templateContext() {
	        return {
	            show_date: this.getOption('show_date'),
	            show_add: this.getOption('edit')
	        };
	    },
	    updateDeposit: function updateDeposit() {
	        console.log("PaymentLineTableView.updateDeposit");
	        var deposit = this.model.get('deposit');
	        var deposit_amount = this.collection.depositAmount(deposit);
	        this.depositmodel.set({ amount: deposit_amount });
	        this.updateLines();
	    },
	    updateLines: function updateLines() {
	        console.log("PaymentLineTableView.updateLines");
	        var payment_times = this.model.get('payment_times');
	        var deposit = this.model.get('deposit');
	
	        payment_times = (0, _math.strToFloat)(payment_times);
	        if (payment_times > 0) {
	            this.collection.genPaymentLines(payment_times, deposit);
	        } else {
	            this.collection.updateSold(deposit);
	        }
	    },
	    showDeposit: function showDeposit() {
	        var view = new _PaymentDepositView2.default({
	            model: this.depositmodel,
	            show_date: this.getOption('show_date')
	        });
	        this.showChildView('deposit', view);
	    },
	    showLines: function showLines() {
	        this.showChildView('lines', new _PaymentLineCollectionView2.default({
	            collection: this.collection,
	            show_date: this.getOption('show_date'),
	            edit: this.getOption('edit')
	        }));
	    },
	    onRender: function onRender() {
	        this.showDeposit();
	        this.showLines();
	    }
	});
	exports.default = PaymentLineTableView;

/***/ }),
/* 181 */
/*!**********************************************!*\
  !*** ./src/task/views/PaymentDepositView.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : PaymentDepositView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var PaymentDepositView = _backbone2.default.View.extend({
	    className: 'row taskline',
	    template: __webpack_require__(/*! ./templates/PaymentDepositView.mustache */ 182),
	    modelEvents: {
	        'change:amount': 'render'
	    },
	    templateContext: function templateContext() {
	        return {
	            show_date: this.getOption('show_date'),
	            amount_label: (0, _math.formatAmount)(this.model.get('amount'))
	        };
	    }
	});
	exports.default = PaymentDepositView;

/***/ }),
/* 182 */
/*!**************************************************************!*\
  !*** ./src/task/views/templates/PaymentDepositView.mustache ***!
  \**************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class='col-lg-4 col-md-4 col-sm-4 col-xs-12 description'>\n    <b>Facture d'acompte</b>\n</div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_date : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "<div class='col-lg-3 col-md-3 col-sm4 col-xs-12 text-center'>";
	  stack1 = ((helper = (helper = helpers.amount_label || (depth0 != null ? depth0.amount_label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"amount_label","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>\n<div class='col-lg-3 col-md-5 col-sm-7 text-right'>\n</div>\n";
	},"2":function(depth0,helpers,partials,data) {
	  return "<div class='col-md-2 col-sm-4 col-xs-12 date'> à la commmande </div>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.amount : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 183 */
/*!*********************************************!*\
  !*** ./src/task/models/PaymentLineModel.js ***!
  \*********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _BaseModel = __webpack_require__(/*! ./BaseModel.js */ 132);
	
	var _BaseModel2 = _interopRequireDefault(_BaseModel);
	
	var _date = __webpack_require__(/*! ../../date.js */ 32);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var PaymentLineModel = _BaseModel2.default.extend({
	    props: ['id', 'task_id', 'order', 'description', 'amount', 'date'],
	    defaults: {
	        date: (0, _date.dateToIso)(new Date()),
	        order: 1
	    },
	    validation: {
	        description: {
	            required: true,
	            msg: "Veuillez saisir un objet"
	        },
	        amount: {
	            required: true,
	            pattern: "amount2",
	            msg: "Veuillez saisir un montant, dans la limite de 2 chiffres après la virgule"
	        }
	    },
	    isLast: function isLast() {
	        var order = this.get('order');
	        var max_order = this.collection.getMaxOrder();
	        return order == max_order;
	    },
	    isFirst: function isFirst() {
	        var min_order = this.model.collection.getMinOrder();
	        var order = this.get('order');
	        return order == min_order;
	    }
	}); /*
	     * File Name : PaymentLineModel.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = PaymentLineModel;

/***/ }),
/* 184 */
/*!*****************************************************!*\
  !*** ./src/task/views/PaymentLineCollectionView.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _PaymentLineView = __webpack_require__(/*! ./PaymentLineView.js */ 185);
	
	var _PaymentLineView2 = _interopRequireDefault(_PaymentLineView);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : PaymentLineCollectionView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var PaymentLineCollectionView = _backbone2.default.CollectionView.extend({
	    tagName: 'div',
	    className: 'col-xs-12',
	    childView: _PaymentLineView2.default,
	    collectionEvents: {
	        'change:reorder': 'render'
	    },
	    childViewTriggers: {
	        'edit': 'line:edit',
	        'delete': 'line:delete'
	    },
	    childViewOptions: function childViewOptions(model) {
	        var edit = this.getOption('edit');
	        return {
	            show_date: this.getOption('show_date'),
	            edit: edit
	        };
	    },
	    onChildviewOrderUp: function onChildviewOrderUp(childView) {
	        this.collection.moveUp(childView.model);
	    },
	    onChildviewOrderDown: function onChildviewOrderDown(childView) {
	        this.collection.moveDown(childView.model);
	    }
	});
	exports.default = PaymentLineCollectionView;

/***/ }),
/* 185 */
/*!*******************************************!*\
  !*** ./src/task/views/PaymentLineView.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _date = __webpack_require__(/*! ../../date.js */ 32);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var PaymentLineView = _backbone2.default.View.extend({
	    className: 'row taskline',
	    template: __webpack_require__(/*! ./templates/PaymentLineView.mustache */ 186),
	    modelEvents: {
	        'change': 'render'
	    },
	    ui: {
	        up_button: 'button.up',
	        down_button: 'button.down',
	        edit_button: 'button.edit',
	        delete_button: 'button.delete'
	    },
	    triggers: {
	        'click @ui.up_button': 'order:up',
	        'click @ui.down_button': 'order:down',
	        'click @ui.edit_button': 'edit',
	        'click @ui.delete_button': 'delete'
	    },
	    templateContext: function templateContext() {
	        var min_order = this.model.collection.getMinOrder();
	        var max_order = this.model.collection.getMaxOrder();
	        var order = this.model.get('order');
	        return {
	            edit: this.getOption('edit'),
	            show_date: this.getOption('show_date'),
	            date: (0, _date.formatDate)(this.model.get('date')),
	            amount: (0, _math.formatAmount)(this.model.get('amount')),
	            is_not_first: order != min_order,
	            is_not_before_last: order != max_order - 1,
	            is_not_last: order != max_order
	        };
	    }
	}); /*
	     * File Name : PaymentLineView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = PaymentLineView;

/***/ }),
/* 186 */
/*!***********************************************************!*\
  !*** ./src/task/views/templates/PaymentLineView.mustache ***!
  \***********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<div class='col-md-2 col-sm-4 col-xs-12 date'>"
	    + escapeExpression(((helper = (helper = helpers.date || (depth0 != null ? depth0.date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"date","hash":{},"data":data}) : helper)))
	    + " </div>\n";
	},"3":function(depth0,helpers,partials,data) {
	  return "    <button type='button' class='btn btn-default delete'>\n        <i class='glyphicon glyphicon-trash'></i> <span class='hidden-xs'>Supprimer</span>\n    </button>\n";
	  },"5":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_not_last : depth0), {"name":"if","hash":{},"fn":this.program(6, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"6":function(depth0,helpers,partials,data) {
	  return "    <button type='button' class='btn btn-default btn-small up'>\n        <i class='glyphicon glyphicon-arrow-up'></i>\n    </button>\n    <br />\n";
	  },"8":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_not_before_last : depth0), {"name":"if","hash":{},"fn":this.program(9, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"9":function(depth0,helpers,partials,data) {
	  return "    <button type='button' class='btn btn-default btn-small down'>\n        <i class='glyphicon glyphicon-arrow-down'></i>\n    </button>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class='col-lg-4 col-md-4 col-sm-4 col-xs-12 description'>\n    ";
	  stack1 = ((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "\n</div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_date : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "<div class='col-lg-3 col-md-3 col-sm4 col-xs-12 text-center'>";
	  stack1 = ((helper = (helper = helpers.amount || (depth0 != null ? depth0.amount : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"amount","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n<div class='col-lg-3 col-md-5 col-sm-7 text-right'>\n    <button type='button' class='btn btn-default edit'>\n        <i class='glyphicon glyphicon-pencil'></i> <span class='hidden-xs'>Modifier</span>\n    </button>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_not_last : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_not_first : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_not_last : depth0), {"name":"if","hash":{},"fn":this.program(8, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>\n";
	},"useData":true});

/***/ }),
/* 187 */
/*!***********************************************!*\
  !*** ./src/task/views/PaymentLineFormView.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 77);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ../../widgets/TextAreaWidget.js */ 114);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _ModalFormBehavior = __webpack_require__(/*! ../../base/behaviors/ModalFormBehavior.js */ 86);
	
	var _ModalFormBehavior2 = _interopRequireDefault(_ModalFormBehavior);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _DatePickerWidget = __webpack_require__(/*! ../../widgets/DatePickerWidget.js */ 75);
	
	var _DatePickerWidget2 = _interopRequireDefault(_DatePickerWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : PaymentLineFormView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/PaymentLineFormView.mustache */ 188);
	
	var PaymentLineFormView = _backbone2.default.View.extend({
	    behaviors: [_ModalFormBehavior2.default],
	    template: template,
	    regions: {
	        'order': '.order',
	        'description': ".description",
	        "date": ".date",
	        "amount": ".amount"
	    },
	    onRender: function onRender() {
	        this.showChildView('order', new _InputWidget2.default({
	            value: this.model.get('order'),
	            field_name: 'order',
	            type: 'hidden'
	        }));
	        var view = new _TextAreaWidget2.default({
	            field_name: "description",
	            value: this.model.get('description'),
	            title: "Intitulé"
	        });
	        this.showChildView('description', view);
	
	        if (this.getOption('show_date')) {
	            view = new _DatePickerWidget2.default({
	                date: this.model.get('date'),
	                title: "Date",
	                field_name: "date"
	            });
	        }
	        this.showChildView('date', view);
	
	        if (this.getOption('edit_amount')) {
	            view = new _InputWidget2.default({
	                field_name: 'amount',
	                value: this.model.get('amount'),
	                title: "Montant"
	            });
	            this.showChildView('amount', view);
	        }
	    },
	    templateContext: function templateContext() {
	        return {
	            title: this.getOption('title')
	        };
	    }
	});
	exports.default = PaymentLineFormView;

/***/ }),
/* 188 */
/*!***************************************************************!*\
  !*** ./src/task/views/templates/PaymentLineFormView.mustache ***!
  \***************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<div class=\"modal-dialog\" role=\"document\">\n	<div class=\"modal-content\">\n        <form class='form taskline-form'>\n            <div class=\"modal-header\">\n              <button tabindex='-1' type=\"button\" class=\"close\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n              <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n            </div>\n            <div class=\"modal-body\">\n                <div class='order'></div>\n                <div class='description required'></div>\n                <div class='date required'></div>\n                <div class='amount required'></div>\n            </div>\n            <div class=\"modal-footer\">\n                <button\n                    class='btn btn-success primary-action'\n                    type='submit'\n                    value='submit'>\n                    "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n                </button>\n                <button\n                    class='btn btn-default secondary-action'\n                    type='reset'\n                    value='submit'>\n                    Annuler\n                </button>\n            </div>\n        </form>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n\n";
	},"useData":true});

/***/ }),
/* 189 */
/*!****************************************************************!*\
  !*** ./src/task/views/templates/PaymentLineTableView.mustache ***!
  \****************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "<div class='col-md-2 col-sm-4 col-xs-12 date'>Date</div>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "    <div class='col-lg-3 col-md-5 col-sm-7 text-right actions'>Actions</div>\n";
	  },"5":function(depth0,helpers,partials,data) {
	  return "    <div class='row actions'>\n        <div class='col-xs-11 text-right'>\n            <button type='button' class='btn btn-info btn-add'>\n                <i class='glyphicon glyphicon-plus-sign'></i> Ajouter une échéance\n            </button>\n        </div>\n    </div>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<div class='payment-line-modal-container'></div>\n<div class='row lines-header hidden-xs'>\n    <div class='col-lg-4 col-md-4 col-sm-4 col-xs-12 description'>Libellé</div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_date : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    <div class='col-lg-3 col-md-3 col-sm4 col-xs-12 text-center'>Montant</div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_add : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n<div class='row'>\n    <div class='deposit col-xs-12 lines'>\n    </div>\n</div>\n<div class='row lines paymentlines'>\n</div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_add : depth0), {"name":"if","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "<div class='modalregion'></div>\n";
	},"useData":true});

/***/ }),
/* 190 */
/*!************************************************************!*\
  !*** ./src/task/views/templates/PaymentBlockView.mustache ***!
  \************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<h2>Paiements</h2>\n<div class='content'>\n    <div class='payment_display-container'></div>\n    <div class='payment-deposit-container'></div>\n    <div class='payment_times-container'></div>\n    <div class='payment-lines-container'></div>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 191 */
/*!****************************************!*\
  !*** ./src/task/views/RightBarView.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _jquery = __webpack_require__(/*! jquery */ 2);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ActionCollection = __webpack_require__(/*! ../models/ActionCollection.js */ 192);
	
	var _ActionCollection2 = _interopRequireDefault(_ActionCollection);
	
	var _ActionListView = __webpack_require__(/*! ./ActionListView.js */ 194);
	
	var _ActionListView2 = _interopRequireDefault(_ActionListView);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : RightBarView.js
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/RightBarView.mustache */ 195);
	
	var RightBarView = _backbone2.default.View.extend({
	    regions: {
	        container: ".child-container"
	    },
	    ui: {
	        buttons: 'button'
	    },
	    events: {
	        'click @ui.buttons': 'onButtonClick'
	    },
	    modelEvents: {
	        'change': 'render'
	    },
	    template: template,
	    templateContext: function templateContext() {
	        return {
	            buttons: this.getOption('actions')['status'],
	            ttc: (0, _math.formatAmount)(this.model.get('ttc'), true),
	            ht: (0, _math.formatAmount)(this.model.get('ht', true)),
	            ht_before: (0, _math.formatAmount)(this.model.get('ht_before_discounts'), false),
	            tvas: this.model.tva_labels()
	        };
	    },
	    onButtonClick: function onButtonClick(event) {
	        var target = (0, _jquery2.default)(event.target);
	        var status = target.data('status');
	        var title = target.data('title');
	        var label = target.data('label');
	        var url = target.data('url');
	        this.triggerMethod('status:change', status, title, label, url);
	    },
	    onRender: function onRender() {
	        var action_collection = new _ActionCollection2.default(this.getOption('actions')['others']);
	        this.showChildView('container', new _ActionListView2.default({ collection: action_collection }));
	    }
	});
	exports.default = RightBarView;

/***/ }),
/* 192 */
/*!*********************************************!*\
  !*** ./src/task/models/ActionCollection.js ***!
  \*********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ActionModel = __webpack_require__(/*! ./ActionModel.js */ 193);
	
	var _ActionModel2 = _interopRequireDefault(_ActionModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ActionCollection.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ActionCollection = _backbone2.default.Collection.extend({
	  model: _ActionModel2.default
	});
	exports.default = ActionCollection;

/***/ }),
/* 193 */
/*!****************************************!*\
  !*** ./src/task/models/ActionModel.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ActionModel = _backbone2.default.Model.extend({}); /*
	                                                        * File Name : ActionModel.js
	                                                        *
	                                                        * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                        * Company : Majerti ( http://www.majerti.fr )
	                                                        *
	                                                        * This software is distributed under GPLV3
	                                                        * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                        *
	                                                        */
	exports.default = ActionModel;

/***/ }),
/* 194 */
/*!******************************************!*\
  !*** ./src/task/views/ActionListView.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _AnchorWidget = __webpack_require__(/*! ../../widgets/AnchorWidget.js */ 30);
	
	var _AnchorWidget2 = _interopRequireDefault(_AnchorWidget);
	
	var _ToggleWidget = __webpack_require__(/*! ../../widgets/ToggleWidget.js */ 45);
	
	var _ToggleWidget2 = _interopRequireDefault(_ToggleWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ActionListView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ActionListView = _backbone2.default.CollectionView.extend({
	    childTemplates: {
	        'anchor': _AnchorWidget2.default,
	        'toggle': _ToggleWidget2.default
	    },
	    tagName: 'div',
	    childView: function childView(item) {
	        var widget = this.childTemplates[item.get('widget')];
	        if (_underscore2.default.isUndefined(widget)) {
	            console.log("Error : invalid widget type %s", item.get('widget'));
	        }
	        return widget;
	    }
	});
	exports.default = ActionListView;

/***/ }),
/* 195 */
/*!********************************************************!*\
  !*** ./src/task/views/templates/RightBarView.mustache ***!
  \********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "    <button\n        class='btn btn-block "
	    + escapeExpression(lambda((depth0 != null ? depth0.css : depth0), depth0))
	    + "'\n        title=\""
	    + escapeExpression(lambda((depth0 != null ? depth0.title : depth0), depth0))
	    + "\"\n        data-url='"
	    + escapeExpression(lambda((depth0 != null ? depth0.url : depth0), depth0))
	    + "'\n        data-title='"
	    + escapeExpression(lambda((depth0 != null ? depth0.title : depth0), depth0))
	    + "'\n        data-label='"
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "'\n        data-status='"
	    + escapeExpression(lambda((depth0 != null ? depth0.status : depth0), depth0))
	    + "'>\n    <i class='glyphicon glyphicon-"
	    + escapeExpression(lambda((depth0 != null ? depth0.icon : depth0), depth0))
	    + "'></i>\n    "
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "\n    </button>\n";
	},"3":function(depth0,helpers,partials,data) {
	  var stack1, lambda=this.lambda, buffer = "    <div>\n        <div class='text-center'>\n            ";
	  stack1 = lambda((depth0 != null ? depth0.label : depth0), depth0);
	  if (stack1 != null) { buffer += stack1; }
	  buffer += " : ";
	  stack1 = lambda((depth0 != null ? depth0.value : depth0), depth0);
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\n        </div>\n    </div>\n    <hr />\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div>\n<h3 class='text-center'>Actions</h3>\n<hr />\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.buttons : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "<hr />\n<div class='child-container'></div>\n</div>\n<div class='totals'>\n    <div>\n        <div class='text-center'>\n            Total HT avant remise : ";
	  stack1 = ((helper = (helper = helpers.ht_before || (depth0 != null ? depth0.ht_before : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht_before","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "\n        </div>\n    </div>\n    <hr />\n    <div>\n        <div class='text-center'>\n            Total HT : ";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "\n        </div>\n    </div>\n    <hr />\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.tvas : depth0), {"name":"each","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    <div>\n        <div class='text-center'>\n            Total TTC : ";
	  stack1 = ((helper = (helper = helpers.ttc || (depth0 != null ? depth0.ttc : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ttc","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\n        </div>\n    </div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 196 */
/*!**************************************!*\
  !*** ./src/task/views/StatusView.js ***!
  \**************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ModalBehavior = __webpack_require__(/*! ../../base/behaviors/ModalBehavior.js */ 49);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _date = __webpack_require__(/*! ../../date.js */ 32);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/StatusView.mustache */ 197); /*
	                                                            * File Name : StatusView.js
	                                                            *
	                                                            * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                            * Company : Majerti ( http://www.majerti.fr )
	                                                            *
	                                                            * This software is distributed under GPLV3
	                                                            * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                            *
	                                                            */
	
	
	var StatusView = _backbone2.default.View.extend({
	    template: template,
	    ui: {
	        'textarea': 'textarea',
	        btn_cancel: '.cancel',
	        submit: 'button[type=submit]',
	        form: 'form'
	    },
	    behaviors: {
	        modal: {
	            behaviorClass: _ModalBehavior2.default
	        }
	    },
	    events: {
	        'click @ui.btn_cancel': 'destroy',
	        'click @ui.submit': 'onSubmit'
	    },
	    submitCallback: function submitCallback(result) {},
	    submitErroCallback: function submitErroCallback(result) {
	        (0, _tools.hideLoader)();
	        var message = "";
	        if (result.responseJSON.errors) {
	            _.each(result.responseJSON.errors, function (error, key) {
	                message += "   " + key + ":" + error;
	            });
	        }
	        if (message == '') {
	            message = "Votre document est incomplet, merci de vérifier votre saisie.";
	        }
	        window.alert(message);
	    },
	    onSubmit: function onSubmit(event) {
	        event.preventDefault();
	        var datas = (0, _tools.serializeForm)(this.getUI('form'));
	        datas['submit'] = this.getOption('status');
	        var url = this.getOption('url');
	        (0, _tools.showLoader)();
	        this.serverRequest = (0, _tools.ajax_call)(url, datas, "POST");
	        this.serverRequest.then(this.submitCallback.bind(this), this.submitErroCallback.bind(this));
	    },
	    templateContext: function templateContext() {
	        var result = {
	            title: this.getOption('title'),
	            label: this.getOption('label'),
	            status: this.getOption('status'),
	            url: this.getOption('url'),
	            ask_for_date: false
	        };
	        if (this.getOption('status') == 'valid') {
	            var model = this.getOption('model');
	            var date = model.get('date');
	            var today = new Date();
	            if (date != (0, _date.dateToIso)(today)) {
	                result['ask_for_date'] = true;
	                date = (0, _date.parseDate)(date);
	                result['date'] = date.toLocaleDateString();
	                result['today'] = today.toLocaleDateString();
	            }
	        }
	        return result;
	    }
	});
	exports.default = StatusView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 197 */
/*!******************************************************!*\
  !*** ./src/task/views/templates/StatusView.mustache ***!
  \******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "                        <div class='form-group'>\n                            <div class='alert alert-danger'><i class='glyphicon glyphicon-warning-sign'></i> La date du document diffère de la date du jour</div>\n                            <div class='radio'>\n                            <label>\n                                <input type=\"radio\" name=\"change_date\" value='1' checked> Mettre à la date d'aujourd'hui "
	    + escapeExpression(((helper = (helper = helpers.today || (depth0 != null ? depth0.today : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"today","hash":{},"data":data}) : helper)))
	    + "\n                            </label>\n                            </div>\n                            <div class='radio'>\n                            <label>\n                                <input type=\"radio\" name=\"change_date\" value='0'> Conserver la date "
	    + escapeExpression(((helper = (helper = helpers.date || (depth0 != null ? depth0.date : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"date","hash":{},"data":data}) : helper)))
	    + "\n                            </label>\n                            </div>\n                        </div>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\" role=\"document\">\n	<div class=\"modal-content\">\n	  <form class='form' data-url='"
	    + escapeExpression(((helper = (helper = helpers.url || (depth0 != null ? depth0.url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"url","hash":{},"data":data}) : helper)))
	    + "' method='POST'>\n          <div class=\"modal-header\">\n            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n            <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n          </div>\n          <div class=\"modal-body\">\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.ask_for_date : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "                    <div class='form-group'>\n                        <label for='comment'>Commentaires</label>\n                        <textarea class='form-control' name='comment' rows=4></textarea>\n                    </div>\n          </div>\n          <div class=\"modal-footer\">\n            <button class='btn btn-success primary-action' type='submit' name='submit' value='"
	    + escapeExpression(((helper = (helper = helpers.status || (depth0 != null ? depth0.status : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"status","hash":{},"data":data}) : helper)))
	    + "'>"
	    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
	    + "</button>\n            <button class='btn btn-default secondary-action' data-dismiss='modal'>Annuler</button>\n          </div>\n	  </form>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n";
	},"useData":true});

/***/ }),
/* 198 */
/*!********************************************!*\
  !*** ./src/task/views/BootomActionView.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function($) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var BootomActionView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/BootomActionView.mustache */ 199),
	    tagName: 'footer',
	    className: 'sticky-footer hidden-md hidden-lg text-center',
	    ui: {
	        buttons: 'button'
	    },
	    events: {
	        'click @ui.buttons': 'onButtonClick'
	    },
	    templateContext: function templateContext() {
	        return {
	            buttons: this.getOption('actions')['status']
	        };
	    },
	    onButtonClick: function onButtonClick(event) {
	        var target = $(event.target);
	        var status = target.data('status');
	        var title = target.data('title');
	        var label = target.data('label');
	        var url = target.data('url');
	        this.triggerMethod('status:change', status, title, label, url);
	    }
	
	}); /*
	     * File Name : BootomActionView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = BootomActionView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 2)))

/***/ }),
/* 199 */
/*!************************************************************!*\
  !*** ./src/task/views/templates/BootomActionView.mustache ***!
  \************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "    <button\n        class='btn "
	    + escapeExpression(lambda((depth0 != null ? depth0.css : depth0), depth0))
	    + "'\n        data-url='"
	    + escapeExpression(lambda((depth0 != null ? depth0.url : depth0), depth0))
	    + "'\n        data-title='"
	    + escapeExpression(lambda((depth0 != null ? depth0.title : depth0), depth0))
	    + "'\n        data-label='"
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "'\n        data-status='"
	    + escapeExpression(lambda((depth0 != null ? depth0.status : depth0), depth0))
	    + "'>\n    <i class='glyphicon glyphicon-"
	    + escapeExpression(lambda((depth0 != null ? depth0.icon : depth0), depth0))
	    + "'></i> <br />\n    "
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "\n    </button>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.buttons : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 200 */
/*!*************************************!*\
  !*** ./src/base/views/LoginView.js ***!
  \*************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ModalBehavior = __webpack_require__(/*! ../behaviors/ModalBehavior.js */ 49);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/LoginView.mustache */ 201); /*
	                                                           * File Name : LoginView.js
	                                                           *
	                                                           * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                           * Company : Majerti ( http://www.majerti.fr )
	                                                           *
	                                                           * This software is distributed under GPLV3
	                                                           * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                           *
	                                                           */
	
	
	var LoginView = _backbone2.default.View.extend({
	    className: 'modal-overlay',
	    behaviors: [_ModalBehavior2.default],
	    template: template,
	    url: '/api/login/v1',
	    ui: {
	        'form': 'form',
	        'login': 'input[name=login]',
	        'password': 'input[type=password]',
	        'remember_me': 'input[name=remember_me]',
	        'errors': '.errors'
	    },
	    events: {
	        "submit @ui.form": "onSubmit"
	    },
	    onSubmit: function onSubmit(event) {
	        event.preventDefault();
	        this.getUI('errors').hide();
	        var datas = {
	            login: this.getUI('login').val(),
	            password: this.getUI('password').val()
	        };
	        if (this.getUI('remember_me').is(':checked')) {
	            datas['remember_me'] = true;
	        }
	        var channel = _backbone4.default.channel('auth');
	        channel.trigger('login', datas, this.success.bind(this), this.error.bind(this));
	    },
	    onModalBeforeClose: function onModalBeforeClose() {
	        console.log("Redirecting");
	        window.location.replace('#');
	    },
	    success: function success() {
	        this.triggerMethod('close');
	    },
	    error: function error() {
	        this.getUI('errors').html("Erreur d'authentification");
	        this.getUI('errors').show();
	    }
	});
	exports.default = LoginView;

/***/ }),
/* 201 */
/*!*****************************************************!*\
  !*** ./src/base/views/templates/LoginView.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div class=\"modal-dialog login-dialog\" role=\"document\">\n	<div class=\"modal-content\">\n		<form>\n          <div class=\"modal-header\">\n            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n            <h4 class=\"modal-title\">Authentification</h4>\n          </div>\n            <div class=\"modal-body\">\n                <div class='icon'>\n                    <i class='fa fa-user-circle'></i>\n                </div>\n                <div class=\"errors alert alert-danger\" style=\"display:none;\"></div>\n                <div class=\"form-group  item-login item-login\" title=\"\" id=\"item-deformField1\">\n                    <label for=\"deformField1\" class=\"control-label required\" id=\"req-deformField1\">\n                        Identifiant\n                    </label>\n                    <input name=\"login\" value=\"\" id=\"deformField1\" class=\" form-control \" type=\"text\">\n                </div>\n                <div class=\"form-group   item-password\" title=\"\" id=\"item-deformField2\">\n                    <label for=\"deformField2\" class=\"control-label required\" id=\"req-deformField2\">\n                        Mot de passe\n                    </label>\n                    <input name=\"password\" value=\"\" id=\"deformField2\" class=\" form-control \" type=\"password\">\n                </div>\n                <div class=\"form-group   item-remember_me\" title=\"\" id=\"item-deformField4\">\n                    <div class=\"checkbox\">\n                        <label for=\"deformField4\">\n                            <input name=\"remember_me\" value=\"true\" id=\"deformField4\" type=\"checkbox\">\n                            Rester connecté\n                        </label>\n                    </div>\n                </div>\n            </div>\n            <div class=\"modal-footer\">\n            <button class='btn btn-primary btn-block' type='submit'>Connexion</button>\n            </div>\n        </form>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n";
	  },"useData":true});

/***/ }),
/* 202 */
/*!****************************************************!*\
  !*** ./src/task/views/templates/MainView.mustache ***!
  \****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 38);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div id='modalregion'>\n</div>\n<div class='container-fluid page-content'>\n    <div class='task-edit col-md-9 col-xs-12'>\n        <div class='errors'>\n        </div>\n        <div id='general'>\n        </div>\n        <div id='common'>\n        </div>\n        <div id='tasklines'>\n        </div>\n        <div class='ht_before_discounts'>\n        </div>\n        <div id='discounts'>\n        </div>\n        <div id='expenses_ht'>\n        </div>\n        <div class='totals'>\n        </div>\n        <div class='notes'>\n        </div>\n        <div class='payment-conditions'>\n        </div>\n        <div class='payments'>\n        </div>\n    </div>\n\n    <div class='task-desktop-actions col-md-3 hidden-sm hidden-xs'\n         id='rightbar'>\n    </div>\n</div>\n<footer class='footer-actions'></footer>\n";
	  },"useData":true});

/***/ }),
/* 203 */
/*!***************************************!*\
  !*** ./src/task/components/Facade.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _CommonModel = __webpack_require__(/*! ../models/CommonModel.js */ 204);
	
	var _CommonModel2 = _interopRequireDefault(_CommonModel);
	
	var _TaskGroupCollection = __webpack_require__(/*! ../models/TaskGroupCollection.js */ 205);
	
	var _TaskGroupCollection2 = _interopRequireDefault(_TaskGroupCollection);
	
	var _DiscountCollection = __webpack_require__(/*! ../models/DiscountCollection.js */ 206);
	
	var _DiscountCollection2 = _interopRequireDefault(_DiscountCollection);
	
	var _PaymentLineCollection = __webpack_require__(/*! ../models/PaymentLineCollection.js */ 207);
	
	var _PaymentLineCollection2 = _interopRequireDefault(_PaymentLineCollection);
	
	var _StatusHistoryCollection = __webpack_require__(/*! ../models/StatusHistoryCollection.js */ 208);
	
	var _StatusHistoryCollection2 = _interopRequireDefault(_StatusHistoryCollection);
	
	var _TotalModel = __webpack_require__(/*! ../models/TotalModel.js */ 209);
	
	var _TotalModel2 = _interopRequireDefault(_TotalModel);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
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
	    ht: 5,
	    radioEvents: {
	        'changed:task': 'computeTotals',
	        'changed:discount': 'computeMainTotals',
	        'changed:expense_ht': 'computeMainTotals',
	        'changed:payment_lines': "updatePaymentLines",
	        'sync:model': 'syncModel',
	        'save:model': 'saveModel'
	    },
	    radioRequests: {
	        'get:model': 'getModelRequest',
	        'get:collection': 'getCollectionRequest',
	        'get:paymentcollection': 'getPaymentCollectionRequest',
	        'get:totalmodel': 'getTotalModelRequest',
	        'get:status_history_collection': 'getStatusHistory',
	        'is:valid': "isDataValid",
	        'get:attachments': 'getAttachments'
	    },
	    initialize: function initialize(options) {
	        this.syncModel = this.syncModel.bind(this);
	    },
	    loadModels: function loadModels(form_datas) {
	        this.datas = form_datas;
	        this.models = {};
	        this.collections = {};
	        this.totalmodel = new _TotalModel2.default();
	        this.models['common'] = new _CommonModel2.default(form_datas);
	        this.models['common'].url = AppOption['context_url'];
	
	        var lines = form_datas['line_groups'];
	        this.collections['task_groups'] = new _TaskGroupCollection2.default(lines);
	
	        var discounts = form_datas['discounts'];
	        this.collections['discounts'] = new _DiscountCollection2.default(discounts);
	        this.computeTotals();
	
	        if (_.has(form_datas, 'payment_lines')) {
	            var payment_lines = form_datas['payment_lines'];
	            this.payment_lines_collection = new _PaymentLineCollection2.default(payment_lines);
	        }
	
	        if (_.has(form_datas, 'status_history')) {
	            var history = form_datas['status_history'];
	            this.status_history_collection = new _StatusHistoryCollection2.default(history);
	        }
	    },
	    getAttachments: function getAttachments() {
	        return this.datas.attachments;
	    },
	    getStatusHistory: function getStatusHistory() {
	        return this.status_history_collection;
	    },
	    syncModel: function syncModel(modelName) {
	        var modelName = modelName || 'common';
	        this.models[modelName].save(null, { wait: true, sync: true, patch: true });
	    },
	    saveModel: function saveModel(view, model, datas, extra_options, success, error) {
	        /*
	         * Save a model
	         *
	         * :param obj model: The model to save
	         * :param obj datas: The datas to transmit to the save call
	         * :param obj extra_options: The options to pass to the save call
	         * :param func success: The success callback
	         * :param func error: The error callback
	         */
	        var options = {
	            wait: true,
	            patch: true
	        };
	        _.extend(options, extra_options);
	        options['success'] = success;
	        options['error'] = error;
	
	        model.save(datas, options);
	    },
	    getPaymentCollectionRequest: function getPaymentCollectionRequest() {
	        return this.payment_lines_collection;
	    },
	    getTotalModelRequest: function getTotalModelRequest() {
	        return this.totalmodel;
	    },
	    getModelRequest: function getModelRequest(label) {
	        return this.models[label];
	    },
	    getCollectionRequest: function getCollectionRequest(label) {
	        return this.collections[label];
	    },
	    updatePaymentLines: function updatePaymentLines() {
	        var channel = _backbone4.default.channel('facade');
	        channel.trigger('update:payment_lines', this.totalmodel);
	    },
	    computeTotals: function computeTotals() {
	        this.totalmodel.set({
	            'ht_before_discounts': this.tasklines_ht(),
	            'ht': this.HT(),
	            'tvas': this.TVAParts(),
	            'ttc': this.TTC()
	        });
	    },
	    computeMainTotals: function computeMainTotals() {
	        console.log("computeMainTotals");
	        this.totalmodel.set({
	            'ht_before_discounts': this.tasklines_ht(),
	            'ht': this.HT(),
	            'tvas': this.TVAParts(),
	            'ttc': this.TTC()
	        });
	    },
	    tasklines_ht: function tasklines_ht() {
	        return this.collections['task_groups'].ht();
	    },
	    HT: function HT() {
	        var result = 0;
	        _.each(this.collections, function (collection) {
	            result += collection.ht();
	        });
	        _.each(this.models, function (model) {
	            result += model.ht();
	        });
	        console.log("Computing HT : %s", result);
	        return result;
	    },
	    TVAParts: function TVAParts() {
	        var result = {};
	        _.each(this.collections, function (collection) {
	            var tva_parts = collection.tvaParts();
	            _.each(tva_parts, function (value, key) {
	                if (key in result) {
	                    value += result[key];
	                }
	                result[key] = value;
	            });
	        });
	        _.each(this.models, function (model) {
	            var tva_parts = model.tvaParts();
	            _.each(tva_parts, function (value, key) {
	                if (key in result) {
	                    value += result[key];
	                }
	                result[key] = value;
	            });
	        });
	        return result;
	    },
	    TTC: function TTC() {
	        var result = 0;
	        _.each(this.collections, function (collection) {
	            result += collection.ttc();
	        });
	        _.each(this.models, function (model) {
	            result += model.ttc();
	        });
	        return result;
	    },
	    isDataValid: function isDataValid() {
	        var channel = _backbone4.default.channel('facade');
	        channel.trigger('bind:validation');
	        var result = {};
	        _.each(this.models, function (model) {
	            var res = model.validate();
	            if (res) {
	                _.extend(result, res);
	            }
	        });
	        _.each(this.collections, function (collection) {
	            var res = collection.validate();
	            if (res) {
	                _.extend(result, res);
	            }
	        });
	        channel.trigger('unbind:validation');
	        return result;
	    }
	});
	var Facade = new FacadeClass();
	exports.default = Facade;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 204 */
/*!****************************************!*\
  !*** ./src/task/models/CommonModel.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _BaseModel = __webpack_require__(/*! ./BaseModel.js */ 132);
	
	var _BaseModel2 = _interopRequireDefault(_BaseModel);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _backbone = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name :
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var CommonModel = _BaseModel2.default.extend({
	    props: ['id', 'name', 'altdate', 'date', 'description', 'address', 'mentions', 'workplace', 'expenses_ht', 'exclusions', 'payment_conditions', 'deposit', 'payment_times', 'paymentDisplay', 'financial_year', 'prefix', 'course', 'display_units'],
	    validation: {
	        date: {
	            required: true,
	            msg: "Veuillez saisir une date"
	        },
	        description: {
	            required: true,
	            msg: "Veuillez saisir un objet"
	        },
	        address: {
	            required: true,
	            msg: "Veuillez saisir une adresse"
	        },
	        expenses_ht: {
	            required: false,
	            pattern: 'amount',
	            msg: "Le montant doit être un nombre"
	        },
	        payment_conditions: function payment_conditions(value) {
	            var channel = _backbone2.default.channel('config');
	            if (channel.request('has:form_section', 'payment_conditions')) {
	                if (!value) {
	                    return "Veuillez saisir des conditions de paiements";
	                }
	            }
	        },
	        financial_year: {
	            required: false,
	            pattern: 'digits',
	            msg: "L'année fiscale de référence doit être un nombre entier"
	        }
	    },
	    initialize: function initialize() {
	        CommonModel.__super__.initialize.apply(this, arguments);
	        var channel = this.channel = _backbone2.default.channel('facade');
	        this.on('sync', function () {
	            channel.trigger('changed:discount');
	        });
	        var config_channel = _backbone2.default.channel('config');
	        this.tva_options = config_channel.request('get:options', 'tvas');
	    },
	    ht: function ht() {
	        return (0, _math.strToFloat)(this.get('expenses_ht'));
	    },
	    tva_key: function tva_key() {
	        var result;
	        var tva_object = _underscore2.default.find(this.tva_options, function (val) {
	            return val['default'];
	        });
	        if (_underscore2.default.isUndefined(tva_object)) {
	            result = 0;
	        } else {
	            result = (0, _math.strToFloat)(tva_object.value);
	        }
	        if (result < 0) {
	            result = 0;
	        }
	        return result;
	    },
	    tva_amount: function tva_amount() {
	        return (0, _math.getTvaPart)(this.ht(), this.tva_key());
	    },
	    tvaParts: function tvaParts() {
	        var result = {};
	        var tva_key = this.tva_key();
	        var tva_amount = this.tva_amount();
	        if (tva_amount == 0) {
	            return result;
	        }
	        result[tva_key] = tva_amount;
	        return result;
	    },
	    ttc: function ttc() {
	        return this.ht() + this.tva_amount();
	    }
	});
	exports.default = CommonModel;

/***/ }),
/* 205 */
/*!************************************************!*\
  !*** ./src/task/models/TaskGroupCollection.js ***!
  \************************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _OrderableCollection = __webpack_require__(/*! ./OrderableCollection.js */ 133);
	
	var _OrderableCollection2 = _interopRequireDefault(_OrderableCollection);
	
	var _TaskGroupModel = __webpack_require__(/*! ./TaskGroupModel.js */ 129);
	
	var _TaskGroupModel2 = _interopRequireDefault(_TaskGroupModel);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	var _backbone = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : TaskGroupCollection.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var TaskGroupCollection = _OrderableCollection2.default.extend({
	    model: _TaskGroupModel2.default,
	    url: function url() {
	        return AppOption['context_url'] + '/' + 'task_line_groups';
	    },
	    initialize: function initialize(options) {
	        TaskGroupCollection.__super__.initialize.apply(this, options);
	        this.on('remove', this.channelCall);
	        this.on('sync', this.channelCall);
	        this.on('reset', this.channelCall);
	        this.on('add', this.channelCall);
	    },
	    channelCall: function channelCall() {
	        var channel = _backbone2.default.channel('facade');
	        channel.trigger('changed:task');
	    },
	    load_from_catalog: function load_from_catalog(sale_product_group_ids) {
	        var serverRequest = (0, _tools.ajax_call)(this.url() + '?action=load_from_catalog', { sale_product_group_ids: sale_product_group_ids }, 'POST');
	        serverRequest.then(this.fetch.bind(this));
	    },
	    ht: function ht() {
	        var result = 0;
	        this.each(function (model) {
	            result += model.ht();
	        });
	        return result;
	    },
	    tvaParts: function tvaParts() {
	        var result = {};
	        this.each(function (model) {
	            var tva_parts = model.tvaParts();
	            _.each(tva_parts, function (value, key) {
	                if (key in result) {
	                    value += result[key];
	                }
	                result[key] = value;
	            });
	        });
	        return result;
	    },
	    ttc: function ttc() {
	        var result = 0;
	        this.each(function (model) {
	            result += model.ttc();
	        });
	        return result;
	    },
	    validate: function validate() {
	        var result = {};
	        this.each(function (model) {
	            var res = model.validate();
	            if (res) {
	                _.extend(result, res);
	            }
	        });
	        if (this.models.length === 0) {
	            result['groups'] = "Veuillez ajouter au moins un ouvrage";
	            this.trigger('validated:invalid', this, { groups: "Veuillez ajouter au moins un ouvrage" });
	        }
	        return result;
	    }
	});
	exports.default = TaskGroupCollection;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 206 */
/*!***********************************************!*\
  !*** ./src/task/models/DiscountCollection.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _DiscountModel = __webpack_require__(/*! ./DiscountModel.js */ 159);
	
	var _DiscountModel2 = _interopRequireDefault(_DiscountModel);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 31);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : DiscountCollection.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var DiscountCollection = _backbone2.default.Collection.extend({
	    model: _DiscountModel2.default,
	    initialize: function initialize(options) {
	        this.on('remove', this.channelCall);
	        this.on('sync', this.channelCall);
	        this.on('reset', this.channelCall);
	        this.on('add', this.channelCall);
	    },
	    channelCall: function channelCall() {
	        var channel = _backbone4.default.channel('facade');
	        channel.trigger('changed:discount');
	    },
	    url: function url() {
	        return AppOption['context_url'] + '/' + 'discount_lines';
	    },
	    ht: function ht() {
	        var result = 0;
	        this.each(function (model) {
	            result += model.ht();
	        });
	        return result;
	    },
	    tvaParts: function tvaParts() {
	        var result = {};
	        this.each(function (model) {
	            var tva_amount = model.tva();
	            var tva = model.get('tva');
	            if (tva in result) {
	                tva_amount += result[tva];
	            }
	            result[tva] = tva_amount;
	        });
	        return result;
	    },
	    ttc: function ttc() {
	        var result = 0;
	        this.each(function (model) {
	            result += model.ttc();
	        });
	        return result;
	    },
	    insert_percent: function insert_percent(model) {
	        /*
	         * Call the server to generate percent based Discounts
	         * :param obj model: A DiscountPercentModel instance
	         */
	        var serverRequest = (0, _tools.ajax_call)(this.url() + '?action=insert_percent', model.toJSON(), 'POST');
	        serverRequest.then(this.fetch.bind(this));
	    },
	    validate: function validate() {
	        var result = {};
	        this.each(function (model) {
	            var res = model.validate();
	            if (res) {
	                _.extend(result, res);
	            }
	        });
	        return result;
	    }
	});
	exports.default = DiscountCollection;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 207 */
/*!**************************************************!*\
  !*** ./src/task/models/PaymentLineCollection.js ***!
  \**************************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_, $) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _OrderableCollection = __webpack_require__(/*! ./OrderableCollection.js */ 133);
	
	var _OrderableCollection2 = _interopRequireDefault(_OrderableCollection);
	
	var _PaymentLineModel = __webpack_require__(/*! ./PaymentLineModel.js */ 183);
	
	var _PaymentLineModel2 = _interopRequireDefault(_PaymentLineModel);
	
	var _backbone = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : PaymentLineCollection.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var PaymentLineCollection = _OrderableCollection2.default.extend({
	    model: _PaymentLineModel2.default,
	    url: function url() {
	        return AppOption['context_url'] + '/' + 'payment_lines';
	    },
	    initialize: function initialize(options) {
	        PaymentLineCollection.__super__.initialize.apply(this, options);
	        this.channel = _backbone2.default.channel('facade');
	        this.totalmodel = this.channel.request('get:totalmodel');
	        this.callChannel = this.callChannel.bind(this);
	        this.bindEvents();
	    },
	    bindEvents: function bindEvents() {
	        this.listenTo(this, 'add', this.callChannel);
	        this.listenTo(this, 'remove', this.callChannel);
	        this.listenTo(this, 'change:amount', this.callChannel);
	    },
	    unBindEvents: function unBindEvents() {
	        console.log("PaymentLineCollection.unBindEvents");
	        this.stopListening();
	    },
	    callChannel: function callChannel() {
	        console.log("Calling channel");
	        this.channel.trigger('changed:payment_lines');
	    },
	    computeDividedAmount: function computeDividedAmount(total, payment_times) {
	        var result = 0;
	        if (payment_times > 1) {
	            result = Math.round(total * 100 / payment_times);
	        }
	        return result / 100;
	    },
	    depositAmount: function depositAmount(deposit) {
	        var total = this.totalmodel.get('ttc');
	        deposit = parseInt(deposit, 10);
	        var deposit_amount = 0;
	        if (deposit > 0) {
	            deposit_amount = (0, _math.getPercent)(total, deposit);
	        }
	        return deposit_amount;
	    },
	    topayAfterDeposit: function topayAfterDeposit(deposit) {
	        var total = this.totalmodel.get('ttc');
	        var deposit_amount = this.depositAmount(deposit);
	        return total - deposit_amount;
	    },
	    genPaymentLines: function genPaymentLines(payment_times, deposit) {
	        console.log("Gen payment lines");
	        this.unBindEvents();
	        var total = this.topayAfterDeposit(deposit);
	
	        var description = 'Livrable';
	        var part = 0;
	        console.log("Total : %s", total);
	        if (payment_times > 1) {
	            part = this.computeDividedAmount(total, payment_times);
	        }
	        console.log(" + Part %s", part);
	
	        var models = this.slice(0, payment_times);
	        var model;
	        var i;
	        for (i = 1; i < payment_times; i++) {
	            if (models.length >= i) {
	                model = models[i - 1];
	            } else {
	                model = new _PaymentLineModel2.default({ order: i - 1 });
	            }
	            model.set({ amount: part, description: description });
	            description = "Paiement " + (i + 1);
	            models[i - 1] = model;
	        }
	        i = payment_times;
	        // Rest is equal to total if payment_times <=1
	        var rest = total - (payment_times - 1) * part;
	        if (models.length >= i) {
	            model = models[i - 1];
	        } else {
	            model = new _PaymentLineModel2.default();
	        }
	        model.set({ amount: rest, description: "Solde" });
	        models[i - 1] = model;
	        var old_models = this.models.slice(payment_times);
	        this.set(models);
	        console.log("New number of models : %s", this.models.length);
	        this.updateModelOrder(false);
	        return this.syncAll(old_models);
	    },
	    syncAll: function syncAll(old_models) {
	        var _$;
	
	        var promises = [];
	        var collection_url = this.url();
	        _.each(old_models, function (model) {
	            // Here the model is not attached to the collection anymore, we
	            // manually set the urlRoot
	            model.urlRoot = collection_url;
	            promises.push(model.destroy({
	                'success': function success() {
	                    console.log("Suppression d'échéances : OK");
	                }
	            }));
	        });
	        this.each(function (model) {
	            promises.push(model.save(null, { 'wait': true, 'sync': true, patch: true }));
	        });
	        var resulting_deferred = (_$ = $).when.apply(_$, promises).then(this.afterSyncAll.bind(this));
	        return resulting_deferred;
	    },
	    afterSyncAll: function afterSyncAll() {
	        console.log("The PaymentLineCollection was synced");
	        this.bindEvents();
	    },
	    getSoldAmount: function getSoldAmount(deposit) {
	        var ttc = this.topayAfterDeposit(deposit);
	        var sum = 0;
	        var models = this.slice(0, this.models.length - 1);
	        _.each(models, function (item) {
	            sum += item.get('amount');
	        });
	        return ttc - sum;
	    },
	    updateSold: function updateSold(deposit) {
	        this.unBindEvents();
	        var value = this.getSoldAmount(deposit);
	        this.models[this.models.length - 1].set({ 'amount': value });
	        this.models[this.models.length - 1].save();
	    },
	
	    validate: function validate() {
	        var result = {};
	        this.each(function (model) {
	            var res = model.validate();
	            if (res) {
	                _.extend(result, res);
	            }
	        });
	        return result;
	    }
	});
	exports.default = PaymentLineCollection;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1), __webpack_require__(/*! jquery */ 2)))

/***/ }),
/* 208 */
/*!****************************************************!*\
  !*** ./src/task/models/StatusHistoryCollection.js ***!
  \****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var StatusHistoryModel = _backbone2.default.Model.extend({}); /*
	                                                               * File Name : StatusHistoryCollection.js
	                                                               *
	                                                               * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                               * Company : Majerti ( http://www.majerti.fr )
	                                                               *
	                                                               * This software is distributed under GPLV3
	                                                               * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                               *
	                                                               */
	
	var StatusHistoryCollection = _backbone2.default.Collection.extend({
	  model: StatusHistoryModel
	});
	exports.default = StatusHistoryCollection;

/***/ }),
/* 209 */
/*!***************************************!*\
  !*** ./src/task/models/TotalModel.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 36);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TotalModel = _backbone2.default.Model.extend({
	    initialize: function initialize() {
	        TotalModel.__super__.initialize.apply(this, arguments);
	        var channel = _backbone4.default.channel('config');
	        this.tva_options = channel.request('get:options', 'tvas');
	    },
	    getTvaLabel: function getTvaLabel(tva_value, tva_key) {
	        var res = {
	            'value': (0, _math.formatAmount)(tva_value, true),
	            'label': 'Tva Inconnue'
	        };
	        _.each(this.tva_options, function (tva) {
	            if (tva.value == tva_key) {
	                res['label'] = tva.name;
	            }
	        });
	        return res;
	    },
	    tva_labels: function tva_labels() {
	        var values = [];
	        var this_ = this;
	        _.each(this.get('tvas'), function (item, key) {
	            values.push(this_.getTvaLabel(item, key));
	        });
	        return values;
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
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ })
]);
//# sourceMappingURL=task.js.map