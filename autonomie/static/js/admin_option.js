/*
 *
 * Copyright (C) 2014 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */

/*
 * Administration views special cases handling
 */
function get_integre_input(){
  return $('input[value=Intégré]');
}
function find_closest_link_in_parents(tag){
  /*
   * Starting from tag, go through the parents to find a a link
   */
  var current = tag;

  while (current.find('a').length === 0) {
    current = current.parent();
  }
  return current.find('a');
}
$(function(){
  var input = get_integre_input();
  input.attr('disabled', true);
  // We look for the closest a link : the mapping delete button
  var remove_tag =  find_closest_link_in_parents(input.parent().parent());
  remove_tag.remove();
});
