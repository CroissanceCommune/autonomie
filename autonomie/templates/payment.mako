<%doc>
 * Copyright (C) 2012-2014 Croissance Commune
 * Authors:
       * Arezki Feth <f.a@majerti.fr>;
       * Miotte Julien <j.m@majerti.fr>;
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
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="definition_list" />
<%block name="content">
<dl class="dl-horizontal">
    <dt>Enregistré par </dt><dd>${api.format_account(request.context.user)}</dd>
    <dt>Date</dt><dd>${api.format_date(request.context.date)}</dd>
    <dt>Mode de paiement</dt><dd>${request.context.mode}</dd>
    <dt>Montant</dt><dd>${api.format_amount(request.context.amount, precision=request.context.precision)|n}&nbsp;&euro;</dd>
    <dt>Banque</dt><dd>
        % if request.context.bank:
            ${request.context.bank.label} (${request.context.bank.compte_cg})
        % else:
            Non renseignée
        % endif
        </dd>
</dl>
</%block>
