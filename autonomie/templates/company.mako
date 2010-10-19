<%doc>
    company View page
</%doc>
<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_phone" />
<%namespace file="/base/utils.mako" import="format_company" />
<%block name='content'>
<div class='row'>
    <div class="span4 offset1">
        <div class='well'>
            ${format_company(company)}
            % if not company.enabled():
                <span class='label label-warning'>Cette entreprise a été désactivée</span>
            % endif
        %for link in link_list:
            <p>${link.render(request)|n}</p>
        %endfor
        </div>
    </div>
    <div class="span6">
        <div class='well'>
        %if len(company.employees) > 1:
            <h3>Employé(s)</h3>
        %elif len(company.employees) == 1:
            <h3>Employé</h3>
        %else:
            <h3>Il n'y a aucun compte associé à cette entreprise</h3>
        %endif

        % for empl in company.employees:
            <a href="${request.route_path('user', id=empl.id)}" title='Voir ce compte'>
                <i class='icon-user'></i>${empl.lastname} ${empl.firstname}
            </a>
            <br />
            <br />
        % endfor
    </div>
    </div>
</div>
</%block>
