webpackJsonp([1],[
/* 0 */
/*!********************************!*\
  !*** ./src/expense/expense.js ***!
  \********************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	var _jquery = __webpack_require__(/*! jquery */ 3);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _bootstrap = __webpack_require__(/*! bootstrap */ 11);
	
	var _bootstrap2 = _interopRequireDefault(_bootstrap);
	
	__webpack_require__(/*! jstree */ 23);
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone */ 24);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _App = __webpack_require__(/*! ./components/App.js */ 27);
	
	var _App2 = _interopRequireDefault(_App);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 28);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	var _backboneTools = __webpack_require__(/*! ../backbone-tools.js */ 29);
	
	var _Router = __webpack_require__(/*! ./components/Router.js */ 30);
	
	var _Router2 = _interopRequireDefault(_Router);
	
	var _Controller = __webpack_require__(/*! ./components/Controller.js */ 31);
	
	var _Controller2 = _interopRequireDefault(_Controller);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 4);
	
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
/* 4 */
/*!**********************!*\
  !*** ./src/tools.js ***!
  \**********************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	exports.attachTools = exports.hideLoader = exports.showLoader = exports.setupAjaxCallbacks = exports.serializeForm = exports.getOpt = exports.findCurrentSelected = exports.getDefaultItem = exports.updateSelectOptions = exports.ajax_call = exports.setDatePicker = undefined;
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _jquery = __webpack_require__(/*! jquery */ 3);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _date = __webpack_require__(/*! ./date.js */ 5);
	
	var _math = __webpack_require__(/*! ./math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	__webpack_require__(/*! jquery */ 3);
	
	
	var datepicker = __webpack_require__(/*! jquery-ui/ui/widgets/datepicker */ 7);
	
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
	function openPopup(url, callback) {
	    var screen_width = screen.width;
	    var screen_height = screen.height;
	    var width = (0, _math.getPercent)(screen_width, 60);
	    var height = (0, _math.getPercent)(screen_height, 60);
	    var uniq_id = _underscore2.default.uniqueId('popup');
	    if (_underscore2.default.indexOf(url, '?') != -1) {
	        url = url + "&popup=" + uniq_id;
	    } else {
	        url = url + "?popup=" + uniq_id;
	    }
	
	    var new_win = window.open(url, uniq_id, "width=" + width + ",height=" + height);
	    if (!_underscore2.default.isUndefined(callback)) {
	        window.popupCallbacks[uniq_id] = callback;
	    }
	}
	
	function dismissPopup(win, options) {
	    var callback = window.popupCallbacks[win.name];
	    if (!_underscore2.default.isUndefined(callback)) {
	        callback(options);
	        delete window.popupCallbacks[win.name];
	    } else {
	        var default_options = { refresh: true };
	        _underscore2.default.extend(default_options, options);
	        if (!_underscore2.default.isUndefined(default_options.force_reload)) {
	            window.location.reload();
	        } else {
	            var new_content = "";
	
	            if (!_underscore2.default.isUndefined(default_options.message)) {
	                new_content += "<div class='alert alert-success text-center'>";
	                new_content += default_options.message;
	            } else if (!_underscore2.default.isUndefined(default_options.error)) {
	                new_content += "<div class='alert alert-danger text-center'>";
	                new_content += default_options.error;
	            }
	
	            if (default_options.refresh) {
	                new_content += "&nbsp;<a href='#' onclick='window.location.reload();'><i class='glyphicon glyphicon-refresh'></i> Rafraîchir</a>";
	            }
	
	            new_content += '</div>';
	            var dest_tag = (0, _jquery2.default)('#popupmessage');
	            if (dest_tag.length == 0) {
	                dest_tag = (0, _jquery2.default)('.pagetitle');
	            }
	            dest_tag.after(new_content);
	        }
	    }
	
	    win.close();
	}
	
	var attachTools = exports.attachTools = function attachTools() {
	    window.dismissPopup = dismissPopup;
	    window.openPopup = openPopup;
	    window.popupCallbacks = {};
	};

/***/ }),
/* 5 */
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
/* 6 */
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
/* 7 */
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
				__webpack_require__(/*! jquery */ 3),
				__webpack_require__(/*! ../version */ 8),
				__webpack_require__(/*! ../keycode */ 9)
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
/* 8 */
/*!***********************************!*\
  !*** ./~/jquery-ui/ui/version.js ***!
  \***********************************/
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;( function( factory ) {
		if ( true ) {
	
			// AMD. Register as an anonymous module.
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [ __webpack_require__(/*! jquery */ 3) ], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
		} else {
	
			// Browser globals
			factory( jQuery );
		}
	} ( function( $ ) {
	
	$.ui = $.ui || {};
	
	return $.ui.version = "1.12.1";
	
	} ) );


/***/ }),
/* 9 */
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
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [ __webpack_require__(/*! jquery */ 3), __webpack_require__(/*! ./version */ 8) ], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
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
/* 22 */,
/* 23 */,
/* 24 */,
/* 25 */,
/* 26 */,
/* 27 */
/*!***************************************!*\
  !*** ./src/expense/components/App.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
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
/* 28 */,
/* 29 */
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
/* 30 */
/*!******************************************!*\
  !*** ./src/expense/components/Router.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
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
/* 31 */
/*!**********************************************!*\
  !*** ./src/expense/components/Controller.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _MainView = __webpack_require__(/*! ../views/MainView.js */ 32);
	
	var _MainView2 = _interopRequireDefault(_MainView);
	
	var _App = __webpack_require__(/*! ./App.js */ 27);
	
	var _App2 = _interopRequireDefault(_App);
	
	var _Facade = __webpack_require__(/*! ./Facade.js */ 98);
	
	var _Facade2 = _interopRequireDefault(_Facade);
	
	var _AuthBus = __webpack_require__(/*! ../../base/components/AuthBus.js */ 103);
	
	var _AuthBus2 = _interopRequireDefault(_AuthBus);
	
	var _MessageBus = __webpack_require__(/*! ../../base/components/MessageBus.js */ 104);
	
	var _MessageBus2 = _interopRequireDefault(_MessageBus);
	
	var _ConfigBus = __webpack_require__(/*! ../../base/components/ConfigBus.js */ 105);
	
	var _ConfigBus2 = _interopRequireDefault(_ConfigBus);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var Controller = _backbone2.default.Object.extend({
	    initialize: function initialize(options) {
	        _ConfigBus2.default.setFormConfig(options.form_config);
	        _Facade2.default.loadModels(options.form_datas, options.form_config);
	        AppOption.facade = _Facade2.default;
	        AppOption.config = _ConfigBus2.default;
	        AppOption.messagebus = _MessageBus2.default;
	
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
/* 32 */
/*!***************************************!*\
  !*** ./src/expense/views/MainView.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone */ 24);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _backbone5 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone6 = _interopRequireDefault(_backbone5);
	
	var _RightBarView = __webpack_require__(/*! ./RightBarView.js */ 33);
	
	var _RightBarView2 = _interopRequireDefault(_RightBarView);
	
	var _StatusView = __webpack_require__(/*! ./StatusView.js */ 49);
	
	var _StatusView2 = _interopRequireDefault(_StatusView);
	
	var _BootomActionView = __webpack_require__(/*! ./BootomActionView.js */ 52);
	
	var _BootomActionView2 = _interopRequireDefault(_BootomActionView);
	
	var _ExpenseModel = __webpack_require__(/*! ../models/ExpenseModel.js */ 54);
	
	var _ExpenseModel2 = _interopRequireDefault(_ExpenseModel);
	
	var _ExpenseKmModel = __webpack_require__(/*! ../models/ExpenseKmModel.js */ 56);
	
	var _ExpenseKmModel2 = _interopRequireDefault(_ExpenseKmModel);
	
	var _ExpenseTableView = __webpack_require__(/*! ./ExpenseTableView.js */ 57);
	
	var _ExpenseTableView2 = _interopRequireDefault(_ExpenseTableView);
	
	var _ExpenseKmTableView = __webpack_require__(/*! ./ExpenseKmTableView.js */ 67);
	
	var _ExpenseKmTableView2 = _interopRequireDefault(_ExpenseKmTableView);
	
	var _ExpenseFormPopupView = __webpack_require__(/*! ./ExpenseFormPopupView.js */ 72);
	
	var _ExpenseFormPopupView2 = _interopRequireDefault(_ExpenseFormPopupView);
	
	var _ExpenseKmFormView = __webpack_require__(/*! ./ExpenseKmFormView.js */ 86);
	
	var _ExpenseKmFormView2 = _interopRequireDefault(_ExpenseKmFormView);
	
	var _ExpenseDuplicateFormView = __webpack_require__(/*! ./ExpenseDuplicateFormView.js */ 89);
	
	var _ExpenseDuplicateFormView2 = _interopRequireDefault(_ExpenseDuplicateFormView);
	
	var _TotalView = __webpack_require__(/*! ./TotalView.js */ 91);
	
	var _TotalView2 = _interopRequireDefault(_TotalView);
	
	var _TabTotalView = __webpack_require__(/*! ./TabTotalView.js */ 93);
	
	var _TabTotalView2 = _interopRequireDefault(_TabTotalView);
	
	var _MessageView = __webpack_require__(/*! ../../base/views/MessageView.js */ 95);
	
	var _MessageView2 = _interopRequireDefault(_MessageView);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 29);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var MainView = _backbone2.default.View.extend({
	    className: 'container-fluid page-content',
	    template: __webpack_require__(/*! ./templates/MainView.mustache */ 97),
	    regions: {
	        modalRegion: '.modalRegion',
	        internalLines: '.internal-lines',
	        internalKmLines: '.internal-kmlines',
	        internalTotal: '.internal-total',
	        activityLines: '.activity-lines',
	        activityKmLines: '.activity-kmlines',
	        activityTotal: '.activity-total',
	        totals: '.totals',
	        footer: {
	            el: '.footer-actions',
	            replaceElement: true
	        },
	        rightbar: "#rightbar",
	        messages: {
	            el: '.messages-container',
	            replaceElement: true
	        }
	    },
	    ui: {
	        internal: '#internal-container',
	        activity: '#activity-container'
	    },
	    childViewEvents: {
	        'line:add': 'onLineAdd',
	        'line:edit': 'onLineEdit',
	        'line:delete': 'onLineDelete',
	        'kmline:add': 'onKmLineAdd',
	        'kmline:edit': 'onKmLineEdit',
	        'kmline:delete': 'onLineDelete',
	        'line:duplicate': 'onLineDuplicate',
	        'kmline:duplicate': 'onLineDuplicate',
	        'bookmark:add': 'onBookMarkAdd',
	        'bookmark:delete': 'onBookMarkDelete',
	        "status:change": 'onStatusChange'
	    },
	    initialize: function initialize() {
	        this.facade = _backbone6.default.channel('facade');
	        this.config = _backbone6.default.channel('config');
	        this.categories = this.config.request('get:options', 'categories');
	        this.edit = this.config.request('get:options', 'edit');
	    },
	    onLineAdd: function onLineAdd(childView) {
	        /*
	         * Launch when a line should be added
	         *
	         * :param childView: category 1/2 or a childView with a category option
	         */
	        var category;
	        if (_.isNumber(childView) || _.isString(childView)) {
	            category = childView;
	        } else {
	            category = childView.getOption('category').value;
	        }
	        var model = new _ExpenseModel2.default({ category: category });
	        this.showLineForm(model, true, "Enregistrer une dépense");
	    },
	    onKmLineAdd: function onKmLineAdd(childView) {
	        var category = childView.getOption('category').value;
	        var model = new _ExpenseKmModel2.default({ category: category });
	        this.showKmLineForm(model, true, "Enregistrer une dépense");
	    },
	    onLineEdit: function onLineEdit(childView) {
	        this.showLineForm(childView.model, false, "Modifier une dépense");
	    },
	    onKmLineEdit: function onKmLineEdit(childView) {
	        this.showKmLineForm(childView.model, false, "Modifier une dépense");
	    },
	    showLineForm: function showLineForm(model, add, title) {
	        var view = new _ExpenseFormPopupView2.default({
	            title: title,
	            add: add,
	            model: model,
	            destCollection: this.facade.request('get:collection', 'lines')
	        });
	        this.showChildView('modalRegion', view);
	    },
	    showKmLineForm: function showKmLineForm(model, add, title) {
	        var view = new _ExpenseKmFormView2.default({
	            title: title,
	            add: add,
	            model: model,
	            destCollection: this.facade.request('get:collection', 'kmlines')
	        });
	        this.showChildView('modalRegion', view);
	    },
	    showDuplicateForm: function showDuplicateForm(model) {
	        var view = new _ExpenseDuplicateFormView2.default({ model: model });
	        this.showChildView('modalRegion', view);
	    },
	    onLineDuplicate: function onLineDuplicate(childView) {
	        this.showDuplicateForm(childView.model);
	    },
	
	    onDeleteSuccess: function onDeleteSuccess() {
	        (0, _backboneTools.displayServerSuccess)("Vos données ont bien été supprimées");
	    },
	    onDeleteError: function onDeleteError() {
	        (0, _backboneTools.displayServerError)("Une erreur a été rencontrée lors de la " + "suppression de cet élément");
	    },
	    onLineDelete: function onLineDelete(childView) {
	        var result = window.confirm("Êtes-vous sûr de vouloir supprimer cette dépense ?");
	        if (result) {
	            childView.model.destroy({
	                success: this.onDeleteSuccess,
	                error: this.onDeleteError
	            });
	        }
	    },
	    onBookMarkAdd: function onBookMarkAdd(childView) {
	        var collection = this.facade.request('get:bookmarks');
	        collection.addBookMark(childView.model);
	        childView.highlightBookMark();
	    },
	    onBookMarkDelete: function onBookMarkDelete(childView) {
	        var result = window.confirm("Êtes-vous sûr de vouloir supprimer ce favoris ?");
	        if (result) {
	            childView.model.destroy({
	                success: this.onDeleteSuccess,
	                error: this.onDeleteError
	            });
	        }
	    },
	    showInternalTab: function showInternalTab() {
	        var collection = this.facade.request('get:collection', 'lines');
	        var view = new _ExpenseTableView2.default({
	            collection: collection,
	            category: this.categories[0],
	            edit: this.edit
	        });
	        this.showChildView('internalLines', view);
	
	        var km_type_options = this.config.request('get:options', 'expensekm_types');
	        if (!_.isEmpty(km_type_options)) {
	            collection = this.facade.request('get:collection', 'kmlines');
	            view = new _ExpenseKmTableView2.default({
	                collection: collection,
	                category: this.categories[0],
	                edit: this.edit
	            });
	            this.showChildView('internalKmLines', view);
	        }
	    },
	    showActitityTab: function showActitityTab() {
	        var collection = this.facade.request('get:collection', 'lines');
	        var view = new _ExpenseTableView2.default({
	            collection: collection,
	            category: this.categories[1],
	            edit: this.edit
	        });
	        this.showChildView('activityLines', view);
	
	        var km_type_options = this.config.request('get:options', 'expensekm_types');
	        if (!_.isEmpty(km_type_options)) {
	            collection = this.facade.request('get:collection', 'kmlines');
	            view = new _ExpenseKmTableView2.default({
	                collection: collection,
	                category: this.categories[1],
	                edit: this.edit
	            });
	            this.showChildView('activityKmLines', view);
	        }
	    },
	    showActions: function showActions() {
	        var view = new _RightBarView2.default({
	            actions: this.config.request('get:form_actions')
	        });
	        this.showChildView('rightbar', view);
	
	        view = new _BootomActionView2.default({
	            actions: this.config.request('get:form_actions')
	        });
	        this.showChildView('footer', view);
	    },
	    showMessages: function showMessages() {
	        var model = new _backbone4.default.Model();
	        var view = new _MessageView2.default({ model: model });
	        this.showChildView('messages', view);
	    },
	    showTotals: function showTotals() {
	        var model = this.facade.request('get:totalmodel');
	        var view = new _TotalView2.default({ model: model });
	        this.showChildView('totals', view);
	
	        view = new _TabTotalView2.default({ model: model, category: 1 });
	        this.showChildView('internalTotal', view);
	        view = new _TabTotalView2.default({ model: model, category: 2 });
	        this.showChildView('activityTotal', view);
	    },
	    onRender: function onRender() {
	        this.showInternalTab();
	        this.showActitityTab();
	        this.showTotals();
	        this.showActions();
	        this.showMessages();
	    },
	    onStatusChange: function onStatusChange(status, title, label, url) {
	        var view = new _StatusView2.default({
	            status: status,
	            title: title,
	            label: label,
	            url: url
	        });
	        this.showChildView('modalRegion', view);
	    }
	}); /*
	     * File Name : MainView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = MainView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 33 */
/*!*******************************************!*\
  !*** ./src/expense/views/RightBarView.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _jquery = __webpack_require__(/*! jquery */ 3);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ActionCollection = __webpack_require__(/*! ../models/ActionCollection.js */ 34);
	
	var _ActionCollection2 = _interopRequireDefault(_ActionCollection);
	
	var _ActionListView = __webpack_require__(/*! ./ActionListView.js */ 36);
	
	var _ActionListView2 = _interopRequireDefault(_ActionListView);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
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
	var template = __webpack_require__(/*! ./templates/RightBarView.mustache */ 48);
	
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
	            buttons: this.getOption('actions')['status']
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
/* 34 */
/*!************************************************!*\
  !*** ./src/expense/models/ActionCollection.js ***!
  \************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 24);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ActionModel = __webpack_require__(/*! ./ActionModel.js */ 35);
	
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
/* 35 */
/*!*******************************************!*\
  !*** ./src/expense/models/ActionModel.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 24);
	
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
/* 36 */
/*!*********************************************!*\
  !*** ./src/expense/views/ActionListView.js ***!
  \*********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _AnchorWidget = __webpack_require__(/*! ../../widgets/AnchorWidget.js */ 37);
	
	var _AnchorWidget2 = _interopRequireDefault(_AnchorWidget);
	
	var _ToggleWidget = __webpack_require__(/*! ../../widgets/ToggleWidget.js */ 46);
	
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
/* 37 */
/*!*************************************!*\
  !*** ./src/widgets/AnchorWidget.js ***!
  \*************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 4);
	
	var _math = __webpack_require__(/*! ../math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var AnchorWidget = _backbone2.default.View.extend({
	    tagName: 'div',
	    template: __webpack_require__(/*! ./templates/AnchorWidget.mustache */ 38),
	    ui: {
	        anchor: 'a'
	    },
	    events: {
	        'click @ui.anchor': "onClick"
	    },
	    onClick: function onClick() {
	        var options = this.model.get('option');
	        if (options.popup) {
	            window.openPopup(options.url);
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
/* 38 */
/*!*****************************************************!*\
  !*** ./src/widgets/templates/AnchorWidget.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
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
/* 39 */
/*!*********************************!*\
  !*** ./~/handlebars/runtime.js ***!
  \*********************************/
/***/ (function(module, exports, __webpack_require__) {

	// Create a simple path alias to allow browserify to resolve
	// the runtime on a supported path.
	module.exports = __webpack_require__(/*! ./dist/cjs/handlebars.runtime */ 40);


/***/ }),
/* 40 */
/*!*****************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars.runtime.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	/*globals Handlebars: true */
	var base = __webpack_require__(/*! ./handlebars/base */ 41);
	
	// Each of these augment the Handlebars object. No need to setup here.
	// (This is done to easily share code between commonjs and browse envs)
	var SafeString = __webpack_require__(/*! ./handlebars/safe-string */ 43)["default"];
	var Exception = __webpack_require__(/*! ./handlebars/exception */ 44)["default"];
	var Utils = __webpack_require__(/*! ./handlebars/utils */ 42);
	var runtime = __webpack_require__(/*! ./handlebars/runtime */ 45);
	
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
/* 41 */
/*!**************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/base.js ***!
  \**************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	var Utils = __webpack_require__(/*! ./utils */ 42);
	var Exception = __webpack_require__(/*! ./exception */ 44)["default"];
	
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
/* 42 */
/*!***************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/utils.js ***!
  \***************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	/*jshint -W004 */
	var SafeString = __webpack_require__(/*! ./safe-string */ 43)["default"];
	
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
/* 43 */
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
/* 44 */
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
/* 45 */
/*!*****************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/runtime.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	var Utils = __webpack_require__(/*! ./utils */ 42);
	var Exception = __webpack_require__(/*! ./exception */ 44)["default"];
	var COMPILER_REVISION = __webpack_require__(/*! ./base */ 41).COMPILER_REVISION;
	var REVISION_CHANGES = __webpack_require__(/*! ./base */ 41).REVISION_CHANGES;
	var createFrame = __webpack_require__(/*! ./base */ 41).createFrame;
	
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
/* 46 */
/*!*************************************!*\
  !*** ./src/widgets/ToggleWidget.js ***!
  \*************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function($) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 4);
	
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
	var template = __webpack_require__(/*! ./templates/ToggleWidget.mustache */ 47);
	
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
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 3)))

