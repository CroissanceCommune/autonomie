webpackJsonp([0],[
/* 0 */
/*!**************************!*\
  !*** ./src/task/task.js ***!
  \**************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	var _jquery = __webpack_require__(/*! jquery */ 1);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	__webpack_require__(/*! bootstrap/dist/js/bootstrap */ 2);
	
	var _bootstrap = __webpack_require__(/*! bootstrap */ 3);
	
	var _bootstrap2 = _interopRequireDefault(_bootstrap);
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
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
	
	var _tools = __webpack_require__(/*! ../tools.js */ 27);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/* global AppOptions; */
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
	(0, _tools.setupJsonRedirect)();
	
	var template = __webpack_require__(/*! ../handlebars/job/file_generation.mustache */ 100);
	
	_App2.default.on('start', function (app, options) {
	    console.log("  => Starting the app");
	    AppOption['form_options'] = options.form_options;
	    (0, _backboneTools.setupBbValidationCallbacks)(_backboneValidation2.default.callbacks);
	    (0, _backboneTools.setupBbValidationPatterns)(_backboneValidation2.default);
	    var controller = new _Controller2.default(options.form_datas);
	    var router = new _Router2.default({ controller: controller });
	    _backbone2.default.history.start();
	});
	
	(0, _jquery2.default)(function () {
	    console.log("# Retrieving datas from the server");
	    console.log(AppOption['load_url']);
	    var serverCall1 = (0, _tools.ajax_call)(AppOption['load_url']);
	    console.log(AppOption['context_url']);
	    var serverCall2 = (0, _tools.ajax_call)(AppOption['context_url']);
	
	    _jquery2.default.when(serverCall1, serverCall2).done(function (result1, result2) {
	        console.log("  => Datas retrieved");
	        _App2.default.start({
	            form_options: result1[0],
	            form_datas: result2[0]
	        });
	    });
	});

/***/ }),
/* 1 */,
/* 2 */
/*!******************************************!*\
  !*** ./~/bootstrap/dist/js/bootstrap.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/*!
	 * Bootstrap v3.3.7 (http://getbootstrap.com)
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under the MIT license
	 */
	
	if (typeof jQuery === 'undefined') {
	  throw new Error('Bootstrap\'s JavaScript requires jQuery')
	}
	
	+function ($) {
	  'use strict';
	  var version = $.fn.jquery.split(' ')[0].split('.')
	  if ((version[0] < 2 && version[1] < 9) || (version[0] == 1 && version[1] == 9 && version[2] < 1) || (version[0] > 3)) {
	    throw new Error('Bootstrap\'s JavaScript requires jQuery version 1.9.1 or higher, but lower than version 4')
	  }
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: transition.js v3.3.7
	 * http://getbootstrap.com/javascript/#transitions
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // CSS TRANSITION SUPPORT (Shoutout: http://www.modernizr.com/)
	  // ============================================================
	
	  function transitionEnd() {
	    var el = document.createElement('bootstrap')
	
	    var transEndEventNames = {
	      WebkitTransition : 'webkitTransitionEnd',
	      MozTransition    : 'transitionend',
	      OTransition      : 'oTransitionEnd otransitionend',
	      transition       : 'transitionend'
	    }
	
	    for (var name in transEndEventNames) {
	      if (el.style[name] !== undefined) {
	        return { end: transEndEventNames[name] }
	      }
	    }
	
	    return false // explicit for ie8 (  ._.)
	  }
	
	  // http://blog.alexmaccaw.com/css-transitions
	  $.fn.emulateTransitionEnd = function (duration) {
	    var called = false
	    var $el = this
	    $(this).one('bsTransitionEnd', function () { called = true })
	    var callback = function () { if (!called) $($el).trigger($.support.transition.end) }
	    setTimeout(callback, duration)
	    return this
	  }
	
	  $(function () {
	    $.support.transition = transitionEnd()
	
	    if (!$.support.transition) return
	
	    $.event.special.bsTransitionEnd = {
	      bindType: $.support.transition.end,
	      delegateType: $.support.transition.end,
	      handle: function (e) {
	        if ($(e.target).is(this)) return e.handleObj.handler.apply(this, arguments)
	      }
	    }
	  })
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: alert.js v3.3.7
	 * http://getbootstrap.com/javascript/#alerts
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // ALERT CLASS DEFINITION
	  // ======================
	
	  var dismiss = '[data-dismiss="alert"]'
	  var Alert   = function (el) {
	    $(el).on('click', dismiss, this.close)
	  }
	
	  Alert.VERSION = '3.3.7'
	
	  Alert.TRANSITION_DURATION = 150
	
	  Alert.prototype.close = function (e) {
	    var $this    = $(this)
	    var selector = $this.attr('data-target')
	
	    if (!selector) {
	      selector = $this.attr('href')
	      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
	    }
	
	    var $parent = $(selector === '#' ? [] : selector)
	
	    if (e) e.preventDefault()
	
	    if (!$parent.length) {
	      $parent = $this.closest('.alert')
	    }
	
	    $parent.trigger(e = $.Event('close.bs.alert'))
	
	    if (e.isDefaultPrevented()) return
	
	    $parent.removeClass('in')
	
	    function removeElement() {
	      // detach from parent, fire event then clean up data
	      $parent.detach().trigger('closed.bs.alert').remove()
	    }
	
	    $.support.transition && $parent.hasClass('fade') ?
	      $parent
	        .one('bsTransitionEnd', removeElement)
	        .emulateTransitionEnd(Alert.TRANSITION_DURATION) :
	      removeElement()
	  }
	
	
	  // ALERT PLUGIN DEFINITION
	  // =======================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this = $(this)
	      var data  = $this.data('bs.alert')
	
	      if (!data) $this.data('bs.alert', (data = new Alert(this)))
	      if (typeof option == 'string') data[option].call($this)
	    })
	  }
	
	  var old = $.fn.alert
	
	  $.fn.alert             = Plugin
	  $.fn.alert.Constructor = Alert
	
	
	  // ALERT NO CONFLICT
	  // =================
	
	  $.fn.alert.noConflict = function () {
	    $.fn.alert = old
	    return this
	  }
	
	
	  // ALERT DATA-API
	  // ==============
	
	  $(document).on('click.bs.alert.data-api', dismiss, Alert.prototype.close)
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: button.js v3.3.7
	 * http://getbootstrap.com/javascript/#buttons
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // BUTTON PUBLIC CLASS DEFINITION
	  // ==============================
	
	  var Button = function (element, options) {
	    this.$element  = $(element)
	    this.options   = $.extend({}, Button.DEFAULTS, options)
	    this.isLoading = false
	  }
	
	  Button.VERSION  = '3.3.7'
	
	  Button.DEFAULTS = {
	    loadingText: 'loading...'
	  }
	
	  Button.prototype.setState = function (state) {
	    var d    = 'disabled'
	    var $el  = this.$element
	    var val  = $el.is('input') ? 'val' : 'html'
	    var data = $el.data()
	
	    state += 'Text'
	
	    if (data.resetText == null) $el.data('resetText', $el[val]())
	
	    // push to event loop to allow forms to submit
	    setTimeout($.proxy(function () {
	      $el[val](data[state] == null ? this.options[state] : data[state])
	
	      if (state == 'loadingText') {
	        this.isLoading = true
	        $el.addClass(d).attr(d, d).prop(d, true)
	      } else if (this.isLoading) {
	        this.isLoading = false
	        $el.removeClass(d).removeAttr(d).prop(d, false)
	      }
	    }, this), 0)
	  }
	
	  Button.prototype.toggle = function () {
	    var changed = true
	    var $parent = this.$element.closest('[data-toggle="buttons"]')
	
	    if ($parent.length) {
	      var $input = this.$element.find('input')
	      if ($input.prop('type') == 'radio') {
	        if ($input.prop('checked')) changed = false
	        $parent.find('.active').removeClass('active')
	        this.$element.addClass('active')
	      } else if ($input.prop('type') == 'checkbox') {
	        if (($input.prop('checked')) !== this.$element.hasClass('active')) changed = false
	        this.$element.toggleClass('active')
	      }
	      $input.prop('checked', this.$element.hasClass('active'))
	      if (changed) $input.trigger('change')
	    } else {
	      this.$element.attr('aria-pressed', !this.$element.hasClass('active'))
	      this.$element.toggleClass('active')
	    }
	  }
	
	
	  // BUTTON PLUGIN DEFINITION
	  // ========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.button')
	      var options = typeof option == 'object' && option
	
	      if (!data) $this.data('bs.button', (data = new Button(this, options)))
	
	      if (option == 'toggle') data.toggle()
	      else if (option) data.setState(option)
	    })
	  }
	
	  var old = $.fn.button
	
	  $.fn.button             = Plugin
	  $.fn.button.Constructor = Button
	
	
	  // BUTTON NO CONFLICT
	  // ==================
	
	  $.fn.button.noConflict = function () {
	    $.fn.button = old
	    return this
	  }
	
	
	  // BUTTON DATA-API
	  // ===============
	
	  $(document)
	    .on('click.bs.button.data-api', '[data-toggle^="button"]', function (e) {
	      var $btn = $(e.target).closest('.btn')
	      Plugin.call($btn, 'toggle')
	      if (!($(e.target).is('input[type="radio"], input[type="checkbox"]'))) {
	        // Prevent double click on radios, and the double selections (so cancellation) on checkboxes
	        e.preventDefault()
	        // The target component still receive the focus
	        if ($btn.is('input,button')) $btn.trigger('focus')
	        else $btn.find('input:visible,button:visible').first().trigger('focus')
	      }
	    })
	    .on('focus.bs.button.data-api blur.bs.button.data-api', '[data-toggle^="button"]', function (e) {
	      $(e.target).closest('.btn').toggleClass('focus', /^focus(in)?$/.test(e.type))
	    })
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: carousel.js v3.3.7
	 * http://getbootstrap.com/javascript/#carousel
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // CAROUSEL CLASS DEFINITION
	  // =========================
	
	  var Carousel = function (element, options) {
	    this.$element    = $(element)
	    this.$indicators = this.$element.find('.carousel-indicators')
	    this.options     = options
	    this.paused      = null
	    this.sliding     = null
	    this.interval    = null
	    this.$active     = null
	    this.$items      = null
	
	    this.options.keyboard && this.$element.on('keydown.bs.carousel', $.proxy(this.keydown, this))
	
	    this.options.pause == 'hover' && !('ontouchstart' in document.documentElement) && this.$element
	      .on('mouseenter.bs.carousel', $.proxy(this.pause, this))
	      .on('mouseleave.bs.carousel', $.proxy(this.cycle, this))
	  }
	
	  Carousel.VERSION  = '3.3.7'
	
	  Carousel.TRANSITION_DURATION = 600
	
	  Carousel.DEFAULTS = {
	    interval: 5000,
	    pause: 'hover',
	    wrap: true,
	    keyboard: true
	  }
	
	  Carousel.prototype.keydown = function (e) {
	    if (/input|textarea/i.test(e.target.tagName)) return
	    switch (e.which) {
	      case 37: this.prev(); break
	      case 39: this.next(); break
	      default: return
	    }
	
	    e.preventDefault()
	  }
	
	  Carousel.prototype.cycle = function (e) {
	    e || (this.paused = false)
	
	    this.interval && clearInterval(this.interval)
	
	    this.options.interval
	      && !this.paused
	      && (this.interval = setInterval($.proxy(this.next, this), this.options.interval))
	
	    return this
	  }
	
	  Carousel.prototype.getItemIndex = function (item) {
	    this.$items = item.parent().children('.item')
	    return this.$items.index(item || this.$active)
	  }
	
	  Carousel.prototype.getItemForDirection = function (direction, active) {
	    var activeIndex = this.getItemIndex(active)
	    var willWrap = (direction == 'prev' && activeIndex === 0)
	                || (direction == 'next' && activeIndex == (this.$items.length - 1))
	    if (willWrap && !this.options.wrap) return active
	    var delta = direction == 'prev' ? -1 : 1
	    var itemIndex = (activeIndex + delta) % this.$items.length
	    return this.$items.eq(itemIndex)
	  }
	
	  Carousel.prototype.to = function (pos) {
	    var that        = this
	    var activeIndex = this.getItemIndex(this.$active = this.$element.find('.item.active'))
	
	    if (pos > (this.$items.length - 1) || pos < 0) return
	
	    if (this.sliding)       return this.$element.one('slid.bs.carousel', function () { that.to(pos) }) // yes, "slid"
	    if (activeIndex == pos) return this.pause().cycle()
	
	    return this.slide(pos > activeIndex ? 'next' : 'prev', this.$items.eq(pos))
	  }
	
	  Carousel.prototype.pause = function (e) {
	    e || (this.paused = true)
	
	    if (this.$element.find('.next, .prev').length && $.support.transition) {
	      this.$element.trigger($.support.transition.end)
	      this.cycle(true)
	    }
	
	    this.interval = clearInterval(this.interval)
	
	    return this
	  }
	
	  Carousel.prototype.next = function () {
	    if (this.sliding) return
	    return this.slide('next')
	  }
	
	  Carousel.prototype.prev = function () {
	    if (this.sliding) return
	    return this.slide('prev')
	  }
	
	  Carousel.prototype.slide = function (type, next) {
	    var $active   = this.$element.find('.item.active')
	    var $next     = next || this.getItemForDirection(type, $active)
	    var isCycling = this.interval
	    var direction = type == 'next' ? 'left' : 'right'
	    var that      = this
	
	    if ($next.hasClass('active')) return (this.sliding = false)
	
	    var relatedTarget = $next[0]
	    var slideEvent = $.Event('slide.bs.carousel', {
	      relatedTarget: relatedTarget,
	      direction: direction
	    })
	    this.$element.trigger(slideEvent)
	    if (slideEvent.isDefaultPrevented()) return
	
	    this.sliding = true
	
	    isCycling && this.pause()
	
	    if (this.$indicators.length) {
	      this.$indicators.find('.active').removeClass('active')
	      var $nextIndicator = $(this.$indicators.children()[this.getItemIndex($next)])
	      $nextIndicator && $nextIndicator.addClass('active')
	    }
	
	    var slidEvent = $.Event('slid.bs.carousel', { relatedTarget: relatedTarget, direction: direction }) // yes, "slid"
	    if ($.support.transition && this.$element.hasClass('slide')) {
	      $next.addClass(type)
	      $next[0].offsetWidth // force reflow
	      $active.addClass(direction)
	      $next.addClass(direction)
	      $active
	        .one('bsTransitionEnd', function () {
	          $next.removeClass([type, direction].join(' ')).addClass('active')
	          $active.removeClass(['active', direction].join(' '))
	          that.sliding = false
	          setTimeout(function () {
	            that.$element.trigger(slidEvent)
	          }, 0)
	        })
	        .emulateTransitionEnd(Carousel.TRANSITION_DURATION)
	    } else {
	      $active.removeClass('active')
	      $next.addClass('active')
	      this.sliding = false
	      this.$element.trigger(slidEvent)
	    }
	
	    isCycling && this.cycle()
	
	    return this
	  }
	
	
	  // CAROUSEL PLUGIN DEFINITION
	  // ==========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.carousel')
	      var options = $.extend({}, Carousel.DEFAULTS, $this.data(), typeof option == 'object' && option)
	      var action  = typeof option == 'string' ? option : options.slide
	
	      if (!data) $this.data('bs.carousel', (data = new Carousel(this, options)))
	      if (typeof option == 'number') data.to(option)
	      else if (action) data[action]()
	      else if (options.interval) data.pause().cycle()
	    })
	  }
	
	  var old = $.fn.carousel
	
	  $.fn.carousel             = Plugin
	  $.fn.carousel.Constructor = Carousel
	
	
	  // CAROUSEL NO CONFLICT
	  // ====================
	
	  $.fn.carousel.noConflict = function () {
	    $.fn.carousel = old
	    return this
	  }
	
	
	  // CAROUSEL DATA-API
	  // =================
	
	  var clickHandler = function (e) {
	    var href
	    var $this   = $(this)
	    var $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) // strip for ie7
	    if (!$target.hasClass('carousel')) return
	    var options = $.extend({}, $target.data(), $this.data())
	    var slideIndex = $this.attr('data-slide-to')
	    if (slideIndex) options.interval = false
	
	    Plugin.call($target, options)
	
	    if (slideIndex) {
	      $target.data('bs.carousel').to(slideIndex)
	    }
	
	    e.preventDefault()
	  }
	
	  $(document)
	    .on('click.bs.carousel.data-api', '[data-slide]', clickHandler)
	    .on('click.bs.carousel.data-api', '[data-slide-to]', clickHandler)
	
	  $(window).on('load', function () {
	    $('[data-ride="carousel"]').each(function () {
	      var $carousel = $(this)
	      Plugin.call($carousel, $carousel.data())
	    })
	  })
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: collapse.js v3.3.7
	 * http://getbootstrap.com/javascript/#collapse
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	/* jshint latedef: false */
	
	+function ($) {
	  'use strict';
	
	  // COLLAPSE PUBLIC CLASS DEFINITION
	  // ================================
	
	  var Collapse = function (element, options) {
	    this.$element      = $(element)
	    this.options       = $.extend({}, Collapse.DEFAULTS, options)
	    this.$trigger      = $('[data-toggle="collapse"][href="#' + element.id + '"],' +
	                           '[data-toggle="collapse"][data-target="#' + element.id + '"]')
	    this.transitioning = null
	
	    if (this.options.parent) {
	      this.$parent = this.getParent()
	    } else {
	      this.addAriaAndCollapsedClass(this.$element, this.$trigger)
	    }
	
	    if (this.options.toggle) this.toggle()
	  }
	
	  Collapse.VERSION  = '3.3.7'
	
	  Collapse.TRANSITION_DURATION = 350
	
	  Collapse.DEFAULTS = {
	    toggle: true
	  }
	
	  Collapse.prototype.dimension = function () {
	    var hasWidth = this.$element.hasClass('width')
	    return hasWidth ? 'width' : 'height'
	  }
	
	  Collapse.prototype.show = function () {
	    if (this.transitioning || this.$element.hasClass('in')) return
	
	    var activesData
	    var actives = this.$parent && this.$parent.children('.panel').children('.in, .collapsing')
	
	    if (actives && actives.length) {
	      activesData = actives.data('bs.collapse')
	      if (activesData && activesData.transitioning) return
	    }
	
	    var startEvent = $.Event('show.bs.collapse')
	    this.$element.trigger(startEvent)
	    if (startEvent.isDefaultPrevented()) return
	
	    if (actives && actives.length) {
	      Plugin.call(actives, 'hide')
	      activesData || actives.data('bs.collapse', null)
	    }
	
	    var dimension = this.dimension()
	
	    this.$element
	      .removeClass('collapse')
	      .addClass('collapsing')[dimension](0)
	      .attr('aria-expanded', true)
	
	    this.$trigger
	      .removeClass('collapsed')
	      .attr('aria-expanded', true)
	
	    this.transitioning = 1
	
	    var complete = function () {
	      this.$element
	        .removeClass('collapsing')
	        .addClass('collapse in')[dimension]('')
	      this.transitioning = 0
	      this.$element
	        .trigger('shown.bs.collapse')
	    }
	
	    if (!$.support.transition) return complete.call(this)
	
	    var scrollSize = $.camelCase(['scroll', dimension].join('-'))
	
	    this.$element
	      .one('bsTransitionEnd', $.proxy(complete, this))
	      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)[dimension](this.$element[0][scrollSize])
	  }
	
	  Collapse.prototype.hide = function () {
	    if (this.transitioning || !this.$element.hasClass('in')) return
	
	    var startEvent = $.Event('hide.bs.collapse')
	    this.$element.trigger(startEvent)
	    if (startEvent.isDefaultPrevented()) return
	
	    var dimension = this.dimension()
	
	    this.$element[dimension](this.$element[dimension]())[0].offsetHeight
	
	    this.$element
	      .addClass('collapsing')
	      .removeClass('collapse in')
	      .attr('aria-expanded', false)
	
	    this.$trigger
	      .addClass('collapsed')
	      .attr('aria-expanded', false)
	
	    this.transitioning = 1
	
	    var complete = function () {
	      this.transitioning = 0
	      this.$element
	        .removeClass('collapsing')
	        .addClass('collapse')
	        .trigger('hidden.bs.collapse')
	    }
	
	    if (!$.support.transition) return complete.call(this)
	
	    this.$element
	      [dimension](0)
	      .one('bsTransitionEnd', $.proxy(complete, this))
	      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)
	  }
	
	  Collapse.prototype.toggle = function () {
	    this[this.$element.hasClass('in') ? 'hide' : 'show']()
	  }
	
	  Collapse.prototype.getParent = function () {
	    return $(this.options.parent)
	      .find('[data-toggle="collapse"][data-parent="' + this.options.parent + '"]')
	      .each($.proxy(function (i, element) {
	        var $element = $(element)
	        this.addAriaAndCollapsedClass(getTargetFromTrigger($element), $element)
	      }, this))
	      .end()
	  }
	
	  Collapse.prototype.addAriaAndCollapsedClass = function ($element, $trigger) {
	    var isOpen = $element.hasClass('in')
	
	    $element.attr('aria-expanded', isOpen)
	    $trigger
	      .toggleClass('collapsed', !isOpen)
	      .attr('aria-expanded', isOpen)
	  }
	
	  function getTargetFromTrigger($trigger) {
	    var href
	    var target = $trigger.attr('data-target')
	      || (href = $trigger.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') // strip for ie7
	
	    return $(target)
	  }
	
	
	  // COLLAPSE PLUGIN DEFINITION
	  // ==========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.collapse')
	      var options = $.extend({}, Collapse.DEFAULTS, $this.data(), typeof option == 'object' && option)
	
	      if (!data && options.toggle && /show|hide/.test(option)) options.toggle = false
	      if (!data) $this.data('bs.collapse', (data = new Collapse(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.collapse
	
	  $.fn.collapse             = Plugin
	  $.fn.collapse.Constructor = Collapse
	
	
	  // COLLAPSE NO CONFLICT
	  // ====================
	
	  $.fn.collapse.noConflict = function () {
	    $.fn.collapse = old
	    return this
	  }
	
	
	  // COLLAPSE DATA-API
	  // =================
	
	  $(document).on('click.bs.collapse.data-api', '[data-toggle="collapse"]', function (e) {
	    var $this   = $(this)
	
	    if (!$this.attr('data-target')) e.preventDefault()
	
	    var $target = getTargetFromTrigger($this)
	    var data    = $target.data('bs.collapse')
	    var option  = data ? 'toggle' : $this.data()
	
	    Plugin.call($target, option)
	  })
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: dropdown.js v3.3.7
	 * http://getbootstrap.com/javascript/#dropdowns
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // DROPDOWN CLASS DEFINITION
	  // =========================
	
	  var backdrop = '.dropdown-backdrop'
	  var toggle   = '[data-toggle="dropdown"]'
	  var Dropdown = function (element) {
	    $(element).on('click.bs.dropdown', this.toggle)
	  }
	
	  Dropdown.VERSION = '3.3.7'
	
	  function getParent($this) {
	    var selector = $this.attr('data-target')
	
	    if (!selector) {
	      selector = $this.attr('href')
	      selector = selector && /#[A-Za-z]/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
	    }
	
	    var $parent = selector && $(selector)
	
	    return $parent && $parent.length ? $parent : $this.parent()
	  }
	
	  function clearMenus(e) {
	    if (e && e.which === 3) return
	    $(backdrop).remove()
	    $(toggle).each(function () {
	      var $this         = $(this)
	      var $parent       = getParent($this)
	      var relatedTarget = { relatedTarget: this }
	
	      if (!$parent.hasClass('open')) return
	
	      if (e && e.type == 'click' && /input|textarea/i.test(e.target.tagName) && $.contains($parent[0], e.target)) return
	
	      $parent.trigger(e = $.Event('hide.bs.dropdown', relatedTarget))
	
	      if (e.isDefaultPrevented()) return
	
	      $this.attr('aria-expanded', 'false')
	      $parent.removeClass('open').trigger($.Event('hidden.bs.dropdown', relatedTarget))
	    })
	  }
	
	  Dropdown.prototype.toggle = function (e) {
	    var $this = $(this)
	
	    if ($this.is('.disabled, :disabled')) return
	
	    var $parent  = getParent($this)
	    var isActive = $parent.hasClass('open')
	
	    clearMenus()
	
	    if (!isActive) {
	      if ('ontouchstart' in document.documentElement && !$parent.closest('.navbar-nav').length) {
	        // if mobile we use a backdrop because click events don't delegate
	        $(document.createElement('div'))
	          .addClass('dropdown-backdrop')
	          .insertAfter($(this))
	          .on('click', clearMenus)
	      }
	
	      var relatedTarget = { relatedTarget: this }
	      $parent.trigger(e = $.Event('show.bs.dropdown', relatedTarget))
	
	      if (e.isDefaultPrevented()) return
	
	      $this
	        .trigger('focus')
	        .attr('aria-expanded', 'true')
	
	      $parent
	        .toggleClass('open')
	        .trigger($.Event('shown.bs.dropdown', relatedTarget))
	    }
	
	    return false
	  }
	
	  Dropdown.prototype.keydown = function (e) {
	    if (!/(38|40|27|32)/.test(e.which) || /input|textarea/i.test(e.target.tagName)) return
	
	    var $this = $(this)
	
	    e.preventDefault()
	    e.stopPropagation()
	
	    if ($this.is('.disabled, :disabled')) return
	
	    var $parent  = getParent($this)
	    var isActive = $parent.hasClass('open')
	
	    if (!isActive && e.which != 27 || isActive && e.which == 27) {
	      if (e.which == 27) $parent.find(toggle).trigger('focus')
	      return $this.trigger('click')
	    }
	
	    var desc = ' li:not(.disabled):visible a'
	    var $items = $parent.find('.dropdown-menu' + desc)
	
	    if (!$items.length) return
	
	    var index = $items.index(e.target)
	
	    if (e.which == 38 && index > 0)                 index--         // up
	    if (e.which == 40 && index < $items.length - 1) index++         // down
	    if (!~index)                                    index = 0
	
	    $items.eq(index).trigger('focus')
	  }
	
	
	  // DROPDOWN PLUGIN DEFINITION
	  // ==========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this = $(this)
	      var data  = $this.data('bs.dropdown')
	
	      if (!data) $this.data('bs.dropdown', (data = new Dropdown(this)))
	      if (typeof option == 'string') data[option].call($this)
	    })
	  }
	
	  var old = $.fn.dropdown
	
	  $.fn.dropdown             = Plugin
	  $.fn.dropdown.Constructor = Dropdown
	
	
	  // DROPDOWN NO CONFLICT
	  // ====================
	
	  $.fn.dropdown.noConflict = function () {
	    $.fn.dropdown = old
	    return this
	  }
	
	
	  // APPLY TO STANDARD DROPDOWN ELEMENTS
	  // ===================================
	
	  $(document)
	    .on('click.bs.dropdown.data-api', clearMenus)
	    .on('click.bs.dropdown.data-api', '.dropdown form', function (e) { e.stopPropagation() })
	    .on('click.bs.dropdown.data-api', toggle, Dropdown.prototype.toggle)
	    .on('keydown.bs.dropdown.data-api', toggle, Dropdown.prototype.keydown)
	    .on('keydown.bs.dropdown.data-api', '.dropdown-menu', Dropdown.prototype.keydown)
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: modal.js v3.3.7
	 * http://getbootstrap.com/javascript/#modals
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // MODAL CLASS DEFINITION
	  // ======================
	
	  var Modal = function (element, options) {
	    this.options             = options
	    this.$body               = $(document.body)
	    this.$element            = $(element)
	    this.$dialog             = this.$element.find('.modal-dialog')
	    this.$backdrop           = null
	    this.isShown             = null
	    this.originalBodyPad     = null
	    this.scrollbarWidth      = 0
	    this.ignoreBackdropClick = false
	
	    if (this.options.remote) {
	      this.$element
	        .find('.modal-content')
	        .load(this.options.remote, $.proxy(function () {
	          this.$element.trigger('loaded.bs.modal')
	        }, this))
	    }
	  }
	
	  Modal.VERSION  = '3.3.7'
	
	  Modal.TRANSITION_DURATION = 300
	  Modal.BACKDROP_TRANSITION_DURATION = 150
	
	  Modal.DEFAULTS = {
	    backdrop: true,
	    keyboard: true,
	    show: true
	  }
	
	  Modal.prototype.toggle = function (_relatedTarget) {
	    return this.isShown ? this.hide() : this.show(_relatedTarget)
	  }
	
	  Modal.prototype.show = function (_relatedTarget) {
	    var that = this
	    var e    = $.Event('show.bs.modal', { relatedTarget: _relatedTarget })
	
	    this.$element.trigger(e)
	
	    if (this.isShown || e.isDefaultPrevented()) return
	
	    this.isShown = true
	
	    this.checkScrollbar()
	    this.setScrollbar()
	    this.$body.addClass('modal-open')
	
	    this.escape()
	    this.resize()
	
	    this.$element.on('click.dismiss.bs.modal', '[data-dismiss="modal"]', $.proxy(this.hide, this))
	
	    this.$dialog.on('mousedown.dismiss.bs.modal', function () {
	      that.$element.one('mouseup.dismiss.bs.modal', function (e) {
	        if ($(e.target).is(that.$element)) that.ignoreBackdropClick = true
	      })
	    })
	
	    this.backdrop(function () {
	      var transition = $.support.transition && that.$element.hasClass('fade')
	
	      if (!that.$element.parent().length) {
	        that.$element.appendTo(that.$body) // don't move modals dom position
	      }
	
	      that.$element
	        .show()
	        .scrollTop(0)
	
	      that.adjustDialog()
	
	      if (transition) {
	        that.$element[0].offsetWidth // force reflow
	      }
	
	      that.$element.addClass('in')
	
	      that.enforceFocus()
	
	      var e = $.Event('shown.bs.modal', { relatedTarget: _relatedTarget })
	
	      transition ?
	        that.$dialog // wait for modal to slide in
	          .one('bsTransitionEnd', function () {
	            that.$element.trigger('focus').trigger(e)
	          })
	          .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
	        that.$element.trigger('focus').trigger(e)
	    })
	  }
	
	  Modal.prototype.hide = function (e) {
	    if (e) e.preventDefault()
	
	    e = $.Event('hide.bs.modal')
	
	    this.$element.trigger(e)
	
	    if (!this.isShown || e.isDefaultPrevented()) return
	
	    this.isShown = false
	
	    this.escape()
	    this.resize()
	
	    $(document).off('focusin.bs.modal')
	
	    this.$element
	      .removeClass('in')
	      .off('click.dismiss.bs.modal')
	      .off('mouseup.dismiss.bs.modal')
	
	    this.$dialog.off('mousedown.dismiss.bs.modal')
	
	    $.support.transition && this.$element.hasClass('fade') ?
	      this.$element
	        .one('bsTransitionEnd', $.proxy(this.hideModal, this))
	        .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
	      this.hideModal()
	  }
	
	  Modal.prototype.enforceFocus = function () {
	    $(document)
	      .off('focusin.bs.modal') // guard against infinite focus loop
	      .on('focusin.bs.modal', $.proxy(function (e) {
	        if (document !== e.target &&
	            this.$element[0] !== e.target &&
	            !this.$element.has(e.target).length) {
	          this.$element.trigger('focus')
	        }
	      }, this))
	  }
	
	  Modal.prototype.escape = function () {
	    if (this.isShown && this.options.keyboard) {
	      this.$element.on('keydown.dismiss.bs.modal', $.proxy(function (e) {
	        e.which == 27 && this.hide()
	      }, this))
	    } else if (!this.isShown) {
	      this.$element.off('keydown.dismiss.bs.modal')
	    }
	  }
	
	  Modal.prototype.resize = function () {
	    if (this.isShown) {
	      $(window).on('resize.bs.modal', $.proxy(this.handleUpdate, this))
	    } else {
	      $(window).off('resize.bs.modal')
	    }
	  }
	
	  Modal.prototype.hideModal = function () {
	    var that = this
	    this.$element.hide()
	    this.backdrop(function () {
	      that.$body.removeClass('modal-open')
	      that.resetAdjustments()
	      that.resetScrollbar()
	      that.$element.trigger('hidden.bs.modal')
	    })
	  }
	
	  Modal.prototype.removeBackdrop = function () {
	    this.$backdrop && this.$backdrop.remove()
	    this.$backdrop = null
	  }
	
	  Modal.prototype.backdrop = function (callback) {
	    var that = this
	    var animate = this.$element.hasClass('fade') ? 'fade' : ''
	
	    if (this.isShown && this.options.backdrop) {
	      var doAnimate = $.support.transition && animate
	
	      this.$backdrop = $(document.createElement('div'))
	        .addClass('modal-backdrop ' + animate)
	        .appendTo(this.$body)
	
	      this.$element.on('click.dismiss.bs.modal', $.proxy(function (e) {
	        if (this.ignoreBackdropClick) {
	          this.ignoreBackdropClick = false
	          return
	        }
	        if (e.target !== e.currentTarget) return
	        this.options.backdrop == 'static'
	          ? this.$element[0].focus()
	          : this.hide()
	      }, this))
	
	      if (doAnimate) this.$backdrop[0].offsetWidth // force reflow
	
	      this.$backdrop.addClass('in')
	
	      if (!callback) return
	
	      doAnimate ?
	        this.$backdrop
	          .one('bsTransitionEnd', callback)
	          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
	        callback()
	
	    } else if (!this.isShown && this.$backdrop) {
	      this.$backdrop.removeClass('in')
	
	      var callbackRemove = function () {
	        that.removeBackdrop()
	        callback && callback()
	      }
	      $.support.transition && this.$element.hasClass('fade') ?
	        this.$backdrop
	          .one('bsTransitionEnd', callbackRemove)
	          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
	        callbackRemove()
	
	    } else if (callback) {
	      callback()
	    }
	  }
	
	  // these following methods are used to handle overflowing modals
	
	  Modal.prototype.handleUpdate = function () {
	    this.adjustDialog()
	  }
	
	  Modal.prototype.adjustDialog = function () {
	    var modalIsOverflowing = this.$element[0].scrollHeight > document.documentElement.clientHeight
	
	    this.$element.css({
	      paddingLeft:  !this.bodyIsOverflowing && modalIsOverflowing ? this.scrollbarWidth : '',
	      paddingRight: this.bodyIsOverflowing && !modalIsOverflowing ? this.scrollbarWidth : ''
	    })
	  }
	
	  Modal.prototype.resetAdjustments = function () {
	    this.$element.css({
	      paddingLeft: '',
	      paddingRight: ''
	    })
	  }
	
	  Modal.prototype.checkScrollbar = function () {
	    var fullWindowWidth = window.innerWidth
	    if (!fullWindowWidth) { // workaround for missing window.innerWidth in IE8
	      var documentElementRect = document.documentElement.getBoundingClientRect()
	      fullWindowWidth = documentElementRect.right - Math.abs(documentElementRect.left)
	    }
	    this.bodyIsOverflowing = document.body.clientWidth < fullWindowWidth
	    this.scrollbarWidth = this.measureScrollbar()
	  }
	
	  Modal.prototype.setScrollbar = function () {
	    var bodyPad = parseInt((this.$body.css('padding-right') || 0), 10)
	    this.originalBodyPad = document.body.style.paddingRight || ''
	    if (this.bodyIsOverflowing) this.$body.css('padding-right', bodyPad + this.scrollbarWidth)
	  }
	
	  Modal.prototype.resetScrollbar = function () {
	    this.$body.css('padding-right', this.originalBodyPad)
	  }
	
	  Modal.prototype.measureScrollbar = function () { // thx walsh
	    var scrollDiv = document.createElement('div')
	    scrollDiv.className = 'modal-scrollbar-measure'
	    this.$body.append(scrollDiv)
	    var scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth
	    this.$body[0].removeChild(scrollDiv)
	    return scrollbarWidth
	  }
	
	
	  // MODAL PLUGIN DEFINITION
	  // =======================
	
	  function Plugin(option, _relatedTarget) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.modal')
	      var options = $.extend({}, Modal.DEFAULTS, $this.data(), typeof option == 'object' && option)
	
	      if (!data) $this.data('bs.modal', (data = new Modal(this, options)))
	      if (typeof option == 'string') data[option](_relatedTarget)
	      else if (options.show) data.show(_relatedTarget)
	    })
	  }
	
	  var old = $.fn.modal
	
	  $.fn.modal             = Plugin
	  $.fn.modal.Constructor = Modal
	
	
	  // MODAL NO CONFLICT
	  // =================
	
	  $.fn.modal.noConflict = function () {
	    $.fn.modal = old
	    return this
	  }
	
	
	  // MODAL DATA-API
	  // ==============
	
	  $(document).on('click.bs.modal.data-api', '[data-toggle="modal"]', function (e) {
	    var $this   = $(this)
	    var href    = $this.attr('href')
	    var $target = $($this.attr('data-target') || (href && href.replace(/.*(?=#[^\s]+$)/, ''))) // strip for ie7
	    var option  = $target.data('bs.modal') ? 'toggle' : $.extend({ remote: !/#/.test(href) && href }, $target.data(), $this.data())
	
	    if ($this.is('a')) e.preventDefault()
	
	    $target.one('show.bs.modal', function (showEvent) {
	      if (showEvent.isDefaultPrevented()) return // only register focus restorer if modal will actually get shown
	      $target.one('hidden.bs.modal', function () {
	        $this.is(':visible') && $this.trigger('focus')
	      })
	    })
	    Plugin.call($target, option, this)
	  })
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: tooltip.js v3.3.7
	 * http://getbootstrap.com/javascript/#tooltip
	 * Inspired by the original jQuery.tipsy by Jason Frame
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // TOOLTIP PUBLIC CLASS DEFINITION
	  // ===============================
	
	  var Tooltip = function (element, options) {
	    this.type       = null
	    this.options    = null
	    this.enabled    = null
	    this.timeout    = null
	    this.hoverState = null
	    this.$element   = null
	    this.inState    = null
	
	    this.init('tooltip', element, options)
	  }
	
	  Tooltip.VERSION  = '3.3.7'
	
	  Tooltip.TRANSITION_DURATION = 150
	
	  Tooltip.DEFAULTS = {
	    animation: true,
	    placement: 'top',
	    selector: false,
	    template: '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
	    trigger: 'hover focus',
	    title: '',
	    delay: 0,
	    html: false,
	    container: false,
	    viewport: {
	      selector: 'body',
	      padding: 0
	    }
	  }
	
	  Tooltip.prototype.init = function (type, element, options) {
	    this.enabled   = true
	    this.type      = type
	    this.$element  = $(element)
	    this.options   = this.getOptions(options)
	    this.$viewport = this.options.viewport && $($.isFunction(this.options.viewport) ? this.options.viewport.call(this, this.$element) : (this.options.viewport.selector || this.options.viewport))
	    this.inState   = { click: false, hover: false, focus: false }
	
	    if (this.$element[0] instanceof document.constructor && !this.options.selector) {
	      throw new Error('`selector` option must be specified when initializing ' + this.type + ' on the window.document object!')
	    }
	
	    var triggers = this.options.trigger.split(' ')
	
	    for (var i = triggers.length; i--;) {
	      var trigger = triggers[i]
	
	      if (trigger == 'click') {
	        this.$element.on('click.' + this.type, this.options.selector, $.proxy(this.toggle, this))
	      } else if (trigger != 'manual') {
	        var eventIn  = trigger == 'hover' ? 'mouseenter' : 'focusin'
	        var eventOut = trigger == 'hover' ? 'mouseleave' : 'focusout'
	
	        this.$element.on(eventIn  + '.' + this.type, this.options.selector, $.proxy(this.enter, this))
	        this.$element.on(eventOut + '.' + this.type, this.options.selector, $.proxy(this.leave, this))
	      }
	    }
	
	    this.options.selector ?
	      (this._options = $.extend({}, this.options, { trigger: 'manual', selector: '' })) :
	      this.fixTitle()
	  }
	
	  Tooltip.prototype.getDefaults = function () {
	    return Tooltip.DEFAULTS
	  }
	
	  Tooltip.prototype.getOptions = function (options) {
	    options = $.extend({}, this.getDefaults(), this.$element.data(), options)
	
	    if (options.delay && typeof options.delay == 'number') {
	      options.delay = {
	        show: options.delay,
	        hide: options.delay
	      }
	    }
	
	    return options
	  }
	
	  Tooltip.prototype.getDelegateOptions = function () {
	    var options  = {}
	    var defaults = this.getDefaults()
	
	    this._options && $.each(this._options, function (key, value) {
	      if (defaults[key] != value) options[key] = value
	    })
	
	    return options
	  }
	
	  Tooltip.prototype.enter = function (obj) {
	    var self = obj instanceof this.constructor ?
	      obj : $(obj.currentTarget).data('bs.' + this.type)
	
	    if (!self) {
	      self = new this.constructor(obj.currentTarget, this.getDelegateOptions())
	      $(obj.currentTarget).data('bs.' + this.type, self)
	    }
	
	    if (obj instanceof $.Event) {
	      self.inState[obj.type == 'focusin' ? 'focus' : 'hover'] = true
	    }
	
	    if (self.tip().hasClass('in') || self.hoverState == 'in') {
	      self.hoverState = 'in'
	      return
	    }
	
	    clearTimeout(self.timeout)
	
	    self.hoverState = 'in'
	
	    if (!self.options.delay || !self.options.delay.show) return self.show()
	
	    self.timeout = setTimeout(function () {
	      if (self.hoverState == 'in') self.show()
	    }, self.options.delay.show)
	  }
	
	  Tooltip.prototype.isInStateTrue = function () {
	    for (var key in this.inState) {
	      if (this.inState[key]) return true
	    }
	
	    return false
	  }
	
	  Tooltip.prototype.leave = function (obj) {
	    var self = obj instanceof this.constructor ?
	      obj : $(obj.currentTarget).data('bs.' + this.type)
	
	    if (!self) {
	      self = new this.constructor(obj.currentTarget, this.getDelegateOptions())
	      $(obj.currentTarget).data('bs.' + this.type, self)
	    }
	
	    if (obj instanceof $.Event) {
	      self.inState[obj.type == 'focusout' ? 'focus' : 'hover'] = false
	    }
	
	    if (self.isInStateTrue()) return
	
	    clearTimeout(self.timeout)
	
	    self.hoverState = 'out'
	
	    if (!self.options.delay || !self.options.delay.hide) return self.hide()
	
	    self.timeout = setTimeout(function () {
	      if (self.hoverState == 'out') self.hide()
	    }, self.options.delay.hide)
	  }
	
	  Tooltip.prototype.show = function () {
	    var e = $.Event('show.bs.' + this.type)
	
	    if (this.hasContent() && this.enabled) {
	      this.$element.trigger(e)
	
	      var inDom = $.contains(this.$element[0].ownerDocument.documentElement, this.$element[0])
	      if (e.isDefaultPrevented() || !inDom) return
	      var that = this
	
	      var $tip = this.tip()
	
	      var tipId = this.getUID(this.type)
	
	      this.setContent()
	      $tip.attr('id', tipId)
	      this.$element.attr('aria-describedby', tipId)
	
	      if (this.options.animation) $tip.addClass('fade')
	
	      var placement = typeof this.options.placement == 'function' ?
	        this.options.placement.call(this, $tip[0], this.$element[0]) :
	        this.options.placement
	
	      var autoToken = /\s?auto?\s?/i
	      var autoPlace = autoToken.test(placement)
	      if (autoPlace) placement = placement.replace(autoToken, '') || 'top'
	
	      $tip
	        .detach()
	        .css({ top: 0, left: 0, display: 'block' })
	        .addClass(placement)
	        .data('bs.' + this.type, this)
	
	      this.options.container ? $tip.appendTo(this.options.container) : $tip.insertAfter(this.$element)
	      this.$element.trigger('inserted.bs.' + this.type)
	
	      var pos          = this.getPosition()
	      var actualWidth  = $tip[0].offsetWidth
	      var actualHeight = $tip[0].offsetHeight
	
	      if (autoPlace) {
	        var orgPlacement = placement
	        var viewportDim = this.getPosition(this.$viewport)
	
	        placement = placement == 'bottom' && pos.bottom + actualHeight > viewportDim.bottom ? 'top'    :
	                    placement == 'top'    && pos.top    - actualHeight < viewportDim.top    ? 'bottom' :
	                    placement == 'right'  && pos.right  + actualWidth  > viewportDim.width  ? 'left'   :
	                    placement == 'left'   && pos.left   - actualWidth  < viewportDim.left   ? 'right'  :
	                    placement
	
	        $tip
	          .removeClass(orgPlacement)
	          .addClass(placement)
	      }
	
	      var calculatedOffset = this.getCalculatedOffset(placement, pos, actualWidth, actualHeight)
	
	      this.applyPlacement(calculatedOffset, placement)
	
	      var complete = function () {
	        var prevHoverState = that.hoverState
	        that.$element.trigger('shown.bs.' + that.type)
	        that.hoverState = null
	
	        if (prevHoverState == 'out') that.leave(that)
	      }
	
	      $.support.transition && this.$tip.hasClass('fade') ?
	        $tip
	          .one('bsTransitionEnd', complete)
	          .emulateTransitionEnd(Tooltip.TRANSITION_DURATION) :
	        complete()
	    }
	  }
	
	  Tooltip.prototype.applyPlacement = function (offset, placement) {
	    var $tip   = this.tip()
	    var width  = $tip[0].offsetWidth
	    var height = $tip[0].offsetHeight
	
	    // manually read margins because getBoundingClientRect includes difference
	    var marginTop = parseInt($tip.css('margin-top'), 10)
	    var marginLeft = parseInt($tip.css('margin-left'), 10)
	
	    // we must check for NaN for ie 8/9
	    if (isNaN(marginTop))  marginTop  = 0
	    if (isNaN(marginLeft)) marginLeft = 0
	
	    offset.top  += marginTop
	    offset.left += marginLeft
	
	    // $.fn.offset doesn't round pixel values
	    // so we use setOffset directly with our own function B-0
	    $.offset.setOffset($tip[0], $.extend({
	      using: function (props) {
	        $tip.css({
	          top: Math.round(props.top),
	          left: Math.round(props.left)
	        })
	      }
	    }, offset), 0)
	
	    $tip.addClass('in')
	
	    // check to see if placing tip in new offset caused the tip to resize itself
	    var actualWidth  = $tip[0].offsetWidth
	    var actualHeight = $tip[0].offsetHeight
	
	    if (placement == 'top' && actualHeight != height) {
	      offset.top = offset.top + height - actualHeight
	    }
	
	    var delta = this.getViewportAdjustedDelta(placement, offset, actualWidth, actualHeight)
	
	    if (delta.left) offset.left += delta.left
	    else offset.top += delta.top
	
	    var isVertical          = /top|bottom/.test(placement)
	    var arrowDelta          = isVertical ? delta.left * 2 - width + actualWidth : delta.top * 2 - height + actualHeight
	    var arrowOffsetPosition = isVertical ? 'offsetWidth' : 'offsetHeight'
	
	    $tip.offset(offset)
	    this.replaceArrow(arrowDelta, $tip[0][arrowOffsetPosition], isVertical)
	  }
	
	  Tooltip.prototype.replaceArrow = function (delta, dimension, isVertical) {
	    this.arrow()
	      .css(isVertical ? 'left' : 'top', 50 * (1 - delta / dimension) + '%')
	      .css(isVertical ? 'top' : 'left', '')
	  }
	
	  Tooltip.prototype.setContent = function () {
	    var $tip  = this.tip()
	    var title = this.getTitle()
	
	    $tip.find('.tooltip-inner')[this.options.html ? 'html' : 'text'](title)
	    $tip.removeClass('fade in top bottom left right')
	  }
	
	  Tooltip.prototype.hide = function (callback) {
	    var that = this
	    var $tip = $(this.$tip)
	    var e    = $.Event('hide.bs.' + this.type)
	
	    function complete() {
	      if (that.hoverState != 'in') $tip.detach()
	      if (that.$element) { // TODO: Check whether guarding this code with this `if` is really necessary.
	        that.$element
	          .removeAttr('aria-describedby')
	          .trigger('hidden.bs.' + that.type)
	      }
	      callback && callback()
	    }
	
	    this.$element.trigger(e)
	
	    if (e.isDefaultPrevented()) return
	
	    $tip.removeClass('in')
	
	    $.support.transition && $tip.hasClass('fade') ?
	      $tip
	        .one('bsTransitionEnd', complete)
	        .emulateTransitionEnd(Tooltip.TRANSITION_DURATION) :
	      complete()
	
	    this.hoverState = null
	
	    return this
	  }
	
	  Tooltip.prototype.fixTitle = function () {
	    var $e = this.$element
	    if ($e.attr('title') || typeof $e.attr('data-original-title') != 'string') {
	      $e.attr('data-original-title', $e.attr('title') || '').attr('title', '')
	    }
	  }
	
	  Tooltip.prototype.hasContent = function () {
	    return this.getTitle()
	  }
	
	  Tooltip.prototype.getPosition = function ($element) {
	    $element   = $element || this.$element
	
	    var el     = $element[0]
	    var isBody = el.tagName == 'BODY'
	
	    var elRect    = el.getBoundingClientRect()
	    if (elRect.width == null) {
	      // width and height are missing in IE8, so compute them manually; see https://github.com/twbs/bootstrap/issues/14093
	      elRect = $.extend({}, elRect, { width: elRect.right - elRect.left, height: elRect.bottom - elRect.top })
	    }
	    var isSvg = window.SVGElement && el instanceof window.SVGElement
	    // Avoid using $.offset() on SVGs since it gives incorrect results in jQuery 3.
	    // See https://github.com/twbs/bootstrap/issues/20280
	    var elOffset  = isBody ? { top: 0, left: 0 } : (isSvg ? null : $element.offset())
	    var scroll    = { scroll: isBody ? document.documentElement.scrollTop || document.body.scrollTop : $element.scrollTop() }
	    var outerDims = isBody ? { width: $(window).width(), height: $(window).height() } : null
	
	    return $.extend({}, elRect, scroll, outerDims, elOffset)
	  }
	
	  Tooltip.prototype.getCalculatedOffset = function (placement, pos, actualWidth, actualHeight) {
	    return placement == 'bottom' ? { top: pos.top + pos.height,   left: pos.left + pos.width / 2 - actualWidth / 2 } :
	           placement == 'top'    ? { top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2 } :
	           placement == 'left'   ? { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth } :
	        /* placement == 'right' */ { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width }
	
	  }
	
	  Tooltip.prototype.getViewportAdjustedDelta = function (placement, pos, actualWidth, actualHeight) {
	    var delta = { top: 0, left: 0 }
	    if (!this.$viewport) return delta
	
	    var viewportPadding = this.options.viewport && this.options.viewport.padding || 0
	    var viewportDimensions = this.getPosition(this.$viewport)
	
	    if (/right|left/.test(placement)) {
	      var topEdgeOffset    = pos.top - viewportPadding - viewportDimensions.scroll
	      var bottomEdgeOffset = pos.top + viewportPadding - viewportDimensions.scroll + actualHeight
	      if (topEdgeOffset < viewportDimensions.top) { // top overflow
	        delta.top = viewportDimensions.top - topEdgeOffset
	      } else if (bottomEdgeOffset > viewportDimensions.top + viewportDimensions.height) { // bottom overflow
	        delta.top = viewportDimensions.top + viewportDimensions.height - bottomEdgeOffset
	      }
	    } else {
	      var leftEdgeOffset  = pos.left - viewportPadding
	      var rightEdgeOffset = pos.left + viewportPadding + actualWidth
	      if (leftEdgeOffset < viewportDimensions.left) { // left overflow
	        delta.left = viewportDimensions.left - leftEdgeOffset
	      } else if (rightEdgeOffset > viewportDimensions.right) { // right overflow
	        delta.left = viewportDimensions.left + viewportDimensions.width - rightEdgeOffset
	      }
	    }
	
	    return delta
	  }
	
	  Tooltip.prototype.getTitle = function () {
	    var title
	    var $e = this.$element
	    var o  = this.options
	
	    title = $e.attr('data-original-title')
	      || (typeof o.title == 'function' ? o.title.call($e[0]) :  o.title)
	
	    return title
	  }
	
	  Tooltip.prototype.getUID = function (prefix) {
	    do prefix += ~~(Math.random() * 1000000)
	    while (document.getElementById(prefix))
	    return prefix
	  }
	
	  Tooltip.prototype.tip = function () {
	    if (!this.$tip) {
	      this.$tip = $(this.options.template)
	      if (this.$tip.length != 1) {
	        throw new Error(this.type + ' `template` option must consist of exactly 1 top-level element!')
	      }
	    }
	    return this.$tip
	  }
	
	  Tooltip.prototype.arrow = function () {
	    return (this.$arrow = this.$arrow || this.tip().find('.tooltip-arrow'))
	  }
	
	  Tooltip.prototype.enable = function () {
	    this.enabled = true
	  }
	
	  Tooltip.prototype.disable = function () {
	    this.enabled = false
	  }
	
	  Tooltip.prototype.toggleEnabled = function () {
	    this.enabled = !this.enabled
	  }
	
	  Tooltip.prototype.toggle = function (e) {
	    var self = this
	    if (e) {
	      self = $(e.currentTarget).data('bs.' + this.type)
	      if (!self) {
	        self = new this.constructor(e.currentTarget, this.getDelegateOptions())
	        $(e.currentTarget).data('bs.' + this.type, self)
	      }
	    }
	
	    if (e) {
	      self.inState.click = !self.inState.click
	      if (self.isInStateTrue()) self.enter(self)
	      else self.leave(self)
	    } else {
	      self.tip().hasClass('in') ? self.leave(self) : self.enter(self)
	    }
	  }
	
	  Tooltip.prototype.destroy = function () {
	    var that = this
	    clearTimeout(this.timeout)
	    this.hide(function () {
	      that.$element.off('.' + that.type).removeData('bs.' + that.type)
	      if (that.$tip) {
	        that.$tip.detach()
	      }
	      that.$tip = null
	      that.$arrow = null
	      that.$viewport = null
	      that.$element = null
	    })
	  }
	
	
	  // TOOLTIP PLUGIN DEFINITION
	  // =========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.tooltip')
	      var options = typeof option == 'object' && option
	
	      if (!data && /destroy|hide/.test(option)) return
	      if (!data) $this.data('bs.tooltip', (data = new Tooltip(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.tooltip
	
	  $.fn.tooltip             = Plugin
	  $.fn.tooltip.Constructor = Tooltip
	
	
	  // TOOLTIP NO CONFLICT
	  // ===================
	
	  $.fn.tooltip.noConflict = function () {
	    $.fn.tooltip = old
	    return this
	  }
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: popover.js v3.3.7
	 * http://getbootstrap.com/javascript/#popovers
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // POPOVER PUBLIC CLASS DEFINITION
	  // ===============================
	
	  var Popover = function (element, options) {
	    this.init('popover', element, options)
	  }
	
	  if (!$.fn.tooltip) throw new Error('Popover requires tooltip.js')
	
	  Popover.VERSION  = '3.3.7'
	
	  Popover.DEFAULTS = $.extend({}, $.fn.tooltip.Constructor.DEFAULTS, {
	    placement: 'right',
	    trigger: 'click',
	    content: '',
	    template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'
	  })
	
	
	  // NOTE: POPOVER EXTENDS tooltip.js
	  // ================================
	
	  Popover.prototype = $.extend({}, $.fn.tooltip.Constructor.prototype)
	
	  Popover.prototype.constructor = Popover
	
	  Popover.prototype.getDefaults = function () {
	    return Popover.DEFAULTS
	  }
	
	  Popover.prototype.setContent = function () {
	    var $tip    = this.tip()
	    var title   = this.getTitle()
	    var content = this.getContent()
	
	    $tip.find('.popover-title')[this.options.html ? 'html' : 'text'](title)
	    $tip.find('.popover-content').children().detach().end()[ // we use append for html objects to maintain js events
	      this.options.html ? (typeof content == 'string' ? 'html' : 'append') : 'text'
	    ](content)
	
	    $tip.removeClass('fade top bottom left right in')
	
	    // IE8 doesn't accept hiding via the `:empty` pseudo selector, we have to do
	    // this manually by checking the contents.
	    if (!$tip.find('.popover-title').html()) $tip.find('.popover-title').hide()
	  }
	
	  Popover.prototype.hasContent = function () {
	    return this.getTitle() || this.getContent()
	  }
	
	  Popover.prototype.getContent = function () {
	    var $e = this.$element
	    var o  = this.options
	
	    return $e.attr('data-content')
	      || (typeof o.content == 'function' ?
	            o.content.call($e[0]) :
	            o.content)
	  }
	
	  Popover.prototype.arrow = function () {
	    return (this.$arrow = this.$arrow || this.tip().find('.arrow'))
	  }
	
	
	  // POPOVER PLUGIN DEFINITION
	  // =========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.popover')
	      var options = typeof option == 'object' && option
	
	      if (!data && /destroy|hide/.test(option)) return
	      if (!data) $this.data('bs.popover', (data = new Popover(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.popover
	
	  $.fn.popover             = Plugin
	  $.fn.popover.Constructor = Popover
	
	
	  // POPOVER NO CONFLICT
	  // ===================
	
	  $.fn.popover.noConflict = function () {
	    $.fn.popover = old
	    return this
	  }
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: scrollspy.js v3.3.7
	 * http://getbootstrap.com/javascript/#scrollspy
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // SCROLLSPY CLASS DEFINITION
	  // ==========================
	
	  function ScrollSpy(element, options) {
	    this.$body          = $(document.body)
	    this.$scrollElement = $(element).is(document.body) ? $(window) : $(element)
	    this.options        = $.extend({}, ScrollSpy.DEFAULTS, options)
	    this.selector       = (this.options.target || '') + ' .nav li > a'
	    this.offsets        = []
	    this.targets        = []
	    this.activeTarget   = null
	    this.scrollHeight   = 0
	
	    this.$scrollElement.on('scroll.bs.scrollspy', $.proxy(this.process, this))
	    this.refresh()
	    this.process()
	  }
	
	  ScrollSpy.VERSION  = '3.3.7'
	
	  ScrollSpy.DEFAULTS = {
	    offset: 10
	  }
	
	  ScrollSpy.prototype.getScrollHeight = function () {
	    return this.$scrollElement[0].scrollHeight || Math.max(this.$body[0].scrollHeight, document.documentElement.scrollHeight)
	  }
	
	  ScrollSpy.prototype.refresh = function () {
	    var that          = this
	    var offsetMethod  = 'offset'
	    var offsetBase    = 0
	
	    this.offsets      = []
	    this.targets      = []
	    this.scrollHeight = this.getScrollHeight()
	
	    if (!$.isWindow(this.$scrollElement[0])) {
	      offsetMethod = 'position'
	      offsetBase   = this.$scrollElement.scrollTop()
	    }
	
	    this.$body
	      .find(this.selector)
	      .map(function () {
	        var $el   = $(this)
	        var href  = $el.data('target') || $el.attr('href')
	        var $href = /^#./.test(href) && $(href)
	
	        return ($href
	          && $href.length
	          && $href.is(':visible')
	          && [[$href[offsetMethod]().top + offsetBase, href]]) || null
	      })
	      .sort(function (a, b) { return a[0] - b[0] })
	      .each(function () {
	        that.offsets.push(this[0])
	        that.targets.push(this[1])
	      })
	  }
	
	  ScrollSpy.prototype.process = function () {
	    var scrollTop    = this.$scrollElement.scrollTop() + this.options.offset
	    var scrollHeight = this.getScrollHeight()
	    var maxScroll    = this.options.offset + scrollHeight - this.$scrollElement.height()
	    var offsets      = this.offsets
	    var targets      = this.targets
	    var activeTarget = this.activeTarget
	    var i
	
	    if (this.scrollHeight != scrollHeight) {
	      this.refresh()
	    }
	
	    if (scrollTop >= maxScroll) {
	      return activeTarget != (i = targets[targets.length - 1]) && this.activate(i)
	    }
	
	    if (activeTarget && scrollTop < offsets[0]) {
	      this.activeTarget = null
	      return this.clear()
	    }
	
	    for (i = offsets.length; i--;) {
	      activeTarget != targets[i]
	        && scrollTop >= offsets[i]
	        && (offsets[i + 1] === undefined || scrollTop < offsets[i + 1])
	        && this.activate(targets[i])
	    }
	  }
	
	  ScrollSpy.prototype.activate = function (target) {
	    this.activeTarget = target
	
	    this.clear()
	
	    var selector = this.selector +
	      '[data-target="' + target + '"],' +
	      this.selector + '[href="' + target + '"]'
	
	    var active = $(selector)
	      .parents('li')
	      .addClass('active')
	
	    if (active.parent('.dropdown-menu').length) {
	      active = active
	        .closest('li.dropdown')
	        .addClass('active')
	    }
	
	    active.trigger('activate.bs.scrollspy')
	  }
	
	  ScrollSpy.prototype.clear = function () {
	    $(this.selector)
	      .parentsUntil(this.options.target, '.active')
	      .removeClass('active')
	  }
	
	
	  // SCROLLSPY PLUGIN DEFINITION
	  // ===========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.scrollspy')
	      var options = typeof option == 'object' && option
	
	      if (!data) $this.data('bs.scrollspy', (data = new ScrollSpy(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.scrollspy
	
	  $.fn.scrollspy             = Plugin
	  $.fn.scrollspy.Constructor = ScrollSpy
	
	
	  // SCROLLSPY NO CONFLICT
	  // =====================
	
	  $.fn.scrollspy.noConflict = function () {
	    $.fn.scrollspy = old
	    return this
	  }
	
	
	  // SCROLLSPY DATA-API
	  // ==================
	
	  $(window).on('load.bs.scrollspy.data-api', function () {
	    $('[data-spy="scroll"]').each(function () {
	      var $spy = $(this)
	      Plugin.call($spy, $spy.data())
	    })
	  })
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: tab.js v3.3.7
	 * http://getbootstrap.com/javascript/#tabs
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // TAB CLASS DEFINITION
	  // ====================
	
	  var Tab = function (element) {
	    // jscs:disable requireDollarBeforejQueryAssignment
	    this.element = $(element)
	    // jscs:enable requireDollarBeforejQueryAssignment
	  }
	
	  Tab.VERSION = '3.3.7'
	
	  Tab.TRANSITION_DURATION = 150
	
	  Tab.prototype.show = function () {
	    var $this    = this.element
	    var $ul      = $this.closest('ul:not(.dropdown-menu)')
	    var selector = $this.data('target')
	
	    if (!selector) {
	      selector = $this.attr('href')
	      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
	    }
	
	    if ($this.parent('li').hasClass('active')) return
	
	    var $previous = $ul.find('.active:last a')
	    var hideEvent = $.Event('hide.bs.tab', {
	      relatedTarget: $this[0]
	    })
	    var showEvent = $.Event('show.bs.tab', {
	      relatedTarget: $previous[0]
	    })
	
	    $previous.trigger(hideEvent)
	    $this.trigger(showEvent)
	
	    if (showEvent.isDefaultPrevented() || hideEvent.isDefaultPrevented()) return
	
	    var $target = $(selector)
	
	    this.activate($this.closest('li'), $ul)
	    this.activate($target, $target.parent(), function () {
	      $previous.trigger({
	        type: 'hidden.bs.tab',
	        relatedTarget: $this[0]
	      })
	      $this.trigger({
	        type: 'shown.bs.tab',
	        relatedTarget: $previous[0]
	      })
	    })
	  }
	
	  Tab.prototype.activate = function (element, container, callback) {
	    var $active    = container.find('> .active')
	    var transition = callback
	      && $.support.transition
	      && ($active.length && $active.hasClass('fade') || !!container.find('> .fade').length)
	
	    function next() {
	      $active
	        .removeClass('active')
	        .find('> .dropdown-menu > .active')
	          .removeClass('active')
	        .end()
	        .find('[data-toggle="tab"]')
	          .attr('aria-expanded', false)
	
	      element
	        .addClass('active')
	        .find('[data-toggle="tab"]')
	          .attr('aria-expanded', true)
	
	      if (transition) {
	        element[0].offsetWidth // reflow for transition
	        element.addClass('in')
	      } else {
	        element.removeClass('fade')
	      }
	
	      if (element.parent('.dropdown-menu').length) {
	        element
	          .closest('li.dropdown')
	            .addClass('active')
	          .end()
	          .find('[data-toggle="tab"]')
	            .attr('aria-expanded', true)
	      }
	
	      callback && callback()
	    }
	
	    $active.length && transition ?
	      $active
	        .one('bsTransitionEnd', next)
	        .emulateTransitionEnd(Tab.TRANSITION_DURATION) :
	      next()
	
	    $active.removeClass('in')
	  }
	
	
	  // TAB PLUGIN DEFINITION
	  // =====================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this = $(this)
	      var data  = $this.data('bs.tab')
	
	      if (!data) $this.data('bs.tab', (data = new Tab(this)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.tab
	
	  $.fn.tab             = Plugin
	  $.fn.tab.Constructor = Tab
	
	
	  // TAB NO CONFLICT
	  // ===============
	
	  $.fn.tab.noConflict = function () {
	    $.fn.tab = old
	    return this
	  }
	
	
	  // TAB DATA-API
	  // ============
	
	  var clickHandler = function (e) {
	    e.preventDefault()
	    Plugin.call($(this), 'show')
	  }
	
	  $(document)
	    .on('click.bs.tab.data-api', '[data-toggle="tab"]', clickHandler)
	    .on('click.bs.tab.data-api', '[data-toggle="pill"]', clickHandler)
	
	}(jQuery);
	
	/* ========================================================================
	 * Bootstrap: affix.js v3.3.7
	 * http://getbootstrap.com/javascript/#affix
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // AFFIX CLASS DEFINITION
	  // ======================
	
	  var Affix = function (element, options) {
	    this.options = $.extend({}, Affix.DEFAULTS, options)
	
	    this.$target = $(this.options.target)
	      .on('scroll.bs.affix.data-api', $.proxy(this.checkPosition, this))
	      .on('click.bs.affix.data-api',  $.proxy(this.checkPositionWithEventLoop, this))
	
	    this.$element     = $(element)
	    this.affixed      = null
	    this.unpin        = null
	    this.pinnedOffset = null
	
	    this.checkPosition()
	  }
	
	  Affix.VERSION  = '3.3.7'
	
	  Affix.RESET    = 'affix affix-top affix-bottom'
	
	  Affix.DEFAULTS = {
	    offset: 0,
	    target: window
	  }
	
	  Affix.prototype.getState = function (scrollHeight, height, offsetTop, offsetBottom) {
	    var scrollTop    = this.$target.scrollTop()
	    var position     = this.$element.offset()
	    var targetHeight = this.$target.height()
	
	    if (offsetTop != null && this.affixed == 'top') return scrollTop < offsetTop ? 'top' : false
	
	    if (this.affixed == 'bottom') {
	      if (offsetTop != null) return (scrollTop + this.unpin <= position.top) ? false : 'bottom'
	      return (scrollTop + targetHeight <= scrollHeight - offsetBottom) ? false : 'bottom'
	    }
	
	    var initializing   = this.affixed == null
	    var colliderTop    = initializing ? scrollTop : position.top
	    var colliderHeight = initializing ? targetHeight : height
	
	    if (offsetTop != null && scrollTop <= offsetTop) return 'top'
	    if (offsetBottom != null && (colliderTop + colliderHeight >= scrollHeight - offsetBottom)) return 'bottom'
	
	    return false
	  }
	
	  Affix.prototype.getPinnedOffset = function () {
	    if (this.pinnedOffset) return this.pinnedOffset
	    this.$element.removeClass(Affix.RESET).addClass('affix')
	    var scrollTop = this.$target.scrollTop()
	    var position  = this.$element.offset()
	    return (this.pinnedOffset = position.top - scrollTop)
	  }
	
	  Affix.prototype.checkPositionWithEventLoop = function () {
	    setTimeout($.proxy(this.checkPosition, this), 1)
	  }
	
	  Affix.prototype.checkPosition = function () {
	    if (!this.$element.is(':visible')) return
	
	    var height       = this.$element.height()
	    var offset       = this.options.offset
	    var offsetTop    = offset.top
	    var offsetBottom = offset.bottom
	    var scrollHeight = Math.max($(document).height(), $(document.body).height())
	
	    if (typeof offset != 'object')         offsetBottom = offsetTop = offset
	    if (typeof offsetTop == 'function')    offsetTop    = offset.top(this.$element)
	    if (typeof offsetBottom == 'function') offsetBottom = offset.bottom(this.$element)
	
	    var affix = this.getState(scrollHeight, height, offsetTop, offsetBottom)
	
	    if (this.affixed != affix) {
	      if (this.unpin != null) this.$element.css('top', '')
	
	      var affixType = 'affix' + (affix ? '-' + affix : '')
	      var e         = $.Event(affixType + '.bs.affix')
	
	      this.$element.trigger(e)
	
	      if (e.isDefaultPrevented()) return
	
	      this.affixed = affix
	      this.unpin = affix == 'bottom' ? this.getPinnedOffset() : null
	
	      this.$element
	        .removeClass(Affix.RESET)
	        .addClass(affixType)
	        .trigger(affixType.replace('affix', 'affixed') + '.bs.affix')
	    }
	
	    if (affix == 'bottom') {
	      this.$element.offset({
	        top: scrollHeight - height - offsetBottom
	      })
	    }
	  }
	
	
	  // AFFIX PLUGIN DEFINITION
	  // =======================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.affix')
	      var options = typeof option == 'object' && option
	
	      if (!data) $this.data('bs.affix', (data = new Affix(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.affix
	
	  $.fn.affix             = Plugin
	  $.fn.affix.Constructor = Affix
	
	
	  // AFFIX NO CONFLICT
	  // =================
	
	  $.fn.affix.noConflict = function () {
	    $.fn.affix = old
	    return this
	  }
	
	
	  // AFFIX DATA-API
	  // ==============
	
	  $(window).on('load', function () {
	    $('[data-spy="affix"]').each(function () {
	      var $spy = $(this)
	      var data = $spy.data()
	
	      data.offset = data.offset || {}
	
	      if (data.offsetBottom != null) data.offset.bottom = data.offsetBottom
	      if (data.offsetTop    != null) data.offset.top    = data.offsetTop
	
	      Plugin.call($spy, data)
	    })
	  })
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 3 */
/*!************************************!*\
  !*** ./~/bootstrap/dist/js/npm.js ***!
  \************************************/
/***/ (function(module, exports, __webpack_require__) {

	// This file is autogenerated via the `commonjs` Grunt task. You can require() this file in a CommonJS environment.
	__webpack_require__(/*! ../../js/transition.js */ 4)
	__webpack_require__(/*! ../../js/alert.js */ 5)
	__webpack_require__(/*! ../../js/button.js */ 6)
	__webpack_require__(/*! ../../js/carousel.js */ 7)
	__webpack_require__(/*! ../../js/collapse.js */ 8)
	__webpack_require__(/*! ../../js/dropdown.js */ 9)
	__webpack_require__(/*! ../../js/modal.js */ 10)
	__webpack_require__(/*! ../../js/tooltip.js */ 11)
	__webpack_require__(/*! ../../js/popover.js */ 12)
	__webpack_require__(/*! ../../js/scrollspy.js */ 13)
	__webpack_require__(/*! ../../js/tab.js */ 14)
	__webpack_require__(/*! ../../js/affix.js */ 15)

/***/ }),
/* 4 */
/*!**************************************!*\
  !*** ./~/bootstrap/js/transition.js ***!
  \**************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: transition.js v3.3.7
	 * http://getbootstrap.com/javascript/#transitions
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // CSS TRANSITION SUPPORT (Shoutout: http://www.modernizr.com/)
	  // ============================================================
	
	  function transitionEnd() {
	    var el = document.createElement('bootstrap')
	
	    var transEndEventNames = {
	      WebkitTransition : 'webkitTransitionEnd',
	      MozTransition    : 'transitionend',
	      OTransition      : 'oTransitionEnd otransitionend',
	      transition       : 'transitionend'
	    }
	
	    for (var name in transEndEventNames) {
	      if (el.style[name] !== undefined) {
	        return { end: transEndEventNames[name] }
	      }
	    }
	
	    return false // explicit for ie8 (  ._.)
	  }
	
	  // http://blog.alexmaccaw.com/css-transitions
	  $.fn.emulateTransitionEnd = function (duration) {
	    var called = false
	    var $el = this
	    $(this).one('bsTransitionEnd', function () { called = true })
	    var callback = function () { if (!called) $($el).trigger($.support.transition.end) }
	    setTimeout(callback, duration)
	    return this
	  }
	
	  $(function () {
	    $.support.transition = transitionEnd()
	
	    if (!$.support.transition) return
	
	    $.event.special.bsTransitionEnd = {
	      bindType: $.support.transition.end,
	      delegateType: $.support.transition.end,
	      handle: function (e) {
	        if ($(e.target).is(this)) return e.handleObj.handler.apply(this, arguments)
	      }
	    }
	  })
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 5 */
/*!*********************************!*\
  !*** ./~/bootstrap/js/alert.js ***!
  \*********************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: alert.js v3.3.7
	 * http://getbootstrap.com/javascript/#alerts
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // ALERT CLASS DEFINITION
	  // ======================
	
	  var dismiss = '[data-dismiss="alert"]'
	  var Alert   = function (el) {
	    $(el).on('click', dismiss, this.close)
	  }
	
	  Alert.VERSION = '3.3.7'
	
	  Alert.TRANSITION_DURATION = 150
	
	  Alert.prototype.close = function (e) {
	    var $this    = $(this)
	    var selector = $this.attr('data-target')
	
	    if (!selector) {
	      selector = $this.attr('href')
	      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
	    }
	
	    var $parent = $(selector === '#' ? [] : selector)
	
	    if (e) e.preventDefault()
	
	    if (!$parent.length) {
	      $parent = $this.closest('.alert')
	    }
	
	    $parent.trigger(e = $.Event('close.bs.alert'))
	
	    if (e.isDefaultPrevented()) return
	
	    $parent.removeClass('in')
	
	    function removeElement() {
	      // detach from parent, fire event then clean up data
	      $parent.detach().trigger('closed.bs.alert').remove()
	    }
	
	    $.support.transition && $parent.hasClass('fade') ?
	      $parent
	        .one('bsTransitionEnd', removeElement)
	        .emulateTransitionEnd(Alert.TRANSITION_DURATION) :
	      removeElement()
	  }
	
	
	  // ALERT PLUGIN DEFINITION
	  // =======================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this = $(this)
	      var data  = $this.data('bs.alert')
	
	      if (!data) $this.data('bs.alert', (data = new Alert(this)))
	      if (typeof option == 'string') data[option].call($this)
	    })
	  }
	
	  var old = $.fn.alert
	
	  $.fn.alert             = Plugin
	  $.fn.alert.Constructor = Alert
	
	
	  // ALERT NO CONFLICT
	  // =================
	
	  $.fn.alert.noConflict = function () {
	    $.fn.alert = old
	    return this
	  }
	
	
	  // ALERT DATA-API
	  // ==============
	
	  $(document).on('click.bs.alert.data-api', dismiss, Alert.prototype.close)
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 6 */
/*!**********************************!*\
  !*** ./~/bootstrap/js/button.js ***!
  \**********************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: button.js v3.3.7
	 * http://getbootstrap.com/javascript/#buttons
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // BUTTON PUBLIC CLASS DEFINITION
	  // ==============================
	
	  var Button = function (element, options) {
	    this.$element  = $(element)
	    this.options   = $.extend({}, Button.DEFAULTS, options)
	    this.isLoading = false
	  }
	
	  Button.VERSION  = '3.3.7'
	
	  Button.DEFAULTS = {
	    loadingText: 'loading...'
	  }
	
	  Button.prototype.setState = function (state) {
	    var d    = 'disabled'
	    var $el  = this.$element
	    var val  = $el.is('input') ? 'val' : 'html'
	    var data = $el.data()
	
	    state += 'Text'
	
	    if (data.resetText == null) $el.data('resetText', $el[val]())
	
	    // push to event loop to allow forms to submit
	    setTimeout($.proxy(function () {
	      $el[val](data[state] == null ? this.options[state] : data[state])
	
	      if (state == 'loadingText') {
	        this.isLoading = true
	        $el.addClass(d).attr(d, d).prop(d, true)
	      } else if (this.isLoading) {
	        this.isLoading = false
	        $el.removeClass(d).removeAttr(d).prop(d, false)
	      }
	    }, this), 0)
	  }
	
	  Button.prototype.toggle = function () {
	    var changed = true
	    var $parent = this.$element.closest('[data-toggle="buttons"]')
	
	    if ($parent.length) {
	      var $input = this.$element.find('input')
	      if ($input.prop('type') == 'radio') {
	        if ($input.prop('checked')) changed = false
	        $parent.find('.active').removeClass('active')
	        this.$element.addClass('active')
	      } else if ($input.prop('type') == 'checkbox') {
	        if (($input.prop('checked')) !== this.$element.hasClass('active')) changed = false
	        this.$element.toggleClass('active')
	      }
	      $input.prop('checked', this.$element.hasClass('active'))
	      if (changed) $input.trigger('change')
	    } else {
	      this.$element.attr('aria-pressed', !this.$element.hasClass('active'))
	      this.$element.toggleClass('active')
	    }
	  }
	
	
	  // BUTTON PLUGIN DEFINITION
	  // ========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.button')
	      var options = typeof option == 'object' && option
	
	      if (!data) $this.data('bs.button', (data = new Button(this, options)))
	
	      if (option == 'toggle') data.toggle()
	      else if (option) data.setState(option)
	    })
	  }
	
	  var old = $.fn.button
	
	  $.fn.button             = Plugin
	  $.fn.button.Constructor = Button
	
	
	  // BUTTON NO CONFLICT
	  // ==================
	
	  $.fn.button.noConflict = function () {
	    $.fn.button = old
	    return this
	  }
	
	
	  // BUTTON DATA-API
	  // ===============
	
	  $(document)
	    .on('click.bs.button.data-api', '[data-toggle^="button"]', function (e) {
	      var $btn = $(e.target).closest('.btn')
	      Plugin.call($btn, 'toggle')
	      if (!($(e.target).is('input[type="radio"], input[type="checkbox"]'))) {
	        // Prevent double click on radios, and the double selections (so cancellation) on checkboxes
	        e.preventDefault()
	        // The target component still receive the focus
	        if ($btn.is('input,button')) $btn.trigger('focus')
	        else $btn.find('input:visible,button:visible').first().trigger('focus')
	      }
	    })
	    .on('focus.bs.button.data-api blur.bs.button.data-api', '[data-toggle^="button"]', function (e) {
	      $(e.target).closest('.btn').toggleClass('focus', /^focus(in)?$/.test(e.type))
	    })
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 7 */
/*!************************************!*\
  !*** ./~/bootstrap/js/carousel.js ***!
  \************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: carousel.js v3.3.7
	 * http://getbootstrap.com/javascript/#carousel
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // CAROUSEL CLASS DEFINITION
	  // =========================
	
	  var Carousel = function (element, options) {
	    this.$element    = $(element)
	    this.$indicators = this.$element.find('.carousel-indicators')
	    this.options     = options
	    this.paused      = null
	    this.sliding     = null
	    this.interval    = null
	    this.$active     = null
	    this.$items      = null
	
	    this.options.keyboard && this.$element.on('keydown.bs.carousel', $.proxy(this.keydown, this))
	
	    this.options.pause == 'hover' && !('ontouchstart' in document.documentElement) && this.$element
	      .on('mouseenter.bs.carousel', $.proxy(this.pause, this))
	      .on('mouseleave.bs.carousel', $.proxy(this.cycle, this))
	  }
	
	  Carousel.VERSION  = '3.3.7'
	
	  Carousel.TRANSITION_DURATION = 600
	
	  Carousel.DEFAULTS = {
	    interval: 5000,
	    pause: 'hover',
	    wrap: true,
	    keyboard: true
	  }
	
	  Carousel.prototype.keydown = function (e) {
	    if (/input|textarea/i.test(e.target.tagName)) return
	    switch (e.which) {
	      case 37: this.prev(); break
	      case 39: this.next(); break
	      default: return
	    }
	
	    e.preventDefault()
	  }
	
	  Carousel.prototype.cycle = function (e) {
	    e || (this.paused = false)
	
	    this.interval && clearInterval(this.interval)
	
	    this.options.interval
	      && !this.paused
	      && (this.interval = setInterval($.proxy(this.next, this), this.options.interval))
	
	    return this
	  }
	
	  Carousel.prototype.getItemIndex = function (item) {
	    this.$items = item.parent().children('.item')
	    return this.$items.index(item || this.$active)
	  }
	
	  Carousel.prototype.getItemForDirection = function (direction, active) {
	    var activeIndex = this.getItemIndex(active)
	    var willWrap = (direction == 'prev' && activeIndex === 0)
	                || (direction == 'next' && activeIndex == (this.$items.length - 1))
	    if (willWrap && !this.options.wrap) return active
	    var delta = direction == 'prev' ? -1 : 1
	    var itemIndex = (activeIndex + delta) % this.$items.length
	    return this.$items.eq(itemIndex)
	  }
	
	  Carousel.prototype.to = function (pos) {
	    var that        = this
	    var activeIndex = this.getItemIndex(this.$active = this.$element.find('.item.active'))
	
	    if (pos > (this.$items.length - 1) || pos < 0) return
	
	    if (this.sliding)       return this.$element.one('slid.bs.carousel', function () { that.to(pos) }) // yes, "slid"
	    if (activeIndex == pos) return this.pause().cycle()
	
	    return this.slide(pos > activeIndex ? 'next' : 'prev', this.$items.eq(pos))
	  }
	
	  Carousel.prototype.pause = function (e) {
	    e || (this.paused = true)
	
	    if (this.$element.find('.next, .prev').length && $.support.transition) {
	      this.$element.trigger($.support.transition.end)
	      this.cycle(true)
	    }
	
	    this.interval = clearInterval(this.interval)
	
	    return this
	  }
	
	  Carousel.prototype.next = function () {
	    if (this.sliding) return
	    return this.slide('next')
	  }
	
	  Carousel.prototype.prev = function () {
	    if (this.sliding) return
	    return this.slide('prev')
	  }
	
	  Carousel.prototype.slide = function (type, next) {
	    var $active   = this.$element.find('.item.active')
	    var $next     = next || this.getItemForDirection(type, $active)
	    var isCycling = this.interval
	    var direction = type == 'next' ? 'left' : 'right'
	    var that      = this
	
	    if ($next.hasClass('active')) return (this.sliding = false)
	
	    var relatedTarget = $next[0]
	    var slideEvent = $.Event('slide.bs.carousel', {
	      relatedTarget: relatedTarget,
	      direction: direction
	    })
	    this.$element.trigger(slideEvent)
	    if (slideEvent.isDefaultPrevented()) return
	
	    this.sliding = true
	
	    isCycling && this.pause()
	
	    if (this.$indicators.length) {
	      this.$indicators.find('.active').removeClass('active')
	      var $nextIndicator = $(this.$indicators.children()[this.getItemIndex($next)])
	      $nextIndicator && $nextIndicator.addClass('active')
	    }
	
	    var slidEvent = $.Event('slid.bs.carousel', { relatedTarget: relatedTarget, direction: direction }) // yes, "slid"
	    if ($.support.transition && this.$element.hasClass('slide')) {
	      $next.addClass(type)
	      $next[0].offsetWidth // force reflow
	      $active.addClass(direction)
	      $next.addClass(direction)
	      $active
	        .one('bsTransitionEnd', function () {
	          $next.removeClass([type, direction].join(' ')).addClass('active')
	          $active.removeClass(['active', direction].join(' '))
	          that.sliding = false
	          setTimeout(function () {
	            that.$element.trigger(slidEvent)
	          }, 0)
	        })
	        .emulateTransitionEnd(Carousel.TRANSITION_DURATION)
	    } else {
	      $active.removeClass('active')
	      $next.addClass('active')
	      this.sliding = false
	      this.$element.trigger(slidEvent)
	    }
	
	    isCycling && this.cycle()
	
	    return this
	  }
	
	
	  // CAROUSEL PLUGIN DEFINITION
	  // ==========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.carousel')
	      var options = $.extend({}, Carousel.DEFAULTS, $this.data(), typeof option == 'object' && option)
	      var action  = typeof option == 'string' ? option : options.slide
	
	      if (!data) $this.data('bs.carousel', (data = new Carousel(this, options)))
	      if (typeof option == 'number') data.to(option)
	      else if (action) data[action]()
	      else if (options.interval) data.pause().cycle()
	    })
	  }
	
	  var old = $.fn.carousel
	
	  $.fn.carousel             = Plugin
	  $.fn.carousel.Constructor = Carousel
	
	
	  // CAROUSEL NO CONFLICT
	  // ====================
	
	  $.fn.carousel.noConflict = function () {
	    $.fn.carousel = old
	    return this
	  }
	
	
	  // CAROUSEL DATA-API
	  // =================
	
	  var clickHandler = function (e) {
	    var href
	    var $this   = $(this)
	    var $target = $($this.attr('data-target') || (href = $this.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '')) // strip for ie7
	    if (!$target.hasClass('carousel')) return
	    var options = $.extend({}, $target.data(), $this.data())
	    var slideIndex = $this.attr('data-slide-to')
	    if (slideIndex) options.interval = false
	
	    Plugin.call($target, options)
	
	    if (slideIndex) {
	      $target.data('bs.carousel').to(slideIndex)
	    }
	
	    e.preventDefault()
	  }
	
	  $(document)
	    .on('click.bs.carousel.data-api', '[data-slide]', clickHandler)
	    .on('click.bs.carousel.data-api', '[data-slide-to]', clickHandler)
	
	  $(window).on('load', function () {
	    $('[data-ride="carousel"]').each(function () {
	      var $carousel = $(this)
	      Plugin.call($carousel, $carousel.data())
	    })
	  })
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 8 */
/*!************************************!*\
  !*** ./~/bootstrap/js/collapse.js ***!
  \************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: collapse.js v3.3.7
	 * http://getbootstrap.com/javascript/#collapse
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	/* jshint latedef: false */
	
	+function ($) {
	  'use strict';
	
	  // COLLAPSE PUBLIC CLASS DEFINITION
	  // ================================
	
	  var Collapse = function (element, options) {
	    this.$element      = $(element)
	    this.options       = $.extend({}, Collapse.DEFAULTS, options)
	    this.$trigger      = $('[data-toggle="collapse"][href="#' + element.id + '"],' +
	                           '[data-toggle="collapse"][data-target="#' + element.id + '"]')
	    this.transitioning = null
	
	    if (this.options.parent) {
	      this.$parent = this.getParent()
	    } else {
	      this.addAriaAndCollapsedClass(this.$element, this.$trigger)
	    }
	
	    if (this.options.toggle) this.toggle()
	  }
	
	  Collapse.VERSION  = '3.3.7'
	
	  Collapse.TRANSITION_DURATION = 350
	
	  Collapse.DEFAULTS = {
	    toggle: true
	  }
	
	  Collapse.prototype.dimension = function () {
	    var hasWidth = this.$element.hasClass('width')
	    return hasWidth ? 'width' : 'height'
	  }
	
	  Collapse.prototype.show = function () {
	    if (this.transitioning || this.$element.hasClass('in')) return
	
	    var activesData
	    var actives = this.$parent && this.$parent.children('.panel').children('.in, .collapsing')
	
	    if (actives && actives.length) {
	      activesData = actives.data('bs.collapse')
	      if (activesData && activesData.transitioning) return
	    }
	
	    var startEvent = $.Event('show.bs.collapse')
	    this.$element.trigger(startEvent)
	    if (startEvent.isDefaultPrevented()) return
	
	    if (actives && actives.length) {
	      Plugin.call(actives, 'hide')
	      activesData || actives.data('bs.collapse', null)
	    }
	
	    var dimension = this.dimension()
	
	    this.$element
	      .removeClass('collapse')
	      .addClass('collapsing')[dimension](0)
	      .attr('aria-expanded', true)
	
	    this.$trigger
	      .removeClass('collapsed')
	      .attr('aria-expanded', true)
	
	    this.transitioning = 1
	
	    var complete = function () {
	      this.$element
	        .removeClass('collapsing')
	        .addClass('collapse in')[dimension]('')
	      this.transitioning = 0
	      this.$element
	        .trigger('shown.bs.collapse')
	    }
	
	    if (!$.support.transition) return complete.call(this)
	
	    var scrollSize = $.camelCase(['scroll', dimension].join('-'))
	
	    this.$element
	      .one('bsTransitionEnd', $.proxy(complete, this))
	      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)[dimension](this.$element[0][scrollSize])
	  }
	
	  Collapse.prototype.hide = function () {
	    if (this.transitioning || !this.$element.hasClass('in')) return
	
	    var startEvent = $.Event('hide.bs.collapse')
	    this.$element.trigger(startEvent)
	    if (startEvent.isDefaultPrevented()) return
	
	    var dimension = this.dimension()
	
	    this.$element[dimension](this.$element[dimension]())[0].offsetHeight
	
	    this.$element
	      .addClass('collapsing')
	      .removeClass('collapse in')
	      .attr('aria-expanded', false)
	
	    this.$trigger
	      .addClass('collapsed')
	      .attr('aria-expanded', false)
	
	    this.transitioning = 1
	
	    var complete = function () {
	      this.transitioning = 0
	      this.$element
	        .removeClass('collapsing')
	        .addClass('collapse')
	        .trigger('hidden.bs.collapse')
	    }
	
	    if (!$.support.transition) return complete.call(this)
	
	    this.$element
	      [dimension](0)
	      .one('bsTransitionEnd', $.proxy(complete, this))
	      .emulateTransitionEnd(Collapse.TRANSITION_DURATION)
	  }
	
	  Collapse.prototype.toggle = function () {
	    this[this.$element.hasClass('in') ? 'hide' : 'show']()
	  }
	
	  Collapse.prototype.getParent = function () {
	    return $(this.options.parent)
	      .find('[data-toggle="collapse"][data-parent="' + this.options.parent + '"]')
	      .each($.proxy(function (i, element) {
	        var $element = $(element)
	        this.addAriaAndCollapsedClass(getTargetFromTrigger($element), $element)
	      }, this))
	      .end()
	  }
	
	  Collapse.prototype.addAriaAndCollapsedClass = function ($element, $trigger) {
	    var isOpen = $element.hasClass('in')
	
	    $element.attr('aria-expanded', isOpen)
	    $trigger
	      .toggleClass('collapsed', !isOpen)
	      .attr('aria-expanded', isOpen)
	  }
	
	  function getTargetFromTrigger($trigger) {
	    var href
	    var target = $trigger.attr('data-target')
	      || (href = $trigger.attr('href')) && href.replace(/.*(?=#[^\s]+$)/, '') // strip for ie7
	
	    return $(target)
	  }
	
	
	  // COLLAPSE PLUGIN DEFINITION
	  // ==========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.collapse')
	      var options = $.extend({}, Collapse.DEFAULTS, $this.data(), typeof option == 'object' && option)
	
	      if (!data && options.toggle && /show|hide/.test(option)) options.toggle = false
	      if (!data) $this.data('bs.collapse', (data = new Collapse(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.collapse
	
	  $.fn.collapse             = Plugin
	  $.fn.collapse.Constructor = Collapse
	
	
	  // COLLAPSE NO CONFLICT
	  // ====================
	
	  $.fn.collapse.noConflict = function () {
	    $.fn.collapse = old
	    return this
	  }
	
	
	  // COLLAPSE DATA-API
	  // =================
	
	  $(document).on('click.bs.collapse.data-api', '[data-toggle="collapse"]', function (e) {
	    var $this   = $(this)
	
	    if (!$this.attr('data-target')) e.preventDefault()
	
	    var $target = getTargetFromTrigger($this)
	    var data    = $target.data('bs.collapse')
	    var option  = data ? 'toggle' : $this.data()
	
	    Plugin.call($target, option)
	  })
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 9 */
/*!************************************!*\
  !*** ./~/bootstrap/js/dropdown.js ***!
  \************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: dropdown.js v3.3.7
	 * http://getbootstrap.com/javascript/#dropdowns
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // DROPDOWN CLASS DEFINITION
	  // =========================
	
	  var backdrop = '.dropdown-backdrop'
	  var toggle   = '[data-toggle="dropdown"]'
	  var Dropdown = function (element) {
	    $(element).on('click.bs.dropdown', this.toggle)
	  }
	
	  Dropdown.VERSION = '3.3.7'
	
	  function getParent($this) {
	    var selector = $this.attr('data-target')
	
	    if (!selector) {
	      selector = $this.attr('href')
	      selector = selector && /#[A-Za-z]/.test(selector) && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
	    }
	
	    var $parent = selector && $(selector)
	
	    return $parent && $parent.length ? $parent : $this.parent()
	  }
	
	  function clearMenus(e) {
	    if (e && e.which === 3) return
	    $(backdrop).remove()
	    $(toggle).each(function () {
	      var $this         = $(this)
	      var $parent       = getParent($this)
	      var relatedTarget = { relatedTarget: this }
	
	      if (!$parent.hasClass('open')) return
	
	      if (e && e.type == 'click' && /input|textarea/i.test(e.target.tagName) && $.contains($parent[0], e.target)) return
	
	      $parent.trigger(e = $.Event('hide.bs.dropdown', relatedTarget))
	
	      if (e.isDefaultPrevented()) return
	
	      $this.attr('aria-expanded', 'false')
	      $parent.removeClass('open').trigger($.Event('hidden.bs.dropdown', relatedTarget))
	    })
	  }
	
	  Dropdown.prototype.toggle = function (e) {
	    var $this = $(this)
	
	    if ($this.is('.disabled, :disabled')) return
	
	    var $parent  = getParent($this)
	    var isActive = $parent.hasClass('open')
	
	    clearMenus()
	
	    if (!isActive) {
	      if ('ontouchstart' in document.documentElement && !$parent.closest('.navbar-nav').length) {
	        // if mobile we use a backdrop because click events don't delegate
	        $(document.createElement('div'))
	          .addClass('dropdown-backdrop')
	          .insertAfter($(this))
	          .on('click', clearMenus)
	      }
	
	      var relatedTarget = { relatedTarget: this }
	      $parent.trigger(e = $.Event('show.bs.dropdown', relatedTarget))
	
	      if (e.isDefaultPrevented()) return
	
	      $this
	        .trigger('focus')
	        .attr('aria-expanded', 'true')
	
	      $parent
	        .toggleClass('open')
	        .trigger($.Event('shown.bs.dropdown', relatedTarget))
	    }
	
	    return false
	  }
	
	  Dropdown.prototype.keydown = function (e) {
	    if (!/(38|40|27|32)/.test(e.which) || /input|textarea/i.test(e.target.tagName)) return
	
	    var $this = $(this)
	
	    e.preventDefault()
	    e.stopPropagation()
	
	    if ($this.is('.disabled, :disabled')) return
	
	    var $parent  = getParent($this)
	    var isActive = $parent.hasClass('open')
	
	    if (!isActive && e.which != 27 || isActive && e.which == 27) {
	      if (e.which == 27) $parent.find(toggle).trigger('focus')
	      return $this.trigger('click')
	    }
	
	    var desc = ' li:not(.disabled):visible a'
	    var $items = $parent.find('.dropdown-menu' + desc)
	
	    if (!$items.length) return
	
	    var index = $items.index(e.target)
	
	    if (e.which == 38 && index > 0)                 index--         // up
	    if (e.which == 40 && index < $items.length - 1) index++         // down
	    if (!~index)                                    index = 0
	
	    $items.eq(index).trigger('focus')
	  }
	
	
	  // DROPDOWN PLUGIN DEFINITION
	  // ==========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this = $(this)
	      var data  = $this.data('bs.dropdown')
	
	      if (!data) $this.data('bs.dropdown', (data = new Dropdown(this)))
	      if (typeof option == 'string') data[option].call($this)
	    })
	  }
	
	  var old = $.fn.dropdown
	
	  $.fn.dropdown             = Plugin
	  $.fn.dropdown.Constructor = Dropdown
	
	
	  // DROPDOWN NO CONFLICT
	  // ====================
	
	  $.fn.dropdown.noConflict = function () {
	    $.fn.dropdown = old
	    return this
	  }
	
	
	  // APPLY TO STANDARD DROPDOWN ELEMENTS
	  // ===================================
	
	  $(document)
	    .on('click.bs.dropdown.data-api', clearMenus)
	    .on('click.bs.dropdown.data-api', '.dropdown form', function (e) { e.stopPropagation() })
	    .on('click.bs.dropdown.data-api', toggle, Dropdown.prototype.toggle)
	    .on('keydown.bs.dropdown.data-api', toggle, Dropdown.prototype.keydown)
	    .on('keydown.bs.dropdown.data-api', '.dropdown-menu', Dropdown.prototype.keydown)
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 10 */
/*!*********************************!*\
  !*** ./~/bootstrap/js/modal.js ***!
  \*********************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: modal.js v3.3.7
	 * http://getbootstrap.com/javascript/#modals
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // MODAL CLASS DEFINITION
	  // ======================
	
	  var Modal = function (element, options) {
	    this.options             = options
	    this.$body               = $(document.body)
	    this.$element            = $(element)
	    this.$dialog             = this.$element.find('.modal-dialog')
	    this.$backdrop           = null
	    this.isShown             = null
	    this.originalBodyPad     = null
	    this.scrollbarWidth      = 0
	    this.ignoreBackdropClick = false
	
	    if (this.options.remote) {
	      this.$element
	        .find('.modal-content')
	        .load(this.options.remote, $.proxy(function () {
	          this.$element.trigger('loaded.bs.modal')
	        }, this))
	    }
	  }
	
	  Modal.VERSION  = '3.3.7'
	
	  Modal.TRANSITION_DURATION = 300
	  Modal.BACKDROP_TRANSITION_DURATION = 150
	
	  Modal.DEFAULTS = {
	    backdrop: true,
	    keyboard: true,
	    show: true
	  }
	
	  Modal.prototype.toggle = function (_relatedTarget) {
	    return this.isShown ? this.hide() : this.show(_relatedTarget)
	  }
	
	  Modal.prototype.show = function (_relatedTarget) {
	    var that = this
	    var e    = $.Event('show.bs.modal', { relatedTarget: _relatedTarget })
	
	    this.$element.trigger(e)
	
	    if (this.isShown || e.isDefaultPrevented()) return
	
	    this.isShown = true
	
	    this.checkScrollbar()
	    this.setScrollbar()
	    this.$body.addClass('modal-open')
	
	    this.escape()
	    this.resize()
	
	    this.$element.on('click.dismiss.bs.modal', '[data-dismiss="modal"]', $.proxy(this.hide, this))
	
	    this.$dialog.on('mousedown.dismiss.bs.modal', function () {
	      that.$element.one('mouseup.dismiss.bs.modal', function (e) {
	        if ($(e.target).is(that.$element)) that.ignoreBackdropClick = true
	      })
	    })
	
	    this.backdrop(function () {
	      var transition = $.support.transition && that.$element.hasClass('fade')
	
	      if (!that.$element.parent().length) {
	        that.$element.appendTo(that.$body) // don't move modals dom position
	      }
	
	      that.$element
	        .show()
	        .scrollTop(0)
	
	      that.adjustDialog()
	
	      if (transition) {
	        that.$element[0].offsetWidth // force reflow
	      }
	
	      that.$element.addClass('in')
	
	      that.enforceFocus()
	
	      var e = $.Event('shown.bs.modal', { relatedTarget: _relatedTarget })
	
	      transition ?
	        that.$dialog // wait for modal to slide in
	          .one('bsTransitionEnd', function () {
	            that.$element.trigger('focus').trigger(e)
	          })
	          .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
	        that.$element.trigger('focus').trigger(e)
	    })
	  }
	
	  Modal.prototype.hide = function (e) {
	    if (e) e.preventDefault()
	
	    e = $.Event('hide.bs.modal')
	
	    this.$element.trigger(e)
	
	    if (!this.isShown || e.isDefaultPrevented()) return
	
	    this.isShown = false
	
	    this.escape()
	    this.resize()
	
	    $(document).off('focusin.bs.modal')
	
	    this.$element
	      .removeClass('in')
	      .off('click.dismiss.bs.modal')
	      .off('mouseup.dismiss.bs.modal')
	
	    this.$dialog.off('mousedown.dismiss.bs.modal')
	
	    $.support.transition && this.$element.hasClass('fade') ?
	      this.$element
	        .one('bsTransitionEnd', $.proxy(this.hideModal, this))
	        .emulateTransitionEnd(Modal.TRANSITION_DURATION) :
	      this.hideModal()
	  }
	
	  Modal.prototype.enforceFocus = function () {
	    $(document)
	      .off('focusin.bs.modal') // guard against infinite focus loop
	      .on('focusin.bs.modal', $.proxy(function (e) {
	        if (document !== e.target &&
	            this.$element[0] !== e.target &&
	            !this.$element.has(e.target).length) {
	          this.$element.trigger('focus')
	        }
	      }, this))
	  }
	
	  Modal.prototype.escape = function () {
	    if (this.isShown && this.options.keyboard) {
	      this.$element.on('keydown.dismiss.bs.modal', $.proxy(function (e) {
	        e.which == 27 && this.hide()
	      }, this))
	    } else if (!this.isShown) {
	      this.$element.off('keydown.dismiss.bs.modal')
	    }
	  }
	
	  Modal.prototype.resize = function () {
	    if (this.isShown) {
	      $(window).on('resize.bs.modal', $.proxy(this.handleUpdate, this))
	    } else {
	      $(window).off('resize.bs.modal')
	    }
	  }
	
	  Modal.prototype.hideModal = function () {
	    var that = this
	    this.$element.hide()
	    this.backdrop(function () {
	      that.$body.removeClass('modal-open')
	      that.resetAdjustments()
	      that.resetScrollbar()
	      that.$element.trigger('hidden.bs.modal')
	    })
	  }
	
	  Modal.prototype.removeBackdrop = function () {
	    this.$backdrop && this.$backdrop.remove()
	    this.$backdrop = null
	  }
	
	  Modal.prototype.backdrop = function (callback) {
	    var that = this
	    var animate = this.$element.hasClass('fade') ? 'fade' : ''
	
	    if (this.isShown && this.options.backdrop) {
	      var doAnimate = $.support.transition && animate
	
	      this.$backdrop = $(document.createElement('div'))
	        .addClass('modal-backdrop ' + animate)
	        .appendTo(this.$body)
	
	      this.$element.on('click.dismiss.bs.modal', $.proxy(function (e) {
	        if (this.ignoreBackdropClick) {
	          this.ignoreBackdropClick = false
	          return
	        }
	        if (e.target !== e.currentTarget) return
	        this.options.backdrop == 'static'
	          ? this.$element[0].focus()
	          : this.hide()
	      }, this))
	
	      if (doAnimate) this.$backdrop[0].offsetWidth // force reflow
	
	      this.$backdrop.addClass('in')
	
	      if (!callback) return
	
	      doAnimate ?
	        this.$backdrop
	          .one('bsTransitionEnd', callback)
	          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
	        callback()
	
	    } else if (!this.isShown && this.$backdrop) {
	      this.$backdrop.removeClass('in')
	
	      var callbackRemove = function () {
	        that.removeBackdrop()
	        callback && callback()
	      }
	      $.support.transition && this.$element.hasClass('fade') ?
	        this.$backdrop
	          .one('bsTransitionEnd', callbackRemove)
	          .emulateTransitionEnd(Modal.BACKDROP_TRANSITION_DURATION) :
	        callbackRemove()
	
	    } else if (callback) {
	      callback()
	    }
	  }
	
	  // these following methods are used to handle overflowing modals
	
	  Modal.prototype.handleUpdate = function () {
	    this.adjustDialog()
	  }
	
	  Modal.prototype.adjustDialog = function () {
	    var modalIsOverflowing = this.$element[0].scrollHeight > document.documentElement.clientHeight
	
	    this.$element.css({
	      paddingLeft:  !this.bodyIsOverflowing && modalIsOverflowing ? this.scrollbarWidth : '',
	      paddingRight: this.bodyIsOverflowing && !modalIsOverflowing ? this.scrollbarWidth : ''
	    })
	  }
	
	  Modal.prototype.resetAdjustments = function () {
	    this.$element.css({
	      paddingLeft: '',
	      paddingRight: ''
	    })
	  }
	
	  Modal.prototype.checkScrollbar = function () {
	    var fullWindowWidth = window.innerWidth
	    if (!fullWindowWidth) { // workaround for missing window.innerWidth in IE8
	      var documentElementRect = document.documentElement.getBoundingClientRect()
	      fullWindowWidth = documentElementRect.right - Math.abs(documentElementRect.left)
	    }
	    this.bodyIsOverflowing = document.body.clientWidth < fullWindowWidth
	    this.scrollbarWidth = this.measureScrollbar()
	  }
	
	  Modal.prototype.setScrollbar = function () {
	    var bodyPad = parseInt((this.$body.css('padding-right') || 0), 10)
	    this.originalBodyPad = document.body.style.paddingRight || ''
	    if (this.bodyIsOverflowing) this.$body.css('padding-right', bodyPad + this.scrollbarWidth)
	  }
	
	  Modal.prototype.resetScrollbar = function () {
	    this.$body.css('padding-right', this.originalBodyPad)
	  }
	
	  Modal.prototype.measureScrollbar = function () { // thx walsh
	    var scrollDiv = document.createElement('div')
	    scrollDiv.className = 'modal-scrollbar-measure'
	    this.$body.append(scrollDiv)
	    var scrollbarWidth = scrollDiv.offsetWidth - scrollDiv.clientWidth
	    this.$body[0].removeChild(scrollDiv)
	    return scrollbarWidth
	  }
	
	
	  // MODAL PLUGIN DEFINITION
	  // =======================
	
	  function Plugin(option, _relatedTarget) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.modal')
	      var options = $.extend({}, Modal.DEFAULTS, $this.data(), typeof option == 'object' && option)
	
	      if (!data) $this.data('bs.modal', (data = new Modal(this, options)))
	      if (typeof option == 'string') data[option](_relatedTarget)
	      else if (options.show) data.show(_relatedTarget)
	    })
	  }
	
	  var old = $.fn.modal
	
	  $.fn.modal             = Plugin
	  $.fn.modal.Constructor = Modal
	
	
	  // MODAL NO CONFLICT
	  // =================
	
	  $.fn.modal.noConflict = function () {
	    $.fn.modal = old
	    return this
	  }
	
	
	  // MODAL DATA-API
	  // ==============
	
	  $(document).on('click.bs.modal.data-api', '[data-toggle="modal"]', function (e) {
	    var $this   = $(this)
	    var href    = $this.attr('href')
	    var $target = $($this.attr('data-target') || (href && href.replace(/.*(?=#[^\s]+$)/, ''))) // strip for ie7
	    var option  = $target.data('bs.modal') ? 'toggle' : $.extend({ remote: !/#/.test(href) && href }, $target.data(), $this.data())
	
	    if ($this.is('a')) e.preventDefault()
	
	    $target.one('show.bs.modal', function (showEvent) {
	      if (showEvent.isDefaultPrevented()) return // only register focus restorer if modal will actually get shown
	      $target.one('hidden.bs.modal', function () {
	        $this.is(':visible') && $this.trigger('focus')
	      })
	    })
	    Plugin.call($target, option, this)
	  })
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 11 */
/*!***********************************!*\
  !*** ./~/bootstrap/js/tooltip.js ***!
  \***********************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: tooltip.js v3.3.7
	 * http://getbootstrap.com/javascript/#tooltip
	 * Inspired by the original jQuery.tipsy by Jason Frame
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // TOOLTIP PUBLIC CLASS DEFINITION
	  // ===============================
	
	  var Tooltip = function (element, options) {
	    this.type       = null
	    this.options    = null
	    this.enabled    = null
	    this.timeout    = null
	    this.hoverState = null
	    this.$element   = null
	    this.inState    = null
	
	    this.init('tooltip', element, options)
	  }
	
	  Tooltip.VERSION  = '3.3.7'
	
	  Tooltip.TRANSITION_DURATION = 150
	
	  Tooltip.DEFAULTS = {
	    animation: true,
	    placement: 'top',
	    selector: false,
	    template: '<div class="tooltip" role="tooltip"><div class="tooltip-arrow"></div><div class="tooltip-inner"></div></div>',
	    trigger: 'hover focus',
	    title: '',
	    delay: 0,
	    html: false,
	    container: false,
	    viewport: {
	      selector: 'body',
	      padding: 0
	    }
	  }
	
	  Tooltip.prototype.init = function (type, element, options) {
	    this.enabled   = true
	    this.type      = type
	    this.$element  = $(element)
	    this.options   = this.getOptions(options)
	    this.$viewport = this.options.viewport && $($.isFunction(this.options.viewport) ? this.options.viewport.call(this, this.$element) : (this.options.viewport.selector || this.options.viewport))
	    this.inState   = { click: false, hover: false, focus: false }
	
	    if (this.$element[0] instanceof document.constructor && !this.options.selector) {
	      throw new Error('`selector` option must be specified when initializing ' + this.type + ' on the window.document object!')
	    }
	
	    var triggers = this.options.trigger.split(' ')
	
	    for (var i = triggers.length; i--;) {
	      var trigger = triggers[i]
	
	      if (trigger == 'click') {
	        this.$element.on('click.' + this.type, this.options.selector, $.proxy(this.toggle, this))
	      } else if (trigger != 'manual') {
	        var eventIn  = trigger == 'hover' ? 'mouseenter' : 'focusin'
	        var eventOut = trigger == 'hover' ? 'mouseleave' : 'focusout'
	
	        this.$element.on(eventIn  + '.' + this.type, this.options.selector, $.proxy(this.enter, this))
	        this.$element.on(eventOut + '.' + this.type, this.options.selector, $.proxy(this.leave, this))
	      }
	    }
	
	    this.options.selector ?
	      (this._options = $.extend({}, this.options, { trigger: 'manual', selector: '' })) :
	      this.fixTitle()
	  }
	
	  Tooltip.prototype.getDefaults = function () {
	    return Tooltip.DEFAULTS
	  }
	
	  Tooltip.prototype.getOptions = function (options) {
	    options = $.extend({}, this.getDefaults(), this.$element.data(), options)
	
	    if (options.delay && typeof options.delay == 'number') {
	      options.delay = {
	        show: options.delay,
	        hide: options.delay
	      }
	    }
	
	    return options
	  }
	
	  Tooltip.prototype.getDelegateOptions = function () {
	    var options  = {}
	    var defaults = this.getDefaults()
	
	    this._options && $.each(this._options, function (key, value) {
	      if (defaults[key] != value) options[key] = value
	    })
	
	    return options
	  }
	
	  Tooltip.prototype.enter = function (obj) {
	    var self = obj instanceof this.constructor ?
	      obj : $(obj.currentTarget).data('bs.' + this.type)
	
	    if (!self) {
	      self = new this.constructor(obj.currentTarget, this.getDelegateOptions())
	      $(obj.currentTarget).data('bs.' + this.type, self)
	    }
	
	    if (obj instanceof $.Event) {
	      self.inState[obj.type == 'focusin' ? 'focus' : 'hover'] = true
	    }
	
	    if (self.tip().hasClass('in') || self.hoverState == 'in') {
	      self.hoverState = 'in'
	      return
	    }
	
	    clearTimeout(self.timeout)
	
	    self.hoverState = 'in'
	
	    if (!self.options.delay || !self.options.delay.show) return self.show()
	
	    self.timeout = setTimeout(function () {
	      if (self.hoverState == 'in') self.show()
	    }, self.options.delay.show)
	  }
	
	  Tooltip.prototype.isInStateTrue = function () {
	    for (var key in this.inState) {
	      if (this.inState[key]) return true
	    }
	
	    return false
	  }
	
	  Tooltip.prototype.leave = function (obj) {
	    var self = obj instanceof this.constructor ?
	      obj : $(obj.currentTarget).data('bs.' + this.type)
	
	    if (!self) {
	      self = new this.constructor(obj.currentTarget, this.getDelegateOptions())
	      $(obj.currentTarget).data('bs.' + this.type, self)
	    }
	
	    if (obj instanceof $.Event) {
	      self.inState[obj.type == 'focusout' ? 'focus' : 'hover'] = false
	    }
	
	    if (self.isInStateTrue()) return
	
	    clearTimeout(self.timeout)
	
	    self.hoverState = 'out'
	
	    if (!self.options.delay || !self.options.delay.hide) return self.hide()
	
	    self.timeout = setTimeout(function () {
	      if (self.hoverState == 'out') self.hide()
	    }, self.options.delay.hide)
	  }
	
	  Tooltip.prototype.show = function () {
	    var e = $.Event('show.bs.' + this.type)
	
	    if (this.hasContent() && this.enabled) {
	      this.$element.trigger(e)
	
	      var inDom = $.contains(this.$element[0].ownerDocument.documentElement, this.$element[0])
	      if (e.isDefaultPrevented() || !inDom) return
	      var that = this
	
	      var $tip = this.tip()
	
	      var tipId = this.getUID(this.type)
	
	      this.setContent()
	      $tip.attr('id', tipId)
	      this.$element.attr('aria-describedby', tipId)
	
	      if (this.options.animation) $tip.addClass('fade')
	
	      var placement = typeof this.options.placement == 'function' ?
	        this.options.placement.call(this, $tip[0], this.$element[0]) :
	        this.options.placement
	
	      var autoToken = /\s?auto?\s?/i
	      var autoPlace = autoToken.test(placement)
	      if (autoPlace) placement = placement.replace(autoToken, '') || 'top'
	
	      $tip
	        .detach()
	        .css({ top: 0, left: 0, display: 'block' })
	        .addClass(placement)
	        .data('bs.' + this.type, this)
	
	      this.options.container ? $tip.appendTo(this.options.container) : $tip.insertAfter(this.$element)
	      this.$element.trigger('inserted.bs.' + this.type)
	
	      var pos          = this.getPosition()
	      var actualWidth  = $tip[0].offsetWidth
	      var actualHeight = $tip[0].offsetHeight
	
	      if (autoPlace) {
	        var orgPlacement = placement
	        var viewportDim = this.getPosition(this.$viewport)
	
	        placement = placement == 'bottom' && pos.bottom + actualHeight > viewportDim.bottom ? 'top'    :
	                    placement == 'top'    && pos.top    - actualHeight < viewportDim.top    ? 'bottom' :
	                    placement == 'right'  && pos.right  + actualWidth  > viewportDim.width  ? 'left'   :
	                    placement == 'left'   && pos.left   - actualWidth  < viewportDim.left   ? 'right'  :
	                    placement
	
	        $tip
	          .removeClass(orgPlacement)
	          .addClass(placement)
	      }
	
	      var calculatedOffset = this.getCalculatedOffset(placement, pos, actualWidth, actualHeight)
	
	      this.applyPlacement(calculatedOffset, placement)
	
	      var complete = function () {
	        var prevHoverState = that.hoverState
	        that.$element.trigger('shown.bs.' + that.type)
	        that.hoverState = null
	
	        if (prevHoverState == 'out') that.leave(that)
	      }
	
	      $.support.transition && this.$tip.hasClass('fade') ?
	        $tip
	          .one('bsTransitionEnd', complete)
	          .emulateTransitionEnd(Tooltip.TRANSITION_DURATION) :
	        complete()
	    }
	  }
	
	  Tooltip.prototype.applyPlacement = function (offset, placement) {
	    var $tip   = this.tip()
	    var width  = $tip[0].offsetWidth
	    var height = $tip[0].offsetHeight
	
	    // manually read margins because getBoundingClientRect includes difference
	    var marginTop = parseInt($tip.css('margin-top'), 10)
	    var marginLeft = parseInt($tip.css('margin-left'), 10)
	
	    // we must check for NaN for ie 8/9
	    if (isNaN(marginTop))  marginTop  = 0
	    if (isNaN(marginLeft)) marginLeft = 0
	
	    offset.top  += marginTop
	    offset.left += marginLeft
	
	    // $.fn.offset doesn't round pixel values
	    // so we use setOffset directly with our own function B-0
	    $.offset.setOffset($tip[0], $.extend({
	      using: function (props) {
	        $tip.css({
	          top: Math.round(props.top),
	          left: Math.round(props.left)
	        })
	      }
	    }, offset), 0)
	
	    $tip.addClass('in')
	
	    // check to see if placing tip in new offset caused the tip to resize itself
	    var actualWidth  = $tip[0].offsetWidth
	    var actualHeight = $tip[0].offsetHeight
	
	    if (placement == 'top' && actualHeight != height) {
	      offset.top = offset.top + height - actualHeight
	    }
	
	    var delta = this.getViewportAdjustedDelta(placement, offset, actualWidth, actualHeight)
	
	    if (delta.left) offset.left += delta.left
	    else offset.top += delta.top
	
	    var isVertical          = /top|bottom/.test(placement)
	    var arrowDelta          = isVertical ? delta.left * 2 - width + actualWidth : delta.top * 2 - height + actualHeight
	    var arrowOffsetPosition = isVertical ? 'offsetWidth' : 'offsetHeight'
	
	    $tip.offset(offset)
	    this.replaceArrow(arrowDelta, $tip[0][arrowOffsetPosition], isVertical)
	  }
	
	  Tooltip.prototype.replaceArrow = function (delta, dimension, isVertical) {
	    this.arrow()
	      .css(isVertical ? 'left' : 'top', 50 * (1 - delta / dimension) + '%')
	      .css(isVertical ? 'top' : 'left', '')
	  }
	
	  Tooltip.prototype.setContent = function () {
	    var $tip  = this.tip()
	    var title = this.getTitle()
	
	    $tip.find('.tooltip-inner')[this.options.html ? 'html' : 'text'](title)
	    $tip.removeClass('fade in top bottom left right')
	  }
	
	  Tooltip.prototype.hide = function (callback) {
	    var that = this
	    var $tip = $(this.$tip)
	    var e    = $.Event('hide.bs.' + this.type)
	
	    function complete() {
	      if (that.hoverState != 'in') $tip.detach()
	      if (that.$element) { // TODO: Check whether guarding this code with this `if` is really necessary.
	        that.$element
	          .removeAttr('aria-describedby')
	          .trigger('hidden.bs.' + that.type)
	      }
	      callback && callback()
	    }
	
	    this.$element.trigger(e)
	
	    if (e.isDefaultPrevented()) return
	
	    $tip.removeClass('in')
	
	    $.support.transition && $tip.hasClass('fade') ?
	      $tip
	        .one('bsTransitionEnd', complete)
	        .emulateTransitionEnd(Tooltip.TRANSITION_DURATION) :
	      complete()
	
	    this.hoverState = null
	
	    return this
	  }
	
	  Tooltip.prototype.fixTitle = function () {
	    var $e = this.$element
	    if ($e.attr('title') || typeof $e.attr('data-original-title') != 'string') {
	      $e.attr('data-original-title', $e.attr('title') || '').attr('title', '')
	    }
	  }
	
	  Tooltip.prototype.hasContent = function () {
	    return this.getTitle()
	  }
	
	  Tooltip.prototype.getPosition = function ($element) {
	    $element   = $element || this.$element
	
	    var el     = $element[0]
	    var isBody = el.tagName == 'BODY'
	
	    var elRect    = el.getBoundingClientRect()
	    if (elRect.width == null) {
	      // width and height are missing in IE8, so compute them manually; see https://github.com/twbs/bootstrap/issues/14093
	      elRect = $.extend({}, elRect, { width: elRect.right - elRect.left, height: elRect.bottom - elRect.top })
	    }
	    var isSvg = window.SVGElement && el instanceof window.SVGElement
	    // Avoid using $.offset() on SVGs since it gives incorrect results in jQuery 3.
	    // See https://github.com/twbs/bootstrap/issues/20280
	    var elOffset  = isBody ? { top: 0, left: 0 } : (isSvg ? null : $element.offset())
	    var scroll    = { scroll: isBody ? document.documentElement.scrollTop || document.body.scrollTop : $element.scrollTop() }
	    var outerDims = isBody ? { width: $(window).width(), height: $(window).height() } : null
	
	    return $.extend({}, elRect, scroll, outerDims, elOffset)
	  }
	
	  Tooltip.prototype.getCalculatedOffset = function (placement, pos, actualWidth, actualHeight) {
	    return placement == 'bottom' ? { top: pos.top + pos.height,   left: pos.left + pos.width / 2 - actualWidth / 2 } :
	           placement == 'top'    ? { top: pos.top - actualHeight, left: pos.left + pos.width / 2 - actualWidth / 2 } :
	           placement == 'left'   ? { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left - actualWidth } :
	        /* placement == 'right' */ { top: pos.top + pos.height / 2 - actualHeight / 2, left: pos.left + pos.width }
	
	  }
	
	  Tooltip.prototype.getViewportAdjustedDelta = function (placement, pos, actualWidth, actualHeight) {
	    var delta = { top: 0, left: 0 }
	    if (!this.$viewport) return delta
	
	    var viewportPadding = this.options.viewport && this.options.viewport.padding || 0
	    var viewportDimensions = this.getPosition(this.$viewport)
	
	    if (/right|left/.test(placement)) {
	      var topEdgeOffset    = pos.top - viewportPadding - viewportDimensions.scroll
	      var bottomEdgeOffset = pos.top + viewportPadding - viewportDimensions.scroll + actualHeight
	      if (topEdgeOffset < viewportDimensions.top) { // top overflow
	        delta.top = viewportDimensions.top - topEdgeOffset
	      } else if (bottomEdgeOffset > viewportDimensions.top + viewportDimensions.height) { // bottom overflow
	        delta.top = viewportDimensions.top + viewportDimensions.height - bottomEdgeOffset
	      }
	    } else {
	      var leftEdgeOffset  = pos.left - viewportPadding
	      var rightEdgeOffset = pos.left + viewportPadding + actualWidth
	      if (leftEdgeOffset < viewportDimensions.left) { // left overflow
	        delta.left = viewportDimensions.left - leftEdgeOffset
	      } else if (rightEdgeOffset > viewportDimensions.right) { // right overflow
	        delta.left = viewportDimensions.left + viewportDimensions.width - rightEdgeOffset
	      }
	    }
	
	    return delta
	  }
	
	  Tooltip.prototype.getTitle = function () {
	    var title
	    var $e = this.$element
	    var o  = this.options
	
	    title = $e.attr('data-original-title')
	      || (typeof o.title == 'function' ? o.title.call($e[0]) :  o.title)
	
	    return title
	  }
	
	  Tooltip.prototype.getUID = function (prefix) {
	    do prefix += ~~(Math.random() * 1000000)
	    while (document.getElementById(prefix))
	    return prefix
	  }
	
	  Tooltip.prototype.tip = function () {
	    if (!this.$tip) {
	      this.$tip = $(this.options.template)
	      if (this.$tip.length != 1) {
	        throw new Error(this.type + ' `template` option must consist of exactly 1 top-level element!')
	      }
	    }
	    return this.$tip
	  }
	
	  Tooltip.prototype.arrow = function () {
	    return (this.$arrow = this.$arrow || this.tip().find('.tooltip-arrow'))
	  }
	
	  Tooltip.prototype.enable = function () {
	    this.enabled = true
	  }
	
	  Tooltip.prototype.disable = function () {
	    this.enabled = false
	  }
	
	  Tooltip.prototype.toggleEnabled = function () {
	    this.enabled = !this.enabled
	  }
	
	  Tooltip.prototype.toggle = function (e) {
	    var self = this
	    if (e) {
	      self = $(e.currentTarget).data('bs.' + this.type)
	      if (!self) {
	        self = new this.constructor(e.currentTarget, this.getDelegateOptions())
	        $(e.currentTarget).data('bs.' + this.type, self)
	      }
	    }
	
	    if (e) {
	      self.inState.click = !self.inState.click
	      if (self.isInStateTrue()) self.enter(self)
	      else self.leave(self)
	    } else {
	      self.tip().hasClass('in') ? self.leave(self) : self.enter(self)
	    }
	  }
	
	  Tooltip.prototype.destroy = function () {
	    var that = this
	    clearTimeout(this.timeout)
	    this.hide(function () {
	      that.$element.off('.' + that.type).removeData('bs.' + that.type)
	      if (that.$tip) {
	        that.$tip.detach()
	      }
	      that.$tip = null
	      that.$arrow = null
	      that.$viewport = null
	      that.$element = null
	    })
	  }
	
	
	  // TOOLTIP PLUGIN DEFINITION
	  // =========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.tooltip')
	      var options = typeof option == 'object' && option
	
	      if (!data && /destroy|hide/.test(option)) return
	      if (!data) $this.data('bs.tooltip', (data = new Tooltip(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.tooltip
	
	  $.fn.tooltip             = Plugin
	  $.fn.tooltip.Constructor = Tooltip
	
	
	  // TOOLTIP NO CONFLICT
	  // ===================
	
	  $.fn.tooltip.noConflict = function () {
	    $.fn.tooltip = old
	    return this
	  }
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 12 */
/*!***********************************!*\
  !*** ./~/bootstrap/js/popover.js ***!
  \***********************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: popover.js v3.3.7
	 * http://getbootstrap.com/javascript/#popovers
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // POPOVER PUBLIC CLASS DEFINITION
	  // ===============================
	
	  var Popover = function (element, options) {
	    this.init('popover', element, options)
	  }
	
	  if (!$.fn.tooltip) throw new Error('Popover requires tooltip.js')
	
	  Popover.VERSION  = '3.3.7'
	
	  Popover.DEFAULTS = $.extend({}, $.fn.tooltip.Constructor.DEFAULTS, {
	    placement: 'right',
	    trigger: 'click',
	    content: '',
	    template: '<div class="popover" role="tooltip"><div class="arrow"></div><h3 class="popover-title"></h3><div class="popover-content"></div></div>'
	  })
	
	
	  // NOTE: POPOVER EXTENDS tooltip.js
	  // ================================
	
	  Popover.prototype = $.extend({}, $.fn.tooltip.Constructor.prototype)
	
	  Popover.prototype.constructor = Popover
	
	  Popover.prototype.getDefaults = function () {
	    return Popover.DEFAULTS
	  }
	
	  Popover.prototype.setContent = function () {
	    var $tip    = this.tip()
	    var title   = this.getTitle()
	    var content = this.getContent()
	
	    $tip.find('.popover-title')[this.options.html ? 'html' : 'text'](title)
	    $tip.find('.popover-content').children().detach().end()[ // we use append for html objects to maintain js events
	      this.options.html ? (typeof content == 'string' ? 'html' : 'append') : 'text'
	    ](content)
	
	    $tip.removeClass('fade top bottom left right in')
	
	    // IE8 doesn't accept hiding via the `:empty` pseudo selector, we have to do
	    // this manually by checking the contents.
	    if (!$tip.find('.popover-title').html()) $tip.find('.popover-title').hide()
	  }
	
	  Popover.prototype.hasContent = function () {
	    return this.getTitle() || this.getContent()
	  }
	
	  Popover.prototype.getContent = function () {
	    var $e = this.$element
	    var o  = this.options
	
	    return $e.attr('data-content')
	      || (typeof o.content == 'function' ?
	            o.content.call($e[0]) :
	            o.content)
	  }
	
	  Popover.prototype.arrow = function () {
	    return (this.$arrow = this.$arrow || this.tip().find('.arrow'))
	  }
	
	
	  // POPOVER PLUGIN DEFINITION
	  // =========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.popover')
	      var options = typeof option == 'object' && option
	
	      if (!data && /destroy|hide/.test(option)) return
	      if (!data) $this.data('bs.popover', (data = new Popover(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.popover
	
	  $.fn.popover             = Plugin
	  $.fn.popover.Constructor = Popover
	
	
	  // POPOVER NO CONFLICT
	  // ===================
	
	  $.fn.popover.noConflict = function () {
	    $.fn.popover = old
	    return this
	  }
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 13 */
/*!*************************************!*\
  !*** ./~/bootstrap/js/scrollspy.js ***!
  \*************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: scrollspy.js v3.3.7
	 * http://getbootstrap.com/javascript/#scrollspy
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // SCROLLSPY CLASS DEFINITION
	  // ==========================
	
	  function ScrollSpy(element, options) {
	    this.$body          = $(document.body)
	    this.$scrollElement = $(element).is(document.body) ? $(window) : $(element)
	    this.options        = $.extend({}, ScrollSpy.DEFAULTS, options)
	    this.selector       = (this.options.target || '') + ' .nav li > a'
	    this.offsets        = []
	    this.targets        = []
	    this.activeTarget   = null
	    this.scrollHeight   = 0
	
	    this.$scrollElement.on('scroll.bs.scrollspy', $.proxy(this.process, this))
	    this.refresh()
	    this.process()
	  }
	
	  ScrollSpy.VERSION  = '3.3.7'
	
	  ScrollSpy.DEFAULTS = {
	    offset: 10
	  }
	
	  ScrollSpy.prototype.getScrollHeight = function () {
	    return this.$scrollElement[0].scrollHeight || Math.max(this.$body[0].scrollHeight, document.documentElement.scrollHeight)
	  }
	
	  ScrollSpy.prototype.refresh = function () {
	    var that          = this
	    var offsetMethod  = 'offset'
	    var offsetBase    = 0
	
	    this.offsets      = []
	    this.targets      = []
	    this.scrollHeight = this.getScrollHeight()
	
	    if (!$.isWindow(this.$scrollElement[0])) {
	      offsetMethod = 'position'
	      offsetBase   = this.$scrollElement.scrollTop()
	    }
	
	    this.$body
	      .find(this.selector)
	      .map(function () {
	        var $el   = $(this)
	        var href  = $el.data('target') || $el.attr('href')
	        var $href = /^#./.test(href) && $(href)
	
	        return ($href
	          && $href.length
	          && $href.is(':visible')
	          && [[$href[offsetMethod]().top + offsetBase, href]]) || null
	      })
	      .sort(function (a, b) { return a[0] - b[0] })
	      .each(function () {
	        that.offsets.push(this[0])
	        that.targets.push(this[1])
	      })
	  }
	
	  ScrollSpy.prototype.process = function () {
	    var scrollTop    = this.$scrollElement.scrollTop() + this.options.offset
	    var scrollHeight = this.getScrollHeight()
	    var maxScroll    = this.options.offset + scrollHeight - this.$scrollElement.height()
	    var offsets      = this.offsets
	    var targets      = this.targets
	    var activeTarget = this.activeTarget
	    var i
	
	    if (this.scrollHeight != scrollHeight) {
	      this.refresh()
	    }
	
	    if (scrollTop >= maxScroll) {
	      return activeTarget != (i = targets[targets.length - 1]) && this.activate(i)
	    }
	
	    if (activeTarget && scrollTop < offsets[0]) {
	      this.activeTarget = null
	      return this.clear()
	    }
	
	    for (i = offsets.length; i--;) {
	      activeTarget != targets[i]
	        && scrollTop >= offsets[i]
	        && (offsets[i + 1] === undefined || scrollTop < offsets[i + 1])
	        && this.activate(targets[i])
	    }
	  }
	
	  ScrollSpy.prototype.activate = function (target) {
	    this.activeTarget = target
	
	    this.clear()
	
	    var selector = this.selector +
	      '[data-target="' + target + '"],' +
	      this.selector + '[href="' + target + '"]'
	
	    var active = $(selector)
	      .parents('li')
	      .addClass('active')
	
	    if (active.parent('.dropdown-menu').length) {
	      active = active
	        .closest('li.dropdown')
	        .addClass('active')
	    }
	
	    active.trigger('activate.bs.scrollspy')
	  }
	
	  ScrollSpy.prototype.clear = function () {
	    $(this.selector)
	      .parentsUntil(this.options.target, '.active')
	      .removeClass('active')
	  }
	
	
	  // SCROLLSPY PLUGIN DEFINITION
	  // ===========================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.scrollspy')
	      var options = typeof option == 'object' && option
	
	      if (!data) $this.data('bs.scrollspy', (data = new ScrollSpy(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.scrollspy
	
	  $.fn.scrollspy             = Plugin
	  $.fn.scrollspy.Constructor = ScrollSpy
	
	
	  // SCROLLSPY NO CONFLICT
	  // =====================
	
	  $.fn.scrollspy.noConflict = function () {
	    $.fn.scrollspy = old
	    return this
	  }
	
	
	  // SCROLLSPY DATA-API
	  // ==================
	
	  $(window).on('load.bs.scrollspy.data-api', function () {
	    $('[data-spy="scroll"]').each(function () {
	      var $spy = $(this)
	      Plugin.call($spy, $spy.data())
	    })
	  })
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 14 */
/*!*******************************!*\
  !*** ./~/bootstrap/js/tab.js ***!
  \*******************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: tab.js v3.3.7
	 * http://getbootstrap.com/javascript/#tabs
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // TAB CLASS DEFINITION
	  // ====================
	
	  var Tab = function (element) {
	    // jscs:disable requireDollarBeforejQueryAssignment
	    this.element = $(element)
	    // jscs:enable requireDollarBeforejQueryAssignment
	  }
	
	  Tab.VERSION = '3.3.7'
	
	  Tab.TRANSITION_DURATION = 150
	
	  Tab.prototype.show = function () {
	    var $this    = this.element
	    var $ul      = $this.closest('ul:not(.dropdown-menu)')
	    var selector = $this.data('target')
	
	    if (!selector) {
	      selector = $this.attr('href')
	      selector = selector && selector.replace(/.*(?=#[^\s]*$)/, '') // strip for ie7
	    }
	
	    if ($this.parent('li').hasClass('active')) return
	
	    var $previous = $ul.find('.active:last a')
	    var hideEvent = $.Event('hide.bs.tab', {
	      relatedTarget: $this[0]
	    })
	    var showEvent = $.Event('show.bs.tab', {
	      relatedTarget: $previous[0]
	    })
	
	    $previous.trigger(hideEvent)
	    $this.trigger(showEvent)
	
	    if (showEvent.isDefaultPrevented() || hideEvent.isDefaultPrevented()) return
	
	    var $target = $(selector)
	
	    this.activate($this.closest('li'), $ul)
	    this.activate($target, $target.parent(), function () {
	      $previous.trigger({
	        type: 'hidden.bs.tab',
	        relatedTarget: $this[0]
	      })
	      $this.trigger({
	        type: 'shown.bs.tab',
	        relatedTarget: $previous[0]
	      })
	    })
	  }
	
	  Tab.prototype.activate = function (element, container, callback) {
	    var $active    = container.find('> .active')
	    var transition = callback
	      && $.support.transition
	      && ($active.length && $active.hasClass('fade') || !!container.find('> .fade').length)
	
	    function next() {
	      $active
	        .removeClass('active')
	        .find('> .dropdown-menu > .active')
	          .removeClass('active')
	        .end()
	        .find('[data-toggle="tab"]')
	          .attr('aria-expanded', false)
	
	      element
	        .addClass('active')
	        .find('[data-toggle="tab"]')
	          .attr('aria-expanded', true)
	
	      if (transition) {
	        element[0].offsetWidth // reflow for transition
	        element.addClass('in')
	      } else {
	        element.removeClass('fade')
	      }
	
	      if (element.parent('.dropdown-menu').length) {
	        element
	          .closest('li.dropdown')
	            .addClass('active')
	          .end()
	          .find('[data-toggle="tab"]')
	            .attr('aria-expanded', true)
	      }
	
	      callback && callback()
	    }
	
	    $active.length && transition ?
	      $active
	        .one('bsTransitionEnd', next)
	        .emulateTransitionEnd(Tab.TRANSITION_DURATION) :
	      next()
	
	    $active.removeClass('in')
	  }
	
	
	  // TAB PLUGIN DEFINITION
	  // =====================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this = $(this)
	      var data  = $this.data('bs.tab')
	
	      if (!data) $this.data('bs.tab', (data = new Tab(this)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.tab
	
	  $.fn.tab             = Plugin
	  $.fn.tab.Constructor = Tab
	
	
	  // TAB NO CONFLICT
	  // ===============
	
	  $.fn.tab.noConflict = function () {
	    $.fn.tab = old
	    return this
	  }
	
	
	  // TAB DATA-API
	  // ============
	
	  var clickHandler = function (e) {
	    e.preventDefault()
	    Plugin.call($(this), 'show')
	  }
	
	  $(document)
	    .on('click.bs.tab.data-api', '[data-toggle="tab"]', clickHandler)
	    .on('click.bs.tab.data-api', '[data-toggle="pill"]', clickHandler)
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 15 */
/*!*********************************!*\
  !*** ./~/bootstrap/js/affix.js ***!
  \*********************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {/* ========================================================================
	 * Bootstrap: affix.js v3.3.7
	 * http://getbootstrap.com/javascript/#affix
	 * ========================================================================
	 * Copyright 2011-2016 Twitter, Inc.
	 * Licensed under MIT (https://github.com/twbs/bootstrap/blob/master/LICENSE)
	 * ======================================================================== */
	
	
	+function ($) {
	  'use strict';
	
	  // AFFIX CLASS DEFINITION
	  // ======================
	
	  var Affix = function (element, options) {
	    this.options = $.extend({}, Affix.DEFAULTS, options)
	
	    this.$target = $(this.options.target)
	      .on('scroll.bs.affix.data-api', $.proxy(this.checkPosition, this))
	      .on('click.bs.affix.data-api',  $.proxy(this.checkPositionWithEventLoop, this))
	
	    this.$element     = $(element)
	    this.affixed      = null
	    this.unpin        = null
	    this.pinnedOffset = null
	
	    this.checkPosition()
	  }
	
	  Affix.VERSION  = '3.3.7'
	
	  Affix.RESET    = 'affix affix-top affix-bottom'
	
	  Affix.DEFAULTS = {
	    offset: 0,
	    target: window
	  }
	
	  Affix.prototype.getState = function (scrollHeight, height, offsetTop, offsetBottom) {
	    var scrollTop    = this.$target.scrollTop()
	    var position     = this.$element.offset()
	    var targetHeight = this.$target.height()
	
	    if (offsetTop != null && this.affixed == 'top') return scrollTop < offsetTop ? 'top' : false
	
	    if (this.affixed == 'bottom') {
	      if (offsetTop != null) return (scrollTop + this.unpin <= position.top) ? false : 'bottom'
	      return (scrollTop + targetHeight <= scrollHeight - offsetBottom) ? false : 'bottom'
	    }
	
	    var initializing   = this.affixed == null
	    var colliderTop    = initializing ? scrollTop : position.top
	    var colliderHeight = initializing ? targetHeight : height
	
	    if (offsetTop != null && scrollTop <= offsetTop) return 'top'
	    if (offsetBottom != null && (colliderTop + colliderHeight >= scrollHeight - offsetBottom)) return 'bottom'
	
	    return false
	  }
	
	  Affix.prototype.getPinnedOffset = function () {
	    if (this.pinnedOffset) return this.pinnedOffset
	    this.$element.removeClass(Affix.RESET).addClass('affix')
	    var scrollTop = this.$target.scrollTop()
	    var position  = this.$element.offset()
	    return (this.pinnedOffset = position.top - scrollTop)
	  }
	
	  Affix.prototype.checkPositionWithEventLoop = function () {
	    setTimeout($.proxy(this.checkPosition, this), 1)
	  }
	
	  Affix.prototype.checkPosition = function () {
	    if (!this.$element.is(':visible')) return
	
	    var height       = this.$element.height()
	    var offset       = this.options.offset
	    var offsetTop    = offset.top
	    var offsetBottom = offset.bottom
	    var scrollHeight = Math.max($(document).height(), $(document.body).height())
	
	    if (typeof offset != 'object')         offsetBottom = offsetTop = offset
	    if (typeof offsetTop == 'function')    offsetTop    = offset.top(this.$element)
	    if (typeof offsetBottom == 'function') offsetBottom = offset.bottom(this.$element)
	
	    var affix = this.getState(scrollHeight, height, offsetTop, offsetBottom)
	
	    if (this.affixed != affix) {
	      if (this.unpin != null) this.$element.css('top', '')
	
	      var affixType = 'affix' + (affix ? '-' + affix : '')
	      var e         = $.Event(affixType + '.bs.affix')
	
	      this.$element.trigger(e)
	
	      if (e.isDefaultPrevented()) return
	
	      this.affixed = affix
	      this.unpin = affix == 'bottom' ? this.getPinnedOffset() : null
	
	      this.$element
	        .removeClass(Affix.RESET)
	        .addClass(affixType)
	        .trigger(affixType.replace('affix', 'affixed') + '.bs.affix')
	    }
	
	    if (affix == 'bottom') {
	      this.$element.offset({
	        top: scrollHeight - height - offsetBottom
	      })
	    }
	  }
	
	
	  // AFFIX PLUGIN DEFINITION
	  // =======================
	
	  function Plugin(option) {
	    return this.each(function () {
	      var $this   = $(this)
	      var data    = $this.data('bs.affix')
	      var options = typeof option == 'object' && option
	
	      if (!data) $this.data('bs.affix', (data = new Affix(this, options)))
	      if (typeof option == 'string') data[option]()
	    })
	  }
	
	  var old = $.fn.affix
	
	  $.fn.affix             = Plugin
	  $.fn.affix.Constructor = Affix
	
	
	  // AFFIX NO CONFLICT
	  // =================
	
	  $.fn.affix.noConflict = function () {
	    $.fn.affix = old
	    return this
	  }
	
	
	  // AFFIX DATA-API
	  // ==============
	
	  $(window).on('load', function () {
	    $('[data-spy="affix"]').each(function () {
	      var $spy = $(this)
	      var data = $spy.data()
	
	      data.offset = data.offset || {}
	
	      if (data.offsetBottom != null) data.offset.bottom = data.offsetBottom
	      if (data.offsetTop    != null) data.offset.top    = data.offsetTop
	
	      Plugin.call($spy, data)
	    })
	  })
	
	}(jQuery);
	
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 16 */,
/* 17 */,
/* 18 */,
/* 19 */,
/* 20 */
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
/* 21 */
/*!***************************************************************!*\
  !*** ./~/backbone-validation/dist/backbone-validation-amd.js ***!
  \***************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	// Backbone.Validation v0.11.5
	//
	// Copyright (c) 2011-2015 Thomas Pedersen
	// Distributed under MIT License
	//
	// Documentation and full license available at:
	// http://thedersen.com/projects/backbone-validation
	(function (factory) {
	  if (true) {
	    module.exports = factory(__webpack_require__(/*! backbone */ 17), __webpack_require__(/*! underscore */ 16));
	  } else if (typeof define === 'function' && define.amd) {
	    define(['backbone', 'underscore'], factory);
	  }
	}(function (Backbone, _) {
	  Backbone.Validation = (function(_){
	    'use strict';
	  
	    // Default options
	    // ---------------
	  
	    var defaultOptions = {
	      forceUpdate: false,
	      selector: 'name',
	      labelFormatter: 'sentenceCase',
	      valid: Function.prototype,
	      invalid: Function.prototype
	    };
	  
	  
	    // Helper functions
	    // ----------------
	  
	    // Formatting functions used for formatting error messages
	    var formatFunctions = {
	      // Uses the configured label formatter to format the attribute name
	      // to make it more readable for the user
	      formatLabel: function(attrName, model) {
	        return defaultLabelFormatters[defaultOptions.labelFormatter](attrName, model);
	      },
	  
	      // Replaces nummeric placeholders like {0} in a string with arguments
	      // passed to the function
	      format: function() {
	        var args = Array.prototype.slice.call(arguments),
	            text = args.shift();
	        return text.replace(/\{(\d+)\}/g, function(match, number) {
	          return typeof args[number] !== 'undefined' ? args[number] : match;
	        });
	      }
	    };
	  
	    // Flattens an object
	    // eg:
	    //
	    //     var o = {
	    //       owner: {
	    //         name: 'Backbone',
	    //         address: {
	    //           street: 'Street',
	    //           zip: 1234
	    //         }
	    //       }
	    //     };
	    //
	    // becomes:
	    //
	    //     var o = {
	    //       'owner': {
	    //         name: 'Backbone',
	    //         address: {
	    //           street: 'Street',
	    //           zip: 1234
	    //         }
	    //       },
	    //       'owner.name': 'Backbone',
	    //       'owner.address': {
	    //         street: 'Street',
	    //         zip: 1234
	    //       },
	    //       'owner.address.street': 'Street',
	    //       'owner.address.zip': 1234
	    //     };
	    // This may seem redundant, but it allows for maximum flexibility
	    // in validation rules.
	    var flatten = function (obj, into, prefix) {
	      into = into || {};
	      prefix = prefix || '';
	  
	      _.each(obj, function(val, key) {
	        if(obj.hasOwnProperty(key)) {
	          if (!!val && _.isArray(val)) {
	            _.forEach(val, function(v, k) {
	              flatten(v, into, prefix + key + '.' + k + '.');
	              into[prefix + key + '.' + k] = v;
	            });
	          } else if (!!val && typeof val === 'object' && val.constructor === Object) {
	            flatten(val, into, prefix + key + '.');
	          }
	  
	          // Register the current level object as well
	          into[prefix + key] = val;
	        }
	      });
	  
	      return into;
	    };
	  
	    // Validation
	    // ----------
	  
	    var Validation = (function(){
	  
	      // Returns an object with undefined properties for all
	      // attributes on the model that has defined one or more
	      // validation rules.
	      var getValidatedAttrs = function(model, attrs) {
	        attrs = attrs || _.keys(_.result(model, 'validation') || {});
	        return _.reduce(attrs, function(memo, key) {
	          memo[key] = void 0;
	          return memo;
	        }, {});
	      };
	  
	      // Returns an array with attributes passed through options
	      var getOptionsAttrs = function(options, view) {
	        var attrs = options.attributes;
	        if (_.isFunction(attrs)) {
	          attrs = attrs(view);
	        } else if (_.isString(attrs) && (_.isFunction(defaultAttributeLoaders[attrs]))) {
	          attrs = defaultAttributeLoaders[attrs](view);
	        }
	        if (_.isArray(attrs)) {
	          return attrs;
	        }
	      };
	  
	  
	      // Looks on the model for validations for a specified
	      // attribute. Returns an array of any validators defined,
	      // or an empty array if none is defined.
	      var getValidators = function(model, attr) {
	        var attrValidationSet = model.validation ? _.result(model, 'validation')[attr] || {} : {};
	  
	        // If the validator is a function or a string, wrap it in a function validator
	        if (_.isFunction(attrValidationSet) || _.isString(attrValidationSet)) {
	          attrValidationSet = {
	            fn: attrValidationSet
	          };
	        }
	  
	        // Stick the validator object into an array
	        if(!_.isArray(attrValidationSet)) {
	          attrValidationSet = [attrValidationSet];
	        }
	  
	        // Reduces the array of validators into a new array with objects
	        // with a validation method to call, the value to validate against
	        // and the specified error message, if any
	        return _.reduce(attrValidationSet, function(memo, attrValidation) {
	          _.each(_.without(_.keys(attrValidation), 'msg'), function(validator) {
	            memo.push({
	              fn: defaultValidators[validator],
	              val: attrValidation[validator],
	              msg: attrValidation.msg
	            });
	          });
	          return memo;
	        }, []);
	      };
	  
	      // Validates an attribute against all validators defined
	      // for that attribute. If one or more errors are found,
	      // the first error message is returned.
	      // If the attribute is valid, an empty string is returned.
	      var validateAttr = function(model, attr, value, computed) {
	        // Reduces the array of validators to an error message by
	        // applying all the validators and returning the first error
	        // message, if any.
	        return _.reduce(getValidators(model, attr), function(memo, validator){
	          // Pass the format functions plus the default
	          // validators as the context to the validator
	          var ctx = _.extend({}, formatFunctions, defaultValidators),
	              result = validator.fn.call(ctx, value, attr, validator.val, model, computed);
	  
	          if(result === false || memo === false) {
	            return false;
	          }
	          if (result && !memo) {
	            return _.result(validator, 'msg') || result;
	          }
	          return memo;
	        }, '');
	      };
	  
	      // Loops through the model's attributes and validates the specified attrs.
	      // Returns and object containing names of invalid attributes
	      // as well as error messages.
	      var validateModel = function(model, attrs, validatedAttrs) {
	        var error,
	            invalidAttrs = {},
	            isValid = true,
	            computed = _.clone(attrs);
	  
	        _.each(validatedAttrs, function(val, attr) {
	          error = validateAttr(model, attr, val, computed);
	          if (error) {
	            invalidAttrs[attr] = error;
	            isValid = false;
	          }
	        });
	  
	        return {
	          invalidAttrs: invalidAttrs,
	          isValid: isValid
	        };
	      };
	  
	      // Contains the methods that are mixed in on the model when binding
	      var mixin = function(view, options) {
	        return {
	  
	          // Check whether or not a value, or a hash of values
	          // passes validation without updating the model
	          preValidate: function(attr, value) {
	            var self = this,
	                result = {},
	                error;
	  
	            if(_.isObject(attr)){
	              _.each(attr, function(value, key) {
	                error = self.preValidate(key, value);
	                if(error){
	                  result[key] = error;
	                }
	              });
	  
	              return _.isEmpty(result) ? undefined : result;
	            }
	            else {
	              return validateAttr(this, attr, value, _.extend({}, this.attributes));
	            }
	          },
	  
	          // Check to see if an attribute, an array of attributes or the
	          // entire model is valid. Passing true will force a validation
	          // of the model.
	          isValid: function(option) {
	            var flattened, attrs, error, invalidAttrs;
	  
	            option = option || getOptionsAttrs(options, view);
	  
	            if(_.isString(option)){
	              attrs = [option];
	            } else if(_.isArray(option)) {
	              attrs = option;
	            }
	            if (attrs) {
	              flattened = flatten(this.attributes);
	              //Loop through all associated views
	              _.each(this.associatedViews, function(view) {
	                _.each(attrs, function (attr) {
	                  error = validateAttr(this, attr, flattened[attr], _.extend({}, this.attributes));
	                  if (error) {
	                    options.invalid(view, attr, error, options.selector);
	                    invalidAttrs = invalidAttrs || {};
	                    invalidAttrs[attr] = error;
	                  } else {
	                    options.valid(view, attr, options.selector);
	                  }
	                }, this);
	              }, this);
	            }
	  
	            if(option === true) {
	              invalidAttrs = this.validate();
	            }
	            if (invalidAttrs) {
	              this.trigger('invalid', this, invalidAttrs, {validationError: invalidAttrs});
	            }
	            return attrs ? !invalidAttrs : this.validation ? this._isValid : true;
	          },
	  
	          // This is called by Backbone when it needs to perform validation.
	          // You can call it manually without any parameters to validate the
	          // entire model.
	          validate: function(attrs, setOptions){
	            var model = this,
	                validateAll = !attrs,
	                opt = _.extend({}, options, setOptions),
	                validatedAttrs = getValidatedAttrs(model, getOptionsAttrs(options, view)),
	                allAttrs = _.extend({}, validatedAttrs, model.attributes, attrs),
	                flattened = flatten(allAttrs),
	                changedAttrs = attrs ? flatten(attrs) : flattened,
	                result = validateModel(model, allAttrs, _.pick(flattened, _.keys(validatedAttrs)));
	  
	            model._isValid = result.isValid;
	  
	            //After validation is performed, loop through all associated views
	            _.each(model.associatedViews, function(view){
	  
	              // After validation is performed, loop through all validated and changed attributes
	              // and call the valid and invalid callbacks so the view is updated.
	              _.each(validatedAttrs, function(val, attr){
	                  var invalid = result.invalidAttrs.hasOwnProperty(attr),
	                    changed = changedAttrs.hasOwnProperty(attr);
	  
	                  if(!invalid){
	                    opt.valid(view, attr, opt.selector);
	                  }
	                  if(invalid && (changed || validateAll)){
	                    opt.invalid(view, attr, result.invalidAttrs[attr], opt.selector);
	                  }
	              });
	            });
	  
	            // Trigger validated events.
	            // Need to defer this so the model is actually updated before
	            // the event is triggered.
	            _.defer(function() {
	              model.trigger('validated', model._isValid, model, result.invalidAttrs);
	              model.trigger('validated:' + (model._isValid ? 'valid' : 'invalid'), model, result.invalidAttrs);
	            });
	  
	            // Return any error messages to Backbone, unless the forceUpdate flag is set.
	            // Then we do not return anything and fools Backbone to believe the validation was
	            // a success. That way Backbone will update the model regardless.
	            if (!opt.forceUpdate && _.intersection(_.keys(result.invalidAttrs), _.keys(changedAttrs)).length > 0) {
	              return result.invalidAttrs;
	            }
	          }
	        };
	      };
	  
	      // Helper to mix in validation on a model. Stores the view in the associated views array.
	      var bindModel = function(view, model, options) {
	        if (model.associatedViews) {
	          model.associatedViews.push(view);
	        } else {
	          model.associatedViews = [view];
	        }
	        _.extend(model, mixin(view, options));
	      };
	  
	      // Removes view from associated views of the model or the methods
	      // added to a model if no view or single view provided
	      var unbindModel = function(model, view) {
	        if (view && model.associatedViews && model.associatedViews.length > 1){
	          model.associatedViews = _.without(model.associatedViews, view);
	        } else {
	          delete model.validate;
	          delete model.preValidate;
	          delete model.isValid;
	          delete model.associatedViews;
	        }
	      };
	  
	      // Mix in validation on a model whenever a model is
	      // added to a collection
	      var collectionAdd = function(model) {
	        bindModel(this.view, model, this.options);
	      };
	  
	      // Remove validation from a model whenever a model is
	      // removed from a collection
	      var collectionRemove = function(model) {
	        unbindModel(model);
	      };
	  
	      // Returns the public methods on Backbone.Validation
	      return {
	  
	        // Current version of the library
	        version: '0.11.3',
	  
	        // Called to configure the default options
	        configure: function(options) {
	          _.extend(defaultOptions, options);
	        },
	  
	        // Hooks up validation on a view with a model
	        // or collection
	        bind: function(view, options) {
	          options = _.extend({}, defaultOptions, defaultCallbacks, options);
	  
	          var model = options.model || view.model,
	              collection = options.collection || view.collection;
	  
	          if(typeof model === 'undefined' && typeof collection === 'undefined'){
	            throw 'Before you execute the binding your view must have a model or a collection.\n' +
	                  'See http://thedersen.com/projects/backbone-validation/#using-form-model-validation for more information.';
	          }
	  
	          if(model) {
	            bindModel(view, model, options);
	          }
	          else if(collection) {
	            collection.each(function(model){
	              bindModel(view, model, options);
	            });
	            collection.bind('add', collectionAdd, {view: view, options: options});
	            collection.bind('remove', collectionRemove);
	          }
	        },
	  
	        // Removes validation from a view with a model
	        // or collection
	        unbind: function(view, options) {
	          options = _.extend({}, options);
	          var model = options.model || view.model,
	              collection = options.collection || view.collection;
	  
	          if(model) {
	            unbindModel(model, view);
	          }
	          else if(collection) {
	            collection.each(function(model){
	              unbindModel(model, view);
	            });
	            collection.unbind('add', collectionAdd);
	            collection.unbind('remove', collectionRemove);
	          }
	        },
	  
	        // Used to extend the Backbone.Model.prototype
	        // with validation
	        mixin: mixin(null, defaultOptions)
	      };
	    }());
	  
	  
	    // Callbacks
	    // ---------
	  
	    var defaultCallbacks = Validation.callbacks = {
	  
	      // Gets called when a previously invalid field in the
	      // view becomes valid. Removes any error message.
	      // Should be overridden with custom functionality.
	      valid: function(view, attr, selector) {
	        view.$('[' + selector + '~="' + attr + '"]')
	            .removeClass('invalid')
	            .removeAttr('data-error');
	      },
	  
	      // Gets called when a field in the view becomes invalid.
	      // Adds a error message.
	      // Should be overridden with custom functionality.
	      invalid: function(view, attr, error, selector) {
	        view.$('[' + selector + '~="' + attr + '"]')
	            .addClass('invalid')
	            .attr('data-error', error);
	      }
	    };
	  
	  
	    // Patterns
	    // --------
	  
	    var defaultPatterns = Validation.patterns = {
	      // Matches any digit(s) (i.e. 0-9)
	      digits: /^\d+$/,
	  
	      // Matches any number (e.g. 100.000)
	      number: /^-?(?:\d+|\d{1,3}(?:,\d{3})+)(?:\.\d+)?$/,
	  
	      // Matches a valid email address (e.g. mail@example.com)
	      email: /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i,
	  
	      // Mathes any valid url (e.g. http://www.xample.com)
	      url: /^(https?|ftp):\/\/(((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:)*@)?(((\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5])\.(\d|[1-9]\d|1\d\d|2[0-4]\d|25[0-5]))|((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?)(:\d*)?)(\/((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)+(\/(([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)*)*)?)?(\?((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|[\uE000-\uF8FF]|\/|\?)*)?(\#((([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(%[\da-f]{2})|[!\$&'\(\)\*\+,;=]|:|@)|\/|\?)*)?$/i
	    };
	  
	  
	    // Error messages
	    // --------------
	  
	    // Error message for the build in validators.
	    // {x} gets swapped out with arguments form the validator.
	    var defaultMessages = Validation.messages = {
	      required: '{0} is required',
	      acceptance: '{0} must be accepted',
	      min: '{0} must be greater than or equal to {1}',
	      max: '{0} must be less than or equal to {1}',
	      range: '{0} must be between {1} and {2}',
	      length: '{0} must be {1} characters',
	      minLength: '{0} must be at least {1} characters',
	      maxLength: '{0} must be at most {1} characters',
	      rangeLength: '{0} must be between {1} and {2} characters',
	      oneOf: '{0} must be one of: {1}',
	      equalTo: '{0} must be the same as {1}',
	      digits: '{0} must only contain digits',
	      number: '{0} must be a number',
	      email: '{0} must be a valid email',
	      url: '{0} must be a valid url',
	      inlinePattern: '{0} is invalid'
	    };
	  
	    // Label formatters
	    // ----------------
	  
	    // Label formatters are used to convert the attribute name
	    // to a more human friendly label when using the built in
	    // error messages.
	    // Configure which one to use with a call to
	    //
	    //     Backbone.Validation.configure({
	    //       labelFormatter: 'label'
	    //     });
	    var defaultLabelFormatters = Validation.labelFormatters = {
	  
	      // Returns the attribute name with applying any formatting
	      none: function(attrName) {
	        return attrName;
	      },
	  
	      // Converts attributeName or attribute_name to Attribute name
	      sentenceCase: function(attrName) {
	        return attrName.replace(/(?:^\w|[A-Z]|\b\w)/g, function(match, index) {
	          return index === 0 ? match.toUpperCase() : ' ' + match.toLowerCase();
	        }).replace(/_/g, ' ');
	      },
	  
	      // Looks for a label configured on the model and returns it
	      //
	      //      var Model = Backbone.Model.extend({
	      //        validation: {
	      //          someAttribute: {
	      //            required: true
	      //          }
	      //        },
	      //
	      //        labels: {
	      //          someAttribute: 'Custom label'
	      //        }
	      //      });
	      label: function(attrName, model) {
	        return (model.labels && model.labels[attrName]) || defaultLabelFormatters.sentenceCase(attrName, model);
	      }
	    };
	  
	    // AttributeLoaders
	  
	    var defaultAttributeLoaders = Validation.attributeLoaders = {
	      inputNames: function (view) {
	        var attrs = [];
	        if (view) {
	          view.$('form [name]').each(function () {
	            if (/^(?:input|select|textarea)$/i.test(this.nodeName) && this.name &&
	              this.type !== 'submit' && attrs.indexOf(this.name) === -1) {
	              attrs.push(this.name);
	            }
	          });
	        }
	        return attrs;
	      }
	    };
	  
	  
	    // Built in validators
	    // -------------------
	  
	    var defaultValidators = Validation.validators = (function(){
	      // Use native trim when defined
	      var trim = String.prototype.trim ?
	        function(text) {
	          return text === null ? '' : String.prototype.trim.call(text);
	        } :
	        function(text) {
	          var trimLeft = /^\s+/,
	              trimRight = /\s+$/;
	  
	          return text === null ? '' : text.toString().replace(trimLeft, '').replace(trimRight, '');
	        };
	  
	      // Determines whether or not a value is a number
	      var isNumber = function(value){
	        return _.isNumber(value) || (_.isString(value) && value.match(defaultPatterns.number));
	      };
	  
	      // Determines whether or not a value is empty
	      var hasValue = function(value) {
	        return !(_.isNull(value) || _.isUndefined(value) || (_.isString(value) && trim(value) === '') || (_.isArray(value) && _.isEmpty(value)));
	      };
	  
	      return {
	        // Function validator
	        // Lets you implement a custom function used for validation
	        fn: function(value, attr, fn, model, computed) {
	          if(_.isString(fn)){
	            fn = model[fn];
	          }
	          return fn.call(model, value, attr, computed);
	        },
	  
	        // Required validator
	        // Validates if the attribute is required or not
	        // This can be specified as either a boolean value or a function that returns a boolean value
	        required: function(value, attr, required, model, computed) {
	          var isRequired = _.isFunction(required) ? required.call(model, value, attr, computed) : required;
	          if(!isRequired && !hasValue(value)) {
	            return false; // overrides all other validators
	          }
	          if (isRequired && !hasValue(value)) {
	            return this.format(defaultMessages.required, this.formatLabel(attr, model));
	          }
	        },
	  
	        // Acceptance validator
	        // Validates that something has to be accepted, e.g. terms of use
	        // `true` or 'true' are valid
	        acceptance: function(value, attr, accept, model) {
	          if(value !== 'true' && (!_.isBoolean(value) || value === false)) {
	            return this.format(defaultMessages.acceptance, this.formatLabel(attr, model));
	          }
	        },
	  
	        // Min validator
	        // Validates that the value has to be a number and equal to or greater than
	        // the min value specified
	        min: function(value, attr, minValue, model) {
	          if (!isNumber(value) || value < minValue) {
	            return this.format(defaultMessages.min, this.formatLabel(attr, model), minValue);
	          }
	        },
	  
	        // Max validator
	        // Validates that the value has to be a number and equal to or less than
	        // the max value specified
	        max: function(value, attr, maxValue, model) {
	          if (!isNumber(value) || value > maxValue) {
	            return this.format(defaultMessages.max, this.formatLabel(attr, model), maxValue);
	          }
	        },
	  
	        // Range validator
	        // Validates that the value has to be a number and equal to or between
	        // the two numbers specified
	        range: function(value, attr, range, model) {
	          if(!isNumber(value) || value < range[0] || value > range[1]) {
	            return this.format(defaultMessages.range, this.formatLabel(attr, model), range[0], range[1]);
	          }
	        },
	  
	        // Length validator
	        // Validates that the value has to be a string with length equal to
	        // the length value specified
	        length: function(value, attr, length, model) {
	          if (!_.isString(value) || value.length !== length) {
	            return this.format(defaultMessages.length, this.formatLabel(attr, model), length);
	          }
	        },
	  
	        // Min length validator
	        // Validates that the value has to be a string with length equal to or greater than
	        // the min length value specified
	        minLength: function(value, attr, minLength, model) {
	          if (!_.isString(value) || value.length < minLength) {
	            return this.format(defaultMessages.minLength, this.formatLabel(attr, model), minLength);
	          }
	        },
	  
	        // Max length validator
	        // Validates that the value has to be a string with length equal to or less than
	        // the max length value specified
	        maxLength: function(value, attr, maxLength, model) {
	          if (!_.isString(value) || value.length > maxLength) {
	            return this.format(defaultMessages.maxLength, this.formatLabel(attr, model), maxLength);
	          }
	        },
	  
	        // Range length validator
	        // Validates that the value has to be a string and equal to or between
	        // the two numbers specified
	        rangeLength: function(value, attr, range, model) {
	          if (!_.isString(value) || value.length < range[0] || value.length > range[1]) {
	            return this.format(defaultMessages.rangeLength, this.formatLabel(attr, model), range[0], range[1]);
	          }
	        },
	  
	        // One of validator
	        // Validates that the value has to be equal to one of the elements in
	        // the specified array. Case sensitive matching
	        oneOf: function(value, attr, values, model) {
	          if(!_.include(values, value)){
	            return this.format(defaultMessages.oneOf, this.formatLabel(attr, model), values.join(', '));
	          }
	        },
	  
	        // Equal to validator
	        // Validates that the value has to be equal to the value of the attribute
	        // with the name specified
	        equalTo: function(value, attr, equalTo, model, computed) {
	          if(value !== computed[equalTo]) {
	            return this.format(defaultMessages.equalTo, this.formatLabel(attr, model), this.formatLabel(equalTo, model));
	          }
	        },
	  
	        // Pattern validator
	        // Validates that the value has to match the pattern specified.
	        // Can be a regular expression or the name of one of the built in patterns
	        pattern: function(value, attr, pattern, model) {
	          if (!hasValue(value) || !value.toString().match(defaultPatterns[pattern] || pattern)) {
	            return this.format(defaultMessages[pattern] || defaultMessages.inlinePattern, this.formatLabel(attr, model), pattern);
	          }
	        }
	      };
	    }());
	  
	    // Set the correct context for all validators
	    // when used from within a method validator
	    _.each(defaultValidators, function(validator, key){
	      defaultValidators[key] = _.bind(defaultValidators[key], _.extend({}, formatFunctions, defaultValidators));
	    });
	  
	    return Validation;
	  }(_));
	  return Backbone.Validation;
	}));

/***/ }),
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
	        amount: /^(\d+(?:[\.\,]\d{1,5})?)$/
	    });
	    _.extend(bb_module.messages, {
	        amount: "Doit être un nombre avec au maximum 5 chiffres après la virgule"
	    });
	};
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 23 */
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
	  appRoutes: {}
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
/* 24 */
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
	
	var _MainView = __webpack_require__(/*! ../views/MainView.js */ 25);
	
	var _MainView2 = _interopRequireDefault(_MainView);
	
	var _App = __webpack_require__(/*! ./App.js */ 20);
	
	var _App2 = _interopRequireDefault(_App);
	
	var _Facade = __webpack_require__(/*! ./Facade.js */ 102);
	
	var _Facade2 = _interopRequireDefault(_Facade);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : Controller.js
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var Controller = _backbone2.default.Object.extend({
	    initialize: function initialize(datas) {
	        _Facade2.default.loadModels(datas);
	        AppOption.facade = _Facade2.default;
	        this.mainView = new _MainView2.default();
	        _App2.default.showView(this.mainView);
	    },
	    status: function status(_status) {
	        this.mainView.showBox(_status);
	    }
	});
	exports.default = Controller;

/***/ }),
/* 25 */
/*!************************************!*\
  !*** ./src/task/views/MainView.js ***!
  \************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {"use strict";
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _CommonView = __webpack_require__(/*! ./CommonView.js */ 26);
	
	var _CommonView2 = _interopRequireDefault(_CommonView);
	
	var _RightBarView = __webpack_require__(/*! ./RightBarView.js */ 51);
	
	var _RightBarView2 = _interopRequireDefault(_RightBarView);
	
	var _TaskBlockView = __webpack_require__(/*! ./TaskBlockView.js */ 61);
	
	var _TaskBlockView2 = _interopRequireDefault(_TaskBlockView);
	
	var _DiscountBlockView = __webpack_require__(/*! ./DiscountBlockView.js */ 90);
	
	var _DiscountBlockView2 = _interopRequireDefault(_DiscountBlockView);
	
	var _StatusView = __webpack_require__(/*! ./StatusView.js */ 88);
	
	var _StatusView2 = _interopRequireDefault(_StatusView);
	
	var _backbone3 = __webpack_require__(/*! backbone.radio */ 19);
	
	var _backbone4 = _interopRequireDefault(_backbone3);
	
	var _bootstrap = __webpack_require__(/*! bootstrap */ 3);
	
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
	var template = __webpack_require__(/*! ./templates/MainView.mustache */ 99);
	
	var MainView = _backbone2.default.View.extend({
	    template: template,
	    regions: {
	        modalRegion: '#modalregion',
	        common: '#common',
	        tasklines: '#tasklines',
	        discounts: '#discounts',
	        rightbar: "#rightbar",
	        footer: '#footer'
	    },
	    childViewEvents: {
	        'status:change': 'onStatusChange'
	    },
	    initialize: function initialize(options) {
	        this.channel = _backbone4.default.channel('facade');
	    },
	    showCommonBlock: function showCommonBlock(datas) {
	        var model = this.channel.request('get:model', 'common');
	        var view = new _CommonView2.default({ model: model });
	        this.showChildView('common', view);
	    },
	    showTaskGroupBlock: function showTaskGroupBlock(datas) {
	        var collection = this.channel.request('get:collection', 'task_groups');
	        var view = new _TaskBlockView2.default({ collection: collection });
	        this.showChildView('tasklines', view);
	    },
	    showDiscountBlock: function showDiscountBlock(datas) {
	        var collection = this.channel.request('get:collection', 'discounts');
	        var model = this.channel.request('get:model', 'common');
	        var view = new _DiscountBlockView2.default({ collection: collection, model: model });
	        this.showChildView('discounts', view);
	    },
	
	    onRender: function onRender() {
	        if (_.indexOf(AppOption['form_options']['sections'], "common") != -1) {
	            this.showCommonBlock();
	        }
	        if (_.indexOf(AppOption['form_options']['sections'], "tasklines") != -1) {
	            this.showTaskGroupBlock();
	        }
	        if (_.indexOf(AppOption['form_options']['sections'], "discounts") != -1) {
	            this.showDiscountBlock();
	        }
	
	        var view = new _RightBarView2.default({ actions: AppOption['form_options']['actions'] });
	        this.showChildView('rightbar', view);
	    },
	    onStatusChange: function onStatusChange(status, title, label, url) {
	        this.showChildView('modalRegion', new _StatusView2.default({
	            status: status,
	            title: title,
	            label: label,
	            model: this.commonModel,
	            url: url
	        }));
	    },
	    onChildviewDestroyModal: function onChildviewDestroyModal() {
	        this.getRegion('modalRegion').empty();
	    }
	});
	exports.default = MainView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 26 */
/*!**************************************!*\
  !*** ./src/task/views/CommonView.js ***!
  \**************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _jquery = __webpack_require__(/*! jquery */ 1);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	var _FormBehavior = __webpack_require__(/*! ../behaviors/FormBehavior.js */ 31);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _CheckboxListWidget = __webpack_require__(/*! ./CheckboxListWidget.js */ 32);
	
	var _CheckboxListWidget2 = _interopRequireDefault(_CheckboxListWidget);
	
	var _DatePickerWidget = __webpack_require__(/*! ./DatePickerWidget.js */ 41);
	
	var _DatePickerWidget2 = _interopRequireDefault(_DatePickerWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ./TextAreaWidget.js */ 43);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/CommonView.mustache */ 50); /*
	                                                            * File Name : CommonView.js
	                                                            *
	                                                            * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	                                                            * Company : Majerti ( http://www.majerti.fr )
	                                                            *
	                                                            * This software is distributed under GPLV3
	                                                            * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                            *
	                                                            */
	
	
	var CommonView = _backbone2.default.View.extend({
	    /*
	     * Wrapper around the component making part of the 'common'
	     * invoice/estimation form, provide a main layout with regions for each
	     * field
	     */
	    tagName: 'div',
	    className: 'form-section',
	    template: template,
	    formname: "common",
	    regions: {
	        mentions: '.mentions',
	        date: '.date',
	        description: '.description',
	        address: '.address',
	        workplace: '.workplace'
	    },
	    behaviors: [{
	        behaviorClass: _FormBehavior2.default,
	        errorMessage: "Vérifiez votre saisie"
	    }],
	    childViewEvents: {
	        'change': 'onChildChange',
	        'finish': 'onChildFinish'
	    },
	    onChildChange: function onChildChange(attribute, value) {
	        this.triggerMethod('data:modified', this, attribute, value);
	    },
	    onChildFinish: function onChildFinish(attribute, value) {
	        this.triggerMethod('data:persist', this, attribute, value);
	    },
	    getMentionIds: function getMentionIds() {
	        var mentions = this.model.get('mentions');
	        var mention_ids = [];
	        _.each(mentions, function (mention) {
	            mention_ids.push(mention.id);
	        });
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
	        var mention_list = new _CheckboxListWidget2.default({
	            options: AppOption['form_options']['mention_options'],
	            value: this.getMentionIds(),
	            title: "Mentions facultatives",
	            description: "Choisissez les mentions à ajouter au document",
	            field_name: "mentions"
	        });
	        this.showChildView('mentions', mention_list);
	
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
	    }
	});
	exports.default = CommonView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 27 */
/*!**********************!*\
  !*** ./src/tools.js ***!
  \**********************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(jQuery) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	exports.setupJsonRedirect = exports.serializeForm = exports.getOpt = exports.updateSelectOptions = exports.ajax_call = exports.setDatePicker = undefined;
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _jquery = __webpack_require__(/*! jquery */ 1);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	__webpack_require__(/*! jquery */ 1);
	
	var datepicker = __webpack_require__(/*! jquery-ui/ui/widgets/datepicker */ 28);
	
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
	        value = parseDate(value);
	        input_tag.datepicker('setDate', value);
	    } else {
	        if (!_underscore2.default.isUndefined(default_value)) {
	            value = parseDate(default_value);
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
	        console.log("POST method");
	        console.log(data);
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
	        _underscore2.default.each(options, function (option) {
	            if (option['default']) {
	                option['selected'] = true;
	            }
	        });
	    }
	    return options;
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
	
	// Important point : handle redirection by json dict for ajax calls
	// Expects a redirect value to be returned with the 302 code
	var setupJsonRedirect = exports.setupJsonRedirect = function setupJsonRedirect() {
	    (0, _jquery2.default)(document).ajaxComplete(function (data, xhr, settings) {
	        var json_resp = jQuery.parseJSON(xhr.responseText);
	        if (json_resp.redirect) {
	            window.location.href = json_resp.redirect;
	        }
	    });
	};
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 28 */
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
				__webpack_require__(/*! jquery */ 1),
				__webpack_require__(/*! ../version */ 29),
				__webpack_require__(/*! ../keycode */ 30)
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
/* 29 */
/*!***********************************!*\
  !*** ./~/jquery-ui/ui/version.js ***!
  \***********************************/
/***/ (function(module, exports, __webpack_require__) {

	var __WEBPACK_AMD_DEFINE_FACTORY__, __WEBPACK_AMD_DEFINE_ARRAY__, __WEBPACK_AMD_DEFINE_RESULT__;( function( factory ) {
		if ( true ) {
	
			// AMD. Register as an anonymous module.
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [ __webpack_require__(/*! jquery */ 1) ], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
		} else {
	
			// Browser globals
			factory( jQuery );
		}
	} ( function( $ ) {
	
	$.ui = $.ui || {};
	
	return $.ui.version = "1.12.1";
	
	} ) );


/***/ }),
/* 30 */
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
			!(__WEBPACK_AMD_DEFINE_ARRAY__ = [ __webpack_require__(/*! jquery */ 1), __webpack_require__(/*! ./version */ 29) ], __WEBPACK_AMD_DEFINE_FACTORY__ = (factory), __WEBPACK_AMD_DEFINE_RESULT__ = (typeof __WEBPACK_AMD_DEFINE_FACTORY__ === 'function' ? (__WEBPACK_AMD_DEFINE_FACTORY__.apply(exports, __WEBPACK_AMD_DEFINE_ARRAY__)) : __WEBPACK_AMD_DEFINE_FACTORY__), __WEBPACK_AMD_DEFINE_RESULT__ !== undefined && (module.exports = __WEBPACK_AMD_DEFINE_RESULT__));
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
/* 31 */
/*!********************************************!*\
  !*** ./src/task/behaviors/FormBehavior.js ***!
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
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 22);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : FormBehavior.js
	 *
	 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var FormBehavior = _backbone2.default.Behavior.extend({
	    ui: {
	        form: "form",
	        submit: "button[type=submit]"
	    },
	    events: {
	        'click @ui.submit': 'onSubmitForm'
	    },
	    defaults: {
	        errorMessage: "Une erreur est survenue"
	    },
	    serializeForm: function serializeForm() {
	        return (0, _tools.serializeForm)(this.getUI('form'));
	    },
	    onRender: function onRender() {},
	    onSyncError: function onSyncError() {
	        (0, _backboneTools.displayServerError)("Une erreur a été rencontrée lors de la " + "sauvegarde de vos données");
	        _backboneValidation2.default.unbind(this.view);
	    },
	    onSyncSuccess: function onSyncSuccess() {
	        (0, _backboneTools.displayServerSuccess)("Vos données ont bien été sauvegardées");
	        _backboneValidation2.default.unbind(this.view);
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
	        if (this.view.model.isValid()) {
	            this.view.model.save(datas, {
	                success: this.onSyncSuccess.bind(this),
	                error: this.onSyncError.bind(this)
	            });
	        }
	    },
	    onSubmitForm: function onSubmitForm(event) {
	        event.preventDefault();
	        this.view.model.set(this.serializeForm(), { validate: true });
	        this.syncServer();
	    },
	    onDataPersist: function onDataPersist(view, attribute, value) {
	        _backboneValidation2.default.unbind(this.view);
	        _backboneValidation2.default.bind(this.view, {
	            attributes: function attributes(view) {
	                return [attribute];
	            }
	        });
	
	        var datas = {};
	        datas[attribute] = value;
	        this.view.model.set(datas);
	        this.syncServer(datas, true);
	    },
	    onDataModified: function onDataModified(view, attribute, value) {
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
	
	exports.default = FormBehavior;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 32 */
/*!**********************************************!*\
  !*** ./src/task/views/CheckboxListWidget.js ***!
  \**********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _jquery = __webpack_require__(/*! jquery */ 1);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
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
	var template = __webpack_require__(/*! ./templates/widgets/CheckboxListWidget.mustache */ 33);
	
	var CheckboxListWidget = _backbone2.default.View.extend({
	    template: template,
	    ui: {
	        checkboxes: 'input[type=checkbox]'
	    },
	    events: {
	        'click @ui.checkboxes': 'onClick'
	    },
	    getCurrentValues: function getCurrentValues() {
	        var checkboxes = this.getUI('checkboxes').find(':checked');
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
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 33 */
/*!**********************************************************************!*\
  !*** ./src/task/views/templates/widgets/CheckboxListWidget.mustache ***!
  \**********************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
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
/* 34 */
/*!*********************************!*\
  !*** ./~/handlebars/runtime.js ***!
  \*********************************/
/***/ (function(module, exports, __webpack_require__) {

	// Create a simple path alias to allow browserify to resolve
	// the runtime on a supported path.
	module.exports = __webpack_require__(/*! ./dist/cjs/handlebars.runtime */ 35);


/***/ }),
/* 35 */
/*!*****************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars.runtime.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	/*globals Handlebars: true */
	var base = __webpack_require__(/*! ./handlebars/base */ 36);
	
	// Each of these augment the Handlebars object. No need to setup here.
	// (This is done to easily share code between commonjs and browse envs)
	var SafeString = __webpack_require__(/*! ./handlebars/safe-string */ 38)["default"];
	var Exception = __webpack_require__(/*! ./handlebars/exception */ 39)["default"];
	var Utils = __webpack_require__(/*! ./handlebars/utils */ 37);
	var runtime = __webpack_require__(/*! ./handlebars/runtime */ 40);
	
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
/* 36 */
/*!**************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/base.js ***!
  \**************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	var Utils = __webpack_require__(/*! ./utils */ 37);
	var Exception = __webpack_require__(/*! ./exception */ 39)["default"];
	
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
/* 37 */
/*!***************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/utils.js ***!
  \***************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	/*jshint -W004 */
	var SafeString = __webpack_require__(/*! ./safe-string */ 38)["default"];
	
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
/* 38 */
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
/* 39 */
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
/* 40 */
/*!*****************************************************!*\
  !*** ./~/handlebars/dist/cjs/handlebars/runtime.js ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	var Utils = __webpack_require__(/*! ./utils */ 37);
	var Exception = __webpack_require__(/*! ./exception */ 39)["default"];
	var COMPILER_REVISION = __webpack_require__(/*! ./base */ 36).COMPILER_REVISION;
	var REVISION_CHANGES = __webpack_require__(/*! ./base */ 36).REVISION_CHANGES;
	var createFrame = __webpack_require__(/*! ./base */ 36).createFrame;
	
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
/* 41 */
/*!********************************************!*\
  !*** ./src/task/views/DatePickerWidget.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function($) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/widgets/DatePickerWidget.mustache */ 42); /*
	                                                                          * File Name : DatePickerWidget.js
	                                                                          *
	                                                                          * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	                                                                          * Company : Majerti ( http://www.majerti.fr )
	                                                                          *
	                                                                          * This software is distributed under GPLV3
	                                                                          * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                          *
	                                                                          */
	
	
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
	            var date = this.getOption('date');
	            var selector = this.getSelector();
	            (0, _tools.setDatePicker)(this.getUI('altdate'), selector, date,
	            // Bind the method to access view through the 'this' param
	            { onSelect: this.onDateSelect.bind(this) });
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
	            ctx['date'] = formatDate(this.getOption('date'));
	        }
	        return ctx;
	    }
	});
	exports.default = DatePickerWidget;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! jquery */ 1)))

/***/ }),
/* 42 */
/*!********************************************************************!*\
  !*** ./src/task/views/templates/widgets/DatePickerWidget.mustache ***!
  \********************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
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
/* 43 */
/*!******************************************!*\
  !*** ./src/task/views/TextAreaWidget.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	var _tinymce = __webpack_require__(/*! ../../tinymce.js */ 44);
	
	var _tinymce2 = _interopRequireDefault(_tinymce);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/widgets/TextAreaWidget.mustache */ 49); /*
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
	            tagId: this.getTagId()
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
/* 44 */,
/* 45 */,
/* 46 */,
/* 47 */,
/* 48 */,
/* 49 */
/*!******************************************************************!*\
  !*** ./src/task/views/templates/widgets/TextAreaWidget.mustache ***!
  \******************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "    <label for='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "'>"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</label>\n    <textarea name='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "' ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.tagId : depth0), {"name":"if","hash":{},"fn":this.program(2, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + " class='form-control' rows='"
	    + escapeExpression(((helper = (helper = helpers.rows || (depth0 != null ? depth0.rows : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"rows","hash":{},"data":data}) : helper)))
	    + "'>"
	    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
	    + "</textarea>\n";
	},"2":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "id=\""
	    + escapeExpression(((helper = (helper = helpers.tagId || (depth0 != null ? depth0.tagId : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"tagId","hash":{},"data":data}) : helper)))
	    + "\"";
	},"4":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "    "
	    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
	    + "\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.editable : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(4, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 50 */
