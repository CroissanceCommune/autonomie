<%doc>
    Directory templates, list users and companies
</%doc>
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a title='Référencer un nouveau client' href='#new' onclick="$('#addform').dialog('open');">
        Ajouter un Utilisateur
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
            <th>${sortable("Nom", "account_lastname")}</th>
            <th>${sortable("E-mail", "account_email")}</th>
            <th>Entreprises</th>
        </tr>
    </thead>
    <tbody>
        % if users:
            % for user in users:
                <tr>
                    <td onclick="document.location='${request.route_path("user", id=user.id)}'" class="rowlink" >${user.lastname.upper()} ${user.firstname.capitalize()}</td>
                    <td onclick="document.location='${request.route_path("user", id=user.id)}'" class="rowlink" >${user.email}</td>
                    <td onclick="document.location='${request.route_path("user", id=user.id)}'" class="rowlink" >
                        <ul>
                            % for company in user.companies:
                                <li>${company.name}</li>
                            % endfor
                        </ul>
                    </td>
                </tr>
            % endfor
        % else:
            <tr><td colspan='3'>Aucun utilisateur n'est présent dans la base</td></tr>
        % endif
</tbody></table>
${pager(users)}
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
    title:"Ajouter un compte utilisateur",
    open: function(event, ui){
    $('.ui-widget-overlay').css('width','100%');
    $('.ui-widget-overlay').css('height','100%');
    }
    });
    });
% endif
</%block>
