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