/*!******************************************************!*\
  !*** ./src/task/views/templates/CommonView.mustache ***!
  \******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "in";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<h2>Informations générales</h2>\n<div class='content'>\n    <form class='form' name='common' action=\"#\" onSubmit=\"return false;\">\n        <div class='row'>\n            <div class='col-md-6 col-xs-12'>\n                <div class='date'></div>\n                <div class='description'></div>\n            </div>\n            <div class='col-md-6 col-xs-12'>\n                <div class='address'></div>\n            </div>\n        </div>\n        <a\n            data-target='#common-more'\n            data-toggle='collapse'\n            aria-expanded=\"false\"\n            aria-controls=\"common-more\"\n            >\n            <i class='glyphicon glyphicon-plus-sign'></i> Plus d'options (Lieu des travaux, mentions facultatives ...)\n        </a>\n        <div class='collapse row ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_more_set : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "' id=\"common-more\">\n            <div class='col-md-6 col-xs-12'>\n                <div class='workplace'></div>\n            </div>\n            <div class='col-md-6 col-xs-12'>\n                <div class='mentions'>\n                </div>\n            </div>\n        </div>\n    </form>\n</div>\n";
	},"useData":true});

/***/ }),
/* 51 */
/*!****************************************!*\
  !*** ./src/task/views/RightBarView.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _jquery = __webpack_require__(/*! jquery */ 1);
	
	var _jquery2 = _interopRequireDefault(_jquery);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _ActionCollection = __webpack_require__(/*! ../models/ActionCollection.js */ 52);
	
	var _ActionCollection2 = _interopRequireDefault(_ActionCollection);
	
	var _ActionListView = __webpack_require__(/*! ./ActionListView.js */ 54);
	
	var _ActionListView2 = _interopRequireDefault(_ActionListView);
	
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
	var template = __webpack_require__(/*! ./templates/RightBarView.mustache */ 59);
	
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
/* 52 */
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
	
	var _ActionModel = __webpack_require__(/*! ./ActionModel.js */ 53);
	
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
/* 53 */
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
/* 54 */
/*!******************************************!*\
  !*** ./src/task/views/ActionListView.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _AnchorWidget = __webpack_require__(/*! ./AnchorWidget.js */ 55);
	
	var _AnchorWidget2 = _interopRequireDefault(_AnchorWidget);
	
	var _ToggleWidgetView = __webpack_require__(/*! ./ToggleWidgetView.js */ 57);
	
	var _ToggleWidgetView2 = _interopRequireDefault(_ToggleWidgetView);
	
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
	        'toggle': _ToggleWidgetView2.default
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
/* 55 */
/*!****************************************!*\
  !*** ./src/task/views/AnchorWidget.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var AnchorWidget = _backbone2.default.View.extend({
	  tagName: 'div',
	  template: __webpack_require__(/*! ./templates/widgets/AnchorWidget.mustache */ 56)
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
/* 56 */
/*!****************************************************************!*\
  !*** ./src/task/views/templates/widgets/AnchorWidget.mustache ***!
  \****************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "<a class='"
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.css : stack1), depth0))
	    + " btn-block' href='"
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.url : stack1), depth0))
	    + "' title=\""
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.title : stack1), depth0))
	    + "\">\n    <i class='"
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.icon : stack1), depth0))
	    + "'></i> "
	    + escapeExpression(lambda(((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.label : stack1), depth0))
	    + "\n</a>\n";
	},"useData":true});

/***/ }),
/* 57 */
/*!********************************************!*\
  !*** ./src/task/views/ToggleWidgetView.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/widgets/ToggleWidgetView.mustache */ 58); /*
	                                                                          * File Name : ToggleWidgetView.js
	                                                                          *
	                                                                          * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                                          * Company : Majerti ( http://www.majerti.fr )
	                                                                          *
	                                                                          * This software is distributed under GPLV3
	                                                                          * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                          *
	                                                                          */
	
	
	var ToggleWidgetView = _backbone2.default.View.extend({
	  template: template,
	  ui: {}
	});
	
	exports.default = ToggleWidgetView;

