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
    buttons_states: function(element) {
        page_num = element.attr("active_page");
        page_max = element.attr("total_pages_nb");
        console.log("current page: " + page_num);
        prev_btn = element.find(".previous_btn_state");
        next_btn = element.find(".next_btn_state");
        TaskList.switch_btn(prev_btn, (page_num != 0));
        TaskList.switch_btn(next_btn, (page_num != page_max));
        $.each(
            element.find("[id^=companytaskpage_]"), 
            function(index, button) {
                if (button.id == "companytaskpage_" + page_num) {
                    TaskList.switch_btn($(button), false);
                } else {
                    TaskList.switch_btn($(button), true);
                    console.log("setting up link for " + button.id);
                    $(button).bind("click", function(){
                        console.log("clicked on " + button.id);
                        TaskList.refresh_list(table, index);
                        });
                } 
            });
    },
    refresh_list: function(table, page_num) {
        $(table).html("Recuperation en cours: page " + page_num);
        console.log("Recuperation en cours: page " + page_num);
        url = '?action=tasks_html';
        data = {'tasks_page_nb': page_num};
        $.post(
            url,
            data,
            function(data, httpstatus, xhr){
                console.log('success: ');
                $(table).html(data);
            });
    },
    setup: function(element) {
        /* 
         * Arguments:
         * * tasklist_elt: a jquery elt 
         */
        console.log("Task list: setup for element " + element);
        TaskList.buttons_states(element);
        console.log('prev btn: ' + prev_btn);
        console.log("Task list: setup done");
        table = element.find("table.tasklist");
    },
};

$(function(){
    $.each($("div.tasklist"), function(index, element) {
        TaskList.setup($(element));
    });
});
