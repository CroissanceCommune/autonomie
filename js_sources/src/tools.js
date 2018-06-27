require('jquery');
import _ from 'underscore';
import $ from 'jquery';
import { parseDate } from './date.js';
import { getPercent } from './math.js';

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
    input_tag.datepicker(options);

    if ((value !== null) && (! _.isUndefined(value))){
        value = parseDate(value);
        input_tag.datepicker('setDate', value);
    } else {
        if (! _.isUndefined(options.default_value)) {
            value = parseDate(options.default_value);
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
     * :returns: True if a default or an existing value has been found
     * :rtype: bool
     */
    if (!_.isArray(val)){
      val = [val];
    }
    if (_.isUndefined(key)){
      key = 'value';
    }
    var has_selected = false;
    _.each(options, function(option){
      delete option['selected'];
      if (_.contains(val, option[key])){
        option['selected'] = 'true';
        has_selected = true;
      }
    });
    if (! has_selected){
        var option = getDefaultItem(options);
        if (!_.isUndefined(option)){
            option['selected'] = true;
            has_selected = true;
        }
    }
    return has_selected;
}
export const getDefaultItem = function(items){
    /*
     * Get The default item from an array of items looking for a default key
     *
     * :param list items: list of objects
     * :rtype: obj or undefined
     */
    var result = _.find(items, function(item){ return item.default==true});
    return result;
}
export const findCurrentSelected = function(options, current_value, key){
    /*
     * Return the full object definition from options matching the current value
     *
     * :param list options: List of objects
     * :param str current_value: The current value in int or str
     * :param str key: The key used to identify objects (value by default)
     * :returns: The object matching the current_value
     */
    return _.find(
        options,
        function(item){
            return item[key] == current_value
        }
    );
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

export const serializeForm = function(form_object){
    /*
     * Return the form datas as an object
     * :param obj form_object: A jquery instance wrapping the form
     */
    var result = {};
    var serial = form_object.serializeArray();
    $.each(serial, function() {
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
}

export const setupAjaxCallbacks = function() {
    /*
     * Setup ajax calls callbacks
     *
     * if 'redirect' is found in the json resp, we go there
     *
     * if status code is 401 : we redirect to #login
     */
    $(document).ajaxComplete(
        function( event, xhr, settings ) {
            if (xhr.status  == 401){
                window.location.replace('#login');
            } else {
                let json_resp = xhr.responseJSON;
                if (!_.isUndefined(json_resp) && ( json_resp.redirect )){
                  window.location.href = json_resp.redirect;
                }
            }
        }
    );
}
export const showLoader = function(){
    /*
     * Show a loading box
     */
    $('#loading-box').show();
}
export const hideLoader = function(){
    /*
     * Show a loading box
     */
    $('#loading-box').hide();
}
function openPopup(url, callback){
    var screen_width =  screen.width;
    var screen_height = screen.height;
    var width = getPercent(screen_width, 60);
    var height = getPercent(screen_height, 60);
    var uniq_id = _.uniqueId('popup');
    if (_.indexOf(url, '?') != -1){
        url = url + "&popup=" + uniq_id;
    } else {
        url = url + "?popup=" + uniq_id;
    }

    var new_win = window.open(
        url,
        uniq_id,
        "width=" + width + ",height=" + height
    );
    if (!_.isUndefined(callback)){
        window.popupCallbacks[uniq_id] = callback;
    }
}

function dismissPopup(win, options){
    var callback = window.popupCallbacks[win.name];
    if (!_.isUndefined(callback)){
        callback(options);
        delete window.popupCallbacks[win.name];
    } else {
        var default_options = {refresh: true};
        _.extend(default_options, options);
        if (!_.isUndefined(default_options.force_reload)){
            window.location.reload();
        } else {
            var new_content = "";

            if (!_.isUndefined(default_options.message)){
                new_content += "<div class='alert alert-success text-center'>";
                new_content += default_options.message;
            } else if (!_.isUndefined(default_options.error)){
                new_content += "<div class='alert alert-danger text-center'>";
                new_content += default_options.error;
            }

            if (default_options.refresh){
                new_content += "&nbsp;<a href='#' onclick='window.location.reload();'><i class='glyphicon glyphicon-refresh'></i> Rafraîchir</a>";
            }

            new_content += '</div>';
            var dest_tag = $('#popupmessage');
            if (dest_tag.length == 0){
                dest_tag = $('.pagetitle');
            }
            dest_tag.after(new_content);
        }
    }

    win.close();
}

export const attachTools = function(){
    window.dismissPopup = dismissPopup;
    window.openPopup = openPopup;
    window.popupCallbacks = {};
}