/***/ }),
/* 58 */
/*!********************************************************************!*\
  !*** ./src/task/views/templates/widgets/ToggleWidgetView.mustache ***!
  \********************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "    <input type=\"radio\" id=\""
	    + escapeExpression(lambda((depth0 != null ? depth0.value : depth0), depth0))
	    + "\" name=\"radio-group\" data-toggle=\"button\">\n    <label class=\""
	    + escapeExpression(lambda((depth0 != null ? depth0.css : depth0), depth0))
	    + "\" for=\""
	    + escapeExpression(lambda((depth0 != null ? depth0.value : depth0), depth0))
	    + "\">\n        <i class='"
	    + escapeExpression(lambda((depth0 != null ? depth0.icon : depth0), depth0))
	    + "'></i> "
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "\n    </label>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<div class='btn-group' data-toggle=\"buttons-radio\">\n";
	  stack1 = helpers.each.call(depth0, ((stack1 = (depth0 != null ? depth0.option : depth0)) != null ? stack1.values : stack1), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>\n";
	},"useData":true});

/***/ }),
/* 59 */
/*!********************************************************!*\
  !*** ./src/task/views/templates/RightBarView.mustache ***!
  \********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var lambda=this.lambda, escapeExpression=this.escapeExpression;
	  return "    <button\n        class='btn btn-block "
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
	    + "'></i>\n    "
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "\n    </button>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<div>\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.buttons : depth0), {"name":"each","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "<div class='child-container'></div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 60 */
/*!****************************************!*\
  !*** ./src/task/models/CommonModel.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
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
	var CommonModel = _backbone2.default.Model.extend({
	    props: ['id', 'altdate', 'date', 'description', 'address', 'mention_ids', 'workplace', 'expenses_ht'],
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
	        }
	    },
	    constructor: function constructor() {
	        arguments[0] = _underscore2.default.pick(arguments[0], this.props);
	        _backbone2.default.Model.apply(this, arguments);
	    }
	});
	exports.default = CommonModel;

/***/ }),
/* 61 */
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
	
	var _TaskGroupModel = __webpack_require__(/*! ../models/TaskGroupModel.js */ 63);
	
	var _TaskGroupModel2 = _interopRequireDefault(_TaskGroupModel);
	
	var _TaskGroupCollectionView = __webpack_require__(/*! ./TaskGroupCollectionView.js */ 66);
	
	var _TaskGroupCollectionView2 = _interopRequireDefault(_TaskGroupCollectionView);
	
	var _TaskGroupFormView = __webpack_require__(/*! ./TaskGroupFormView.js */ 85);
	
	var _TaskGroupFormView2 = _interopRequireDefault(_TaskGroupFormView);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 22);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TaskBlockView = _backbone2.default.View.extend({
	    template: __webpack_require__(/*! ./templates/TaskBlockView.mustache */ 87),
	    tagName: 'div',
	    className: 'form-section',
	    regions: {
	        container: '.group-container',
	        modalRegion: ".group-modalregion"
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
	    initialize: function initialize(options) {
	        this.collection = options['collection'];
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
/* 62 */
/*!************************************************!*\
  !*** ./src/task/models/TaskGroupCollection.js ***!
  \************************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TaskGroupModel = __webpack_require__(/*! ./TaskGroupModel.js */ 63);
	
	var _TaskGroupModel2 = _interopRequireDefault(_TaskGroupModel);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TaskGroupCollection = _backbone2.default.Collection.extend({
	    model: _TaskGroupModel2.default,
	    url: function url() {
	        return AppOption['context_url'] + '/' + 'task_line_groups';
	    },
	    comparator: 'order',
	    initialize: function initialize(options) {
	        this.on('change:reorder', this.updateModelOrder);
	        this.updateModelOrder(false);
	    },
	    updateModelOrder: function updateModelOrder(sync) {
	        var sync = sync || true;
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
	        var first_model = _.min(this.models, function (model) {
	            return model.get('order');
	        });
	        return first_model.get('order');
	    },
	    getMaxOrder: function getMaxOrder() {
	        if (this.models.length == 0) {
	            return 0;
	        }
	        var last_model = _.max(this.models, function (model) {
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
	    },
	    load_from_catalog: function load_from_catalog(sale_product_group_ids) {
	        var serverRequest = (0, _tools.ajax_call)(this.url() + '?action=load_from_catalog', { sale_product_group_ids: sale_product_group_ids }, 'POST');
	        serverRequest.then(this.fetch.bind(this));
	    }
	}); /*
	     * File Name : TaskGroupCollection.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = TaskGroupCollection;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 63 */
/*!*******************************************!*\
  !*** ./src/task/models/TaskGroupModel.js ***!
  \*******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TaskLineCollection = __webpack_require__(/*! ./TaskLineCollection.js */ 64);
	
	var _TaskLineCollection2 = _interopRequireDefault(_TaskLineCollection);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : TaskGroupModel.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var TaskGroupModel = _backbone2.default.Model.extend({
	    props: ['id', 'order', 'title', 'description', 'lines', 'task_id'],
	    constructor: function constructor() {
	        arguments[0] = _underscore2.default.pick(arguments[0], this.props);
	        _backbone2.default.Model.apply(this, arguments);
	    },
	    initialize: function initialize() {
	        this.populate();
	        this.on('change:id', this.populate.bind(this));
	    },
	    populate: function populate() {
	        if (this.get('id')) {
	            this.lines = new _TaskLineCollection2.default(this.get('lines'));
	            this.lines.url = this.url() + '/task_lines';
	        }
	    },
	    ht: function ht() {
	        var res = 0;
	        _underscore2.default.each(this.lines.models, function (line) {
	            res += line.ht();
	        });
	        return res;
	    },
	    updateLines: function updateLines(result) {
	        this.fetch({ success: this.populate.bind(this) });
	    },
	    load_from_catalog: function load_from_catalog(sale_product_ids) {
	        var serverRequest = (0, _tools.ajax_call)(this.url() + '?action=load_from_catalog', { sale_product_ids: sale_product_ids }, 'POST');
	        serverRequest.then(this.updateLines.bind(this));
	    },
	    loadProductGroup: function loadProductGroup(sale_product_group_datas) {
	        this.set('title', sale_product_group_datas.title);
	        this.set('description', sale_product_group_datas.description);
	    }
	});
	exports.default = TaskGroupModel;

/***/ }),
/* 64 */
/*!***********************************************!*\
  !*** ./src/task/models/TaskLineCollection.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TaskLineModel = __webpack_require__(/*! ./TaskLineModel.js */ 65);
	
	var _TaskLineModel2 = _interopRequireDefault(_TaskLineModel);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var TaskLineCollection = _backbone2.default.Collection.extend({
	    model: _TaskLineModel2.default,
	    comparator: 'order',
	    initialize: function initialize(options) {
	        this.on('change:reorder', this.updateModelOrder);
	        this.updateModelOrder(false);
	    },
	    updateModelOrder: function updateModelOrder(sync) {
	        var sync = sync || true;
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
/* 65 */
/*!******************************************!*\
  !*** ./src/task/models/TaskLineModel.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
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
	var TaskLineModel = _backbone2.default.Model.extend({
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
	    constructor: function constructor() {
	        arguments[0] = _underscore2.default.pick(arguments[0], this.props);
	        _backbone2.default.Model.apply(this, arguments);
	    },
	    ht: function ht() {
	        return this.get('cost') * this.get('quantity');
	    },
	    loadProduct: function loadProduct(product_datas) {
	        this.set('description', product_datas.label);
	        this.set('cost', product_datas.value);
	        this.set('quantity', 1);
	        this.set('tva', product_datas.tva);
	    }
	});
	
	exports.default = TaskLineModel;

/***/ }),
/* 66 */
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
	
	var _TaskGroupView = __webpack_require__(/*! ./TaskGroupView.js */ 67);
	
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
/* 67 */
/*!*****************************************!*\
  !*** ./src/task/views/TaskGroupView.js ***!
  \*****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _TaskLineCollectionView = __webpack_require__(/*! ./TaskLineCollectionView.js */ 68);
	
	var _TaskLineCollectionView2 = _interopRequireDefault(_TaskLineCollectionView);
	
	var _TaskLineFormView = __webpack_require__(/*! ./TaskLineFormView.js */ 72);
	
	var _TaskLineFormView2 = _interopRequireDefault(_TaskLineFormView);
	
	var _TaskLineModel = __webpack_require__(/*! ../models/TaskLineModel.js */ 65);
	
	var _TaskLineModel2 = _interopRequireDefault(_TaskLineModel);
	
	var _math = __webpack_require__(/*! ../../math.js */ 70);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 22);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	/*
	 * File Name : TaskGroupView.js
	 *
	 * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	 * Company : Majerti ( http://www.majerti.fr )
	 *
	 * This software is distributed under GPLV3
	 * License: http://www.gnu.org/licenses/gpl-3.0.txt
	 *
	 */
	var template = __webpack_require__(/*! ./templates/TaskGroupView.mustache */ 84);
	
	var TaskGroupView = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'taskline-group row',
	    template: template,
	    regions: {
	        lines: '.lines',
	        modalRegion: ".modalregion"
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
	        'catalog:insert': 'onCatalogInsert'
	    },
	    isEmpty: function isEmpty() {
	        return this.model.lines.length === 0;
	    },
	    onRender: function onRender() {
	        if (!this.isEmpty()) {
	            this.showChildView('lines', new _TaskLineCollectionView2.default({ collection: this.model.lines }));
	        }
	    },
	    onLineEdit: function onLineEdit(childView) {
	        this.showTaskLineForm(childView.model, "Modifier la prestation", true);
	    },
	    onLineAdd: function onLineAdd() {
	        var model = new _TaskLineModel2.default({
	            task_id: this.model.get('id'),
	            order: this.model.lines.getMaxOrder() + 1
	        });
	        this.showTaskLineForm(model, "Ajouter une prestation", false);
	    },
	    showTaskLineForm: function showTaskLineForm(model, title, edit) {
	        var form = new _TaskLineFormView2.default({
	            model: model,
	            title: title,
	            destCollection: this.model.lines,
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
	        this.model.load_from_catalog(sale_product_ids);
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
	            total_ht: (0, _math.formatAmount)(this.model.ht()),
	            is_not_first: order != min_order,
	            is_not_last: order != max_order
	        };
	    }
	});
	exports.default = TaskGroupView;