/***/ }),
/* 47 */
/*!*****************************************************!*\
  !*** ./src/widgets/templates/ToggleWidget.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
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
/* 48 */
/*!***********************************************************!*\
  !*** ./src/expense/views/templates/RightBarView.mustache ***!
  \***********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.buttons : depth0), {"name":"each","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "<hr />\n";
	},"2":function(depth0,helpers,partials,data) {
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
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<div>\n<h3 class='text-center'>Actions</h3>\n<hr />\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.buttons : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "<div class='child-container'></div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 49 */
/*!*****************************************!*\
  !*** ./src/expense/views/StatusView.js ***!
  \*****************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ModalBehavior = __webpack_require__(/*! ../../base/behaviors/ModalBehavior.js */ 50);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 4);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _date = __webpack_require__(/*! ../../date.js */ 5);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/StatusView.mustache */ 51); /*
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
	            url: this.getOption('url')
	        };
	        return result;
	    }
	});
	exports.default = StatusView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 50 */
/*!*********************************************!*\
  !*** ./src/base/behaviors/ModalBehavior.js ***!
  \*********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
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
/* 51 */
/*!*********************************************************!*\
  !*** ./src/expense/views/templates/StatusView.mustache ***!
  \*********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<div class=\"modal-dialog\" role=\"document\">\n	<div class=\"modal-content\">\n	  <form class='form' data-url='"
	    + escapeExpression(((helper = (helper = helpers.url || (depth0 != null ? depth0.url : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"url","hash":{},"data":data}) : helper)))
	    + "' method='POST'>\n          <div class=\"modal-header\">\n            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n            <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n          </div>\n          <div class=\"modal-body\">\n                <div class='form-group'>\n                    <label for='comment'>Commentaires</label>\n                    <textarea class='form-control' name='comment' rows=4></textarea>\n                </div>\n          </div>\n          <div class=\"modal-footer\">\n            <button class='btn btn-success primary-action' type='submit' name='submit' value='"
	    + escapeExpression(((helper = (helper = helpers.status || (depth0 != null ? depth0.status : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"status","hash":{},"data":data}) : helper)))
	    + "'>"
	    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
	    + "</button>\n            <button class='btn btn-default secondary-action' data-dismiss='modal'>Annuler</button>\n          </div>\n	  </form>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n";
	},"useData":true});

/***/ }),
/* 52 */
/*!***********************************************!*\
  !*** ./src/expense/views/BootomActionView.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function($) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var BootomActionView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/BootomActionView.mustache */ 53),
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
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 3)))

/***/ }),
/* 53 */
/*!***************************************************************!*\
  !*** ./src/expense/views/templates/BootomActionView.mustache ***!
  \***************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
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
/* 54 */
/*!********************************************!*\
  !*** ./src/expense/models/ExpenseModel.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _BaseModel = __webpack_require__(/*! ./BaseModel.js */ 55);
	
	var _BaseModel2 = _interopRequireDefault(_BaseModel);
	
	var _date = __webpack_require__(/*! ../../date.js */ 5);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	var _backbone = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseModel.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
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
	      this.set('altdate', (0, _date.formatPaymentDate)(options['date']));
	    }
	    this.config = _backbone2.default.channel('config');
	    this.expensetel_types = this.config.request('get:options', 'expensetel_types');
	    this.expense_types = this.config.request('get:options', 'expense_types');
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
	      var percentage = this.getTypeOption(this.expensetel_types).percentage;
	      result = (0, _math.getPercent)(result, percentage);
	    }
	    return result;
	  },
	  getHT: function getHT() {
	    var result = parseFloat(this.get('ht'));
	    if (this.isSpecial()) {
	      var percentage = this.getTypeOption(this.expensetel_types).percentage;
	      result = (0, _math.getPercent)(result, percentage);
	    }
	    return result;
	  },
	  isSpecial: function isSpecial() {
	    /*
	     * return True if this expense is a special one (related to phone)
	     */
	    return this.getTypeOption(this.expensetel_types) !== undefined;
	  },
	  hasNoType: function hasNoType() {
	    var isnottel = _.isUndefined(this.getTypeOption(this.expensetel_types));
	    var isnotexp = _.isUndefined(this.getTypeOption(this.expense_types));
	    if (isnottel && isnotexp) {
	      return true;
	    } else {
	      return false;
	    }
	  },
	  getTypeOptions: function getTypeOptions() {
	    var arr;
	    if (this.isSpecial()) {
	      arr = this.expensetel_types;
	    } else {
	      arr = this.expense_types;
	    }
	    return arr;
	  },
	  loadBookMark: function loadBookMark(bookmark) {
	    var attributes = _.omit(bookmark.attributes, function (value, key) {
	      if (_.indexOf(['id', 'cid'], key) > -1) {
	        return true;
	      } else if (_.isNull(value) || _.isUndefined(value)) {
	        return true;
	      }
	      return false;
	    });
	    this.set(attributes);
	    this.trigger('set:bookmark');
	  }
	});
	exports.default = ExpenseModel;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 55 */
/*!*****************************************!*\
  !*** ./src/expense/models/BaseModel.js ***!
  \*****************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 24);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 4);
	
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
	    },
	
	    rollback: function rollback() {
	        if (this.get('id') && this.url) {
	            this.fetch();
	        }
	    },
	    onDuplicateError: function onDuplicateError(result) {
	        this.collection.fetch();
	        var channel = _backbone4.default.channel('message');
	        channel.trigger('error:ajax', result);
	    },
	    onDuplicateCallback: function onDuplicateCallback(result) {
	        this.collection.fetch();
	        var channel = _backbone4.default.channel('message');
	        channel.trigger('success:ajax', result);
	    },
	    duplicate: function duplicate(datas) {
	        var request = (0, _tools.ajax_call)(this.url() + '?action=duplicate', datas, 'POST');
	        request.done(this.onDuplicateCallback.bind(this)).fail(this.onDuplicateError.bind(this));
	        return request;
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
/* 56 */
/*!**********************************************!*\
  !*** ./src/expense/models/ExpenseKmModel.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _BaseModel = __webpack_require__(/*! ./BaseModel.js */ 55);
	
	var _BaseModel2 = _interopRequireDefault(_BaseModel);
	
	var _date = __webpack_require__(/*! ../../date.js */ 5);
	
	var _backbone = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseKmModel = _BaseModel2.default.extend({
	    defaults: {
	        type: 'km',
	        category: null,
	        start: "",
	        end: "",
	        description: ""
	    },
	    initialize: function initialize(options) {
	        if (options['altdate'] === undefined && options['date'] !== undefined) {
	            this.set('altdate', (0, _date.formatPaymentDate)(options['date']));
	        }
	        this.config = _backbone2.default.channel('config');
	        this.expensekm_types = this.config.request('get:options', 'expensekm_types');
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
	        var type_id = parseInt(this.get('type_id'), 10);
	
	        var elem = _.findWhere(this.expensekm_types, { value: type_id });
	        if (elem === undefined) {
	            return 0;
	        }
	        return parseFloat(elem.amount);
	    },
	    getHT: function getHT() {
	        return this.total();
	    },
	    getTva: function getTva() {
	        return 0;
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
	        return this.expensekm_types;
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
/* 57 */
/*!***********************************************!*\
  !*** ./src/expense/views/ExpenseTableView.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ExpenseCollectionView = __webpack_require__(/*! ./ExpenseCollectionView.js */ 58);
	
	var _ExpenseCollectionView2 = _interopRequireDefault(_ExpenseCollectionView);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseTableView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ExpenseTableView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/ExpenseTableView.mustache */ 66),
	    regions: {
	        lines: {
	            el: 'tbody',
	            replaceElement: true
	        }
	    },
	    ui: {
	        add_btn: 'button.add',
	        total_ht: '.total_ht',
	        total_tva: '.total_tva',
	        total_ttc: '.total_ttc'
	    },
	    triggers: {
	        'click @ui.add_btn': 'line:add'
	    },
	    childViewTriggers: {
	        'line:edit': 'line:edit',
	        'line:delete': 'line:delete',
	        'line:duplicate': 'line:duplicate',
	        'bookmark:add': 'bookmark:add'
	    },
	    collectionEvents: {
	        'change:category': 'render'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('facade');
	        this.totalmodel = channel.request('get:totalmodel');
	
	        this.categoryName = this.getOption('category').value;
	        this.listenTo(channel, 'change:lines_' + this.categoryName, this.showTotals.bind(this));
	    },
	    showTotals: function showTotals() {
	        this.getUI("total_ht").html((0, _math.formatAmount)(this.totalmodel.get('ht_' + this.categoryName)));
	        this.getUI("total_tva").html((0, _math.formatAmount)(this.totalmodel.get('tva_' + this.categoryName)));
	        this.getUI("total_ttc").html((0, _math.formatAmount)(this.totalmodel.get('ttc_' + this.categoryName)));
	    },
	    templateContext: function templateContext() {
	        return {
	            category: this.getOption('category'),
	            edit: this.getOption('edit')
	        };
	    },
	    onRender: function onRender() {
	        var view = new _ExpenseCollectionView2.default({
	            collection: this.collection,
	            category: this.getOption('category'),
	            edit: this.getOption('edit')
	        });
	        this.showChildView('lines', view);
	    },
	    onAttach: function onAttach() {
	        this.showTotals();
	    }
	});
	exports.default = ExpenseTableView;

/***/ }),
/* 58 */
/*!****************************************************!*\
  !*** ./src/expense/views/ExpenseCollectionView.js ***!
  \****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ExpenseView = __webpack_require__(/*! ./ExpenseView.js */ 59);
	
	var _ExpenseView2 = _interopRequireDefault(_ExpenseView);
	
	var _ExpenseEmptyView = __webpack_require__(/*! ./ExpenseEmptyView.js */ 64);
	
	var _ExpenseEmptyView2 = _interopRequireDefault(_ExpenseEmptyView);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseCollectionView = _backbone2.default.CollectionView.extend({
	    tagName: 'tbody',
	    // Bubble up child view events
	    childViewTriggers: {
	        'edit': 'line:edit',
	        'delete': 'line:delete',
	        'bookmark': 'bookmark:add',
	        'duplicate': 'line:duplicate'
	    },
	    childView: _ExpenseView2.default,
	    emptyView: _ExpenseEmptyView2.default,
	    emptyViewOptions: function emptyViewOptions() {
	        return {
	            colspan: 6,
	            edit: this.getOption('edit')
	        };
	    },
	    childViewOptions: function childViewOptions() {
	        return { edit: this.getOption('edit') };
	    },
	    filter: function filter(child, index, collection) {
	        if (child.get('category') == this.getOption('category').value) {
	            return true;
	        } else {
	            return false;
	        }
	    }
	}); /*
	     * File Name : ExpenseCollectionView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseCollectionView;

/***/ }),
/* 59 */
/*!******************************************!*\
  !*** ./src/expense/views/ExpenseView.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var tel_template = __webpack_require__(/*! ./templates/ExpenseTelView.mustache */ 60);
	var template = __webpack_require__(/*! ./templates/ExpenseView.mustache */ 61);
	
	__webpack_require__(/*! jquery-ui/ui/effects/effect-highlight */ 62);
	
	var ExpenseView = _backbone2.default.View.extend({
	    tagName: 'tr',
	    ui: {
	        edit: 'button.edit',
	        delete: 'button.delete',
	        duplicate: 'button.duplicate',
	        bookmark: 'button.bookmark'
	    },
	    triggers: {
	        'click @ui.edit': 'edit',
	        'click @ui.delete': 'delete',
	        'click @ui.duplicate': 'duplicate',
	        'click @ui.bookmark': 'bookmark'
	    },
	    modelEvents: {
	        'change': 'render'
	    },
	    getTemplate: function getTemplate() {
	        if (this.model.isSpecial()) {
	            return tel_template;
	        } else {
	            return template;
	        }
	    },
	    highlightBookMark: function highlightBookMark() {
	        console.log("Highlight bookmark");
	        this.getUI('bookmark').effect("highlight", { color: "#ceff99" }, "slow");
	    },
	    templateContext: function templateContext() {
	        var total = this.model.total();
	        var typelabel = this.model.getTypeLabel();
	
	        return {
	            edit: this.getOption('edit'),
	            typelabel: typelabel,
	            total: (0, _math.formatAmount)(total),
	            ht_label: (0, _math.formatAmount)(this.model.get('ht')),
	            tva_label: (0, _math.formatAmount)(this.model.get('tva'))
	        };
	    }
	});
	exports.default = ExpenseView;

