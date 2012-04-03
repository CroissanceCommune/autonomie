<%inherit file="base.mako"></%inherit>
<%block name='rightbar'>
<div class='well'>
    <ul class="nav nav-list">
        <li class='nav-header'>Gérer vos projets</li>
        <li>
        <a title='Créer un nouveau projet' href='#new' onclick="$('#addform').dialog('open');">
            <span class="ui-icon ui-icon-plusthick"></span>
            Ajouter un Projet
        </a>
        </li>
        <li class='nav-header'>Filtrer</li>
        <li>
            <select id="filter-element-select">
                <option value='__TOUS'>Tous</option>
                %for project in projects:
                    <option value="${project.id}">${project.name}</option>
                %endfor
            </select>
        </li>
    </ul>
</div>
</%block>
<%block name='content'>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>Code</th>
            <th>Nom du projet</th>
            <th>Client</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        % if projects:
            % for project in projects:
                <tr class='tableelement' id="${project.id}">
                    <td>${project.code}</td>
                    <td>${project.name}</td>
                    <td>${project.client.name}</td>
                    <td>
                        <div class='btn-group'>
                            <a class='btn' href='${request.route_path("company_project", cid=company.id, id=project.id)}'>
                                <span class='ui-icon ui-icon-pencil'></span>
                                Éditer
                            </a>
                            <a class='btn' href='${request.route_path("estimation", cid=company.id, id=project.id)}'>
                                <span class='ui-icon ui-icon-plusthick'></span>
                                Devis
                            </a>
                            <a class='btn' href='${request.route_path("company_project", cid=company.id, id=project.id)}'>
                                <span class='ui-icon ui-icon-plusthick'></span>
                                Facture
                            </a>
                            <a class='btn' href='${request.route_path("company_project", cid=company.id, id=project.id)}'>
                                <span class='ui-icon ui-icon-folder-collapsed'></span>
                                Archiver
                            </a>
                        </td>
                    </tr>
                % endfor
            % else:
                <tr>
                    <td colspan='6'>
                        Aucun projet n'a été créé pour l'instant
                    </td>
                </tr>
            % endif
        </tbody>
    </table>
    % if html_form is not UNDEFINED:
        <div id='addform' style="overflow:hidden;">
            ${html_form|n}
        </div>
    % endif
    </%block>
    <%block name='footerjs'>
        <script>
    % if html_form is not UNDEFINED:
            $( function() {
            $("#addform").dialog({ autoOpen: false,
            modal:true,
            width:"auto",
            height:"auto",
            autoResize:true,
            title:"Ajouter un Projet"
            })
            });
    % endif
    $("#filter-element-select").chosen({allow_single_deselect:true}).change(function(event){
    var clientcode = event.target.value;
    if (clientcode == '__TOUS'){
        $('.tableelement').show();
    }else{
        $('.tableelement').hide();
        $('#'+clientcode).show();
                        }
            });
        </script>
    </%block>

