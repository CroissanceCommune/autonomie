/*
 * File Name : message.js
 *
 * Copyright (C) 2013 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 * Provide tools to display messages coming back from server side
 *
 */
function _displayServerMessage(options){
  /*
   * """ Display a message from the server
   */
  var msgdiv = templates.serverMessage.render(options);
  $(msgdiv).prependTo("#messageboxes").fadeIn('slow').delay(8000).fadeOut(
  'fast', function() { $(this).remove(); });
}
function displayServerError(msg){
  /*
   *  Show errors in a message box
   */
  _displayServerMessage({msg:msg, error:true});
}
function displayServerSuccess(msg){
  /*
   *  Show errors in a message box
   */
  _displayServerMessage({msg:msg});
}
