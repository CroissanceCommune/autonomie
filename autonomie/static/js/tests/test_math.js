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

module("Computing tools");
test("Transformations des strings en centimes", function(){
  equal(strToFloat(), 0.0);
  equal(strToFloat("15,25"), 15.25);
  equal(strToFloat("15,25658"), 15.25658);
  equal(round(583.06), 583.06);
  equal(round(1.009), 1.01);
  equal(round(1.001), 1);
  equal(formatPrice(1), "1,00");
  equal(formatPrice(1.256, true), "1,26");
  equal(formatPrice(1.255555, false), "1,2555...");
  equal(formatPrice(13.2 * 58, false), "765,60");
  equal(formatPrice(13.2 * 58, false), "765,60");
  equal(formatPrice("1.255555", false), "1,2555...");
  equal(formatPrice(1.2555, false), "1,2555");
  equal(formatPrice(583.06), formatPrice(583.06, false));
  equal(isNotFormattable("150 €"), true);
  equal(isNotFormattable("150 "), false);
  equal(formatAmount(125), "125,00&nbsp;&euro;");
  equal(trailingZeros("1", false), "10");
  equal(trailingZeros("15", false), "15");
  equal(trailingZeros("1500", false), "15");
  equal(trailingZeros("1550", false), "155");
  equal(trailingZeros("01550", false), "0155");
  equal(getTvaPart(100, 1960), 19.6);
  equal(getPercent(1.07, 5), 0.05);
});