/***/ }),
/* 68 */
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
	
	var _TaskLineView = __webpack_require__(/*! ./TaskLineView.js */ 69);
	
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
	        'change:reorder': 'render',
	        'sync': 'render'
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
/* 69 */
/*!****************************************!*\
  !*** ./src/task/views/TaskLineView.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 70);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/TaskLineView.mustache */ 71); /*
	                                                              * File Name : TaskLineView.js
	                                                              *
	                                                              * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                              * Company : Majerti ( http://www.majerti.fr )
	                                                              *
	                                                              * This software is distributed under GPLV3
	                                                              * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                              *
	                                                              */
	
	
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
	    getTvaLabel: function getTvaLabel() {
	        var res = "";
	        var current_value = this.model.get('tva');
	        _underscore2.default.each(AppOption['form_options']['tva_options'], function (tva) {
	            if (tva.value == current_value) {
	                res = tva.name;
	            }
	        });
	        return res;
	    },
	    templateContext: function templateContext() {
	        var min_order = this.model.collection.getMinOrder();
	        var max_order = this.model.collection.getMaxOrder();
	        var order = this.model.get('order');
	        return {
	            ht: (0, _math.formatAmount)(this.model.ht()),
	            tva_label: this.getTvaLabel(),
	            is_not_first: order != min_order,
	            is_not_last: order != max_order
	        };
	    }
	});
	exports.default = TaskLineView;

