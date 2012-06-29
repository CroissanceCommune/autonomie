<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_mail" />
<%block name='content'>
<div class='row'>
    <div class='span4 offset2'>
        <div class='well'>
            <dl>
                % for label, value in ((u'Identifiant', user.login), (u"Nom", user.lastname), (u"Prénom", user.firstname)):
                    %if value:
                        <dt>${label}</dt>
                        <dd>${value}</dd>
                    % endif
                % endfor
                <dt>E-mail</dt><dd>${format_mail(user.email)}</dd>
            </dl>
        </div>
    </div>
    <div class='span6'>
        <div class='well'>

            % if len(user.companies) == 1:
                <h3>Entreprise</h3>
            %else:
                <h3>Entreprises</h3>
            % endif
            <br />
            % for company in user.companies:
                <a href="${request.route_path('company', id=company.id)}">
                    <strong>${company.name}</strong>
                    <br />
                    %if company.get_logo_filepath():
                        <img src="/assets/${company.get_logo_filepath()}" alt=""  width="250px" />
                    %endif
                </a>
                <br />
                ${company.goal}
                <br />
            % endfor
        </div>
    </div>
</div>
</%block>

