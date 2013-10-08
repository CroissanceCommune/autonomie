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
function get_form(){
  return $('#duplicate_form');
}
function get_select_client(){
  return $(get_form().find('select')[0]);
}
function get_select_project(){
  return $(get_form().find('select')[1]);
}
function get_select_phase(){
  return $(get_form().find('select')[2]);
}

function update_project_select(projects){
  /*
   * Update the project select
   */
  var options = "";
  if (projects){
    for (var i = 0; i < projects.length; i++) {
      var project = projects[i];
      options += "<option value='" + project.id;
      if (i === 0){
        options += "' selected='selected'>";
      }else{
        options += "'>";
      }
      options += project.name + '(' + project.code + ')' + "</option>";
    }
  }
  get_select_project().html(options);
  get_select_project().change();
}
function update_phase_select(phases){
  /*
   * Update the phase select
   */
  var options = "";
  if (phases){
    for (var i = 0; i < phases.length; i++) {
      var phase = phases[i];
      options += "<option value='" + phase.id + "'>"  +
                phase.name +
                "</option>";
    }
  }
  get_select_phase().html(options);
}
function getCurrentClient(){
  var client_id = get_select_client().children('option:selected').val();
  return get_client(client_id);
}
function getCurrentProject(){
  var project_id = get_select_project().children('option:selected').val();
  var client = getCurrentClient();
  var ret_data = {};
  for (var i=0; i < client.projects.length; i++){
    var project = client.projects[i];
    if (project.id == project_id){
      ret_data = project;
      break;
    }
  }
  return ret_data;
}
$(function(){
  /*
   * Add onchange behaviour at page load
   */
  get_select_client().change(
    function(){
      var client_obj = getCurrentClient();
      if (client_obj.projects){
        update_project_select(client_obj.projects);
      }else{
        update_project_select([]);
      }
    }
    );
  get_select_project().change(
    function(){
      var project_obj = getCurrentProject();

      if (project_obj !== {}){
        if (project_obj.phases){
            update_phase_select(project_obj.phases);
        }else{
          update_phase_select([]);
        }
      }else{
        window.alert("Le client et le projet ne correspondent pas.");
      }
    }
  );
  get_select_client().change();
});
