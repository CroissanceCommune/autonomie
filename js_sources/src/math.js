/*
 * * Copyright (C) 2012-2017 Croissance Commune
 * * Authors:
 *       * Arezki Feth <f.a@majerti.fr>;
 *       * Miotte Julien <j.m@majerti.fr>;
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
import _ from 'underscore';

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

export const strToFloat = function(value) {
  /*
   * Transform the value to a float
   *
   * :param str value: A string value representing a number
   */
  var result;

  if (_.isNumber(value)){
      return value
  }

  if (_.isUndefined(value) || _.isNull(value)){
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
export const round = function(price){
  /*
   *  Round the price (in our comptability model, round_half_up, 1.5->2)
   *
   *  :param float price: The price to round
   */
  var passed_to_cents = price * 100;
  passed_to_cents = Math.round(passed_to_cents);
  return passed_to_cents / 100;
}

export const formatPrice = function(price, rounded) {
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
export const isNotFormattable = function(amount){
  /*
   * Verify if the amount is already formatted (with the euros sign)
   */
  var test = " " + amount;
  if ((test.indexOf("€") >= 0 )||(test.indexOf("&nbsp;&euro;")>=0)){
    return true;
  }
  return false;
}
export const formatAmount = function( amount, rounded ){
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
export const trailingZeros = function(cents, rounded) {
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

export const getTvaPart = function(total, tva){
  /*
   *  Compute the given tva from total
   */
  return total * tva / 100;
}

export const getPercent = function(amount, percent){
  /*
   * Compute a percentage
   */
  return round(amount * percent / 100);
}
