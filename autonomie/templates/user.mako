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
<%namespace file="/base/utils.mako" import="format_phone" />
<%namespace file="/base/utils.mako" import="format_company" />
<%block name='content'>
<div class='row-fluid'>
    <div class='span5'>
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
    <div class='span6 offset1'>
        <div class='well'>
            % if len(user.companies) == 1:
                <h3>Entreprise</h3>
            %else:
                <h3>Entreprises</h3>
            % endif
            <br />
            % for company in user.companies:
                ${format_company(company)}
                % if not company.enabled():
                    <span class='label label-warning'>Cette entreprise a été désactivée</span>
                % endif
            % endfor
        </div>
    </div>
</div>
</%block>