/***/ }),
/* 70 */
/*!*********************!*\
  !*** ./src/math.js ***!
  \*********************/
/***/ (function(module, exports, __webpack_require__) {

	"use strict";
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	exports.getPercent = exports.getTvaPart = exports.trailingZeros = exports.formatAmount = exports.isNotFormattable = exports.formatPrice = exports.round = exports.strToFloat = undefined;
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
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
	
	  if (value === undefined || value === null) {
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
/* 71 */
/*!********************************************************!*\
  !*** ./src/task/views/templates/TaskLineView.mustache ***!
  \********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
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
/* 72 */
/*!********************************************!*\
  !*** ./src/task/views/TaskLineFormView.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	var _InputWidget = __webpack_require__(/*! ./InputWidget.js */ 73);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _SelectWidget = __webpack_require__(/*! ./SelectWidget.js */ 75);
	
	var _SelectWidget2 = _interopRequireDefault(_SelectWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ./TextAreaWidget.js */ 43);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _ModalFormBehavior = __webpack_require__(/*! ../behaviors/ModalFormBehavior.js */ 77);
	
	var _ModalFormBehavior2 = _interopRequireDefault(_ModalFormBehavior);
	
	var _CatalogTreeView = __webpack_require__(/*! ./CatalogTreeView.js */ 79);
	
	var _CatalogTreeView2 = _interopRequireDefault(_CatalogTreeView);
	
	var _LoadingWidget = __webpack_require__(/*! ./LoadingWidget.js */ 81);
	
	var _LoadingWidget2 = _interopRequireDefault(_LoadingWidget);
	
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
	var template = __webpack_require__(/*! ./templates/TaskLineFormView.mustache */ 83);
	
	var TaskLineFormView = _backbone2.default.View.extend({
	    template: template,
	    regions: {
	        'description': '.description',
	        'cost': '.cost',
	        'quantity': '.quantity',
	        'unity': '.unity',
	        'tva': '.tva',
	        'product_id': '.product_id',
	        'catalog_container': '#catalog-container'
	    },
	    ui: {
	        btn_cancel: "button[type=reset]",
	        form: "form",
	        submit: 'button[type=submit]',
	        main_tab: 'ul.nav-tabs li:first a'
	    },
	    behaviors: [_ModalFormBehavior2.default],
	    triggers: {
	        'click @ui.btn_cancel': 'modal:close'
	    },
	    childViewEvents: {
	        'change': 'onChildChange',
	        'catalog:edit': 'onCatalogEdit'
	    },
	    // Bubble up child view events
	    //
	    childViewTriggers: {
	        'catalog:insert': 'catalog:insert'
	    },
	    modelEvents: {
	        'change': 'refreshForm'
	    },
	    onChildChange: function onChildChange(attribute, value) {
	        this.triggerMethod('data:modified', this, attribute, value);
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
	            options: AppOption['form_options']['workunit_options'],
	            title: "Unité",
	            value: this.model.get('unity'),
	            field_name: 'unity'
	        }));
	        this.showChildView('tva', new _SelectWidget2.default({
	            options: AppOption['form_options']['tva_options'],
	            title: "TVA",
	            value: this.model.get('tva'),
	            field_name: 'tva'
	        }));
	        this.showChildView('product_id', new _SelectWidget2.default({
	            options: AppOption['form_options']['product_options'],
	            title: "Code produit",
	            value: this.model.get('product_id'),
	            field_name: 'product_id',
	            id_key: 'id'
	        }));
	        if (this.isAddView()) {
	            this.getUI('main_tab').tab('show');
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

/***/ }),
/* 73 */
/*!***************************************!*\
  !*** ./src/task/views/InputWidget.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
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
	    template: __webpack_require__(/*! ./templates/widgets/InputWidget.mustache */ 74),
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
	            title: this.getOption('title'),
	            field_name: this.getOption('field_name'),
	            description: (0, _tools.getOpt)(this, 'description', false),
	            type: (0, _tools.getOpt)(this, 'type', 'text'),
	            addon: (0, _tools.getOpt)(this, 'addon', '')
	        };
	    }
	});
	
	exports.default = InputWidget;

