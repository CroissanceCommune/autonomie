/*
 * File Name : math.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 * Computing tools and amount manipulation stuff
 *
 */

function transformToCents(value) {
  /*
   * Transform the value to cents
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
   *  Round the price (in our comptability model, we floor it)
   *  We need an epsilon value that handle the 0.999999... case
   *  e.g:
   *  583.06*100 = 58305.99999999999
   *  We'd like to round it to 58306, not 58305 like we will do with 58305.99
   */
  var passed_to_cents = price * 100;
  var epsilon = Math.round(passed_to_cents) - passed_to_cents;
  if (epsilon < 0.000001){
    passed_to_cents = Math.round(passed_to_cents);
  }else{
    passed_to_cents = Math.floor(passed_to_cents);
  }
  return passed_to_cents / 100;
}
function formatPrice(price, rounded) {
  /*
   * Return a formatted price for display
   * @price : compute-formatted price
   */
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
   * Handle the trailing zeros needed for an amount
   */
   if (cents.length === 1){
    cents += 0;
   }
   if ( ! rounded ){
    if ( cents.length > 2 ){
      if (cents.charAt(3) == "0"){
        cents = cents.substr(0,3);
      }
      if (cents.charAt(2) == "0"){
        cents = cents.substr(0,2);
      }
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