/***/ }),
/* 60 */
/*!*************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseTelView.mustache ***!
  \*************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "<td class='hidden-print'>\n<button class='btn btn-default edit'><i class='glyphicon glyphicon-pencil'></i>&nbsp;Modifier</button>\n<button class='btn btn-default delete'><i class='glyphicon glyphicon-remove-sign'></i>&nbsp;Supprimer</button>\n<button class='btn btn-default duplicate'><i class='fa fa-copy'></i>&nbsp;Dupliquer</button>\n<button class='btn btn-default bookmark'><i class='glyphicon glyphicon-star-empty'></i></button>\n</td>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<td>";
	  stack1 = ((helper = (helper = helpers.altdate || (depth0 != null ? depth0.altdate : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"altdate","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</td>\n<td colspan='2'>"
	    + escapeExpression(((helper = (helper = helpers.typelabel || (depth0 != null ? depth0.typelabel : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"typelabel","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>"
	    + escapeExpression(((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>"
	    + escapeExpression(((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>";
	  stack1 = ((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</td>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 61 */
/*!**********************************************************!*\
  !*** ./src/expense/views/templates/ExpenseView.mustache ***!
  \**********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "<td class='hidden-print'>\n<button class='btn btn-default edit'><i class='glyphicon glyphicon-pencil'></i>&nbsp;Modifier</button>\n<button class='btn btn-default delete'><i class='glyphicon glyphicon-remove-sign'></i>&nbsp;Supprimer</button>\n<button class='btn btn-default duplicate'><i class='fa fa-copy'></i>&nbsp;Dupliquer</button>\n<button class='btn btn-default bookmark'><i class='glyphicon glyphicon-star-empty'></i></button>\n</td>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<td>";
	  stack1 = ((helper = (helper = helpers.altdate || (depth0 != null ? depth0.altdate : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"altdate","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</td>\n<td>"
	    + escapeExpression(((helper = (helper = helpers.typelabel || (depth0 != null ? depth0.typelabel : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"typelabel","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>"
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>";
	  stack1 = ((helper = (helper = helpers.ht_label || (depth0 != null ? depth0.ht_label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht_label","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</td>\n<td>";
	  stack1 = ((helper = (helper = helpers.tva_label || (depth0 != null ? depth0.tva_label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva_label","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</td>\n<td>";
	  stack1 = ((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</td>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 62 */
/*!****************************************************!*\
  !*** ./~/jquery-ui/ui/effects/effect-highlight.js ***!
  \****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!
	 * jQuery UI Effects Highlight 1.12.1
	 * http://jqueryui.com
	 *
	 * Copyright jQuery Foundation and other contributors
	 * Released under the MIT license.
	 * http://jquery.org/license
	 */
	
	//>>label: Highlight Effect
	//>>group: Effects
	//>>description: Highlights the background of an element in a defined color for a custom duration.
	//>>docs: http://api.jqueryui.com/highlight-effect/
	//>>demos: http://jqueryui.com/effect/
	
	( function( factory ) {
		if ( true ) {
	
			// AMD. Register as an anonymous module.
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [
				__webpack_require__(/*! jquery */ 3),
				__webpack_require__(/*! ../version */ 8),
				__webpack_require__(/*! ../effect */ 63)
			], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
		} else {
	
			// Browser globals
			factory( jQuery );
		}
	}( function( $ ) {
	
	return $.effects.define( "highlight", "show", function( options, done ) {
		var element = $( this ),
			animation = {
				backgroundColor: element.css( "backgroundColor" )
			};
	
		if ( options.mode === "hide" ) {
			animation.opacity = 0;
		}
	
		$.effects.saveStyle( element );
	
		element
			.css( {
				backgroundImage: "none",
				backgroundColor: options.color || "#ffff99"
			} )
			.animate( animation, {
				queue: false,
				duration: options.duration,
				easing: options.easing,
				complete: done
			} );
	} );
	
	} ) );