/***/ }),
/* 74 */
/*!***************************************************************!*\
  !*** ./src/task/views/templates/widgets/InputWidget.mustache ***!
  \***************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class=\"input-group-addon\">";
	  stack1 = ((helper = (helper = helpers.addon || (depth0 != null ? depth0.addon : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"addon","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</div>";
	},"3":function(depth0,helpers,partials,data) {
	  var helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression;
	  return "<span class='help-block'><small>"
	    + escapeExpression(((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper)))
	    + "</small></span>\n";
	},"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<label for="
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + ">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</label>\n<div class='input-group'><input class='form-control' type='"
	    + escapeExpression(((helper = (helper = helpers.type || (depth0 != null ? depth0.type : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"type","hash":{},"data":data}) : helper)))
	    + "' value='"
	    + escapeExpression(((helper = (helper = helpers.value || (depth0 != null ? depth0.value : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"value","hash":{},"data":data}) : helper)))
	    + "' name=\""
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "\"></input>";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.addon : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.description : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"useData":true});

/***/ }),
/* 75 */
/*!****************************************!*\
  !*** ./src/task/views/SelectWidget.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
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
	var template = __webpack_require__(/*! ./templates/widgets/SelectWidget.mustache */ 76);
	
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
	        this.triggerMethod("change:value", this.$el.chidren('option:selected').val());
	    },
	    templateContext: function templateContext() {
	        var id_key = (0, _tools.getOpt)(this, 'id_key', 'value');
	        var options = this.getOption('options');
	        var current_value = this.getOption('value');
	        (0, _tools.updateSelectOptions)(options, current_value, id_key);
	
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
/* 76 */
/*!****************************************************************!*\
  !*** ./src/task/views/templates/widgets/SelectWidget.mustache ***!
  \****************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "multiple";
	  },"3":function(depth0,helpers,partials,data) {
	  var stack1, lambda=this.lambda, escapeExpression=this.escapeExpression, buffer = "    <option value='"
	    + escapeExpression(lambda((depth0 != null ? depth0.value : depth0), depth0))
	    + "' ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.selected : depth0), {"name":"if","hash":{},"fn":this.program(4, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + ">"
	    + escapeExpression(lambda((depth0 != null ? depth0.label : depth0), depth0))
	    + "</option>\n";
	},"4":function(depth0,helpers,partials,data) {
	  return "selected";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<label for='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "'>"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</label>\n<select class='form-control' ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.multiple : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += " name='"
	    + escapeExpression(((helper = (helper = helpers.field_name || (depth0 != null ? depth0.field_name : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"field_name","hash":{},"data":data}) : helper)))
	    + "'>\n";
	  stack1 = helpers.each.call(depth0, (depth0 != null ? depth0.options : depth0), {"name":"each","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</select>\n";
	},"useData":true});

/***/ }),
/* 77 */
/*!*************************************************!*\
  !*** ./src/task/behaviors/ModalFormBehavior.js ***!
  \*************************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _backboneValidation = __webpack_require__(/*! backbone-validation */ 21);
	
	var _backboneValidation2 = _interopRequireDefault(_backboneValidation);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 22);
	
	var _ModalBehavior = __webpack_require__(/*! ./ModalBehavior.js */ 78);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var ModalFormBehavior = _backbone2.default.Behavior.extend({
	    behaviors: [_ModalBehavior2.default],
	    ui: {
	        form: "form",
	        submit: "button[type=submit]"
	    },
	    events: {
	        'click @ui.submit': 'onSubmitForm',
	        'submit @ui.form': 'onSubmitForm'
	    },
	    defaults: {
	        errorMessage: "Une erreur est survenue"
	    },
	    serializeForm: function serializeForm() {
	        return (0, _tools.serializeForm)(this.getUI('form'));
	    },
	    onSyncError: function onSyncError() {
	        (0, _backboneTools.displayServerError)("Une erreur a été rencontrée lors de la " + "sauvegarde de vos données");
	        _backboneValidation2.default.unbind(this.view);
	    },
	    onSyncSuccess: function onSyncSuccess() {
	        (0, _backboneTools.displayServerSuccess)("Vos données ont bien été sauvegardées");
	        _backboneValidation2.default.unbind(this.view);
	        this.view.triggerMethod('modal:close');
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
	        if (this.view.model.isValid()) {
	            if (!this.view.model.get('id')) {
	                this.addSubmit(datas);
	            } else {
	                this.editSubmit(datas);
	            }
	        }
	    },
	    addSubmit: function addSubmit(datas) {
	        var destCollection = this.view.getOption('destCollection');
	        destCollection.create(datas, {
	            success: this.onSyncSuccess.bind(this),
	            error: this.onSyncError.bind(this),
	            wait: true,
	            sort: true
	        });
	    },
	    editSubmit: function editSubmit(datas) {
	        this.view.model.save(datas, {
	            success: this.onSyncSuccess.bind(this),
	            error: this.onSyncError.bind(this),
	            wait: true
	        });
	    },
	    onSubmitForm: function onSubmitForm(event) {
	        event.preventDefault();
	        this.view.model.set(this.serializeForm(), { validate: true });
	        this.syncServer();
	    },
	    onDataPersist: function onDataPersist(view, attribute, value) {
	        _backboneValidation2.default.unbind(this.view);
	        _backboneValidation2.default.bind(this.view, {
	            attributes: function attributes(view) {
	                return [attribute];
	            }
	        });
	
	        var datas = {};
	        datas[attribute] = value;
	        this.view.model.set(datas);
	        this.syncServer(datas, true);
	    },
	    onDataModified: function onDataModified(view, attribute, value) {
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
	}); /*
	     * File Name : ModalFormBehavior.js
	     *
	     * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = ModalFormBehavior;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 78 */
/*!*********************************************!*\
  !*** ./src/task/behaviors/ModalBehavior.js ***!
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
	    modalOptions: null
	  },
	
	  ui: {
	    close: '.close-modal'
	  },
	  events: {
	    'hidden.bs.modal': 'triggerFinish'
	  },
	
	  triggers: {
	    'click @ui.close': 'modal:close'
	  },
	  onRender: function onRender() {
	    this.view.$el.addClass('modal ' + this.getOption('modalClasses'));
	  },
	  onAttach: function onAttach() {
	    this.view.$el.modal(this.getOption('modalOptions') || {});
	  },
	  onModalClose: function onModalClose() {
	    this.view.$el.modal('hide');
	  },
	  triggerFinish: function triggerFinish() {
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
/* 79 */
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
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
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
	var template = __webpack_require__(/*! ./templates/CatalogTreeView.mustache */ 80);
	
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
	        cancel_btn: 'button.cancel-catalog',
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
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 80 */
/*!***********************************************************!*\
  !*** ./src/task/views/templates/CatalogTreeView.mustache ***!
  \***********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<input class=\"form-control\" name=\"catalog_search\" placeholder=\"Nom ou référence\" type=\"text\" />\n<div class='tree'>\n</div>\n<div class=\"form-group\">\n    <div class=\"text-right\">\n        <button class=\"btn btn-success primary-action edit-catalog\" type=\"button\">\n            Éditer comme un nouvel élément\n        </button>\n        <button class=\"btn btn-success secondary-action insert-catalog\" type=\"button\">\n            Insérer les éléments sélectionnés\n        </button>\n        <button class=\"btn btn-default secondary-action cancel-catalog\" type=\"button\">\n            Annuler\n        </button>\n    </div>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 81 */
/*!*****************************************!*\
  !*** ./src/task/views/LoadingWidget.js ***!
  \*****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	  value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/widgets/LoadingWidget.mustache */ 82); /*
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
/* 82 */
/*!*****************************************************************!*\
  !*** ./src/task/views/templates/widgets/LoadingWidget.mustache ***!
  \*****************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div class='loader'>\n<i class=\"fa fa-spinner fa-spin fa-3x fa-fw\" aria-hidden=\"true\"></i>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 83 */
