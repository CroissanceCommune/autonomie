/*
 * File Name : address.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
var ALREADY_LOADED = new Object();

function fetch_client(client_id){
  return $.ajax({
         type: 'GET',
         url:"/clients/" + client_id,
         dataType: 'json',
         success: function(data) {
           ALREADY_LOADED[client_id] = data;
         },
         async: false
  });
}
function get_select_client(){
  return $("select[name=client_id]");
}
function get_client(client_id){
  /*
   * Fetch the client object through the json api
   */
  if (client_id in ALREADY_LOADED){
    return ALREADY_LOADED[client_id];
  }else{
    fetch_client(client_id);
    return ALREADY_LOADED[client_id];
  }
}
function getCurrentClient(){
  var client_id = get_select_client().children('option:selected').val();
  if (client_id !== '0'){
    return get_client(client_id);
  }else{
    return "0";
  }
}
function getClientAddress(client){
  var address = client.address;
  address += "\n" + client.zipCode + " " + client.city;
  if (client.country != 'France'){
    address += "\n" + client.country;
  }
  return address;
}
function set_client_address(client){
  /*
   * Set the selected client's address
   */
  var address_obj = $('textarea[name=address]');
  address_obj.val(getClientAddress(client));
}
$(function(){
  get_select_client().change(
    function(){
      var client_obj = getCurrentClient();
      if (client_obj !== "0"){
        set_client_address(client_obj);
      }
    }
  );
});
