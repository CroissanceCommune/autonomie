/*
 * File Name : duplicate_form.js
 *
 * Copyright (C) 2012 Gaston TJEBBES g.t@majerti.fr
 * Company : Majerti ( http://www.majerti.fr )
 *
 * This software is distributed under GPLV3
 * License: http://www.gnu.org/licenses/gpl-3.0.txt
 *
 */
/*
 * Handling select changes behaviours for phase choice inside a company
 * Choose a client then choose a project then choose a phase
 * expects the json api to return clients with a projects key and projects
 * with a phases key
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
function update_deformField2(projects){
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
  $('#deformField2').html(options);
  $('#deformField2').change();
}
function update_deformField3(phases){
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
  $('#deformField3').html(options);
}
function getCurrentClient(){
  var client_id = $("#deformField1 option:selected").val();
  return get_client(client_id);
}
function getCurrentProject(){
  var project_id = $("#deformField2 option:selected").val();
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
  $('#deformField1').change(
    function(){
      var client_obj = getCurrentClient();
      if (client_obj.projects){
        update_deformField2(client_obj.projects);
      }else{
        update_deformField2([]);
      }
    }
    );
  $('#deformField2').change(
    function(){
      var project_obj = getCurrentProject();

      if (project_obj !== {}){
        if (project_obj.phases){
            update_deformField3(project_obj.phases);
        }else{
          update_deformField3([]);
        }
      }else{
        window.alert("Le client et le projet ne correspondent pas.");
      }
    }
  );
  $('#deformField1').change();
});

