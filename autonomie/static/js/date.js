/*
 * File Name : date.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

function parseDate(isoDate){
  /*
   * Returns a js Date object from an iso formatted string
   */
   var splitted = isoDate.split('-');
   var year = parseInt(splitted[0], 10);
   var month = parseInt(splitted[1], 10) - 1;
   var day = parseInt(splitted[2], 10);
   return new Date(year, month, day);
}
function formatPaymentDate(isoDate){
  /*
   *  format a date from iso to display format
   */
  if ((isoDate !== '') && (isoDate !== null)){
    return $.datepicker.formatDate("dd/mm/yy", parseDate(isoDate));
  }else{
    return "";
  }
}
