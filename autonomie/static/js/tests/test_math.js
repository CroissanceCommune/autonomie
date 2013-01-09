/*
 * File Name : test_math.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
module("Computing tools");
test("Transformations des strings en centimes", function(){
  equal(transformToCents(), 0.0);
  equal(transformToCents("15,25"), 15.25);
  equal(transformToCents("15,25658"), 15.25658);
  equal(round(583.06), 583.06);
  equal(round(1.009), 1);
  equal(round(1.001), 1);
  equal(formatPrice(1), "1,00");
  equal(formatPrice(1.256, true), "1,25");
  equal(formatPrice(1.255555, false), "1,2555...");
  equal(formatPrice(1.2555, false), "1,2555");
  equal(formatPrice(583.06), formatPrice(583.06, false));
  equal(isNotFormattable("150 €"), true);
  equal(isNotFormattable("150 "), false);
  equal(formatAmount(125), "125,00&nbsp;&euro;");
  equal(trailingZeros("1", false), "10");
  equal(trailingZeros("15", false), "15");
  equal(trailingZeros("1500", false), "15");
  equal(trailingZeros("1550", false), "155");
  equal(getTvaPart(100, 1960), 19.6);
  equal(getPercent(1.07, 5), 0.05);
});