/*!************************************************************!*\
  !*** ./src/task/views/templates/TaskLineFormView.mustache ***!
  \************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "            <ul class=\"nav nav-tabs\" role=\"tablist\">\n                <li role=\"presentation\" class=\"active\">\n                    <a href=\"#form-container\"\n                        aria-controls=\"form-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\"\n                        tabindex='-1'\n                        >\n                        Saisie libre\n                    </a>\n                </li>\n                <li role=\"presentation\">\n                    <a href=\"#catalog-container\"\n                        aria-controls=\"catalog-container\"\n                        role=\"tab\"\n                        tabindex='-1'\n                        data-toggle=\"tab\">\n                        Depuis le catalogue\n                    </a>\n                </li>\n            </ul>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane\"\n                    id=\"catalog-container\">\n                </div>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\" role=\"document\">\n	<div class=\"modal-content\">\n          <div class=\"modal-header\">\n            <button tabindex='-1' type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n            <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n          </div>\n          <div class=\"modal-body\">\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "            <div class='tab-content'>\n                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane fade in active\"\n                    id=\"form-container\">\n                    <form class='form taskline-form'>\n                        <div class='description required'></div>\n                        <div class='cost required'></div>\n                        <div class='quantity required'></div>\n                        <div class='unity'></div>\n                        <div class='tva required'></div>\n                        <div class='product_id'></div>\n                        <button\n                            class='btn btn-success primary-action'\n                            type='submit'\n                            value='submit'>\n                            "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n                        </button>\n                        <button\n                            class='btn btn-default secondary-action'\n                            type='reset'\n                            value='submit'>\n                            Annuler\n                        </button>\n                    </form>\n                </div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "            </div>\n          </div>\n            <div class=\"modal-footer\">\n          </div>\n        </form>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n";
	},"useData":true});

/***/ }),
/* 84 */
/*!*********************************************************!*\
  !*** ./src/task/views/templates/TaskGroupView.mustache ***!
  \*********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
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
	  return "            <small>Aucun titre n'a été saisi pour ce groupe</small>\n";
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
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class='col-xs-12'>\n    <div class='row'>\n        <div class='col-xs-12'>\n            <div class='btn-group pull-right'>\n                <button\n                    type='button'\n                    class='btn btn-danger delete btn-small'\n                    title='Supprimer cet ouvrage'\n                    tabindex='-1'\n                    >\n                    <i class='glyphicon glyphicon-trash'></i>\n                </button>\n";
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
	  buffer += "    <div class='row lines'>\n    </div>\n    <div class='row actions'>\n        <div class='col-xs-11 text-right'>\n            <button type='button' class='btn btn-info btn-add'>\n                <i class='glyphicon glyphicon-plus-sign'></i> Ajouter une prestation\n            </button>\n        </div>\n    </div>\n    <div class='row subtotal'>\n        <div class='col-xs-12 text-right'>\n            Sous total HT      ";
	  stack1 = ((helper = (helper = helpers.total_ht || (depth0 != null ? depth0.total_ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"total_ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\n        </div>\n    </div>\n    <div class='modalregion'></div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 85 */
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
	
	var _InputWidget = __webpack_require__(/*! ./InputWidget.js */ 73);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ./TextAreaWidget.js */ 43);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _ModalFormBehavior = __webpack_require__(/*! ../behaviors/ModalFormBehavior.js */ 77);
	
	var _ModalFormBehavior2 = _interopRequireDefault(_ModalFormBehavior);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	var _CatalogTreeView = __webpack_require__(/*! ./CatalogTreeView.js */ 79);
	
	var _CatalogTreeView2 = _interopRequireDefault(_CatalogTreeView);
	
	var _LoadingWidget = __webpack_require__(/*! ./LoadingWidget.js */ 81);
	
	var _LoadingWidget2 = _interopRequireDefault(_LoadingWidget);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/TaskGroupFormView.mustache */ 86); /*
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
	        'title': '.title',
	        'description': '.description',
	        'catalog_container': '#catalog-container'
	    },
	    ui: {
	        btn_cancel: "button[type=reset]",
	        form: "form",
	        submit: 'button[type=submit]',
	        main_tab: 'ul.nav-tabs li:first a'
	    },
	    behaviors: [_ModalFormBehavior2.default],
	    triggers: {
	        'click @ui.btn_cancel': 'modal:close'
	    },
	    childViewEvents: {
	        'change': 'onChildChange',
	        'catalog:edit': 'onCatalogEdit'
	    },
	    childViewTriggers: {
	        'catalog:insert': 'catalog:insert'
	    },
	    modelEvents: {
	        'change': 'refreshForm'
	    },
	    onChildChange: function onChildChange(attribute, value) {
	        this.triggerMethod('data:modified', this, attribute, value);
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
/* 86 */
/*!*************************************************************!*\
  !*** ./src/task/views/templates/TaskGroupFormView.mustache ***!
  \*************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
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
	  buffer += "            <div class='tab-content'>\n                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane fade in active\"\n                    id=\"form-container\">\n                    <form class='form taskgroup-form'>\n                        <div class='title'></div>\n                        <div class='description'></div>\n                        <button class='btn btn-success primary-action' type='submit' value='submit'>\n                            "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n                        </button>\n                        <button class='btn btn-default secondary-action' type='reset' value='submit'>\n                            Annuler\n                        </button>\n                    </form>\n                </div>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "            </div>\n          </div>\n          <div class=\"modal-footer\">\n          </div>\n        </form>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n\n";
	},"useData":true});

/***/ }),
/* 87 */
/*!*********************************************************!*\
  !*** ./src/task/views/templates/TaskBlockView.mustache ***!
  \*********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<h2>Description des prestations</h2>\n<div class='content'>\n    <div class='group-container'></div>\n    <div class='group-modalregion'></div>\n    <div class='actions text-right'>\n        <button class='btn btn-default add' type='button'>\n            <i class='glyphicon glyphicon-plus-sign'></i> Ajouter un ouvrage\n        </button>\n    </div>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 88 */
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
	
	var _ModalBehavior = __webpack_require__(/*! ../behaviors/ModalBehavior.js */ 78);
	
	var _ModalBehavior2 = _interopRequireDefault(_ModalBehavior);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/StatusView.mustache */ 89); /*
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
	            if (date != dateToIso(today)) {
	                result['ask_for_date'] = true;
	                date = parseDate(date);
	                result['date'] = date.toLocaleDateString();
	                result['today'] = today.toLocaleDateString();
	            }
	        }
	        return result;
	    }
	});
	exports.default = StatusView;
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 89 */
/*!******************************************************!*\
  !*** ./src/task/views/templates/StatusView.mustache ***!
  \******************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
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
	  return buffer + "                    <div class='form-group'>\n                        <label for='comment'>Commentaires</label>\n                        <textarea class='form-control' name='comment' rows=4></textarea>\n                    </div>\n          </div>\n          <div class=\"modal-footer\">\n            <button class='btn btn-default secondary-action' data-dismiss='modal'>Annuler</button>\n            <button class='btn btn-success primary-action' type='submit' name='submit' value='"
	    + escapeExpression(((helper = (helper = helpers.status || (depth0 != null ? depth0.status : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"status","hash":{},"data":data}) : helper)))
	    + "'>"
	    + escapeExpression(((helper = (helper = helpers.label || (depth0 != null ? depth0.label : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"label","hash":{},"data":data}) : helper)))
	    + "</button>\n          </div>\n	  </form>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n";
	},"useData":true});

/***/ }),
/* 90 */
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
	
	var _FormBehavior = __webpack_require__(/*! ../behaviors/FormBehavior.js */ 31);
	
	var _FormBehavior2 = _interopRequireDefault(_FormBehavior);
	
	var _DiscountModel = __webpack_require__(/*! ../models/DiscountModel.js */ 91);
	
	var _DiscountModel2 = _interopRequireDefault(_DiscountModel);
	
	var _DiscountCollectionView = __webpack_require__(/*! ./DiscountCollectionView.js */ 93);
	
	var _DiscountCollectionView2 = _interopRequireDefault(_DiscountCollectionView);
	
	var _DiscountFormView = __webpack_require__(/*! ./DiscountFormView.js */ 96);
	
	var _DiscountFormView2 = _interopRequireDefault(_DiscountFormView);
	
	var _InputWidget = __webpack_require__(/*! ./InputWidget.js */ 73);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _backboneTools = __webpack_require__(/*! ../../backbone-tools.js */ 22);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var DiscountBlockView = _backbone2.default.View.extend({
	    tagName: 'div',
	    className: 'form-section discount-group',
	    template: __webpack_require__(/*! ./templates/DiscountBlockView.mustache */ 98),
	    regions: {
	        'lines': '.lines',
	        'modalRegion': '.modalregion',
	        'expenses_ht': '.expenses_ht'
	    },
	    behaviors: [{
	        behaviorClass: _FormBehavior2.default,
	        errorMessage: "Vérifiez votre saisie"
	    }],
	    ui: {
	        add_button: 'button.btn-add'
	    },
	    triggers: {
	        "click @ui.add_button": "line:add"
	    },
	    childViewEvents: {
	        'line:edit': 'onLineEdit',
	        'line:delete': 'onLineDelete',
	        'change': 'onChildChange',
	        'finish': 'onChildFinish'
	    },
	    initialize: function initialize(options) {
	        this.collection = options['collection'];
	        this.model = options['model'];
	    },
	    isEmpty: function isEmpty() {
	        return this.collection.length === 0;
	    },
	    onChildChange: function onChildChange(attribute, value) {
	        console.log("Data modified");
	        this.triggerMethod('data:modified', this, attribute, value);
	    },
	    onChildFinish: function onChildFinish(attribute, value) {
	        console.log("Data should be persisted");
	        this.triggerMethod('data:persist', this, attribute, value);
	    },
	    onLineAdd: function onLineAdd() {
	        var model = new _DiscountModel2.default();
	        this.showDiscountLineForm(model, "Ajouter la remise", false);
	    },
	    onLineEdit: function onLineEdit(childView) {
	        this.showDiscountLineForm(childView.model, "Modifier la remise", true);
	    },
	    showDiscountLineForm: function showDiscountLineForm(model, title, edit) {
	        var form = new _DiscountFormView2.default({
	            model: model,
	            title: title,
	            destCollection: this.collection
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
	    isMoreSet: function isMoreSet() {
	        var value = this.model.get('expenses_ht');
	        if (value) {
	            return true;
	        }
	        return false;
	    },
	    templateContext: function templateContext() {
	        return {
	            not_empty: !this.isEmpty(),
	            is_more_set: this.isMoreSet()
	        };
	    },
	    onRender: function onRender() {
	        if (!this.isEmpty()) {
	            this.showChildView('lines', new _DiscountCollectionView2.default({ collection: this.collection }));
	        }
	        this.showChildView('expenses_ht', new _InputWidget2.default({
	            title: "Frais forfaitaires (HT)",
	            value: this.model.get('expenses_ht'),
	            field_name: 'expenses_ht'
	        }));
	    }
	}); /*
	     * File Name : DiscountBlockView.js
	     *
	     * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	     * Company : Majerti ( http://www.majerti.fr )
	     *
	     * This software is distributed under GPLV3
	     * License: http://www.gnu.org/licenses/gpl-3.0.txt
	     *
	     */
	exports.default = DiscountBlockView;

/***/ }),
/* 91 */
/*!******************************************!*\
  !*** ./src/task/models/DiscountModel.js ***!
  \******************************************/
/***/ (function(module, exports, __webpack_require__) {

	/* WEBPACK VAR INJECTION */(function(_) {'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var DiscountModel = _backbone2.default.Model.extend({
	    props: ['id', 'amount', 'tva', 'ht', 'description'],
	    validation: {
	        description: {
	            required: true,
	            msg: "Veuillez saisir un objet"
	        },
	        amount: {
	            required: true,
	            pattern: "amount",
	            msg: "Veuillez saisir un coup unitaire, dans la limite de 5 chiffres après la virgule"
	        },
	        tva: {
	            required: true,
	            pattern: "number",
	            msg: "Veuillez sélectionner une TVA"
	        }
	    },
	    constructor: function constructor() {
	        arguments[0] = _.pick(arguments[0], this.props);
	        _backbone2.default.Model.apply(this, arguments);
	    },
	    ht: function ht() {
	        return this.get('amount');
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
	/* WEBPACK VAR INJECTION */}.call(exports, __webpack_require__(/*! underscore */ 16)))

/***/ }),
/* 92 */
/*!***********************************************!*\
  !*** ./src/task/models/DiscountCollection.js ***!
  \***********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone */ 17);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _DiscountModel = __webpack_require__(/*! ./DiscountModel.js */ 91);
	
	var _DiscountModel2 = _interopRequireDefault(_DiscountModel);
	
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
	    url: function url() {
	        return AppOption['context_url'] + '/' + 'discount_lines';
	    }
	});
	exports.default = DiscountCollection;

