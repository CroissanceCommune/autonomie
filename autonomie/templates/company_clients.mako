<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a class="btn-primary" title='Référencer un nouveau client' href='#new' onclick="$('#addform').dialog('open');">
        Ajouter un Client
    </a>
    </li>
    <li>
        ${searchform()}
    </li>
</ul>
</%block>
<%block name='content'>
<table class="table table-striped table-condensed">
    <thead>
        <tr>
            <th>${sortable("Code", "code")}</th>
            <th>${sortable("Entreprise", "name")}</th>
            <th>${sortable("Nom du contact principal", "contactLastName")}</th>
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
                            <a class='btn' href='${request.route_path("company_client", cid=company.id, id=client.id)}'>
                                <span class='ui-icon ui-icon-pencil'></span>
                                Voir
                            </a>
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
${pager(clients)}
% if html_form is not UNDEFINED:
    <div id='addform'>
        ${html_form|n}
    </div>
% endif
</%block>
<%block name='footerjs'>
% if html_form is not UNDEFINED:
    $( function() {
    $("#addform").dialog({ autoOpen: false,
    modal:true,
    width:"auto",
    title:"Ajouter un client",
    open: function(event, ui){
    $('.ui-widget-overlay').css('width','100%');
    $('.ui-widget-overlay').css('height','50%');
    }
    });
    });
% endif
</%block>
