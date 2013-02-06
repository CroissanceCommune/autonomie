/*
 * File Name : commercial.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 * Handle the commercial previsions page
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

