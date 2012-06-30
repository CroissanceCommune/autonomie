<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_mail" />
<%block name='content'>
<div class="row" style="margin-top:10px">
    <div class='span4 offset1'>
        <div class="well">
            <h3>Informations</h3>
            <dl class="dl-horizontal">
                %for label, value in ((u'Identifiant', account.login), (u'Nom', account.lastname), (u'Prénom', account.firstname)):
                    <dt>${label}</dt>
                    <dd>${value}</dd>
                % endfor
                <dt>E-mail</dt><dd>${format_mail(account.email)}</dd>
            </dl>
            <a href="${request.route_path('user', id=account.id, _query=dict(action='edit'))}" class="btn btn-primary">Éditer</a>
        </div>
        <div class="well">
            % if len(account.companies) == 0:
                Vous n'êtes lié(e) à aucune entreprise
            % elif len(account.companies) == 1:
                <h3>Votre entreprise</h3>
            % else:
                <h3>Vos entreprise(s)</h3>
            % endif
            <br />
            % for company in account.companies:
                <a href="${request.route_path('company', id=company.id , _query=dict(edit=True))}">
                    <strong>${company.name}</strong>
                    <br />
                    %if company.get_logo_filepath():
                        <img src="/assets/${company.get_logo_filepath()}" alt=""  width="250px" />
                    %endif
                </a>
                <p>
                ${company.goal}
                </p>
            % endfor
        </div>
    </div>
    <div class='span5 offset1'>
        ${html_form|n}
    </div>
</div>
</%block>