/***/ }),
/* 63 */
/*!**********************************!*\
  !*** ./~/jquery-ui/ui/effect.js ***!
  \**********************************/
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;/*!
	 * jQuery UI Effects 1.12.1
	 * http://jqueryui.com
	 *
	 * Copyright jQuery Foundation and other contributors
	 * Released under the MIT license.
	 * http://jquery.org/license
	 */
	
	//>>label: Effects Core
	//>>group: Effects
	// jscs:disable maximumLineLength
	//>>description: Extends the internal jQuery effects. Includes morphing and easing. Required by all other effects.
	// jscs:enable maximumLineLength
	//>>docs: http://api.jqueryui.com/category/effects-core/
	//>>demos: http://jqueryui.com/effect/
	
	( function( factory ) {
		if ( true ) {
	
			// AMD. Register as an anonymous module.
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [ __webpack_require__(/*! jquery */ 3), __webpack_require__(/*! ./version */ 8) ], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
		} else {
	
			// Browser globals
			factory( jQuery );
		}
	}( function( $ ) {
	
	var dataSpace = "ui-effects-",
		dataSpaceStyle = "ui-effects-style",
		dataSpaceAnimated = "ui-effects-animated",
	
		// Create a local jQuery because jQuery Color relies on it and the
		// global may not exist with AMD and a custom build (#10199)
		jQuery = $;
	
	$.effects = {
		effect: {}
	};
	
	/*!
	 * jQuery Color Animations v2.1.2
	 * https://github.com/jquery/jquery-color
	 *
	 * Copyright 2014 jQuery Foundation and other contributors
	 * Released under the MIT license.
	 * http://jquery.org/license
	 *
	 * Date: Wed Jan 16 08:47:09 2013 -0600
	 */
	( function( jQuery, undefined ) {
	
		var stepHooks = "backgroundColor borderBottomColor borderLeftColor borderRightColor " +
			"borderTopColor color columnRuleColor outlineColor textDecorationColor textEmphasisColor",
	
		// Plusequals test for += 100 -= 100
		rplusequals = /^([\-+])=\s*(\d+\.?\d*)/,
	
		// A set of RE's that can match strings and generate color tuples.
		stringParsers = [ {
				re: /rgba?\(\s*(\d{1,3})\s*,\s*(\d{1,3})\s*,\s*(\d{1,3})\s*(?:,\s*(\d?(?:\.\d+)?)\s*)?\)/,
				parse: function( execResult ) {
					return [
						execResult[ 1 ],
						execResult[ 2 ],
						execResult[ 3 ],
						execResult[ 4 ]
					];
				}
			}, {
				re: /rgba?\(\s*(\d+(?:\.\d+)?)\%\s*,\s*(\d+(?:\.\d+)?)\%\s*,\s*(\d+(?:\.\d+)?)\%\s*(?:,\s*(\d?(?:\.\d+)?)\s*)?\)/,
				parse: function( execResult ) {
					return [
						execResult[ 1 ] * 2.55,
						execResult[ 2 ] * 2.55,
						execResult[ 3 ] * 2.55,
						execResult[ 4 ]
					];
				}
			}, {
	
				// This regex ignores A-F because it's compared against an already lowercased string
				re: /#([a-f0-9]{2})([a-f0-9]{2})([a-f0-9]{2})/,
				parse: function( execResult ) {
					return [
						parseInt( execResult[ 1 ], 16 ),
						parseInt( execResult[ 2 ], 16 ),
						parseInt( execResult[ 3 ], 16 )
					];
				}
			}, {
	
				// This regex ignores A-F because it's compared against an already lowercased string
				re: /#([a-f0-9])([a-f0-9])([a-f0-9])/,
				parse: function( execResult ) {
					return [
						parseInt( execResult[ 1 ] + execResult[ 1 ], 16 ),
						parseInt( execResult[ 2 ] + execResult[ 2 ], 16 ),
						parseInt( execResult[ 3 ] + execResult[ 3 ], 16 )
					];
				}
			}, {
				re: /hsla?\(\s*(\d+(?:\.\d+)?)\s*,\s*(\d+(?:\.\d+)?)\%\s*,\s*(\d+(?:\.\d+)?)\%\s*(?:,\s*(\d?(?:\.\d+)?)\s*)?\)/,
				space: "hsla",
				parse: function( execResult ) {
					return [
						execResult[ 1 ],
						execResult[ 2 ] / 100,
						execResult[ 3 ] / 100,
						execResult[ 4 ]
					];
				}
			} ],
	
		// JQuery.Color( )
		color = jQuery.Color = function( color, green, blue, alpha ) {
			return new jQuery.Color.fn.parse( color, green, blue, alpha );
		},
		spaces = {
			rgba: {
				props: {
					red: {
						idx: 0,
						type: "byte"
					},
					green: {
						idx: 1,
						type: "byte"
					},
					blue: {
						idx: 2,
						type: "byte"
					}
				}
			},
	
			hsla: {
				props: {
					hue: {
						idx: 0,
						type: "degrees"
					},
					saturation: {
						idx: 1,
						type: "percent"
					},
					lightness: {
						idx: 2,
						type: "percent"
					}
				}
			}
		},
		propTypes = {
			"byte": {
				floor: true,
				max: 255
			},
			"percent": {
				max: 1
			},
			"degrees": {
				mod: 360,
				floor: true
			}
		},
		support = color.support = {},
	
		// Element for support tests
		supportElem = jQuery( "<p>" )[ 0 ],
	
		// Colors = jQuery.Color.names
		colors,
	
		// Local aliases of functions called often
		each = jQuery.each;
	
	// Determine rgba support immediately
	supportElem.style.cssText = "background-color:rgba(1,1,1,.5)";
	support.rgba = supportElem.style.backgroundColor.indexOf( "rgba" ) > -1;
	
	// Define cache name and alpha properties
	// for rgba and hsla spaces
	each( spaces, function( spaceName, space ) {
		space.cache = "_" + spaceName;
		space.props.alpha = {
			idx: 3,
			type: "percent",
			def: 1
		};
	} );
	
	function clamp( value, prop, allowEmpty ) {
		var type = propTypes[ prop.type ] || {};
	
		if ( value == null ) {
			return ( allowEmpty || !prop.def ) ? null : prop.def;
		}
	
		// ~~ is an short way of doing floor for positive numbers
		value = type.floor ? ~~value : parseFloat( value );
	
		// IE will pass in empty strings as value for alpha,
		// which will hit this case
		if ( isNaN( value ) ) {
			return prop.def;
		}
	
		if ( type.mod ) {
	
			// We add mod before modding to make sure that negatives values
			// get converted properly: -10 -> 350
			return ( value + type.mod ) % type.mod;
		}
	
		// For now all property types without mod have min and max
		return 0 > value ? 0 : type.max < value ? type.max : value;
	}
	
	function stringParse( string ) {
		var inst = color(),
			rgba = inst._rgba = [];
	
		string = string.toLowerCase();
	
		each( stringParsers, function( i, parser ) {
			var parsed,
				match = parser.re.exec( string ),
				values = match && parser.parse( match ),
				spaceName = parser.space || "rgba";
	
			if ( values ) {
				parsed = inst[ spaceName ]( values );
	
				// If this was an rgba parse the assignment might happen twice
				// oh well....
				inst[ spaces[ spaceName ].cache ] = parsed[ spaces[ spaceName ].cache ];
				rgba = inst._rgba = parsed._rgba;
	
				// Exit each( stringParsers ) here because we matched
				return false;
			}
		} );
	
		// Found a stringParser that handled it
		if ( rgba.length ) {
	
			// If this came from a parsed string, force "transparent" when alpha is 0
			// chrome, (and maybe others) return "transparent" as rgba(0,0,0,0)
			if ( rgba.join() === "0,0,0,0" ) {
				jQuery.extend( rgba, colors.transparent );
			}
			return inst;
		}
	
		// Named colors
		return colors[ string ];
	}
	
	color.fn = jQuery.extend( color.prototype, {
		parse: function( red, green, blue, alpha ) {
			if ( red === undefined ) {
				this._rgba = [ null, null, null, null ];
				return this;
			}
			if ( red.jquery || red.nodeType ) {
				red = jQuery( red ).css( green );
				green = undefined;
			}
	
			var inst = this,
				type = jQuery.type( red ),
				rgba = this._rgba = [];
	
			// More than 1 argument specified - assume ( red, green, blue, alpha )
			if ( green !== undefined ) {
				red = [ red, green, blue, alpha ];
				type = "array";
			}
	
			if ( type === "string" ) {
				return this.parse( stringParse( red ) || colors._default );
			}
	
			if ( type === "array" ) {
				each( spaces.rgba.props, function( key, prop ) {
					rgba[ prop.idx ] = clamp( red[ prop.idx ], prop );
				} );
				return this;
			}
	
			if ( type === "object" ) {
				if ( red instanceof color ) {
					each( spaces, function( spaceName, space ) {
						if ( red[ space.cache ] ) {
							inst[ space.cache ] = red[ space.cache ].slice();
						}
					} );
				} else {
					each( spaces, function( spaceName, space ) {
						var cache = space.cache;
						each( space.props, function( key, prop ) {
	
							// If the cache doesn't exist, and we know how to convert
							if ( !inst[ cache ] && space.to ) {
	
								// If the value was null, we don't need to copy it
								// if the key was alpha, we don't need to copy it either
								if ( key === "alpha" || red[ key ] == null ) {
									return;
								}
								inst[ cache ] = space.to( inst._rgba );
							}
	
							// This is the only case where we allow nulls for ALL properties.
							// call clamp with alwaysAllowEmpty
							inst[ cache ][ prop.idx ] = clamp( red[ key ], prop, true );
						} );
	
						// Everything defined but alpha?
						if ( inst[ cache ] &&
								jQuery.inArray( null, inst[ cache ].slice( 0, 3 ) ) < 0 ) {
	
							// Use the default of 1
							inst[ cache ][ 3 ] = 1;
							if ( space.from ) {
								inst._rgba = space.from( inst[ cache ] );
							}
						}
					} );
				}
				return this;
			}
		},
		is: function( compare ) {
			var is = color( compare ),
				same = true,
				inst = this;
	
			each( spaces, function( _, space ) {
				var localCache,
					isCache = is[ space.cache ];
				if ( isCache ) {
					localCache = inst[ space.cache ] || space.to && space.to( inst._rgba ) || [];
					each( space.props, function( _, prop ) {
						if ( isCache[ prop.idx ] != null ) {
							same = ( isCache[ prop.idx ] === localCache[ prop.idx ] );
							return same;
						}
					} );
				}
				return same;
			} );
			return same;
		},
		_space: function() {
			var used = [],
				inst = this;
			each( spaces, function( spaceName, space ) {
				if ( inst[ space.cache ] ) {
					used.push( spaceName );
				}
			} );
			return used.pop();
		},
		transition: function( other, distance ) {
			var end = color( other ),
				spaceName = end._space(),
				space = spaces[ spaceName ],
				startColor = this.alpha() === 0 ? color( "transparent" ) : this,
				start = startColor[ space.cache ] || space.to( startColor._rgba ),
				result = start.slice();
	
			end = end[ space.cache ];
			each( space.props, function( key, prop ) {
				var index = prop.idx,
					startValue = start[ index ],
					endValue = end[ index ],
					type = propTypes[ prop.type ] || {};
	
				// If null, don't override start value
				if ( endValue === null ) {
					return;
				}
	
				// If null - use end
				if ( startValue === null ) {
					result[ index ] = endValue;
				} else {
					if ( type.mod ) {
						if ( endValue - startValue > type.mod / 2 ) {
							startValue += type.mod;
						} else if ( startValue - endValue > type.mod / 2 ) {
							startValue -= type.mod;
						}
					}
					result[ index ] = clamp( ( endValue - startValue ) * distance + startValue, prop );
				}
			} );
			return this[ spaceName ]( result );
		},
		blend: function( opaque ) {
	
			// If we are already opaque - return ourself
			if ( this._rgba[ 3 ] === 1 ) {
				return this;
			}
	
			var rgb = this._rgba.slice(),
				a = rgb.pop(),
				blend = color( opaque )._rgba;
	
			return color( jQuery.map( rgb, function( v, i ) {
				return ( 1 - a ) * blend[ i ] + a * v;
			} ) );
		},
		toRgbaString: function() {
			var prefix = "rgba(",
				rgba = jQuery.map( this._rgba, function( v, i ) {
					return v == null ? ( i > 2 ? 1 : 0 ) : v;
				} );
	
			if ( rgba[ 3 ] === 1 ) {
				rgba.pop();
				prefix = "rgb(";
			}
	
			return prefix + rgba.join() + ")";
		},
		toHslaString: function() {
			var prefix = "hsla(",
				hsla = jQuery.map( this.hsla(), function( v, i ) {
					if ( v == null ) {
						v = i > 2 ? 1 : 0;
					}
	
					// Catch 1 and 2
					if ( i && i < 3 ) {
						v = Math.round( v * 100 ) + "%";
					}
					return v;
				} );
	
			if ( hsla[ 3 ] === 1 ) {
				hsla.pop();
				prefix = "hsl(";
			}
			return prefix + hsla.join() + ")";
		},
		toHexString: function( includeAlpha ) {
			var rgba = this._rgba.slice(),
				alpha = rgba.pop();
	
			if ( includeAlpha ) {
				rgba.push( ~~( alpha * 255 ) );
			}
	
			return "#" + jQuery.map( rgba, function( v ) {
	
				// Default to 0 when nulls exist
				v = ( v || 0 ).toString( 16 );
				return v.length === 1 ? "0" + v : v;
			} ).join( "" );
		},
		toString: function() {
			return this._rgba[ 3 ] === 0 ? "transparent" : this.toRgbaString();
		}
	} );
	color.fn.parse.prototype = color.fn;
	
	// Hsla conversions adapted from:
	// https://code.google.com/p/maashaack/source/browse/packages/graphics/trunk/src/graphics/colors/HUE2RGB.as?r=5021
	
	function hue2rgb( p, q, h ) {
		h = ( h + 1 ) % 1;
		if ( h * 6 < 1 ) {
			return p + ( q - p ) * h * 6;
		}
		if ( h * 2 < 1 ) {
			return q;
		}
		if ( h * 3 < 2 ) {
			return p + ( q - p ) * ( ( 2 / 3 ) - h ) * 6;
		}
		return p;
	}
	
	spaces.hsla.to = function( rgba ) {
		if ( rgba[ 0 ] == null || rgba[ 1 ] == null || rgba[ 2 ] == null ) {
			return [ null, null, null, rgba[ 3 ] ];
		}
		var r = rgba[ 0 ] / 255,
			g = rgba[ 1 ] / 255,
			b = rgba[ 2 ] / 255,
			a = rgba[ 3 ],
			max = Math.max( r, g, b ),
			min = Math.min( r, g, b ),
			diff = max - min,
			add = max + min,
			l = add * 0.5,
			h, s;
	
		if ( min === max ) {
			h = 0;
		} else if ( r === max ) {
			h = ( 60 * ( g - b ) / diff ) + 360;
		} else if ( g === max ) {
			h = ( 60 * ( b - r ) / diff ) + 120;
		} else {
			h = ( 60 * ( r - g ) / diff ) + 240;
		}
	
		// Chroma (diff) == 0 means greyscale which, by definition, saturation = 0%
		// otherwise, saturation is based on the ratio of chroma (diff) to lightness (add)
		if ( diff === 0 ) {
			s = 0;
		} else if ( l <= 0.5 ) {
			s = diff / add;
		} else {
			s = diff / ( 2 - add );
		}
		return [ Math.round( h ) % 360, s, l, a == null ? 1 : a ];
	};
	
	spaces.hsla.from = function( hsla ) {
		if ( hsla[ 0 ] == null || hsla[ 1 ] == null || hsla[ 2 ] == null ) {
			return [ null, null, null, hsla[ 3 ] ];
		}
		var h = hsla[ 0 ] / 360,
			s = hsla[ 1 ],
			l = hsla[ 2 ],
			a = hsla[ 3 ],
			q = l <= 0.5 ? l * ( 1 + s ) : l + s - l * s,
			p = 2 * l - q;
	
		return [
			Math.round( hue2rgb( p, q, h + ( 1 / 3 ) ) * 255 ),
			Math.round( hue2rgb( p, q, h ) * 255 ),
			Math.round( hue2rgb( p, q, h - ( 1 / 3 ) ) * 255 ),
			a
		];
	};
	
	each( spaces, function( spaceName, space ) {
		var props = space.props,
			cache = space.cache,
			to = space.to,
			from = space.from;
	
		// Makes rgba() and hsla()
		color.fn[ spaceName ] = function( value ) {
	
			// Generate a cache for this space if it doesn't exist
			if ( to && !this[ cache ] ) {
				this[ cache ] = to( this._rgba );
			}
			if ( value === undefined ) {
				return this[ cache ].slice();
			}
	
			var ret,
				type = jQuery.type( value ),
				arr = ( type === "array" || type === "object" ) ? value : arguments,
				local = this[ cache ].slice();
	
			each( props, function( key, prop ) {
				var val = arr[ type === "object" ? key : prop.idx ];
				if ( val == null ) {
					val = local[ prop.idx ];
				}
				local[ prop.idx ] = clamp( val, prop );
			} );
	
			if ( from ) {
				ret = color( from( local ) );
				ret[ cache ] = local;
				return ret;
			} else {
				return color( local );
			}
		};
	
		// Makes red() green() blue() alpha() hue() saturation() lightness()
		each( props, function( key, prop ) {
	
			// Alpha is included in more than one space
			if ( color.fn[ key ] ) {
				return;
			}
			color.fn[ key ] = function( value ) {
				var vtype = jQuery.type( value ),
					fn = ( key === "alpha" ? ( this._hsla ? "hsla" : "rgba" ) : spaceName ),
					local = this[ fn ](),
					cur = local[ prop.idx ],
					match;
	
				if ( vtype === "undefined" ) {
					return cur;
				}
	
				if ( vtype === "function" ) {
					value = value.call( this, cur );
					vtype = jQuery.type( value );
				}
				if ( value == null && prop.empty ) {
					return this;
				}
				if ( vtype === "string" ) {
					match = rplusequals.exec( value );
					if ( match ) {
						value = cur + parseFloat( match[ 2 ] ) * ( match[ 1 ] === "+" ? 1 : -1 );
					}
				}
				local[ prop.idx ] = value;
				return this[ fn ]( local );
			};
		} );
	} );
	
	// Add cssHook and .fx.step function for each named hook.
	// accept a space separated string of properties
	color.hook = function( hook ) {
		var hooks = hook.split( " " );
		each( hooks, function( i, hook ) {
			jQuery.cssHooks[ hook ] = {
				set: function( elem, value ) {
					var parsed, curElem,
						backgroundColor = "";
	
					if ( value !== "transparent" && ( jQuery.type( value ) !== "string" ||
							( parsed = stringParse( value ) ) ) ) {
						value = color( parsed || value );
						if ( !support.rgba && value._rgba[ 3 ] !== 1 ) {
							curElem = hook === "backgroundColor" ? elem.parentNode : elem;
							while (
								( backgroundColor === "" || backgroundColor === "transparent" ) &&
								curElem && curElem.style
							) {
								try {
									backgroundColor = jQuery.css( curElem, "backgroundColor" );
									curElem = curElem.parentNode;
								} catch ( e ) {
								}
							}
	
							value = value.blend( backgroundColor && backgroundColor !== "transparent" ?
								backgroundColor :
								"_default" );
						}
	
						value = value.toRgbaString();
					}
					try {
						elem.style[ hook ] = value;
					} catch ( e ) {
	
						// Wrapped to prevent IE from throwing errors on "invalid" values like
						// 'auto' or 'inherit'
					}
				}
			};
			jQuery.fx.step[ hook ] = function( fx ) {
				if ( !fx.colorInit ) {
					fx.start = color( fx.elem, hook );
					fx.end = color( fx.end );
					fx.colorInit = true;
				}
				jQuery.cssHooks[ hook ].set( fx.elem, fx.start.transition( fx.end, fx.pos ) );
			};
		} );
	
	};
	
	color.hook( stepHooks );
	
	jQuery.cssHooks.borderColor = {
		expand: function( value ) {
			var expanded = {};
	
			each( [ "Top", "Right", "Bottom", "Left" ], function( i, part ) {
				expanded[ "border" + part + "Color" ] = value;
			} );
			return expanded;
		}
	};
	
	// Basic color names only.
	// Usage of any of the other color names requires adding yourself or including
	// jquery.color.svg-names.js.
	colors = jQuery.Color.names = {
	
		// 4.1. Basic color keywords
		aqua: "#00ffff",
		black: "#000000",
		blue: "#0000ff",
		fuchsia: "#ff00ff",
		gray: "#808080",
		green: "#008000",
		lime: "#00ff00",
		maroon: "#800000",
		navy: "#000080",
		olive: "#808000",
		purple: "#800080",
		red: "#ff0000",
		silver: "#c0c0c0",
		teal: "#008080",
		white: "#ffffff",
		yellow: "#ffff00",
	
		// 4.2.3. "transparent" color keyword
		transparent: [ null, null, null, 0 ],
	
		_default: "#ffffff"
	};
	
	} )( jQuery );
	
	/******************************************************************************/
	/****************************** CLASS ANIMATIONS ******************************/
	/******************************************************************************/
	( function() {
	
	var classAnimationActions = [ "add", "remove", "toggle" ],
		shorthandStyles = {
			border: 1,
			borderBottom: 1,
			borderColor: 1,
			borderLeft: 1,
			borderRight: 1,
			borderTop: 1,
			borderWidth: 1,
			margin: 1,
			padding: 1
		};
	
	$.each(
		[ "borderLeftStyle", "borderRightStyle", "borderBottomStyle", "borderTopStyle" ],
		function( _, prop ) {
			$.fx.step[ prop ] = function( fx ) {
				if ( fx.end !== "none" && !fx.setAttr || fx.pos === 1 && !fx.setAttr ) {
					jQuery.style( fx.elem, prop, fx.end );
					fx.setAttr = true;
				}
			};
		}
	);
	
	function getElementStyles( elem ) {
		var key, len,
			style = elem.ownerDocument.defaultView ?
				elem.ownerDocument.defaultView.getComputedStyle( elem, null ) :
				elem.currentStyle,
			styles = {};
	
		if ( style && style.length && style[ 0 ] && style[ style[ 0 ] ] ) {
			len = style.length;
			while ( len-- ) {
				key = style[ len ];
				if ( typeof style[ key ] === "string" ) {
					styles[ $.camelCase( key ) ] = style[ key ];
				}
			}
	
		// Support: Opera, IE <9
		} else {
			for ( key in style ) {
				if ( typeof style[ key ] === "string" ) {
					styles[ key ] = style[ key ];
				}
			}
		}
	
		return styles;
	}
	
	function styleDifference( oldStyle, newStyle ) {
		var diff = {},
			name, value;
	
		for ( name in newStyle ) {
			value = newStyle[ name ];
			if ( oldStyle[ name ] !== value ) {
				if ( !shorthandStyles[ name ] ) {
					if ( $.fx.step[ name ] || !isNaN( parseFloat( value ) ) ) {
						diff[ name ] = value;
					}
				}
			}
		}
	
		return diff;
	}
	
	// Support: jQuery <1.8
	if ( !$.fn.addBack ) {
		$.fn.addBack = function( selector ) {
			return this.add( selector == null ?
				this.prevObject : this.prevObject.filter( selector )
			);
		};
	}
	
	$.effects.animateClass = function( value, duration, easing, callback ) {
		var o = $.speed( duration, easing, callback );
	
		return this.queue( function() {
			var animated = $( this ),
				baseClass = animated.attr( "class" ) || "",
				applyClassChange,
				allAnimations = o.children ? animated.find( "*" ).addBack() : animated;
	
			// Map the animated objects to store the original styles.
			allAnimations = allAnimations.map( function() {
				var el = $( this );
				return {
					el: el,
					start: getElementStyles( this )
				};
			} );
	
			// Apply class change
			applyClassChange = function() {
				$.each( classAnimationActions, function( i, action ) {
					if ( value[ action ] ) {
						animated[ action + "Class" ]( value[ action ] );
					}
				} );
			};
			applyClassChange();
	
			// Map all animated objects again - calculate new styles and diff
			allAnimations = allAnimations.map( function() {
				this.end = getElementStyles( this.el[ 0 ] );
				this.diff = styleDifference( this.start, this.end );
				return this;
			} );
	
			// Apply original class
			animated.attr( "class", baseClass );
	
			// Map all animated objects again - this time collecting a promise
			allAnimations = allAnimations.map( function() {
				var styleInfo = this,
					dfd = $.Deferred(),
					opts = $.extend( {}, o, {
						queue: false,
						complete: function() {
							dfd.resolve( styleInfo );
						}
					} );
	
				this.el.animate( this.diff, opts );
				return dfd.promise();
			} );
	
			// Once all animations have completed:
			$.when.apply( $, allAnimations.get() ).done( function() {
	
				// Set the final class
				applyClassChange();
	
				// For each animated element,
				// clear all css properties that were animated
				$.each( arguments, function() {
					var el = this.el;
					$.each( this.diff, function( key ) {
						el.css( key, "" );
					} );
				} );
	
				// This is guarnteed to be there if you use jQuery.speed()
				// it also handles dequeuing the next anim...
				o.complete.call( animated[ 0 ] );
			} );
		} );
	};
	
	$.fn.extend( {
		addClass: ( function( orig ) {
			return function( classNames, speed, easing, callback ) {
				return speed ?
					$.effects.animateClass.call( this,
						{ add: classNames }, speed, easing, callback ) :
					orig.apply( this, arguments );
			};
		} )( $.fn.addClass ),
	
		removeClass: ( function( orig ) {
			return function( classNames, speed, easing, callback ) {
				return arguments.length > 1 ?
					$.effects.animateClass.call( this,
						{ remove: classNames }, speed, easing, callback ) :
					orig.apply( this, arguments );
			};
		} )( $.fn.removeClass ),
	
		toggleClass: ( function( orig ) {
			return function( classNames, force, speed, easing, callback ) {
				if ( typeof force === "boolean" || force === undefined ) {
					if ( !speed ) {
	
						// Without speed parameter
						return orig.apply( this, arguments );
					} else {
						return $.effects.animateClass.call( this,
							( force ? { add: classNames } : { remove: classNames } ),
							speed, easing, callback );
					}
				} else {
	
					// Without force parameter
					return $.effects.animateClass.call( this,
						{ toggle: classNames }, force, speed, easing );
				}
			};
		} )( $.fn.toggleClass ),
	
		switchClass: function( remove, add, speed, easing, callback ) {
			return $.effects.animateClass.call( this, {
				add: add,
				remove: remove
			}, speed, easing, callback );
		}
	} );
	
	} )();
	
	/******************************************************************************/
	/*********************************** EFFECTS **********************************/
	/******************************************************************************/
	
	( function() {
	
	if ( $.expr && $.expr.filters && $.expr.filters.animated ) {
		$.expr.filters.animated = ( function( orig ) {
			return function( elem ) {
				return !!$( elem ).data( dataSpaceAnimated ) || orig( elem );
			};
		} )( $.expr.filters.animated );
	}
	
	if ( $.uiBackCompat !== false ) {
		$.extend( $.effects, {
	
			// Saves a set of properties in a data storage
			save: function( element, set ) {
				var i = 0, length = set.length;
				for ( ; i < length; i++ ) {
					if ( set[ i ] !== null ) {
						element.data( dataSpace + set[ i ], element[ 0 ].style[ set[ i ] ] );
					}
				}
			},
	
			// Restores a set of previously saved properties from a data storage
			restore: function( element, set ) {
				var val, i = 0, length = set.length;
				for ( ; i < length; i++ ) {
					if ( set[ i ] !== null ) {
						val = element.data( dataSpace + set[ i ] );
						element.css( set[ i ], val );
					}
				}
			},
	
			setMode: function( el, mode ) {
				if ( mode === "toggle" ) {
					mode = el.is( ":hidden" ) ? "show" : "hide";
				}
				return mode;
			},
	
			// Wraps the element around a wrapper that copies position properties
			createWrapper: function( element ) {
	
				// If the element is already wrapped, return it
				if ( element.parent().is( ".ui-effects-wrapper" ) ) {
					return element.parent();
				}
	
				// Wrap the element
				var props = {
						width: element.outerWidth( true ),
						height: element.outerHeight( true ),
						"float": element.css( "float" )
					},
					wrapper = $( "<div></div>" )
						.addClass( "ui-effects-wrapper" )
						.css( {
							fontSize: "100%",
							background: "transparent",
							border: "none",
							margin: 0,
							padding: 0
						} ),
	
					// Store the size in case width/height are defined in % - Fixes #5245
					size = {
						width: element.width(),
						height: element.height()
					},
					active = document.activeElement;
	
				// Support: Firefox
				// Firefox incorrectly exposes anonymous content
				// https://bugzilla.mozilla.org/show_bug.cgi?id=561664
				try {
					active.id;
				} catch ( e ) {
					active = document.body;
				}
	
				element.wrap( wrapper );
	
				// Fixes #7595 - Elements lose focus when wrapped.
				if ( element[ 0 ] === active || $.contains( element[ 0 ], active ) ) {
					$( active ).trigger( "focus" );
				}
	
				// Hotfix for jQuery 1.4 since some change in wrap() seems to actually
				// lose the reference to the wrapped element
				wrapper = element.parent();
	
				// Transfer positioning properties to the wrapper
				if ( element.css( "position" ) === "static" ) {
					wrapper.css( { position: "relative" } );
					element.css( { position: "relative" } );
				} else {
					$.extend( props, {
						position: element.css( "position" ),
						zIndex: element.css( "z-index" )
					} );
					$.each( [ "top", "left", "bottom", "right" ], function( i, pos ) {
						props[ pos ] = element.css( pos );
						if ( isNaN( parseInt( props[ pos ], 10 ) ) ) {
							props[ pos ] = "auto";
						}
					} );
					element.css( {
						position: "relative",
						top: 0,
						left: 0,
						right: "auto",
						bottom: "auto"
					} );
				}
				element.css( size );
	
				return wrapper.css( props ).show();
			},
	
			removeWrapper: function( element ) {
				var active = document.activeElement;
	
				if ( element.parent().is( ".ui-effects-wrapper" ) ) {
					element.parent().replaceWith( element );
	
					// Fixes #7595 - Elements lose focus when wrapped.
					if ( element[ 0 ] === active || $.contains( element[ 0 ], active ) ) {
						$( active ).trigger( "focus" );
					}
				}
	
				return element;
			}
		} );
	}
	
	$.extend( $.effects, {
		version: "1.12.1",
	
		define: function( name, mode, effect ) {
			if ( !effect ) {
				effect = mode;
				mode = "effect";
			}
	
			$.effects.effect[ name ] = effect;
			$.effects.effect[ name ].mode = mode;
	
			return effect;
		},
	
		scaledDimensions: function( element, percent, direction ) {
			if ( percent === 0 ) {
				return {
					height: 0,
					width: 0,
					outerHeight: 0,
					outerWidth: 0
				};
			}
	
			var x = direction !== "horizontal" ? ( ( percent || 100 ) / 100 ) : 1,
				y = direction !== "vertical" ? ( ( percent || 100 ) / 100 ) : 1;
	
			return {
				height: element.height() * y,
				width: element.width() * x,
				outerHeight: element.outerHeight() * y,
				outerWidth: element.outerWidth() * x
			};
	
		},
	
		clipToBox: function( animation ) {
			return {
				width: animation.clip.right - animation.clip.left,
				height: animation.clip.bottom - animation.clip.top,
				left: animation.clip.left,
				top: animation.clip.top
			};
		},
	
		// Injects recently queued functions to be first in line (after "inprogress")
		unshift: function( element, queueLength, count ) {
			var queue = element.queue();
	
			if ( queueLength > 1 ) {
				queue.splice.apply( queue,
					[ 1, 0 ].concat( queue.splice( queueLength, count ) ) );
			}
			element.dequeue();
		},
	
		saveStyle: function( element ) {
			element.data( dataSpaceStyle, element[ 0 ].style.cssText );
		},
	
		restoreStyle: function( element ) {
			element[ 0 ].style.cssText = element.data( dataSpaceStyle ) || "";
			element.removeData( dataSpaceStyle );
		},
	
		mode: function( element, mode ) {
			var hidden = element.is( ":hidden" );
	
			if ( mode === "toggle" ) {
				mode = hidden ? "show" : "hide";
			}
			if ( hidden ? mode === "hide" : mode === "show" ) {
				mode = "none";
			}
			return mode;
		},
	
		// Translates a [top,left] array into a baseline value
		getBaseline: function( origin, original ) {
			var y, x;
	
			switch ( origin[ 0 ] ) {
			case "top":
				y = 0;
				break;
			case "middle":
				y = 0.5;
				break;
			case "bottom":
				y = 1;
				break;
			default:
				y = origin[ 0 ] / original.height;
			}
	
			switch ( origin[ 1 ] ) {
			case "left":
				x = 0;
				break;
			case "center":
				x = 0.5;
				break;
			case "right":
				x = 1;
				break;
			default:
				x = origin[ 1 ] / original.width;
			}
	
			return {
				x: x,
				y: y
			};
		},
	
		// Creates a placeholder element so that the original element can be made absolute
		createPlaceholder: function( element ) {
			var placeholder,
				cssPosition = element.css( "position" ),
				position = element.position();
	
			// Lock in margins first to account for form elements, which
			// will change margin if you explicitly set height
			// see: http://jsfiddle.net/JZSMt/3/ https://bugs.webkit.org/show_bug.cgi?id=107380
			// Support: Safari
			element.css( {
				marginTop: element.css( "marginTop" ),
				marginBottom: element.css( "marginBottom" ),
				marginLeft: element.css( "marginLeft" ),
				marginRight: element.css( "marginRight" )
			} )
			.outerWidth( element.outerWidth() )
			.outerHeight( element.outerHeight() );
	
			if ( /^(static|relative)/.test( cssPosition ) ) {
				cssPosition = "absolute";
	
				placeholder = $( "<" + element[ 0 ].nodeName + ">" ).insertAfter( element ).css( {
	
					// Convert inline to inline block to account for inline elements
					// that turn to inline block based on content (like img)
					display: /^(inline|ruby)/.test( element.css( "display" ) ) ?
						"inline-block" :
						"block",
					visibility: "hidden",
	
					// Margins need to be set to account for margin collapse
					marginTop: element.css( "marginTop" ),
					marginBottom: element.css( "marginBottom" ),
					marginLeft: element.css( "marginLeft" ),
					marginRight: element.css( "marginRight" ),
					"float": element.css( "float" )
				} )
				.outerWidth( element.outerWidth() )
				.outerHeight( element.outerHeight() )
				.addClass( "ui-effects-placeholder" );
	
				element.data( dataSpace + "placeholder", placeholder );
			}
	
			element.css( {
				position: cssPosition,
				left: position.left,
				top: position.top
			} );
	
			return placeholder;
		},
	
		removePlaceholder: function( element ) {
			var dataKey = dataSpace + "placeholder",
					placeholder = element.data( dataKey );
	
			if ( placeholder ) {
				placeholder.remove();
				element.removeData( dataKey );
			}
		},
	
		// Removes a placeholder if it exists and restores
		// properties that were modified during placeholder creation
		cleanUp: function( element ) {
			$.effects.restoreStyle( element );
			$.effects.removePlaceholder( element );
		},
	
		setTransition: function( element, list, factor, value ) {
			value = value || {};
			$.each( list, function( i, x ) {
				var unit = element.cssUnit( x );
				if ( unit[ 0 ] > 0 ) {
					value[ x ] = unit[ 0 ] * factor + unit[ 1 ];
				}
			} );
			return value;
		}
	} );
	
	// Return an effect options object for the given parameters:
	function _normalizeArguments( effect, options, speed, callback ) {
	
		// Allow passing all options as the first parameter
		if ( $.isPlainObject( effect ) ) {
			options = effect;
			effect = effect.effect;
		}
	
		// Convert to an object
		effect = { effect: effect };
	
		// Catch (effect, null, ...)
		if ( options == null ) {
			options = {};
		}
	
		// Catch (effect, callback)
		if ( $.isFunction( options ) ) {
			callback = options;
			speed = null;
			options = {};
		}
	
		// Catch (effect, speed, ?)
		if ( typeof options === "number" || $.fx.speeds[ options ] ) {
			callback = speed;
			speed = options;
			options = {};
		}
	
		// Catch (effect, options, callback)
		if ( $.isFunction( speed ) ) {
			callback = speed;
			speed = null;
		}
	
		// Add options to effect
		if ( options ) {
			$.extend( effect, options );
		}
	
		speed = speed || options.duration;
		effect.duration = $.fx.off ? 0 :
			typeof speed === "number" ? speed :
			speed in $.fx.speeds ? $.fx.speeds[ speed ] :
			$.fx.speeds._default;
	
		effect.complete = callback || options.complete;
	
		return effect;
	}
	
	function standardAnimationOption( option ) {
	
		// Valid standard speeds (nothing, number, named speed)
		if ( !option || typeof option === "number" || $.fx.speeds[ option ] ) {
			return true;
		}
	
		// Invalid strings - treat as "normal" speed
		if ( typeof option === "string" && !$.effects.effect[ option ] ) {
			return true;
		}
	
		// Complete callback
		if ( $.isFunction( option ) ) {
			return true;
		}
	
		// Options hash (but not naming an effect)
		if ( typeof option === "object" && !option.effect ) {
			return true;
		}
	
		// Didn't match any standard API
		return false;
	}
	
	$.fn.extend( {
		effect: function( /* effect, options, speed, callback */ ) {
			var args = _normalizeArguments.apply( this, arguments ),
				effectMethod = $.effects.effect[ args.effect ],
				defaultMode = effectMethod.mode,
				queue = args.queue,
				queueName = queue || "fx",
				complete = args.complete,
				mode = args.mode,
				modes = [],
				prefilter = function( next ) {
					var el = $( this ),
						normalizedMode = $.effects.mode( el, mode ) || defaultMode;
	
					// Sentinel for duck-punching the :animated psuedo-selector
					el.data( dataSpaceAnimated, true );
	
					// Save effect mode for later use,
					// we can't just call $.effects.mode again later,
					// as the .show() below destroys the initial state
					modes.push( normalizedMode );
	
					// See $.uiBackCompat inside of run() for removal of defaultMode in 1.13
					if ( defaultMode && ( normalizedMode === "show" ||
							( normalizedMode === defaultMode && normalizedMode === "hide" ) ) ) {
						el.show();
					}
	
					if ( !defaultMode || normalizedMode !== "none" ) {
						$.effects.saveStyle( el );
					}
	
					if ( $.isFunction( next ) ) {
						next();
					}
				};
	
			if ( $.fx.off || !effectMethod ) {
	
				// Delegate to the original method (e.g., .show()) if possible
				if ( mode ) {
					return this[ mode ]( args.duration, complete );
				} else {
					return this.each( function() {
						if ( complete ) {
							complete.call( this );
						}
					} );
				}
			}
	
			function run( next ) {
				var elem = $( this );
	
				function cleanup() {
					elem.removeData( dataSpaceAnimated );
	
					$.effects.cleanUp( elem );
	
					if ( args.mode === "hide" ) {
						elem.hide();
					}
	
					done();
				}
	
				function done() {
					if ( $.isFunction( complete ) ) {
						complete.call( elem[ 0 ] );
					}
	
					if ( $.isFunction( next ) ) {
						next();
					}
				}
	
				// Override mode option on a per element basis,
				// as toggle can be either show or hide depending on element state
				args.mode = modes.shift();
	
				if ( $.uiBackCompat !== false && !defaultMode ) {
					if ( elem.is( ":hidden" ) ? mode === "hide" : mode === "show" ) {
	
						// Call the core method to track "olddisplay" properly
						elem[ mode ]();
						done();
					} else {
						effectMethod.call( elem[ 0 ], args, done );
					}
				} else {
					if ( args.mode === "none" ) {
	
						// Call the core method to track "olddisplay" properly
						elem[ mode ]();
						done();
					} else {
						effectMethod.call( elem[ 0 ], args, cleanup );
					}
				}
			}
	
			// Run prefilter on all elements first to ensure that
			// any showing or hiding happens before placeholder creation,
			// which ensures that any layout changes are correctly captured.
			return queue === false ?
				this.each( prefilter ).each( run ) :
				this.queue( queueName, prefilter ).queue( queueName, run );
		},
	
		show: ( function( orig ) {
			return function( option ) {
				if ( standardAnimationOption( option ) ) {
					return orig.apply( this, arguments );
				} else {
					var args = _normalizeArguments.apply( this, arguments );
					args.mode = "show";
					return this.effect.call( this, args );
				}
			};
		} )( $.fn.show ),
	
		hide: ( function( orig ) {
			return function( option ) {
				if ( standardAnimationOption( option ) ) {
					return orig.apply( this, arguments );
				} else {
					var args = _normalizeArguments.apply( this, arguments );
					args.mode = "hide";
					return this.effect.call( this, args );
				}
			};
		} )( $.fn.hide ),
	
		toggle: ( function( orig ) {
			return function( option ) {
				if ( standardAnimationOption( option ) || typeof option === "boolean" ) {
					return orig.apply( this, arguments );
				} else {
					var args = _normalizeArguments.apply( this, arguments );
					args.mode = "toggle";
					return this.effect.call( this, args );
				}
			};
		} )( $.fn.toggle ),
	
		cssUnit: function( key ) {
			var style = this.css( key ),
				val = [];
	
			$.each( [ "em", "px", "%", "pt" ], function( i, unit ) {
				if ( style.indexOf( unit ) > 0 ) {
					val = [ parseFloat( style ), unit ];
				}
			} );
			return val;
		},
	
		cssClip: function( clipObj ) {
			if ( clipObj ) {
				return this.css( "clip", "rect(" + clipObj.top + "px " + clipObj.right + "px " +
					clipObj.bottom + "px " + clipObj.left + "px)" );
			}
			return parseClip( this.css( "clip" ), this );
		},
	
		transfer: function( options, done ) {
			var element = $( this ),
				target = $( options.to ),
				targetFixed = target.css( "position" ) === "fixed",
				body = $( "body" ),
				fixTop = targetFixed ? body.scrollTop() : 0,
				fixLeft = targetFixed ? body.scrollLeft() : 0,
				endPosition = target.offset(),
				animation = {
					top: endPosition.top - fixTop,
					left: endPosition.left - fixLeft,
					height: target.innerHeight(),
					width: target.innerWidth()
				},
				startPosition = element.offset(),
				transfer = $( "<div class='ui-effects-transfer'></div>" )
					.appendTo( "body" )
					.addClass( options.className )
					.css( {
						top: startPosition.top - fixTop,
						left: startPosition.left - fixLeft,
						height: element.innerHeight(),
						width: element.innerWidth(),
						position: targetFixed ? "fixed" : "absolute"
					} )
					.animate( animation, options.duration, options.easing, function() {
						transfer.remove();
						if ( $.isFunction( done ) ) {
							done();
						}
					} );
		}
	} );
	
	function parseClip( str, element ) {
			var outerWidth = element.outerWidth(),
				outerHeight = element.outerHeight(),
				clipRegex = /^rect\((-?\d*\.?\d*px|-?\d+%|auto),?\s*(-?\d*\.?\d*px|-?\d+%|auto),?\s*(-?\d*\.?\d*px|-?\d+%|auto),?\s*(-?\d*\.?\d*px|-?\d+%|auto)\)$/,
				values = clipRegex.exec( str ) || [ "", 0, outerWidth, outerHeight, 0 ];
	
			return {
				top: parseFloat( values[ 1 ] ) || 0,
				right: values[ 2 ] === "auto" ? outerWidth : parseFloat( values[ 2 ] ),
				bottom: values[ 3 ] === "auto" ? outerHeight : parseFloat( values[ 3 ] ),
				left: parseFloat( values[ 4 ] ) || 0
			};
	}
	
	$.fx.step.clip = function( fx ) {
		if ( !fx.clipInit ) {
			fx.start = $( fx.elem ).cssClip();
			if ( typeof fx.end === "string" ) {
				fx.end = parseClip( fx.end, fx.elem );
			}
			fx.clipInit = true;
		}
	
		$( fx.elem ).cssClip( {
			top: fx.pos * ( fx.end.top - fx.start.top ) + fx.start.top,
			right: fx.pos * ( fx.end.right - fx.start.right ) + fx.start.right,
			bottom: fx.pos * ( fx.end.bottom - fx.start.bottom ) + fx.start.bottom,
			left: fx.pos * ( fx.end.left - fx.start.left ) + fx.start.left
		} );
	};
	
	} )();
	
	/******************************************************************************/
	/*********************************** EASING ***********************************/
	/******************************************************************************/
	
	( function() {
	
	// Based on easing equations from Robert Penner (http://www.robertpenner.com/easing)
	
	var baseEasings = {};
	
	$.each( [ "Quad", "Cubic", "Quart", "Quint", "Expo" ], function( i, name ) {
		baseEasings[ name ] = function( p ) {
			return Math.pow( p, i + 2 );
		};
	} );
	
	$.extend( baseEasings, {
		Sine: function( p ) {
			return 1 - Math.cos( p * Math.PI / 2 );
		},
		Circ: function( p ) {
			return 1 - Math.sqrt( 1 - p * p );
		},
		Elastic: function( p ) {
			return p === 0 || p === 1 ? p :
				-Math.pow( 2, 8 * ( p - 1 ) ) * Math.sin( ( ( p - 1 ) * 80 - 7.5 ) * Math.PI / 15 );
		},
		Back: function( p ) {
			return p * p * ( 3 * p - 2 );
		},
		Bounce: function( p ) {
			var pow2,
				bounce = 4;
	
			while ( p < ( ( pow2 = Math.pow( 2, --bounce ) ) - 1 ) / 11 ) {}
			return 1 / Math.pow( 4, 3 - bounce ) - 7.5625 * Math.pow( ( pow2 * 3 - 2 ) / 22 - p, 2 );
		}
	} );
	
	$.each( baseEasings, function( name, easeIn ) {
		$.easing[ "easeIn" + name ] = easeIn;
		$.easing[ "easeOut" + name ] = function( p ) {
			return 1 - easeIn( 1 - p );
		};
		$.easing[ "easeInOut" + name ] = function( p ) {
			return p < 0.5 ?
				easeIn( p * 2 ) / 2 :
				1 - easeIn( p * -2 + 2 ) / 2;
		};
	} );
	
	} )();
	
	return $.effects;
	
	} ) );


