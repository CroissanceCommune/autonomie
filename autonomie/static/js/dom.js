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
