webpackJsonp([0],[
/* 0 */
/*!***************************!*\
  !*** ./src/base_setup.js ***!
  \***************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	var _underscore = __webpack_require__(/*! underscore */ 1);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _jquery = __webpack_require__(/*! jquery */ 2);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : base_setup.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	
	/*
	 * Setup the main ui elements
	 */
	(0, _jquery2.default)(function () {
	    var company_menu = (0, _jquery2.default)('company-select-menu');
	    if (!_underscore2.default.isNull(company_menu)) {
	        company_menu.on('change', function () {
	            window.location = this.value;
	        });
	    }
	    (0, _jquery2.default)('a[data-toggle=dropdown]').dropdown();
	});

/***/ })
]);
//# sourceMappingURL=base_setup.js.map