/***/ }),
/* 64 */
/*!***********************************************!*\
  !*** ./src/expense/views/ExpenseEmptyView.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseEmptyView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/ExpenseEmptyView.mustache */ 65),
	    templateContext: function templateContext() {
	        var colspan = this.getOption('colspan');
	        if (this.getOption('edit')) {
	            colspan += 1;
	        }
	        return {
	            colspan: colspan
	        };
	    }
	}); /*
	     * File Name : ExpenseEmptyView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseEmptyView;

/***/ }),
/* 65 */
/*!***************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseEmptyView.mustache ***!
  \***************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<td colspan='"
	    + escapeExpression(((helper = (helper = helpers.colspan || (depth0 != null ? depth0.colspan : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"colspan","hash":{},"data":data}) : helper)))
	    + "'>Aucune dépense n'a été configurée</td>\n";
	},"useData":true});

/***/ }),
/* 66 */
/*!***************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseTableView.mustache ***!
  \***************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "        <button class='btn btn-primary primary-action add'>\n            <i class='glyphicon glyphicon-plus-sign'></i>&nbsp;Ajouter une dépense\n        </button>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "        <th class=\"hidden-print\">Actions</th>\n";
	  },"5":function(depth0,helpers,partials,data) {
	  return "            <td class=\"hidden-print\"></td>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, options, lambda=this.lambda, escapeExpression=this.escapeExpression, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class=\"row\">\n    <div class=\"col-xs-12\">\n        <h2 style=\"margin-top:0px\">\n            "
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.category : depth0)) != null ? stack1.label : stack1), depth0))
	    + "\n        </h2>\n        <span class=\"help-block\">\n            "
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.category : depth0)) != null ? stack1.description : stack1), depth0))
	    + "\n        </span>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </div>\n</div>\n<table class=\"opa table table-bordered table-condensed\">\n    <thead>\n        <th>Date</th>\n        <th>Type de dépense</th>\n        <th>Description</th>\n        <th>Montant HT</th>\n        <th>Tva</th>\n        <th>Total TTC</th>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </thead>\n    <tbody class='lines'>\n    </tbody>\n    <tfoot>\n        <tr>\n            <td colspan='3'>Total</td>\n            <td class='total_ht'></td>\n            <td class='total_tva'></td>\n            <td class='total_ttc'></td>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "        </tr>\n    </tfoot>\n</table>\n";
	},"useData":true});

/***/ }),
/* 67 */
/*!*************************************************!*\
  !*** ./src/expense/views/ExpenseKmTableView.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ExpenseKmCollectionView = __webpack_require__(/*! ./ExpenseKmCollectionView.js */ 68);
	
	var _ExpenseKmCollectionView2 = _interopRequireDefault(_ExpenseKmCollectionView);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseKmTableView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ExpenseKmTableView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/ExpenseKmTableView.mustache */ 71),
	    regions: {
	        lines: {
	            el: 'tbody',
	            replaceElement: true
	        }
	    },
	    ui: {
	        add_btn: 'button.add',
	        total_km: '.total_km',
	        total_ttc: '.total_ttc'
	    },
	    triggers: {
	        'click @ui.add_btn': 'kmline:add'
	    },
	    childViewTriggers: {
	        'kmline:edit': 'kmline:edit',
	        'kmline:delete': 'kmline:delete',
	        'kmline:duplicate': 'kmline:duplicate'
	    },
	    collectionEvents: {
	        'change:category': 'render'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('facade');
	        this.totalmodel = channel.request('get:totalmodel');
	        this.categoryName = this.getOption('category').value;
	        this.listenTo(channel, 'change:kmlines_' + this.categoryName, this.showTotals.bind(this));
	    },
	    showTotals: function showTotals() {
	        this.getUI("total_km").html(this.totalmodel.get('km_' + this.categoryName) + " km");
	        this.getUI("total_ttc").html((0, _math.formatAmount)(this.totalmodel.get('km_ttc_' + this.categoryName)));
	    },
	    templateContext: function templateContext() {
	        return {
	            category: this.getOption('category'),
	            edit: this.getOption('edit')
	        };
	    },
	    onRender: function onRender() {
	        var view = new _ExpenseKmCollectionView2.default({
	            collection: this.collection,
	            category: this.getOption('category'),
	            edit: this.getOption('edit')
	        });
	        this.showChildView('lines', view);
	    },
	    onAttach: function onAttach() {
	        this.showTotals();
	    }
	});
	exports.default = ExpenseKmTableView;

