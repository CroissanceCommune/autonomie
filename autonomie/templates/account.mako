<%doc>
 * Copyright (C) 2012-2013 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
       * Pettier Gabriel;
       * TJEBBES Gaston <g.t@majerti.fr>

 This file is part of Autonomie : Progiciel de gestion de CAE.

    Autonomie is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    Autonomie is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
</%doc>

<%inherit file="base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="format_mail" />
<%block name='content'>
<% account = request.user %>
<div class="row" style="margin-top:10px">
    <div class='col-md-5'>
        <div class="well">
            <dl class="dl-horizontal">
                %for label, value in ((u'Identifiant', account.login), (u'Nom', account.lastname), (u'Prénom', account.firstname)):
                    %if value:
                    <dt>${label}</dt>
                    <dd>${value}</dd>
                % endif
                % endfor
                <dt>E-mail</dt><dd>${format_mail(account.email)}</dd>
            </dl>
            <a href="${request.route_path('user', id=account.id, _query=dict(action='accountedit'))}" class="btn btn-primary">Éditer</a>
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
                    %if company.logo_id:
                        <img src="${api.img_url(company.logo_file)}" alt=""  width="250px" />
                    %endif
                </a>
                <p>
                ${company.goal}
                </p>
            % endfor
        </div>
    </div>
    <div class='col-md-5 col-md-offset-2'>
        ${form|n}
    </div>
</div>
</%block>
