/*
 * File Name : admin_expense.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
var ExpenseList = {
  popup_selector: null,
  get_status_url: function(expensesheet_id){
    return "/expenses/" + expensesheet_id + "?action=status";
  },
  payment_form: function(expensesheet_id, total){
    var popup = $(this.popup_selector);
    var form = popup.find('form');
    var url = this.get_status_url(expensesheet_id);
    form.attr('action', url);
    form.find('input[name=amount]').val(total);
    popup.dialog('open');
    console.log(popup);
  }
};
