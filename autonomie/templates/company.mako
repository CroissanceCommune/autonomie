<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_phone" />
<%block name='content'>
<div class='row'>
    <div class="span4 offset2">
        <div class='well'>
        <h3>Entreprise ${company.name}</h3>
        ${company.goal}
        %if company.get_logo_filepath():
            <img src="/assets/${company.get_logo_filepath()}" alt=""  width="250px" />
        %endif
        <dl>
                % if company.email:
                    <dt>E-mail</dt>
                    <dd>${format_mail(company.email)}</dd>
                % endif

            % for label, attr in ((u'Téléphone', 'phone'), (u"Téléphone portable", "mobile"),):
                %if getattr(company, attr):
                    <dt>${label}</dt>
                    <dd>${format_phone(getattr(company, attr))}</dd>
                % endif
            % endfor
        </dl>
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
