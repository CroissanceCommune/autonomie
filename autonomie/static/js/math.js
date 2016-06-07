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


function getEpsilon(){
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
    }
    while (1.0 + (eps / 2.0) != 1.0);
    return eps;
}

function removeEpsilon(value){
  /*
   * Remove epsilons (75.599999999 -> 75.6 )from the value if needed
   *
   * :param int value: The value to test if it's a string, we convert it to
   * float before
   */
  if (_.isUndefined(value.toPrecision)){
    return value;
  }
  var epsilon = getEpsilon();
  var delta = value.toPrecision(6) - value;
  delta = delta * delta;
  if (delta === 0){
    return value;
  }
  if (delta < epsilon){
    return value.toPrecision(6);
  } else {
    return value;
  }
}

function strToFloat(value) {
  /*
   * Transform the value to a float
   *
   * :param str value: A string value representing a number
   */
  var result;

  if ((value === undefined)||(value === null)){
    value = "0.00";
  }
  value = value.replace(",", ".");
  result = parseFloat(value);
  if (isNaN(result)){
    return 0.0;
  }else{
    return result;
  }
}
function round(price){
  /*
   *  Round the price (in our comptability model, round_half_up, 1.5->2)
   *
   *  :param float price: The price to round
   */
  var passed_to_cents = price * 100;
  passed_to_cents = Math.round(passed_to_cents);
  return passed_to_cents / 100;
}

function formatPrice(price, rounded) {
  /*
   * Return a formatted price for display
   * @price : compute-formatted price
   */
  price = removeEpsilon(price);
  var dots, splitted, cents, ret_string;
  if (rounded){
    price = round(price);
  }

  splitted = String(price).split('.');
  if (splitted[1] != undefined){
    cents = splitted[1];
    if (cents.length>4){
      dots = true;
    }
    cents = cents.substr(0, 4);
    cents = trailingZeros(cents, rounded);
  }else{
    cents = '00';
  }
  ret_string = splitted[0] + "," + cents;
  if (dots){
    ret_string += "...";
  }
  return ret_string;
}
function isNotFormattable(amount){
  /*
   * Verify if the amount is already formatted (with the euros sign)
   */
  var test = " " + amount;
  if ((test.indexOf("€") >= 0 )||(test.indexOf("&nbsp;&euro;")>=0)){
    return true;
  }
  return false;
}
function formatAmount( amount, rounded ){
  /*
   * return a formatted user-friendly amount
   */
  if ( rounded === undefined ){
    rounded = true;
  }
  if (isNotFormattable(amount)){
    return amount;
  }
  return formatPrice( amount, rounded ) + "&nbsp;&euro;";
}
function trailingZeros(cents, rounded) {
  /*
   * Remove trailing zeros in an amount
   *
   * :param str cents: A string value representing cents (14010)
   * :param bool rounded: Should we round the value ?
   */
   if (cents.length === 1){
    cents += 0;
   }
   var last_value;
   if ( ! rounded ){
     last_value = cents.substr(cents.length - 1);
     while ((cents.length > 2) && (last_value == '0')) {
       cents = cents.substr(0, cents.length -1);
       last_value = cents.substr(cents.length - 1);
     }
   }
   return cents;
}

function getTvaPart(total, tva){
  /*
   *  Compute the given tva from total
   */
  return total * tva / 10000;
}

function getPercent(amount, percent){
  /*
   * Compute a percentage
   */
  return round(amount * percent / 100);
}
