<%inherit file="base.mako"></%inherit>
<%block name='actionmenu'>
    <li>
<a class="btn" title='Référencer un nouveau client' href='#new' onclick="$('#addform').dialog('open');">
        <span class="ui-icon ui-icon-plusthick"></span>
        Ajouter un Client
    </a>
    </li><li>
    <form class='navbar-form pull-left form-search' id='search_form' method='GET'>
    <input type='text' name='search' class='input-medium search-query'>
    <button type="submit" class="btn">Rechercher</button>
</form>
</li>
</%block>
<%block name='content'>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>Code</th>
            <th>Entreprise</th>
            <th>Nom du contact principal</th>
            <th>Actions</th>
        </tr>
    </thead>
    <tbody>
        % if clients:
            % for client in clients:
                <tr class='tableelement' id="${client.id}">
                    <td>${client.id}</td>
                    <td>${client.name}</td>
                    <td>${client.contactLastName} ${client.contactFirstName}</td>
                    <td>
                        <div class='btn-group'>
                            <a class='btn' href='${request.route_path("company_client", cid=company.id, id=client.id)}'>
                                <span class='ui-icon ui-icon-pencil'></span>
                                Voir
                            </a>
                            <a class='btn' href='${request.route_path("company_client", cid=company.id, id=client.id, _query=dict(edit=True))}'>
                                <span class='ui-icon ui-icon-pencil'></span>
                                Éditer
                            </a>
                            <a class='btn' href='${request.route_path("company_client", cid=company.id, id=client.id)}'>
                                <span class='ui-icon ui-icon-folder-open'></span>
                                Projets
                            </a>
                        </div>
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='6'>
                    Aucun client n'a été référencé pour l'instant
                </td>
            </tr>
        % endif
    </tbody>
</table>
    % if html_form is not UNDEFINED:
        <div id='addform'>
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
            title:"Ajouter un client",
            open: function(event, ui){
                $('body').css('overflow','hidden');
                $('.ui-widget-overlay').css('width','100%');
                }
            });
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
