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
    % if duplicate_accounts is not UNDEFINED:
        <div class='panel panel-default page-block'>
            <div class='panel-heading'>
            Confirmez l'ajout
            </div>
            <div class='panel-body>'>
                <div class="alert alert-warning">
                    <div class='row'>
                        <div class='col-xs-12 col-md-8'>
                        Vous allez ajouter le compte
                        <strong>${appstruct['lastname']}
                        ${appstruct['firstname']}
                        (${appstruct['email']})</strong>. Il existe des comptes
                        avec des noms ou des adresses de courriels
                        similaires.<br /><br />
                        Après avoir vérifié que le compte n'existe pas encore
                        dans Autonomie, vous pouvez confirmer l'ajout d'un
                        nouveau compte.
                        <br />
                        <br />
                        <br />
                            <div>
                            <button
                                class="btn btn-default btn-success"
                                onclick="submitForm('#${confirm_form_id}');">
                                Confirmer l'ajout
                            </button>
                            <a href="${back_url}"
                                class="btn btn-default btn-danger"
                                >
                                Annuler la saisie
                            </a>
                            </div>
                        </div>
                        <div class='col-xs-12 col-md-4'>
                            <ul>
                            % for account in duplicate_accounts:
                                <li>
                                    <a href="#" onclick="openPopup('${request.route_path(user_view_route, id=account.id)}')">
                                    <i class='fa fa-external-link'></i>&nbsp;${api.format_account(account)} (${account.email})
                                    </a>
                                </li>
                            % endfor
                            </ul>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    % endif
</%block>