/***/ }),
/* 93 */
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
	
	var _DiscountView = __webpack_require__(/*! ./DiscountView.js */ 94);
	
	var _DiscountView2 = _interopRequireDefault(_DiscountView);
	
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
	    collectionEvents: {
	        'sync': 'render'
	    }
	});
	exports.default = DiscountCollectionView;

/***/ }),
/* 94 */
/*!****************************************!*\
  !*** ./src/task/views/DiscountView.js ***!
  \****************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _underscore = __webpack_require__(/*! underscore */ 16);
	
	var _underscore2 = _interopRequireDefault(_underscore);
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _math = __webpack_require__(/*! ../../math.js */ 70);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	var template = __webpack_require__(/*! ./templates/DiscountView.mustache */ 95); /*
	                                                              * File Name : DiscountView.js
	                                                              *
	                                                              * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                              * Company : Majerti ( http://www.majerti.fr )
	                                                              *
	                                                              * This software is distributed under GPLV3
	                                                              * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                              *
	                                                              */
	
	
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
	    getTvaLabel: function getTvaLabel() {
	        var res = "";
	        var current_value = this.model.get('tva');
	        _underscore2.default.each(AppOption['form_options']['tva_options'], function (tva) {
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
/* 95 */
/*!********************************************************!*\
  !*** ./src/task/views/templates/DiscountView.mustache ***!
  \********************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, buffer = "<div class='col-md-3 col-sm-4 col-xs-12 description'>";
	  stack1 = ((helper = (helper = helpers.description || (depth0 != null ? depth0.description : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"description","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</div>\n<div class='col-md-3 col-sm-2 col-xs-12 amount'><b class='visible-xs text-left'>HT : ";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "</b><span class='hidden-xs'>";
	  stack1 = ((helper = (helper = helpers.ht || (depth0 != null ? depth0.ht : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"ht","hash":{},"data":data}) : helper));
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "</span></div>\n<div class='col-md-6 col-sm-6 col-xs-12 text-right actions'>\n    <button type='button' class='btn btn-default edit'>\n        <i class='glyphicon glyphicon-pencil'></i> <span class='hidden-xs'>Modifier</span>\n    </button>\n    <button type='button' class='btn btn-default delete'>\n        <i class='glyphicon glyphicon-trash'></i> <span class='hidden-xs'>Supprimer</span>\n    </button>\n</div>\n";
	},"useData":true});

/***/ }),
/* 96 */
/*!********************************************!*\
  !*** ./src/task/views/DiscountFormView.js ***!
  \********************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _Mn$View$extend;
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _InputWidget = __webpack_require__(/*! ./InputWidget.js */ 73);
	
	var _InputWidget2 = _interopRequireDefault(_InputWidget);
	
	var _SelectWidget = __webpack_require__(/*! ./SelectWidget.js */ 75);
	
	var _SelectWidget2 = _interopRequireDefault(_SelectWidget);
	
	var _TextAreaWidget = __webpack_require__(/*! ./TextAreaWidget.js */ 43);
	
	var _TextAreaWidget2 = _interopRequireDefault(_TextAreaWidget);
	
	var _ModalFormBehavior = __webpack_require__(/*! ../behaviors/ModalFormBehavior.js */ 77);
	
	var _ModalFormBehavior2 = _interopRequireDefault(_ModalFormBehavior);
	
	var _tools = __webpack_require__(/*! ../../tools.js */ 27);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; } /*
	                                                                                                                                                                                                                   * File Name : DiscountFormView.js
	                                                                                                                                                                                                                   *
	                                                                                                                                                                                                                   * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                                                                                                                                                                                   * Company : Majerti ( http://www.majerti.fr )
	                                                                                                                                                                                                                   *
	                                                                                                                                                                                                                   * This software is distributed under GPLV3
	                                                                                                                                                                                                                   * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                                                                                                                                                                   *
	                                                                                                                                                                                                                   */
	
	
	var template = __webpack_require__(/*! ./templates/DiscountFormView.mustache */ 97);
	
	var DiscountFormView = _backbone2.default.View.extend((_Mn$View$extend = {
	    template: template,
	    regions: {
	        'description': '.description',
	        'amount': '.amount',
	        'tva': '.tva',
	        'percentage': '.percentage'
	    },
	    ui: {
	        btn_cancel: "button[type=reset]",
	        form: "form",
	        submit: 'button[type=submit]',
	        main_tab: 'ul.nav-tabs li:first a'
	    },
	    behaviors: [_ModalFormBehavior2.default],
	    triggers: {
	        'click @ui.btn_cancel': 'modal:close'
	    },
	    childViewEvents: {
	        'change': 'onChildChange',
	        'catalog:edit': 'onCatalogEdit'
	    },
	    modelEvents: {
	        'change': 'refreshForm'
	    },
	    refreshForm: function refreshForm() {},
	    isAddView: function isAddView() {
	        return !(0, _tools.getOpt)(this, 'edit', false);
	    }
	}, _defineProperty(_Mn$View$extend, 'refreshForm', function refreshForm() {
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
	        options: AppOption['form_options']['tva_options'],
	        title: "TVA",
	        value: this.model.get('tva'),
	        field_name: 'tva'
	    }));
	    if (this.isAddView()) {
	        this.getUI('main_tab').tab('show');
	    }
	}), _defineProperty(_Mn$View$extend, 'onRender', function onRender() {
	    this.refreshForm();
	    if (this.isAddView()) {
	        this.showChildView('percentage', new _InputWidget2.default({
	            title: "Pourcentage",
	            field_name: 'percentage',
	            addon: "%"
	        }));
	    }
	}), _defineProperty(_Mn$View$extend, 'templateContext', function templateContext() {
	    return {
	        title: this.getOption('title'),
	        add: this.isAddView()
	    };
	}), _Mn$View$extend));
	exports.default = DiscountFormView;

/***/ }),
/* 97 */
/*!************************************************************!*\
  !*** ./src/task/views/templates/DiscountFormView.mustache ***!
  \************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "            <ul class=\"nav nav-tabs\" role=\"tablist\">\n                <li role=\"presentation\" class=\"active\">\n                    <a href=\"#form-container\"\n                        aria-controls=\"form-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\">\n                        Saisie d'un montant\n                    </a>\n                </li>\n                <li role=\"presentation\">\n                    <a href=\"#percentage-container\"\n                        aria-controls=\"percentage-container\"\n                        role=\"tab\"\n                        data-toggle=\"tab\">\n                        Remise en pourcentage\n                    </a>\n                </li>\n            </ul>\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, buffer = "<div class=\"modal-dialog\" role=\"document\">\n	<div class=\"modal-content\">\n          <div class=\"modal-header\">\n            <button type=\"button\" class=\"close\" data-dismiss=\"modal\" aria-label=\"Close\"><span aria-hidden=\"true\">&times;</span></button>\n            <h4 class=\"modal-title\">"
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "</h4>\n          </div>\n          <div class=\"modal-body\">\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.add : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "            <div class='tab-content'>\n                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane fade in active\"\n                    id=\"form-container\">\n                    <form class='form taskgroup-form'>\n                        <div class='description'></div>\n                        <div class='amount'></div>\n                        <div class='tva'></div>\n                        <button class='btn btn-success primary-action' type='submit' value='submit'>\n                            "
	    + escapeExpression(((helper = (helper = helpers.title || (depth0 != null ? depth0.title : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"title","hash":{},"data":data}) : helper)))
	    + "\n                        </button>\n                        <button class='btn btn-default secondary-action' type='reset' value='submit'>\n                            Annuler\n                        </button>\n                    </form>\n                </div>\n                <div\n                    role=\"tabpanel\"\n                    class=\"tab-pane\"\n                    id=\"percentage-container\">\n                    <div class='percentage'></div>\n                </div>\n            </div>\n          </div>\n          <div class=\"modal-footer\">\n          </div>\n        </form>\n	</div><!-- /.modal-content -->\n</div><!-- /.modal-dialog -->\n\n";
	},"useData":true});

/***/ }),
/* 98 */
/*!*************************************************************!*\
  !*** ./src/task/views/templates/DiscountBlockView.mustache ***!
  \*************************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "    <div class='row lines-header hidden-xs'>\n        <div class='col-md-3 col-sm-4'>Description</div>\n        <div class='col-md-3 ol-sm-2 col-xs-12'>Montant HT</div>\n        <div class='col-md-6 col-sm-6 col-xs-12 text-right'>Actions</div>\n    </div>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  return "in";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "<h2>Remises et frais</h2>\n<div class='modalregion'></div>\n<div class='content'>\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.not_empty : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    <div class='row lines'>\n    </div>\n    <div class='row'>\n        <div class='col-xs-11 text-right'>\n            <button type='button' class='btn btn-default btn-add'>\n                <i class='glyphicon glyphicon-plus-sign'></i> Ajouter une remise\n            </button>\n        </div>\n    </div>\n    <a\n        data-target='#discount-more'\n        data-toggle='collapse'\n        aria-expanded=\"false\"\n        aria-controls=\"discount-more\"\n        >\n        <i class='glyphicon glyphicon-plus-sign'></i> Ajouter des frais forfaitaires\n    </a>\n    <div class='collapse row ";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.is_more_set : depth0), {"name":"if","hash":{},"fn":this.program(3, data),"inverse":this.noop,"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "' id=\"discount-more\">\n        <form class='form-inline'>\n        <div class='col-xs-11 expenses_ht text-right'></div>\n        </form>\n    </div>\n</div>\n";
	},"useData":true});

/***/ }),
/* 99 */
/*!****************************************************!*\
  !*** ./src/task/views/templates/MainView.mustache ***!
  \****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  return "<div>\n    <div id='modalregion'>\n    </div>\n	<div class='row'>\n		<div class='task-edit col-md-9 col-xs-12'>\n            <div id='common'>\n            </div>\n            <div id='tasklines'>\n            </div>\n            <div id='discounts'>\n            </div>\n		</div>\n\n		<div class='task-desktop-actions col-md-3 hidden-sm hidden-xs'\n             id='rightbar'>\n		</div>\n	</div>\n\n	<div class='task-desktop-actions sticky-footer hidden-md hidden-lg' id='footer'>\n	</div>\n</div>\n";
	  },"useData":true});

/***/ }),
/* 100 */
/*!*****************************************************!*\
  !*** ./src/handlebars/job/file_generation.mustache ***!
  \*****************************************************/
/***/ (function(module, exports, __webpack_require__) {

	var Handlebars = __webpack_require__(/*! ./~/handlebars/runtime.js */ 34);
	function __default(obj) { return obj && (obj.__esModule ? obj["default"] : obj); }
	module.exports = (Handlebars["default"] || Handlebars).template({"1":function(depth0,helpers,partials,data) {
	  return "<div class=\"text-center btn btn-warning\">\n<i class=\"fa fa-cog fa-spin fa-4x\"></i>\n<br />\n<b>La génération de fichier est en cours</b>\n</div>\n";
	  },"3":function(depth0,helpers,partials,data) {
	  var stack1, buffer = "\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.failed : depth0), {"name":"if","hash":{},"fn":this.program(4, data),"inverse":this.program(6, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  return buffer;
	},"4":function(depth0,helpers,partials,data) {
	  return "    <div class=\"text-center btn btn-danger\">\n        <i class=\"fa fa-warning fa-4x\"></i>\n        <br />\n        <b>La génération de fichier a échoué</b>\n    </div>\n";
	  },"6":function(depth0,helpers,partials,data) {
	  return "    <div class=\"text-center btn btn-success\">\n        <i class=\"fa fa-check fa-4x\"></i>\n        <br />\n        <b>L'import s'est déroulé avec succès</b>\n    </div>\n";
	  },"8":function(depth0,helpers,partials,data) {
	  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row'>\n    <div class='col-md-6'>\n        <h4>Télécharger votre fichier</h4>\n        <a href=\"/cooked/"
	    + escapeExpression(((helper = (helper = helpers.filename || (depth0 != null ? depth0.filename : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"filename","hash":{},"data":data}) : helper)))
	    + "\" target=\"_blank\" class=\"btn btn-success btn-large\">\n        <i class='glyphicon glyphicon-download'></i> Télécharger\n        </a>\n    </div>\n    <div class='col-md-6'>\n    <h4>Messages</h4>\n    "
	    + escapeExpression(((helper = (helper = helpers.message || (depth0 != null ? depth0.message : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"message","hash":{},"data":data}) : helper)))
	    + "\n";
	  stack1 = ((helper = (helper = helpers.has_message || (depth0 != null ? depth0.has_message : depth0)) != null ? helper : helperMissing),(options={"name":"has_message","hash":{},"fn":this.noop,"inverse":this.program(9, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.has_message) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    <h4>Erreurs</h4>\n    "
	    + escapeExpression(((helper = (helper = helpers.err_message || (depth0 != null ? depth0.err_message : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"err_message","hash":{},"data":data}) : helper)))
	    + "\n";
	  stack1 = ((helper = (helper = helpers.has_err_message || (depth0 != null ? depth0.has_err_message : depth0)) != null ? helper : helperMissing),(options={"name":"has_err_message","hash":{},"fn":this.noop,"inverse":this.program(11, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.has_err_message) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "    </div>\n</div>\n";
	},"9":function(depth0,helpers,partials,data) {
	  return "    Aucun message n'a été retourné\n";
	  },"11":function(depth0,helpers,partials,data) {
	  return "    Aucune erreur n'a été retournée\n";
	  },"compiler":[6,">= 2.0.0-beta.1"],"main":function(depth0,helpers,partials,data) {
	  var stack1, helper, options, functionType="function", helperMissing=helpers.helperMissing, escapeExpression=this.escapeExpression, blockHelperMissing=helpers.blockHelperMissing, buffer = "<div class='row'>\n<div class='col-md-6'>\n<h2>Génération de fichier</h2>\n<ul>\n<li>Identifiant de la tâche : "
	    + escapeExpression(((helper = (helper = helpers.jobid || (depth0 != null ? depth0.jobid : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"jobid","hash":{},"data":data}) : helper)))
	    + " </li>\n<li>Initialisée le : "
	    + escapeExpression(((helper = (helper = helpers.created_at || (depth0 != null ? depth0.created_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"created_at","hash":{},"data":data}) : helper)))
	    + " </li>\n<li>Mise à jour le : "
	    + escapeExpression(((helper = (helper = helpers.updated_at || (depth0 != null ? depth0.updated_at : depth0)) != null ? helper : helperMissing),(typeof helper === functionType ? helper.call(depth0, {"name":"updated_at","hash":{},"data":data}) : helper)))
	    + " </li>\n</ul>\n</div>\n<div class=\"col-md-3 col-md-offset-3\">\n";
	  stack1 = helpers['if'].call(depth0, (depth0 != null ? depth0.running : depth0), {"name":"if","hash":{},"fn":this.program(1, data),"inverse":this.program(3, data),"data":data});
	  if (stack1 != null) { buffer += stack1; }
	  buffer += "    </div>\n</div>\n<hr />\n";
	  stack1 = ((helper = (helper = helpers.running || (depth0 != null ? depth0.running : depth0)) != null ? helper : helperMissing),(options={"name":"running","hash":{},"fn":this.noop,"inverse":this.program(8, data),"data":data}),(typeof helper === functionType ? helper.call(depth0, options) : helper));
	  if (!helpers.running) { stack1 = blockHelperMissing.call(depth0, stack1, options); }
	  if (stack1 != null) { buffer += stack1; }
	  return buffer + "\n";
	},"useData":true});

/***/ }),
/* 101 */,
/* 102 */
/*!***************************************!*\
  !*** ./src/task/components/Facade.js ***!
  \***************************************/
/***/ (function(module, exports, __webpack_require__) {

	'use strict';
	
	Object.defineProperty(exports, "__esModule", {
	    value: true
	});
	
	var _backbone = __webpack_require__(/*! backbone.marionette */ 18);
	
	var _backbone2 = _interopRequireDefault(_backbone);
	
	var _CommonModel = __webpack_require__(/*! ../models/CommonModel.js */ 60);
	
	var _CommonModel2 = _interopRequireDefault(_CommonModel);
	
	var _TaskGroupCollection = __webpack_require__(/*! ../models/TaskGroupCollection.js */ 62);
	
	var _TaskGroupCollection2 = _interopRequireDefault(_TaskGroupCollection);
	
	var _DiscountCollection = __webpack_require__(/*! ../models/DiscountCollection.js */ 92);
	
	var _DiscountCollection2 = _interopRequireDefault(_DiscountCollection);
	
	function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }
	
	function _defineProperty(obj, key, value) { if (key in obj) { Object.defineProperty(obj, key, { value: value, enumerable: true, configurable: true, writable: true }); } else { obj[key] = value; } return obj; } /*
	                                                                                                                                                                                                                   * File Name : Facade.js
	                                                                                                                                                                                                                   *
	                                                                                                                                                                                                                   * Copyright (C) 2017 Gaston TJEBBES g.t@majerti.fr
	                                                                                                                                                                                                                   * Company : Majerti ( http://www.majerti.fr )
	                                                                                                                                                                                                                   *
	                                                                                                                                                                                                                   * This software is distributed under GPLV3
	                                                                                                                                                                                                                   * License: http://www.gnu.org/licenses/gpl-3.0.txt
	                                                                                                                                                                                                                   *
	                                                                                                                                                                                                                   */
	
	
	var FacadeClass = _backbone2.default.Object.extend(_defineProperty({
	    channelName: 'facade',
	    ht: 5,
	    radioEvents: {
	        'update:model': 'onModelUpdated'
	    },
	    radioRequests: {
	        'get:total_ht': 'ht',
	        'get:model': 'getModelRequest',
	        'get:collection': 'getCollectionRequest'
	    },
	    initialize: function initialize(options) {
	        this.models = {};
	        this.collections = {};
	    },
	    loadModels: function loadModels(datas) {
	        this.models['common'] = new _CommonModel2.default(datas);
	        this.models['common'].url = AppOption['context_url'];
	
	        var lines = datas['line_groups'];
	        this.collections['task_groups'] = new _TaskGroupCollection2.default(lines);
	
	        var discounts = datas['discounts'];
	        this.collections['discounts'] = new _DiscountCollection2.default(discounts);
	    },
	    getModelRequest: function getModelRequest(label) {
	        return this.models[label];
	    },
	    getCollectionRequest: function getCollectionRequest(label) {
	        return this.collections[label];
	    },
	    onModelUpdated: function onModelUpdated() {
	        console.log("onModelUpdated");
	    }
	}, 'ht', function ht() {
	    console.log("Requesting the ht");
	    return this.ht;
	}));
	var Facade = new FacadeClass();
	exports.default = Facade;

/***/ })
]);
//# sourceMappingURL=task.js.map