/***/ }),
/* 68 */
/*!******************************************************!*\
  !*** ./src/expense/views/ExpenseKmCollectionView.js ***!
  \******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ExpenseKmView = __webpack_require__(/*! ./ExpenseKmView.js */ 69);
	
	var _ExpenseKmView2 = _interopRequireDefault(_ExpenseKmView);
	
	var _ExpenseEmptyView = __webpack_require__(/*! ./ExpenseEmptyView.js */ 64);
	
	var _ExpenseEmptyView2 = _interopRequireDefault(_ExpenseEmptyView);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseKmCollectionView = _backbone2.default.CollectionView.extend({
	    tagName: 'tbody',
	    // Bubble up child view events
	    childViewTriggers: {
	        'edit': 'kmline:edit',
	        'delete': 'kmline:delete',
	        'duplicate': 'kmline:duplicate'
	    },
	    childView: _ExpenseKmView2.default,
	    emptyView: _ExpenseEmptyView2.default,
	    emptyViewOptions: function emptyViewOptions() {
	        return {
	            colspan: 6,
	            edit: this.getOption('edit')
	        };
	    },
	    childViewOptions: function childViewOptions() {
	        return { edit: this.getOption('edit') };
	    },
	
	    filter: function filter(child, index, collection) {
	        if (child.get('category') == this.getOption('category').value) {
	            return true;
	        } else {
	            return false;
	        }
	    }
	}); /*
	     * File Name : ExpenseKmCollectionView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseKmCollectionView;

/***/ }),
/* 69 */
/*!********************************************!*\
  !*** ./src/expense/views/ExpenseKmView.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ExpenseKmView = _backbone2.default.View.extend({
	    tagName: 'tr',
	    template: __webpack_require__(/*! ./templates/ExpenseKmView.mustache */ 70),
	    modelEvents: {
	        'change': 'render'
	    },
	    ui: {
	        edit: 'button.edit',
	        delete: 'button.delete',
	        duplicate: 'button.duplicate'
	    },
	    triggers: {
	        'click @ui.edit': 'edit',
	        'click @ui.delete': 'delete',
	        'click @ui.duplicate': 'duplicate'
	    },
	    templateContext: function templateContext() {
	        var total = this.model.total();
	        var typelabel = this.model.getTypeLabel();
	        return {
	            edit: this.getOption('edit'),
	            typelabel: typelabel,
	            total: (0, _math.formatAmount)(total)
	        };
	    }
	});
	exports.default = ExpenseKmView;

/***/ }),
/* 70 */
/*!************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseKmView.mustache ***!
  \************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "<td class=\"hidden-print\">\n<button class='btn btn-default edit'><i class='glyphicon glyphicon-pencil'></i>&nbsp;Modifier</button>\n<button class='btn btn-default delete'><i class='glyphicon glyphicon-remove-sign'></i>&nbsp;Supprimer</button>\n<button class='btn btn-default duplicate'><i class='fa fa-copy'></i>&nbsp;Dupliquer</button>\n</td>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<td>"
	    + escapeExpression(((helper = (helper = helpers.altdate || (depth0 != null ? depth0.altdate : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"altdate","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>"
	    + escapeExpression(((helper = (helper = helpers.typelabel || (depth0 != null ? depth0.typelabel : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"typelabel","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>"
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>"
	    + escapeExpression(((helper = (helper = helpers.start || (depth0 != null ? depth0.start : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"start","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>"
	    + escapeExpression(((helper = (helper = helpers.end || (depth0 != null ? depth0.end : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"end","hash":{},"data":data}) : helper)))
	    + "</td>\n<td>"
	    + escapeExpression(((helper = (helper = helpers.km || (depth0 != null ? depth0.km : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"km","hash":{},"data":data}) : helper)))
	    + " km</td>\n<td>";
	  stack1 = ((helper = (helper = helpers.total || (depth0 != null ? depth0.total : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</td>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 71 */
/*!*****************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseKmTableView.mustache ***!
  \*****************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "        <button class='btn btn-primary primary-action add'>\n            <i class='glyphicon glyphicon-plus-sign'></i>&nbsp;Ajouter une dépense\n        </button>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "        <th class=\"hidden-print\">Actions</th>\n";
	  },"5":function(depth0,helpers,partials,data) {
	  return "            <td class=\"hidden-print\"></td>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class=\"row\">\n    <div class=\"col-xs-12\">\n        <h3 style=\"margin-top:0px\">\n            Dépenses kilométriques\n        </h3>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </div>\n</div>\n\n<table class=\"opa table table-striped table-bordered table-condensed\">\n    <thead>\n        <th>Date</th>\n        <th>Type</th>\n        <th>Prestation</th>\n        <th>Point de départ</th>\n        <th>Point d'arrivée</th>\n        <th>Kms</th>\n        <th>Indemnités</th>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </thead>\n    <tbody class='lines'>\n    </tbody>\n    <tfoot>\n        <tr>\n            <td colspan='5'>Total</td>\n            <td class='total_km'></td>\n            <td class='total_ttc'></td>\n";
	  stack1 = ((helper = (helper = helpers.edit || (depth0 != null ? depth0.edit : depth0)) != null ? helper : helperMissing),(options={"name":"edit","hash":{},"fn":this.program(5, data),"inverse":this.noop,"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.edit) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "        </tr>\n    </tfoot>\n</table>\n\n";
	},"useData":true});

/***/ }),
/* 72 */
/*!***************************************************!*\
  !*** ./src/expense/views/ExpenseFormPopupView.js ***!
  \***************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ModalBehavior = __webpack_require__(/*! ../../base/behaviors/ModalBehavior.js */ 50);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	var _ExpenseFormView = __webpack_require__(/*! ./ExpenseFormView.js */ 73);
	
	var _ExpenseFormView2 = _interopRequireDefault(_ExpenseFormView);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _BookMarkCollectionView = __webpack_require__(/*! ./BookMarkCollectionView.js */ 83);
	
	var _BookMarkCollectionView2 = _interopRequireDefault(_BookMarkCollectionView);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseFormPopupView = _backbone2.default.View.extend({
	    behaviors: [_ModalBehavior2.default],
	    template: __webpack_require__(/*! ./templates/ExpenseFormPopupView.mustache */ 85),
	    regions: {
	        main: '#mainform-container',
	        tel: '#telform-container',
	        bookmark: '#bookmark-container'
	    },
	    ui: {
	        main_tab: 'ul.nav-tabs li.main a',
	        tel_tab: "ul.nav-tabs li.tel a",
	        modalbody: '.modal-body'
	    },
	    childViewEvents: {
	        'bookmark:insert': 'onBookMarkInsert',
	        'success:sync': 'onSuccessSync'
	    },
	    // Here we bind the child FormBehavior with our ModalBehavior
	    // Like it's done in the ModalFormBehavior
	    childViewTriggers: {
	        'cancel:form': 'modal:close',
	        'bookmark:delete': 'bookmark:delete'
	    },
	    modelEvents: {
	        'set:bookmark': 'refreshForm'
	    },
	    initialize: function initialize() {
	        var facade = _backbone4.default.channel('facade');
	        this.bookmarks = facade.request('get:bookmarks');
	        this.add = this.getOption('add');
	        this.tel = this.model.isSpecial();
	    },
	    refresh: function refresh() {
	        this.triggerMethod('line:add', this.model.get('category'));
	    },
	    onSuccessSync: function onSuccessSync() {
	        if (this.add) {
	            var this_ = this;
	            var modalbody = this.getUI('modalbody');
	
	            modalbody.effect('highlight', { color: '#bbdfbb' }, 800, this_.refresh.bind(this));
	            modalbody.addClass('alert alert-success');
	        } else {
	            this.triggerMethod('modal:close');
	        }
	    },
	    onModalBeforeClose: function onModalBeforeClose() {
	        this.model.rollback();
	    },
	    refreshForm: function refreshForm() {
	        if (this.model.isSpecial()) {
	            this.showTelForm();
	            this.getUI('tel_tab').tab('show');
	        } else {
	            this.showMainForm();
	            this.getUI('main_tab').tab('show');
	        }
	    },
	    showMainForm: function showMainForm() {
	        if (!this.tel || this.add) {
	            var view = new _ExpenseFormView2.default({
	                model: this.model,
	                destCollection: this.getOption('destCollection'),
	                title: this.getOption('title'),
	                tel: false,
	                add: this.add
	            });
	            this.showChildView('main', view);
	        }
	    },
	    showTelForm: function showTelForm() {
	        if (this.tel || this.add) {
	            var view = new _ExpenseFormView2.default({
	                model: this.model,
	                destCollection: this.getOption('destCollection'),
	                title: this.getOption('title'),
	                tel: true,
	                add: this.add
	            });
	            this.showChildView('tel', view);
	        }
	    },
	    onBookMarkInsert: function onBookMarkInsert(childView) {
	        this.model.loadBookMark(childView.model);
	    },
	    showBookMarks: function showBookMarks() {
	        if (this.add) {
	            if (this.bookmarks.length > 0) {
	                var view = new _BookMarkCollectionView2.default({
	                    collection: this.bookmarks
	                });
	                this.showChildView('bookmark', view);
	            }
	        }
	    },
	    templateContext: function templateContext() {
	        /*
	         * Form can be add form : show all tabs
	         * Form can be tel form : show only the tel tab
	         */
	        var show_tel = this.add || this.tel;
	        var show_main = this.add || !this.tel;
	        return {
	            title: this.getOption('title'),
	            add: this.add,
	            show_tel_tab: this.tel,
	            show_tel: show_tel,
	            show_bookmarks: this.add && this.bookmarks.length > 0,
	            show_main: show_main
	        };
	    },
	
	    onRender: function onRender() {
	        this.refreshForm();
	        this.showTelForm();
	        this.showBookMarks();
	    }
	}); /*
	     * File Name : ExpenseFormPopupView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseFormPopupView;

/***/ }),
/* 73 */
/*!**********************************************!*\
  !*** ./src/expense/views/ExpenseFormView.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _FormBehavior = __webpack_require__(/*! ../../base/behaviors/FormBehavior.js */ 74);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _DatePickerWidget = __webpack_require__(/*! ../../widgets/DatePickerWidget.js */ 76);
	
	var _DatePickerWidget2 = _interopRequireDefault(_DatePickerWidget);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 78);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _SelectWidget = __webpack_require__(/*! ../../widgets/SelectWidget.js */ 80);
	
	var _SelectWidget2 = _interopRequireDefault(_SelectWidget);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseFormView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ExpenseFormView = _backbone2.default.View.extend({
	    behaviors: [_FormBehavior2.default],
	    template: __webpack_require__(/*! ./templates/ExpenseFormView.mustache */ 82),
	    regions: {
	        'category': '.category',
	        'date': '.date',
	        'type_id': '.type_id',
	        'description': '.description',
	        'ht': '.ht',
	        'tva': '.tva'
	    },
	    // Bubble up child view events
	    //
	    childViewTriggers: {
	        'change': 'data:modified'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('config');
	        if (this.getOption('tel')) {
	            this.type_options = channel.request('get:options', 'expensetel_types');
	        } else {
	            this.type_options = channel.request('get:options', 'expense_types');
	            this.categories = channel.request('get:options', 'categories');
	        }
	        this.today = channel.request('get:options', 'today');
	    },
	    onRender: function onRender() {
	        var view;
	        if (this.getOption('tel')) {
	            view = new _InputWidget2.default({
	                value: "1",
	                field_name: 'category',
	                type: 'hidden'
	            });
	        } else {
	            view = new _SelectWidget2.default({
	                value: this.model.get('category'),
	                field_name: 'category',
	                options: this.categories,
	                id_key: 'value',
	                title: "Catégorie"
	            });
	        }
	        this.showChildView('category', view);
	
	        view = new _DatePickerWidget2.default({
	            date: this.model.get('date'),
	            title: "Date",
	            field_name: "date",
	            default_value: this.today
	        });
	        this.showChildView("date", view);
	
	        view = new _SelectWidget2.default({
	            value: this.model.get('type_id'),
	            title: 'Type de frais',
	            field_name: 'type_id',
	            options: this.type_options,
	            id_key: 'id'
	        });
	        this.showChildView('type_id', view);
	
	        if (!this.getOption('tel')) {
	            view = new _InputWidget2.default({
	                value: this.model.get('description'),
	                title: 'Description',
	                field_name: 'description'
	            });
	            this.showChildView('description', view);
	        }
	
	        view = new _InputWidget2.default({
	            value: this.model.get('ht'),
	            title: 'Montant HT',
	            field_name: 'ht',
	            addon: "€"
	        });
	        this.showChildView('ht', view);
	
	        view = new _InputWidget2.default({
	            value: this.model.get('tva'),
	            title: 'Montant TVA',
	            field_name: 'tva',
	            addon: "€"
	        });
	        this.showChildView('tva', view);
	    },
	
	    templateContext: function templateContext() {
	        return {
	            title: this.getOption('title'),
	            add: this.getOption('add')
	        };
	    }
	});
	exports.default = ExpenseFormView;

