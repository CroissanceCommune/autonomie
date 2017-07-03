require('jquery');
import _ from 'underscore';
import $ from 'jquery';
var datepicker = require("jquery-ui/ui/widgets/datepicker");

export const setDatePicker = function(input_tag, altfield_selector, value, kwargs){
	/*
     * Set a datepicker
     * Input tag is the visible field
     * altfield_selector is the real world field
     * value : The value to set
     * kwargs: additional options to pass to the datepicker call
     */
    let options = {
        altFormat:"yy-mm-dd",
        dateFormat:"dd/mm/yy",
        altField: altfield_selector
    };
    _.extend(options, kwargs);
    console.log(options);
    input_tag.datepicker(options);

    if ((value !== null) && (! _.isUndefined(value))){
        value = parseDate(value);
        input_tag.datepicker('setDate', value);
    } else {
        if (! _.isUndefined(default_value)) {
            value = parseDate(default_value);
            input_tag.datepicker('setDate', value);
        }
    }

}

export const ajax_call = function(url, data, method, extra_options){
  var data = data || {};
  var method = method || 'GET';

  var options = {
    url: url,
    data: data,
    method: method,
    dataType: 'json',
    cache: false
  }
  if (method == 'POST'){
    options.data = JSON.stringify(data);
    options.contentType = "application/json; charset=UTF-8";
    options.processData = false;
  }

  _.extend(options, extra_options);

  return $.ajax(options);
}

export const updateSelectOptions = function(options, val, key){
    /*
     * Add the selected attr to the option with value 'val'
     *
     * :param list options: list of js objects
     * :param list val: list of values or single value
     * :param str key: the key used to identifiy items ('value' by default)
     */
    if (!_.isArray(val)){
      val = [val];
    }
    if (_.isUndefined(key)){
      key = 'value';
    }
    _.each(options, function(option){
      delete option['selected'];
      if (_.contains(val, option[key])){
        option['selected'] = 'true';
      }
    });
    return options;
}
export const getOpt = function(obj, key, default_val){
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
    if (_.isUndefined(val)){
        val = default_val
    }
    return val;
}
