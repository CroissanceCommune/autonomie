/*
 * File Name : test_task.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
var insecable = '\u00a0';
module("Fonctions générales");
test("Transformations des strings en centimes", function(){
  equal(transformToCents(), 0.0);
  equal(transformToCents("15,25"), 15.25);
  equal(transformToCents("15,25658"), 15.25658);
});

module("Tests des lignes de prestations");
test("Ligne de prestations", function(){
  var taskline = "<span class='taskline'><input name='cost' value='100.25' />" +
                "<input name='quantity' value='1.25' />" +
                "<select name='tva'>" +
                "<option selected='selected' value='1960'>19.6%</option>" +
                "</select>" +
                "<div class='linetotal'><div class='input'></div></div></span>";
  var row = $(taskline);
  $('#qunit-fixture').html(row);
  var ht = computeTaskRowHT(row);
  var tva = getTva(row);
  equal(125.3125, ht);
  equal(1960, tva);
  equal(24.56125, getTvaPart(ht, tva));
  computeTaskRow(row);
  equal("149,8737..." + insecable + "€", $('#qunit-fixture .linetotal .input').text());
  equal(computeRowsTotal(), 149.8737);
});
test("Ligne de remise", function(){
  var discountline = "<span class='discountline'><input name='amount' value='100' />" +
                "<select name='tva'>" +
                "<option selected='selected' value='1960'>19.6%</option>" +
                "</select>" +
                "<div class='linetotal'><div class='input'></div></div></span>";
  var row = $(discountline);
  $('#qunit-fixture').html(row);
  var ht = computeDiscountRowHT(row);
  var tva = getTva(row);
  equal(100, ht);
  equal(1960, tva);
  equal(19.6, getTvaPart(ht, tva));
  computeDiscountRow(row);
  equal("119,60" + insecable + "€", $('#qunit-fixture .linetotal .input').text());
});