/***/ }),
/* 74 */
/*!********************************************!*\
  !*** ./src/base/behaviors/FormBehavior.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 28);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 4);
	
	var _BaseFormBehavior = __webpack_require__(/*! ./BaseFormBehavior.js */ 75);
	
	var _BaseFormBehavior2 = _interopRequireDefault(_BaseFormBehavior);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
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
/* 75 */
/*!************************************************!*\
  !*** ./src/base/behaviors/BaseFormBehavior.js ***!
  \************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 28);
	
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
/* 76 */
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
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 4);
	
	var _date = __webpack_require__(/*! ../date.js */ 5);
	
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
	var template = __webpack_require__(/*! ./templates/DatePickerWidget.mustache */ 77);
	
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
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 3)))

/***/ }),
/* 77 */
/*!*********************************************************!*\
  !*** ./src/widgets/templates/DatePickerWidget.mustache ***!
  \*********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
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
/* 78 */
/*!************************************!*\
  !*** ./src/widgets/InputWidget.js ***!
  \************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 4);
	
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
	    template: __webpack_require__(/*! ./templates/InputWidget.mustache */ 79),
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
/* 79 */
/*!****************************************************!*\
  !*** ./src/widgets/templates/InputWidget.mustache ***!
  \****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
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
/* 80 */
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
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../tools.js */ 4);
	
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
	var template = __webpack_require__(/*! ./templates/SelectWidget.mustache */ 81);
	
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
	        var editable = (0, _tools.getOpt)(this, 'editable', true);
	        var description = (0, _tools.getOpt)(this, 'description', '');
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
	            multiple: multiple,
	            description: description,
	            editable: editable
	        };
	    }
	});
	exports.default = SelectWidget;

/***/ }),
/* 81 */
/*!*****************************************************!*\
  !*** ./src/widgets/templates/SelectWidget.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
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
	  },"5":function(depth0,helpers,partials,data) {
	  return "disabled";
	  },"7":function(depth0,helpers,partials,data,depths) {
	  var stack1, escapeExpression=this.escapeExpression, lambda=this.lambda, buffer = "    <option value='"
	    + escapeExpression(helpers.lookup.call(depth0, depth0, (depths[1] != null ? depths[1].id_key : depths[1]), {"name":"lookup","hash":{},"data":data}))
	    + "' ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.selected : depth0), {"name":"if","hash":{},"fn":this.program(8, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + ">"
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "</option>\n";
	},"8":function(depth0,helpers,partials,data) {
	  return "selected";
	  },"10":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "    <span class='help-block'>"
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + "</span>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data,depths) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.title : depth0), {"name":"if","hash":{},"fn":this.program(1, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "<select class='form-control' ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.multiple : depth0), {"name":"if","hash":{},"fn":this.program(3, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += " name='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "' ";
	  stack1 = helpers.unless.call(depth0, (depth0 != null ? depth0.editable : depth0), {"name":"unless","hash":{},"fn":this.program(5, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += " >\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.options : depth0), {"name":"each","hash":{},"fn":this.program(7, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</select>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.description : depth0), {"name":"if","hash":{},"fn":this.program(10, data, depths),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true,"useDepths":true});

/***/ }),
/* 82 */
/*!**************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseFormView.mustache ***!
  \**************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<form class='form expense-form'>\n    <div class='category'></div>\n    <div class='date required'></div>\n    <div class='type_id required'></div>\n    <div class='description required'></div>\n    <div class='ht'></div>\n    <div class='tva'></div>\n    <button\n        class='btn btn-success'\n        type='submit'\n        value='submit'>\n        "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n    </button>\n\n    <button\n        class='btn btn-default secondary-action'\n        type='reset'\n        value='submit'>\n        Annuler\n    </button>\n</form>\n";
	},"useData":true});

/***/ }),
/* 83 */
/*!*****************************************************!*\
  !*** ./src/expense/views/BookMarkCollectionView.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : BookMarkCollectionView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var BookMarkView = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'row bookmark-line',
	    template: __webpack_require__(/*! ./templates/BookMarkView.mustache */ 84),
	    ui: {
	        delete_btn: '.delete',
	        insert_btn: '.insert'
	    },
	    triggers: {
	        'click @ui.delete_btn': 'bookmark:delete',
	        'click @ui.insert_btn': 'bookmark:insert'
	    },
	    templateContext: function templateContext() {
	        var typelabel = this.model.getTypeLabel();
	        return {
	            ht: (0, _math.formatAmount)(this.model.get('ht')),
	            tva: (0, _math.formatAmount)(this.model.get('tva')),
	            typelabel: typelabel
	        };
	    }
	});
	
	var BookMarkCollectionView = _backbone2.default.CollectionView.extend({
	    childView: BookMarkView,
	    childViewTriggers: {
	        'bookmark:delete': 'bookmark:delete',
	        'bookmark:insert': 'bookmark:insert'
	    }
	});
	exports.default = BookMarkCollectionView;

/***/ }),
/* 84 */
/*!***********************************************************!*\
  !*** ./src/expense/views/templates/BookMarkView.mustache ***!
  \***********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class='col-xs-6'>\n"
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + " <br /> HT ";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += " - TVA ";
	  stack1 = ((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + " <br />"
	    + escapeExpression(((helper = (helper = helpers.typelabel || (depth0 != null ? depth0.typelabel : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"typelabel","hash":{},"data":data}) : helper)))
	    + "\n</div>\n<div class='col-xs-6'>\n<div class=\"btn-group\" role=\"group\" aria-label=\"actions\">\n<button class='btn btn-success insert'><i class=\"glyphicon glyphicon-ok\"></i>&nbsp;Sélectionner</button>\n<button class='btn btn-danger delete'><i class=\"glyphicon glyphicon-remove-sign\"></i>&nbsp;Supprimer</button>\n</div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 85 */
/*!*******************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseFormPopupView.mustache ***!
  \*******************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "            <ul class=\"nav nav-tabs\" role=\"tablist\">\n                <li role=\"presentation\" class=\"active main\">\n                    <a href=\"#mainform-container\"\n                        aria-controls=\"form-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\"\n                        tabindex='-1'\n                        >\n                        Frais généraux\n                    </a>\n                </li>\n                <li role=\"presentation\" class='tel'>\n                    <a href=\"#telform-container\"\n                        aria-controls=\"telform-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\"\n                        tabindex='-1'\n                        >\n                        Frais téléphoniques\n                    </a>\n                </li>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_bookmarks : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "            </ul>\n";
	},"2":function(depth0,helpers,partials,data) {
	  return "                    <li role=\"presentation\">\n                        <a href=\"#bookmark-container\"\n                            aria-controls=\"bookmark-container\"\n                            role=\"tab\"\n                            tabindex='-1'\n                            data-toggle=\"tab\">\n                            Favoris\n                        </a>\n                    </li>\n";
	  },"4":function(depth0,helpers,partials,data) {
	  return "                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane fade in active\"\n                    id=\"mainform-container\">\n                </div>\n";
	  },"6":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane fade in ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_tel_tab : depth0), {"name":"if","hash":{},"fn":this.program(7, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\"\n                    id=\"telform-container\">\n                </div>\n";
	},"7":function(depth0,helpers,partials,data) {
	  return "active";
	  },"9":function(depth0,helpers,partials,data) {
	  return "                    <div\n                        role=\"tabpanel\"\n                        class=\"tab-pane fade in\"\n                        id=\"bookmark-container\">\n                    </div>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\" role=\"document\">\n    <div class=\"modal-content\">\n            <div class=\"modal-header\">\n              <button tabindex='-1' type=\"button\" class=\"close\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n              <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n            </div>\n            <div class=\"modal-body\">\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "            <div class='tab-content'>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_main : depth0), {"name":"if","hash":{},"fn":this.program(4, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_tel : depth0), {"name":"if","hash":{},"fn":this.program(6, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.show_bookmarks : depth0), {"name":"if","hash":{},"fn":this.program(9, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "            </div>\n            <div class=\"modal-footer\">\n            </div>\n    </div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n";
	},"useData":true});

/***/ }),
/* 86 */
/*!************************************************!*\
  !*** ./src/expense/views/ExpenseKmFormView.js ***!
  \************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ModalFormBehavior = __webpack_require__(/*! ../../base/behaviors/ModalFormBehavior.js */ 87);
	
	var _ModalFormBehavior2 = _interopRequireDefault(_ModalFormBehavior);
	
	var _DatePickerWidget = __webpack_require__(/*! ../../widgets/DatePickerWidget.js */ 76);
	
	var _DatePickerWidget2 = _interopRequireDefault(_DatePickerWidget);
	
	var _InputWidget = __webpack_require__(/*! ../../widgets/InputWidget.js */ 78);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _SelectWidget = __webpack_require__(/*! ../../widgets/SelectWidget.js */ 80);
	
	var _SelectWidget2 = _interopRequireDefault(_SelectWidget);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseKmFormView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ExpenseKmFormView = _backbone2.default.View.extend({
	    behaviors: [_ModalFormBehavior2.default],
	    template: __webpack_require__(/*! ./templates/ExpenseKmFormView.mustache */ 88),
	    regions: {
	        'category': '.category',
	        'date': '.date',
	        'type_id': '.type_id',
	        'start': '.start',
	        'end': '.end',
	        'km': '.km',
	        'description': '.description'
	    },
	    // Bubble up child view events
	    //
	    childViewTriggers: {
	        'change': 'data:modified'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('config');
	        this.type_options = channel.request('get:options', 'expensekm_types');
	        this.categories = channel.request('get:options', 'categories');
	        this.today = channel.request('get:options', 'today');
	    },
	    refreshForm: function refreshForm() {
	        var view = new _SelectWidget2.default({
	            value: this.model.get('category'),
	            field_name: 'category',
	            options: this.categories,
	            id_key: 'value',
	            title: "Catégorie"
	        });
	        this.showChildView('category', view);
	
	        view = new _DatePickerWidget2.default({
	            date: this.model.get('date'),
	            title: "Date",
	            field_name: "date",
	            current_year: true,
	            default_value: this.today
	        });
	        this.showChildView("date", view);
	
	        view = new _SelectWidget2.default({
	            value: this.model.get('type_id'),
	            title: 'Type de frais',
	            field_name: 'type_id',
	            options: this.type_options,
	            id_key: 'id'
	        });
	        this.showChildView('type_id', view);
	
	        view = new _InputWidget2.default({
	            value: this.model.get('start'),
	            title: 'Point de départ',
	            field_name: 'start'
	        });
	        this.showChildView('start', view);
	
	        view = new _InputWidget2.default({
	            value: this.model.get('end'),
	            title: "Point d'arrivée",
	            field_name: 'end'
	        });
	        this.showChildView('end', view);
	
	        view = new _InputWidget2.default({
	            value: this.model.get('km'),
	            title: "Nombre de kilomètres",
	            field_name: 'km',
	            addon: "km"
	        });
	        this.showChildView('km', view);
	
	        view = new _InputWidget2.default({
	            value: this.model.get('description'),
	            title: 'Description',
	            description: "Le cas échéant, indiquer la prestation liée à ces dépenses",
	            field_name: 'description'
	        });
	        this.showChildView('description', view);
	    },
	
	    templateContext: function templateContext() {
	        return {
	            title: this.getOption('title')
	        };
	    },
	    onRender: function onRender() {
	        this.refreshForm();
	    }
	});
	exports.default = ExpenseKmFormView;

/***/ }),
/* 87 */
/*!*************************************************!*\
  !*** ./src/base/behaviors/ModalFormBehavior.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 29);
	
	var _ModalBehavior = __webpack_require__(/*! ./ModalBehavior.js */ 50);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	var _FormBehavior = __webpack_require__(/*! ./FormBehavior.js */ 74);
	
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
/* 88 */
/*!****************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseKmFormView.mustache ***!
  \****************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<div class=\"modal-dialog\" role=\"document\">\n    <div class=\"modal-content\">\n        <form class='form expense-form'>\n            <div class=\"modal-header\">\n              <button tabindex='-1' type=\"button\" class=\"close\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n              <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n            </div>\n            <div class=\"modal-body\">\n                    <div class='category'></div>\n                    <div class='date required'></div>\n                    <div class='type_id required'></div>\n                    <div class='start required'></div>\n                    <div class='end required'></div>\n                    <div class='km required'></div>\n                    <div class='description required'></div>\n            </div>\n            <div class=\"modal-footer\">\n                    <button\n                        class='btn btn-success primary-action'\n                        type='submit'\n                        value='submit'>\n                        "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n                    </button>\n                    <button\n                        class='btn btn-default secondary-action'\n                        type='reset'\n                        value='submit'>\n                        Annuler\n                    </button>\n            </div>\n        </form>\n    </div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n";
	},"useData":true});

/***/ }),
/* 89 */
/*!*******************************************************!*\
  !*** ./src/expense/views/ExpenseDuplicateFormView.js ***!
  \*******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _ModalBehavior = __webpack_require__(/*! ../../base/behaviors/ModalBehavior.js */ 50);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	var _SelectWidget = __webpack_require__(/*! ../../widgets/SelectWidget.js */ 80);
	
	var _SelectWidget2 = _interopRequireDefault(_SelectWidget);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 4);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : ExpenseDuplicateFormView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var ExpenseDuplicateFormView = _backbone2.default.View.extend({
	    behaviors: [_ModalBehavior2.default],
	    template: __webpack_require__(/*! ./templates/ExpenseDuplicateFormView.mustache */ 90),
	    regions: {
	        'select': '.select'
	    },
	    ui: {
	        cancel_btn: 'button[type=reset]',
	        form: 'form'
	    },
	    events: {
	        'submit @ui.form': 'onSubmit',
	        'click @ui.cancel_btn': 'onCancelClick'
	    },
	    initialize: function initialize() {
	        var channel = _backbone4.default.channel('config');
	        this.options = channel.request('get:options', 'expenses');
	    },
	    onCancelClick: function onCancelClick() {
	        this.triggerMethod('modal:close');
	    },
	    templateContext: function templateContext() {
	        var ht = this.model.getHT();
	        var tva = this.model.getTva();
	        var ttc = this.model.total();
	        var is_km_fee = this.model.get('type') == 'km';
	        return {
	            ht: (0, _math.formatAmount)(ht),
	            tva: (0, _math.formatAmount)(tva),
	            ttc: (0, _math.formatAmount)(ttc),
	            is_km_fee: is_km_fee
	        };
	    },
	    onRender: function onRender() {
	        var view = new _SelectWidget2.default({
	            options: this.options,
	            title: 'Feuille de note de dépenses vers laquelle dupliquer',
	            id_key: 'id',
	            field_name: 'sheet_id'
	        });
	        this.showChildView('select', view);
	    },
	    onSubmit: function onSubmit(event) {
	        event.preventDefault();
	        var datas = (0, _tools.serializeForm)(this.getUI('form'));
	        var request = this.model.duplicate(datas);
	        var this_ = this;
	        request.done(function () {
	            this_.triggerMethod('modal:close');
	        });
	    }
	});
	exports.default = ExpenseDuplicateFormView;

