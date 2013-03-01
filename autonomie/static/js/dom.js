/*
 * File Name : dom.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
var Facade = Facade || {};
function delNode(id){
  $('#' + id).remove();
  return true;
}
function getIdFromTagId(parseStr, tagid){
  /*
   *  Return an id from a tagid
   *  @param: parseStr: string to parse to get the id from the tagid
   *  @param: tagid: id of the tag to parse
   *  getIdFromTagId("abcdefgh_", "abcdefgh_2") => 2
   */
  return parseInt(tagid.substring(parseStr.length), 10);
}
function getNextId(selector, parseStr){
  /*
   * Returns the next available id
   * @selector : jquery selector
   * @parseStr : base string
   */
  var newid = 1;
  $(selector).each(function(){
    var tagid = this.id;
    var lineid = getIdFromTagId(parseStr, tagid);
    if (lineid >= newid){
      newid = lineid + 1;
    }
  });
  return newid;
}
$.fn.serializeObject = function(){
  /*
   * Add an object serialization to $(object)
   * Usefull to get form datas as an object
   */
  var result = {};
  var data = this.serializeArray();
  $.each(data, function() {
    if (result[this.name] !== undefined) {
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
function resetForm(form){
  /*
   *  Void all fields in a form
   *  @param form: jquery object
   */
  form.find('input:text, input:password, input:file, select, textarea').val('');
  var checkables = form.find('input:radio, input:checkbox');
  checkables.removeAttr('checked').removeAttr('selected');
}
