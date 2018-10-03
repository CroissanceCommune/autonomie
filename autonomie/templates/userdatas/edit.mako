<%doc>
    * Copyright (C) 2012-2016 Croissance Commune
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
<%block name="mainblock">
    ${request.layout_manager.render_panel('help_message_panel', parent_tmpl_dict=context.kwargs)}
    <button
        type="button"
        class="btn btn-info btn-head"
        onclick="javascript:enableForm('#deform');$(this).hide();"
        >
        <i class='fa fa-unlock'></i>&nbsp;Dégeler le formulaire
    </button>
    % if request.has_permission('delete.userdatas', current_userdatas):
        <a
            class='btn text-danger btn-head'
            href="${delete_url}"
            onclick="return confirm('En supprimant cette fiche de gestion sociale, vous supprimerez également \nles données associées (documents sociaux, parcours, historiques...). \n\nContinuer ?')">
            <i class='fa fa-trash'></i>&nbsp;Supprimer la fiche
        </a>
    % endif
    ${form|n}
</%block>
<%block name="footerjs">
    setAuthCheckBeforeSubmit('#deform');
    disableForm("#deform");
</%block>
