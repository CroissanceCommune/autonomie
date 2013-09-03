/*
 * File Name : tva.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

function getCurrentSelection(select){
  /*
   * Return the current selected tva
   */
  return select.children('option:selected').val();
}


function getCodesFromTva(current_tva){
  /*
   *  return the codes associated to the current TVA
   */
  var tva_options = AppOptions['tvas'];
  if (current_tva in tva_options){
    return tva_options[current_tva]['products'];
  }else{
    alert("Code Tva inconnue, contactez votre administrateur");
    return null;
  }
}


function update_product_code_select(pcode_select, codes, current_code){
  /*
   * Update the product code select and provide codes as available options
   */
  if (_.isUndefined(current_code)){
    current_code = "...";
  }
  var options = "";
  if (codes){
    for (var i = 0; i < codes.length; i++) {
      var code = codes[i];
      options += "<option value='" + code.compte_cg + "'";
      if (! _.isUndefined(current_code)){
        if (current_code == code.compte_cg){
          options += " selected='selected'";
        }
      }else{
        if (i === 0){
          options += " selected='selected'";
        }
      }
      options += ">";
      options += code.name + '(' + code.compte_cg + ')' + "</option>";
    }
  }
  pcode_select.html(options);
}


function getProductCodeSelect(select){
  return select.parent().next().find('select');
}


function onTvaSelect(select_tag){
  /*"""
   * Launched when the tva select is selected
   */
  if (AppOptions['manager']){
    /*
     * Only available for managers and admins
     */
    var select = $(select_tag);
    var pcode_select = getProductCodeSelect(select);
    var current_tva = getCurrentSelection(select);
    var codes = getCodesFromTva(current_tva);
    update_product_code_select(pcode_select, codes);
  }
}


function cleanProductSelects(){
  /*
   * On page load, the list of selected products contains all products,
   * only the one associated to the current tva should be available.
   */
  if (AppOptions['manager']){
    $('select[name=tva]').each(function(index, select_tag){
      var select = $(select_tag);
      var pcode_select = getProductCodeSelect(select);
      var current_tva = getCurrentSelection(select);
      var current_code = getCurrentSelection(pcode_select);
      var codes = getCodesFromTva(current_tva);
      update_product_code_select(pcode_select, codes, current_code);
    });
  }
}
