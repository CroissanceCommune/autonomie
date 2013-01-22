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
var address_handler = {
  already_loaded: new Object(),
  fetch_client: function(client_id) {
    var this_ = this;
    return $.ajax({
         type: 'GET',
         url:"/clients/" + client_id,
         dataType: 'json',
         success: function(data) {
           this_.already_loaded[client_id] = data;
         },
         async: false
    });
  },
  getEl: function() {
    return $("select[name=client_id]");
  },
  get: function(client_id) {
    if (! (client_id in this.already_loaded)){
      this.fetch_client(client_id);
    }
    return this.already_loaded[client_id];
  },
  selected: function() {
    var client_id = this.getEl().children('option:selected').val();
    if (client_id !== '0'){
      return this.get(client_id);
    }else{
      return null;
    }
  },
  address: function(client) {
    return client.full_address;
  },
  set: function(client) {
    var address_obj = $('textarea[name=address]');
    address_obj.val(this.address(client));
  },
  change: function(){
    var client_obj = this.selected();
    if (client_obj !== null){
      this.set(client_obj);
    }
  }
};
$(function(){
  address_handler.getEl().change(
    function(){
      address_handler.change();
    }
  );
});
