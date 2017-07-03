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


function getOneMonthAgo(){
  var today = new Date();
  var year = today.getUTCFullYear();
  var month = today.getUTCMonth() - 1;
  var day = today.getUTCDate();
  return new Date(year, month, day);
}

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
var formatDate = formatPaymentDate;
function getDateFromIso(isoDateStr, dateFormat){
 var strdate = "";
 if (isoDateStr !== ''){
  var date = parseDate(isoDateStr);
  strdate = $.datepicker.formatDate(dateFormat, date);
 }
 return strdate;
}

function getTimeFromIso(isoTimeStr, timeFormat){
  var splitted = isoTimeStr.split(':');
  var hour = parseInt(splitted[0], 10);
  var min = parseInt(splitted[1], 10);
  return $.datepicker.formatTime(timeFormat, {hour: hour, minute: min});
}

function getDateTimeFromIso(isoStr, dateFormat, timeFormat){
  var strdatetime = "";
  if (isoStr !== ''){
    var isoDateStr = isoStr.split(' ')[0];
    var isoTimeStr = isoStr.split(' ')[1];
    var strdate = getDateFromIso(isoDateStr, dateFormat);
    var strTime = getTimeFromIso(isoTimeStr, timeFormat);
    strdatetime = strdate + " " + strTime;
  }
  return strdatetime;
}
function dateToIso(dateObject){
    var year = dateObject.getFullYear();
    var month = dateObject.getMonth()+1;
    var dt = dateObject.getDate();

    if (dt < 10) {
        dt = '0' + dt;
    }
    if (month < 10) {
        month = '0' + month;
    }
    return year + "-" + month + "-" + dt;
}
