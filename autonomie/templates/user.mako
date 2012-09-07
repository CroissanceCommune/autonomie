<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_mail" />
<%namespace file="/base/utils.mako" import="format_phone" />
<%namespace file="/base/utils.mako" import="format_company" />
<%block name='content'>
<div class='row'>
    <div class='span4 offset1'>
        <div class='well'>
            <dl class="dl-horizontal">
                % for label, value in ((u'Identifiant', user.login), (u"Nom", user.lastname), (u"Prénom", user.firstname)):
                    %if value:
                        <dt>${label}</dt>
                        <dd>${value}</dd>
                    % endif
                % endfor
                <dt>E-mail</dt><dd>${format_mail(user.email)}</dd>
            </dl>
% if not user.enabled():
    <span class='label label-warning'>Ce compte a été désactivé</span>
% endif
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
                ${format_company(company)}
                % endfor
        </div>
    </div>
</div>
</%block>

