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
<%inherit file="/base/formpage.mako" />
<%namespace file="/base/utils.mako" import="format_text" />
<%block name='beforecontent'>
    % if confirmation_message is not UNDEFINED:
        <div class='panel panel-default page-block'>
            <div class='panel-body>'>
                <div class="alert alert-warning">
                    ${format_text(confirmation_message)}
                    <button
                        class="btn btn-default btn-success"
                        onclick="submitForm('#${confirm_form_id}');">
                        Confirmer l'ajout
                    </button>
                    <button
                        class="btn btn-default btn-danger"
                        onclick="submitForm('#${confirm_form_id}', 'cancel');">
                        Annuler la saisie
                    </button>
                </div>
            </div>
        </div>
    % endif
</%block>
