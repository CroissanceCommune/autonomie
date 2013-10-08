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




function setTurnoverProjectionForm(month_num, value, el){
  /*"""
   *  Display the CAE Prevision Form and set default values
   */
  var container = $('#form_container');
  hideFormError($('#setform'));
  $('#form_container').find("input[name=month]").val(month_num);
  // setting defaults
  var comment = "";
  if (value == undefined){
    value = "";
  }else{
    comment = $(el).attr('title');
  }
  container.find("input[name=value]").val(value);
  container.find("textarea").val(comment);
  // animation
  if (container.is(':visible')){
    container.animate({borderWidth:"10px"}, 400).animate({borderWidth:"1px"}, 200);
  }else{
    $('#form_container').fadeIn("slow");
  }
  $('#form_container').find("input[name=value]").focus();
}

// Page initialisation
$(function(){
  $('#year_form').find('select').change(function(){
    $('#year_form').submit();
  });
  if ($('#setform').find(".alert").length === 0){
    $('#form_container').hide();
  }
});
