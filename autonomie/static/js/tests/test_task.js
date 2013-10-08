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


function initTest(){
  var taskline1 = "<span id='test1' class='taskline'>" +
                "<input name='cost' value='100.25' />" +
                "<input name='quantity' value='1.25' />" +
                "<select name='tva'>" +
                "<option selected='selected' value='1960'>19.6%</option>" +
                "</select>" +
                "<div class='linetotal'><div class='input'></div></div></span>";
  var taskline2 = "<span id='test2' class='taskline'>" +
                "<input name='cost' value='100' />" +
                "<input name='quantity' value='1' />" +
                "<select name='tva'>" +
                "<option selected='selected' value='500'>5%</option>" +
                "</select>" +
                "<div class='linetotal'><div class='input'></div></div></span>";
  var taskline3 = "<span id='test2' class='taskline'>" +
                "<input name='cost' value='3' />" +
                "<input name='quantity' value='1' />" +
                "<select name='tva'>" +
                "<option selected='selected' value='0'>5%</option>" +
                "</select>" +
                "<div class='linetotal'><div class='input'></div></div></span>";

  var line_total = "<div id='tasklines_ht'><div class='input'></div></div>";
  var discountline = "<span id='test-discount' class='discountline'>" +
                "<input name='amount' value='100' />" +
                "<select name='tva'>" +
                "<option selected='selected' value='1960'>19.6%</option>" +
                "</select>" +
                "<div class='linetotal'><div class='input'></div></div></span>";
  var total_ht = "<div id='total_ht'><div class='input'></div></div>";
  var tvalist = "<div id='tvalist'></div>";
  var total_ttc = "<div id='total_ttc'><div class='input'></div></div>";
  var total = "<div id='total'><div class='input'></div></div>";
  $('#qunit-fixture').html($(taskline1));
  $('#qunit-fixture').append($(taskline2));
  $('#qunit-fixture').append($(taskline3));
  $('#qunit-fixture').append($(line_total));
  $('#qunit-fixture').append($(discountline));
  $('#qunit-fixture').append($(total_ht));
  $('#qunit-fixture').append($(tvalist));
  $('#qunit-fixture').append($(total_ttc));
  $('#qunit-fixture').append($(total));
  var deposit = "<select name='deposit'><option value='5'>5%</option></select>";
  $('#qunit-fixture').append($(deposit));
}

var insecable = '\u00a0';
module("Ligne de prestation et totaux");
test("Ligne de prestation", function(){
  initTest();
  var row = new TaskRow('#test1');
  equal(row.tva, 1960);
  equal(row.ht, 125.3125);
  equal(row.tva_amount, 24.56125);
  equal(row.ttc, 149.87375);
  row.update();
  equal("125,3125" + insecable + "€", $('#test1 .linetotal .input').text());
});
test("Ligne de remise", function(){
  initTest();
  var row = new DiscountRow('#test-discount');
  equal(row.ht, -100);
  equal(row.tva, 1960);
  equal(row.tva_amount, -19.6);
  row.update();
  equal("-100,00" + insecable + "€", $('#test-discount .linetotal .input').text());
});
test("Groupe de ligne", function(){
  initTest();
  var collection = new RowCollection();
  collection.load('.taskline', TaskRow);
  equal(collection.models.length, 3);
  equal(collection.HT(), 228.3125);
  equal(collection.TTC(), 257.87375);
  var tvas = collection.Tvas();
  var expected = {1960:24.56125, 500:5, 0:0};
  var index = 0;
  for (var key in tvas){
    equal(tvas[key], expected[key]);
  }
});
test("Contrôle sur le solde", function(){
  initTest();
  computeTotal();
  equal($('#tasklines_ht .input').text(), "228,3125" + insecable + '€');
  equal($('#total_ht .input').text(), '128,31' + insecable + '€');
  equal($('#total .input').text(), '138,27' + insecable + '€');
  equal(getTotal(), 138.27);
});
module("Ligne de configuration des paiements");
test("Calcul de l'acompte", function(){
  initTest();
  $('#total .input').empty().html(formatAmount(1.07));
  equal(getDeposit(), 0.05);
  equal(getToPayAfterDeposit(), 1.02);
});
module("Ligne de paiements", function(){
  test("Calcul des montants des paiements divisés", function(){
    var total_after_deposit = "12566.38";
    equal(computeDivdedAmount(total_after_deposit, 2), 6283.19);
  });
});