/***/ }),
/* 90 */
/*!***********************************************************************!*\
  !*** ./src/expense/views/templates/ExpenseDuplicateFormView.mustache ***!
  \***********************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "                <h3>Note de dépenses kilométriques</h3>\n                De "
	    + escapeExpression(((helper = (helper = helpers.start || (depth0 != null ? depth0.start : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"start","hash":{},"data":data}) : helper)))
	    + " à "
	    + escapeExpression(((helper = (helper = helpers.end || (depth0 != null ? depth0.end : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"end","hash":{},"data":data}) : helper)))
	    + " ( "
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + " )<br />\n                Nombre de kilomètres : "
	    + escapeExpression(((helper = (helper = helpers.km || (depth0 != null ? depth0.km : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"km","hash":{},"data":data}) : helper)))
	    + " <br />\n                Montant remboursé : ";
	  stack1 = ((helper = (helper = helpers.ttc || (depth0 != null ? depth0.ttc : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ttc","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\n";
	},"3":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "                <h3>Note de dépenses</h3>\n                "
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + "<br />\n                HT : ";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "<br />\n                TVA : ";
	  stack1 = ((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<div class=\"modal-dialog\" role=\"document\">\n    <div class=\"modal-content\">\n        <form>\n            <div class=\"modal-header\">\n              <button tabindex='-1' type=\"button\" class=\"close\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n              <h4 class=\"modal-title\">Dupliquer une note de dépense</h4>\n            </div>\n            <div class=\"modal-body\">\n                <div class='well'>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_km_fee : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "                </div>\n                <div class='select'></div>\n            </div>\n            <div class=\"modal-footer\">\n                <button\n                    class='btn btn-success primary-action'\n                    type='submit'\n                    value='submit'>\n                    Dupliquer\n                </button>\n                <button\n                    class='btn btn-default secondary-action'\n                    type='reset'\n                    value='submit'>\n                    Annuler\n                </button>\n            </div>\n        </form>\n    </div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n\n";
	},"useData":true});

/***/ }),
/* 91 */
/*!****************************************!*\
  !*** ./src/expense/views/TotalView.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TotalView = _backbone2.default.View.extend({
	    tagName: 'div',
	    template: __webpack_require__(/*! ./templates/TotalView.mustache */ 92),
	    modelEvents: {
	        'change:ttc': 'render',
	        'change:ht': 'render',
	        'change:tva': 'render',
	        'change:km_ht': 'render',
	        'change:km_tva': 'render',
	        'change:km_ttc': 'render',
	        'change:km': 'render'
	    },
	    templateContext: function templateContext() {
	        return {
	            ht: (0, _math.formatAmount)(this.model.get('ht') + this.model.get('km_ht')),
	            tva: (0, _math.formatAmount)(this.model.get('tva') + this.model.get('km_tva')),
	            ttc: (0, _math.formatAmount)(this.model.get('ttc') + this.model.get('km_ttc')),
	            km: (0, _math.formatPrice)(this.model.get('km'))
	        };
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
/* 92 */
/*!********************************************************!*\
  !*** ./src/expense/views/templates/TotalView.mustache ***!
  \********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class='totals form-section'>\n    <div class=\"text-center\">Total HT : ";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n    <div class=\"text-center\">Total TVA : ";
	  stack1 = ((helper = (helper = helpers.tva || (depth0 != null ? depth0.tva : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tva","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n    <div class=\"text-center\">Total TTC : ";
	  stack1 = ((helper = (helper = helpers.ttc || (depth0 != null ? depth0.ttc : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ttc","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n    <div class=\"text-center\">Total Km : ";
	  stack1 = ((helper = (helper = helpers.km || (depth0 != null ? depth0.km : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"km","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "&nbsp;km</div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 93 */
/*!*******************************************!*\
  !*** ./src/expense/views/TabTotalView.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _math = __webpack_require__(/*! ../../math.js */ 6);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TabTotalView = _backbone2.default.View.extend({
	    tagName: 'div',
	    template: __webpack_require__(/*! ./templates/TabTotalView.mustache */ 94),
	    modelEvents: {
	        'change:ttc': 'render',
	        'change:km_ttc': 'render'
	    },
	    templateContext: function templateContext() {
	        var category = this.getOption('category');
	        return {
	            ttc: (0, _math.formatAmount)(this.model.get('ttc_' + category) + this.model.get('km_ttc_' + category))
	        };
	    }
	}); /*
	     * File Name : TabTotalView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = TabTotalView;

/***/ }),
/* 94 */
/*!***********************************************************!*\
  !*** ./src/expense/views/templates/TabTotalView.mustache ***!
  \***********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class='totals form-section'>\n    <div class=\"text-center\">Total TTC : ";
	  stack1 = ((helper = (helper = helpers.ttc || (depth0 != null ? depth0.ttc : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ttc","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 95 */
/*!***************************************!*\
  !*** ./src/base/views/MessageView.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone */ 24);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _backbone5 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone6 = _interopRequireDefault(_backbone5);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var MessageView = _backbone2.default.View.extend({
	    tagName: 'div',
	    template: __webpack_require__(/*! ./templates/MessageView.mustache */ 96),
	    ui: {
	        close: 'span.link'
	    },
	    events: {
	        'click @ui.close': 'onClose'
	    },
	    modelEvents: {
	        "change:notifyClass": 'render'
	    },
	    className: 'messages-static-top text-center alert',
	    onClose: function onClose() {
	        this.model.set({ notifyText: null });
	        this.$el.hide();
	    },
	    initialize: function initialize() {
	        var channel = _backbone6.default.channel('message');
	        channel.reply({
	            'notify:success': this.notifySuccess.bind(this),
	            'notify:error': this.notifyError.bind(this)
	        });
	    },
	    notifyError: function notifyError(message) {
	        console.log("Notify error");
	        this.model.set({
	            notifyClass: 'error',
	            notifyText: message
	        });
	        this.$el.removeClass('alert-success');
	        this.$el.addClass('alert-danger');
	        this.$el.show();
	    },
	    notifySuccess: function notifySuccess(message) {
	        console.log("Notify success");
	        this.model.set({
	            notifyClass: 'success',
	            notifyText: message
	        });
	        this.$el.removeClass('alert-danger');
	        this.$el.addClass('alert-success');
	        this.$el.show();
	    },
	    templateContext: function templateContext() {
	        var has_message = false;
	        if (this.model.get('notifyText')) {
	            has_message = true;
	        }
	        return {
	            has_message: has_message,
	            error: this.model.get('notifyClass') == 'error'
	        };
	    }
	}); /*
	     * File Name : MessageView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = MessageView;

/***/ }),
/* 96 */
/*!*******************************************************!*\
  !*** ./src/base/views/templates/MessageView.mustache ***!
  \*******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.error : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.program(4, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  stack1 = ((helper = (helper = helpers.notifyText || (depth0 != null ? depth0.notifyText : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"notifyText","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\n<span class='link'><i class='glyphicon glyphicon-remove'></i></span>\n";
	},"2":function(depth0,helpers,partials,data) {
	  return "<i class='glyphicon glyphicon-warning-sign'></i>&nbsp;\n";
	  },"4":function(depth0,helpers,partials,data) {
	  return "<i class='glyphicon glyphicon-ok'></i>&nbsp;\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.has_message : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 97 */
/*!*******************************************************!*\
  !*** ./src/expense/views/templates/MainView.mustache ***!
  \*******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 39);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div class='row'>\n    <div class='col-xs-12 col-md-9 col-print-12'>\n        <div class='messages-container'></div>\n        <div class='modalRegion'></div>\n        <div class='totals'></div>\n        <div class='form-section'>\n            <div class='content'>\n                <ul class=\"nav nav-tabs\" role=\"tablist\">\n                    <li role=\"presentation\" class=\"active\">\n                        <a href=\"#internal-container\"\n                            aria-controls=\"internal-container\"\n                            role=\"tab\"\n                            data-toggle=\"tab\">\n                            Frais\n                        </a>\n                    </li>\n                    <li role=\"presentation\">\n                        <a href=\"#activity-container\"\n                            aria-controls=\"activity-container\"\n                            role=\"tab\"\n                            data-toggle=\"tab\">\n                            Achats\n                        </a>\n                    </li>\n                </ul>\n                <div class='tab-content content'>\n                    <div\n                        role=\"tabpanel\"\n                        class=\"tab-pane fade in active\"\n                        id=\"internal-container\">\n                        <div class='internal-lines'>\n                        </div>\n                        <div class='internal-kmlines'>\n                        <div class='alert alert-warning'>Il n'est pas encore possible de configurer des frais kilométriques sur cette année</div>\n                        </div>\n                        <div class='internal-total'>\n                        </div>\n                    </div>\n                    <div\n                        role=\"tabpanel\"\n                        class=\"tab-pane fade\"\n                        id=\"activity-container\">\n                        <div class='activity-lines'>\n                        </div>\n                        <div class='activity-kmlines'>\n                        <div class='alert alert-warning'>Il n'est pas encore possible de configurer des frais kilométriques sur cette année</div>\n                        </div>\n                        <div class='activity-total'>\n                        </div>\n                    </div>\n                </div>\n            </div>\n        </div>\n    </div>\n    <div\n        class='expense-desktop-actions hidden-xs hidden-sm col-md-3 hidden-print'\n        id=\"rightbar\"\n        >\n    </div>\n</div>\n<footer class='footer-actions hidden-print'></footer>\n";
	  },"useData":true});

/***/ }),
/* 98 */
/*!******************************************!*\
  !*** ./src/expense/components/Facade.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TotalModel = __webpack_require__(/*! ../models/TotalModel.js */ 99);
	
	var _TotalModel2 = _interopRequireDefault(_TotalModel);
	
	var _ExpenseCollection = __webpack_require__(/*! ../models/ExpenseCollection.js */ 100);
	
	var _ExpenseCollection2 = _interopRequireDefault(_ExpenseCollection);
	
	var _ExpenseKmCollection = __webpack_require__(/*! ../models/ExpenseKmCollection.js */ 101);
	
	var _ExpenseKmCollection2 = _interopRequireDefault(_ExpenseKmCollection);
	
	var _BookMarkCollection = __webpack_require__(/*! ../models/BookMarkCollection.js */ 102);
	
	var _BookMarkCollection2 = _interopRequireDefault(_BookMarkCollection);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var FacadeClass = _backbone2.default.Object.extend({
	    channelName: 'facade',
	    radioEvents: {
	        "changed:line": "computeLineTotal",
	        "changed:kmline": "computeKmLineTotal"
	    },
	    radioRequests: {
	        'get:collection': 'getCollectionRequest',
	        'get:totalmodel': 'getTotalModelRequest',
	        'get:bookmarks': 'getBookMarks'
	        // 'get:paymentcollection': 'getPaymentCollectionRequest',
	        // 'get:totalmodel': 'getTotalModelRequest',
	        // 'get:status_history_collection': 'getStatusHistory',
	        // 'is:valid': "isDataValid",
	        // 'get:attachments': 'getAttachments',
	    },
	    loadModels: function loadModels(form_datas, form_config) {
	        this.datas = form_datas;
	        this.models = {};
	        this.collections = {};
	        this.totalmodel = new _TotalModel2.default();
	
	        var lines = form_datas['lines'];
	        this.collections['lines'] = new _ExpenseCollection2.default(lines);
	
	        var kmlines = form_datas['kmlines'];
	        this.collections['kmlines'] = new _ExpenseKmCollection2.default(kmlines);
	
	        this.bookmarks = new _BookMarkCollection2.default(form_config.options.bookmarks);
	
	        this.computeLineTotal();
	        this.computeKmLineTotal();
	    },
	    getBookMarks: function getBookMarks() {
	        return this.bookmarks;
	    },
	    computeLineTotal: function computeLineTotal(category) {
	        /*
	         * compute the line totals for the given category
	         */
	        var categories;
	        if (_.isUndefined(category)) {
	            categories = ['1', '2'];
	        } else {
	            categories = [category];
	        }
	        var collection = this.collections['lines'];
	        var datas = {};
	        _.each(categories, function (category) {
	            datas['ht_' + category] = collection.total_ht(category);
	            datas['tva_' + category] = collection.total_tva(category);
	            datas['ttc_' + category] = collection.total(category);
	        });
	        datas['ht'] = collection.total_ht();
	        datas['tva'] = collection.total_tva();
	        datas['ttc'] = collection.total();
	        this.totalmodel.set(datas);
	        var channel = this.getChannel();
	        _.each(categories, function (category) {
	            channel.trigger('change:lines_' + category);
	        });
	    },
	    computeKmLineTotal: function computeKmLineTotal(category) {
	        /*
	         * Compute the kmline totals for the given category
	         */
	        var categories;
	        if (_.isUndefined(category)) {
	            categories = ['1', '2'];
	        } else {
	            categories = [category];
	        }
	        var collection = this.collections['kmlines'];
	        var datas = {};
	        _.each(categories, function (category) {
	            datas['km_' + category] = collection.total_km(category);
	            datas['km_ttc_' + category] = collection.total(category);
	        });
	        datas['km_tva'] = collection.total_tva();
	        datas['km_ht'] = collection.total_ht();
	        datas['km'] = collection.total_km();
	        datas['km_ttc'] = collection.total();
	        this.totalmodel.set(datas);
	
	        var channel = this.getChannel();
	        _.each(categories, function (category) {
	            channel.trigger('change:kmlines_' + category);
	        });
	    },
	    getCollectionRequest: function getCollectionRequest(label) {
	        return this.collections[label];
	    },
	    getTotalModelRequest: function getTotalModelRequest() {
	        return this.totalmodel;
	    }
	}); /*
	     * File Name : Facade.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	
	var Facade = new FacadeClass();
	exports.default = Facade;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 99 */
/*!******************************************!*\
  !*** ./src/expense/models/TotalModel.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 24);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TotalModel = _backbone2.default.Model.extend({}); /*
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
/* 100 */
/*!*************************************************!*\
  !*** ./src/expense/models/ExpenseCollection.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 24);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ExpenseModel = __webpack_require__(/*! ./ExpenseModel.js */ 54);
	
	var _ExpenseModel2 = _interopRequireDefault(_ExpenseModel);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseCollection = _backbone2.default.Collection.extend({
	  /*
	   *  Collection of expense lines
	   */
	  model: _ExpenseModel2.default,
	  initialize: function initialize() {
	    this.on('remove', this.channelCall);
	    this.on('sync', this.channelCall);
	    this.on('reset', this.channelCall);
	    this.on('add', this.channelCall);
	  },
	
	  channelCall: function channelCall(model) {
	    console.log("Triggering Channel call");
	    var channel = _backbone4.default.channel('facade');
	    channel.trigger('changed:line', model.get('category'));
	  },
	  url: function url() {
	    return AppOption['context_url'] + "/lines";
	  },
	
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
	}); /*
	     * File Name : ExpenseCollection.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseCollection;

/***/ }),
/* 101 */
/*!***************************************************!*\
  !*** ./src/expense/models/ExpenseKmCollection.js ***!
  \***************************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 24);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ExpenseKmModel = __webpack_require__(/*! ./ExpenseKmModel.js */ 56);
	
	var _ExpenseKmModel2 = _interopRequireDefault(_ExpenseKmModel);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ExpenseKmCollection = _backbone2.default.Collection.extend({
	  /*
	   * Collection for expenses related to km fees
	   */
	  model: _ExpenseKmModel2.default,
	  initialize: function initialize() {
	    this.on('remove', this.channelCall);
	    this.on('sync', this.channelCall);
	    this.on('reset', this.channelCall);
	    this.on('add', this.channelCall);
	  },
	
	  channelCall: function channelCall(model) {
	    var channel = _backbone4.default.channel('facade');
	    channel.trigger('changed:kmline', model.get('category'));
	  },
	  url: function url() {
	    return AppOption['context_url'] + '/kmlines';
	  },
	
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
	  total_tva: function total_tva(category) {
	    return 0;
	  },
	  total_ht: function total_ht(category) {
	    return this.total(category);
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
	}); /*
	     * File Name : ExpenseKmCollection.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ExpenseKmCollection;

/***/ }),
/* 102 */
/*!**************************************************!*\
  !*** ./src/expense/models/BookMarkCollection.js ***!
  \**************************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 24);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ExpenseModel = __webpack_require__(/*! ./ExpenseModel.js */ 54);
	
	var _ExpenseModel2 = _interopRequireDefault(_ExpenseModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : BookMarkCollection.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var BookMarkCollection = _backbone2.default.Collection.extend({
	    url: "/api/v1/bookmarks",
	    model: _ExpenseModel2.default,
	    addBookMark: function addBookMark(model) {
	        var _ref;
	
	        var keys = ['ht', 'tva', 'km', 'start', 'end', 'description', 'type_id', 'category'];
	        console.log(model);
	        var attributes = (_ref = _).pick.apply(_ref, [model.attributes].concat(keys));
	        console.log(attributes);
	        this.create(attributes, { wait: true });
	    }
	});
	exports.default = BookMarkCollection;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 1)))

/***/ }),
/* 103 */
/*!****************************************!*\
  !*** ./src/base/components/AuthBus.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 4);
	
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
/* 104 */
/*!*******************************************!*\
  !*** ./src/base/components/MessageBus.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
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
/* 105 */
/*!******************************************!*\
  !*** ./src/base/components/ConfigBus.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 25);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 26);
	
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

/***/ })
]);
//# sourceMappingURL=expense.js.map