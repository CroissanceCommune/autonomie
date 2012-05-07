<%inherit file="base.mako"></%inherit>
<%block name='content'>
<div class='container'>
    <div class="row">
        <div class='span5'>
            <h3>Informations</h3>
            <dl class="dl-horizontal">
                %for label, value in ((u'Identifiant', account.login), (u'Nom', account.lastname), (u'Prénom', account.firstname), (u'E-mail', account.email)):
                    <dt>${label}</dt>
                    <dd>${value}</dd>
                % endfor
            </dl>
            <br />
            <br />
            % if len(account.companies) == 1:
                <h3>Votre entreprise</h3>
            % else:
                <h3>Vos entreprise(s)</h3>
            % endif
            <br />
            % for company in account.companies:
                <a href="${request.route_path('company', cid=company.id)}">
                    <strong>${company.name}</strong>
                    <br />
                    <img src="/assets/${company.get_logo_filepath()}" alt="" />
                    </a>
                <br />
                ${company.goal}
                <br />
            % endfor
        </div>
        <div class='span5 offset2'>
            ${html_form|n}
        </div>
    </div>
</div>
</%block>
