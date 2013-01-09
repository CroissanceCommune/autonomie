/*
 * File Name : test_dom.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
module("DOM Manipulation tools");
test("Test Id manipulation", function(){
  equal(getIdFromTagId("abcdefgh_", "abcdefgh_2"), 2);
  });
test("Del function", function(){
  var line = "<div id='test'>Test</div>";
  $('#qunit-fixture').html($(line));
  delNode('test');
  var test = $('#test');
  equal($('#test').length, 0);
});
