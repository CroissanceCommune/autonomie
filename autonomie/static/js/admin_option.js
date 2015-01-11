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
$(function(){
  var input = $('input[value=Intégré]');
  input.attr('disabled', true);
  var remove_tag = input.parent().parent().parent().find('a').first();
  remove_tag.remove();
});
