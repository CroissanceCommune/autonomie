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
% if request.has_permission('delete.trainerdatas', current_trainerdatas):
<a
    class='btn btn-danger primary-action btn-head'
    href="${delete_url}"
    onclick="return confirm('Êtes-vous sûr de vouloir supprimer cette fiche formateur et tous les éléments associés ?')">
    <i class='fa fa-trash'></i>&nbsp;Supprimer la fiche
</a>
% endif
${request.layout_manager.render_panel('help_message_panel', parent_tmpl_dict=context.kwargs)}
${form|n}
</%block>
<%block name="footerjs">
    setAuthCheckBeforeSubmit('#deform');
</%block>
