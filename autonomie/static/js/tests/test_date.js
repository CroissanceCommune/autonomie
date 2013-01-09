/*
 * File Name : test_date.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
module("Date handling");
test("Date To Iso", function(){
  // L'objet Date prend les mois en partant de janvier->0
  pdate = parseDate("2012-12-25");
  edate = new Date(2012, 11, 25);
  equal(pdate.year, edate.year);
  equal(pdate.month, edate.month);
  equal(pdate.day, edate.day);
});
