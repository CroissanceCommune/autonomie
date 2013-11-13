/*
 * * Copyright (C) 2012-2013 Croissance Commune
 * * Authors:
 *       * Arezki Feth <f.a@majerti.fr>;
 *       * Miotte Julien <j.m@majerti.fr>;
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

var TaskList = {
    switch_btn: function(button, value) {
        if (value) {
            $(button).attr("style", "");
            }
        else {
            $(button).attr("style", "color: #ccc");
            }
    },
    get_table: function(element) {
        return $(element.find("table.tasklist"));
    },
    buttons_states: function(element) {
        table = TaskList.get_table(element);
        page_num = parseInt(table.attr("active_page"));
        page_max = parseInt(table.attr("total_pages_nb"));
        console.log("current page: " + page_num + " - max page=" + page_max);
        TaskList.button_makeup(element.prev_btn, page_num != 0, page_num - 1, element)
        TaskList.button_makeup(element.next_btn, page_num != page_max - 1, page_num + 1, element)
        $.each(
            element.find("[class^=companytaskpage_]"), 
            function(index, button) {
                button = $(button);
                TaskList.button_makeup(button, button.attr('class') != "companytaskpage_" + page_num, index, element)
            });
    },
    button_makeup: function(button, state, target_page, element) {
    button.unbind();
    if (state) {
        button_class = button.attr("class");
        console.log(button_class + " has target " + target_page);
        TaskList.switch_btn(button, true);
        button.bind("click", function(){
            console.log("clicked on " + button_class);
            TaskList.refresh_list(element, target_page);
            });
    }
    else {
        TaskList.switch_btn(button, false);
    }
    },
    refresh_list: function(element, page_num) {
        console.log("Recuperation en cours: page " + page_num);
        url = '?action=tasks_html';
        postdata = {'tasks_page_nb': page_num};
        $.post(
            url,
            postdata,
            function(data, httpstatus, xhr){
                /* TODO: handle failure. 
                 * I got in trouble with callbacks */
                TaskList.get_table(element).replaceWith(data);
                TaskList.buttons_states(element);
            });
    },
    setup: function(element) {
        /* 
         * Arguments:
         * * tasklist_elt: a jquery elt 
         */
        console.log("Task list: setup for element " + element);
        console.log("Task list: setup done");
        element.prev_btn = element.find(".previous_btn_state");
        element.next_btn = element.find(".next_btn_state");
        TaskList.buttons_states(element);
    },
};

$(function(){
    $.each($("div.tasklist"), function(index, element) {
        TaskList.setup($(element));
    });
});
