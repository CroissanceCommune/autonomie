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
                <h4>Votre entreprise</h4>
            % else:
                <h4>Vos entreprise(s)</h4>
            % endif
            <br />
            % for company in account.companies:
                <strong>${company.name}</strong>
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
