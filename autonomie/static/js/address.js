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
  fetch_customer: function(customer_id) {
    var this_ = this;
    return $.ajax({
         type: 'GET',
         url:"/customers/" + customer_id,
         dataType: 'json',
         success: function(data) {
           this_.already_loaded[customer_id] = data;
         },
         async: false
    });
  },
  getEl: function() {
    return $("select[name=customer_id]");
  },
  get: function(customer_id) {
    if (! (customer_id in this.already_loaded)){
      this.fetch_customer(customer_id);
    }
    return this.already_loaded[customer_id];
  },
  selected: function() {
    var customer_id = this.getEl().children('option:selected').val();
    if (customer_id !== '0'){
      return this.get(customer_id);
    }else{
      return null;
    }
  },
  address: function(customer) {
    return customer.full_address;
  },
  set: function(customer) {
    var address_obj = $('textarea[name=address]');
    address_obj.val(this.address(customer));
  },
  change: function(){
    var customer_obj = this.selected();
    if (customer_obj !== null){
      this.set(customer_obj);
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
