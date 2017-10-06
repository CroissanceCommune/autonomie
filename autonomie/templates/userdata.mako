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
<%doc>
    User datas edition page
    Include two forms, one for datas edition, the other for doctypes
    registration
</%doc>
<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/utils.mako" import="table_btn"/>
<%namespace file="/base/utils.mako" import="format_filelist" />
<%namespace file="/base/utils.mako" import="format_filetable" />
<%namespace file="/base/utils.mako" import="format_text" />
<%block name='afteractionmenu'>
<% user = getattr(request.context, "user", None) %>
<div class='page-header-block'>
% if request.has_permission('admin_userdatas') and request.context.__name__ == 'userdatas':
    <a
        class='btn btn-default'
        href="${request.route_path('userdata', id=request.context.id, _query=dict(action="attach_file"))}"
        >
        <i class='glyphicon glyphicon-file'></i>&nbsp;Attacher un fichier
        </a>
% endif
% if user is not None and not user.enabled():
        <% del_url = request.route_path('userdata', id=request.context.id, _query=dict(action="delete")) %>
        <% del_msg = u'Êtes vous sûr de vouloir supprimer les données de cette personne ?' %>
        % if user is not None:
            <% del_msg += u" Le compte associé sera également supprimé. Cette action n\\'est pas réversible." %>
        % endif
        <a
            class='btn btn-danger'
            href='${del_url}'
            onclick="return confirm('${del_msg}');"
            >
            <i class='glyphicon glyphicon-trash'></i> &nbsp;Supprimer les données de gestion sociale
        </a>
% endif
</div>
</%block>
<%block name="content">
<% user = getattr(request.context, "user", None) %>
% if request.context.__name__ == 'userdatas':
        % if user is not None:
            <div class='panel panel-default page-block'>
                <div class='panel-body>'>
                Ces données sont associées à un compte utilisateur
                </div>
            </div>
        % endif
% else:
    ## IT's a new entry
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
% endif
<div class='panel panel-default page-block'>
<div class='panel-heading'>
${title}
</div>
<div class='panel-body'>

<ul class='nav nav-tabs' role="tablist">
    <li class='active'>
        <a href="#tab1" data-toggle='tab' aria-expanded="false" aria-controls="home" role="tab">
            Informations sociales
        </a>
    </li>
    % if doctemplates is not UNDEFINED:
    <li>
        <a href="#tab4" data-toggle='tab'>
            Génération de documents
        </a>
        </li>
    % endif
    % if doctypes_form is not UNDEFINED:
        <li>
        <a href="#tab2" data-toggle='tab'>
            Documents sociaux
        </a>
        </li>
    % endif
    % if account_form is not UNDEFINED and account_form is not None:
        <li>
        <a href="#tab3" data-toggle='tab'>
            Compte utilisateur
            % if user is not None and not user.enabled():
                <span class='label label-warning'>Ce compte a été désactivé</span>
            % endif
        </a>
        </li>
    % endif
    % if user is not None:
        <li>
            <a href="#tab5" data-toggle='tab'>
                Entreprise(s)
            </a>
        </li>
        <li role="presentation">
            <a href="#tab-accompagnement" data-toggle="tab" aria-controls="accompagnement" role="tab">
                Accompagnement
            </a>
        </li>
    % endif
</ul>
<div class='tab-content'>
    <div class='tab-pane container-fluid active' id='tab1'>
        <div class='row'>
            <div class='col-md-9 col-sm-12'>
            % if request.context.__name__ == 'userdatas':
                <button
                    type="button"
                    class="btn btn-default"
                    onclick="javascript:enableForm('#userdatas_edit');$(this).hide();"
                    style="margin-bottom: 15px"
                    >
                    Dégeler le formulaire
               </button>
            % endif
            ${form|n}
            </div>
            <div class='col-md-3 col-sm-12'>
                % if request.context.__name__ == 'userdatas':
                    <h3>Historique</h3>
                    <hr/>
                    % if request.context.situation_history:
                        <h4>Changements de situation</h4>
                        <table class='table table-condensed'>
                            <thead><tr><th>Date</th><th>Situation</th></tr></thead>
                            <tbody>
                            % for situation in request.context.situation_history:
                                <tr>
                                    <td>${api.format_date(situation.date)}</td>
                                    <td>${situation.situation.label}</td>
                                </tr>
                            % endfor
                            </tbody>
                        </table>
                    % endif
                % endif
            </div>
        </div>
    </div>
    % if doctypes_form is not UNDEFINED:
    <div class='tab-pane row' id='tab2'>
        <div class='col-md-3 text-right'>
            <h4>Documents sociaux fournis</h4>
            <div class='alert alert-info'>
                <i class='fa fa-question-circle fa-2x'></i>
                Cochez les documents sociaux fournis par l'entrepreneur
            </div>
            ${doctypes_form.render()|n}
        </div>
        <div class='col-md-9'>
            <h4>Liste des documents disponibles</h4>
            <div class='alert alert-info'>
                <i class='fa fa-question-circle fa-2x'></i>
                Cette liste présente l'ensemble des documents déposés dans Autonomie ainsi que l'ensemble des documents générés depuis l'onglet Génération de documents.<br />
                Ces documents sont visibles par l'entrepreneur.
                <br />
                <br />
                <a class='btn btn-success'
                href="${request.route_path('userdata', id=request.context.id, _query=dict(action='attach_file'))}"
                title="Déposer un document dans autonomie">
                <i class="glyphicon glyphicon-plus"></i>
                Déposer un document
            </a>
            </div>
            ## ${format_filelist(userdata, delete=True)}
            ${format_filetable(request.context.children)}
        </div>
    </div>
    % endif
    % if account_form is not UNDEFINED and account_form is not None:
        <div class='tab-pane row' id='tab3'>
            <div class=''>
            % if user.enabled():
                <% disable_url = request.route_path('user', \
                    id=request.context.user_id, \
                    _query=dict(action='disable')) %>
                <% disable_msg = u'Êtes vous sûr de vouloir désactiver le compte de cet utilisateur ?' %>

                ${table_btn(disable_url, \
                u"Désactiver le compte", \
                u"Désactiver le compte associé à cette entrée de gestion sociale", \
                onclick="return confirm('%s');" % disable_msg, \
                icon="book",
                css_class="btn-warning", \
                )}
            % else:
                <% enable_url = request.route_path('user', \
                id=request.context.user_id, \
                _query=dict(action='enable')) %>

                ${table_btn(enable_url, \
                u"Ré-activer le compte de cet entrepreneur",
                u"Ré-activer ce compte utilisateur",
                icon="book",
                css_class="btn-success", \
                )}
            % endif
        </div>
            <br />
            <hr>
            <br />
            <div class='medium-form-container'>
                ${account_form.render()|n}
            </div>
        </div>
    % endif
    % if doctemplates is not UNDEFINED:
    <div class='tab-pane row' id='tab4'>
        <div class='row'>
            <div class='col-md-10'>
            <ul class="nav nav-pills nav-stacked">
        % for doctemplate in doctemplates:
            <% url = request.route_path('userdata', id=request.context.id, _query=dict(template_id=doctemplate.id, action="py3o")) %>
                <li>
                    <a href="${url}">
                        <i class="fa fa-file fa-1x"></i>
                        ${doctemplate.description} ( ${doctemplate.name} )
                    </a>
                </li>
        % endfor
            </ul>
            <div class='alert alert-info'>
            % if doctemplates == []:
                <i class='fa fa-question-circle fa-2x'></i>
                Vous devez déposer des modèles de document dans Autonomie pour pouvoir accéder à cet outil.
                    <br />
            % endif
            % if request.has_permission('admin'):
                <a class='btn btn-success'
                    href="${request.route_path('templates')}">
                <i class="glyphicon glyphicon-plus"></i>
                    Déposer de nouveau modèle de document
                </a>
            % endif
            </div>
            </div>
            <%doc>
            <div class='col-md-6'>
                <h3>Historique des documents générés depuis Autonomie</h3>
                <span class='help-block'>
                    <i class='fa fa-question-circle fa-2x'></i>
                    Chaque fois qu'un utilisateur génère un document depuis cette page, une entrée est ajoutée à l'historique.<br />
                    Si nécessaire, pour rendre plus pertinente cette liste, vous pouvez supprimer certains entrées.
                </span>
                <table class='table table-stripped table-condensed'>
                    <thead>
                        <th>Nom du document</th>
                        <th>Généré par</th>
                        <th>Date</th>
                        <th class='text-right'>Actions</th>
                    </thead>
                    <tbody>
                        % for history in request.context.template_history:
                            % if history.template is not None:
                                <tr>
                                    <td>${history.template.description}</td>
                                    <td>${api.format_account(history.user)}</td>
                                    <td>${api.format_datetime(history.created_at)}</td>
                                    <td class='text-right'>
                                        <% url = request.route_path('templatinghistory', id=history.id, _query=dict(action='delete')) %>
                                        ${table_btn(url, \
                                        u"Supprimer cette entrée",\
                                        u"Supprimer cette entrée de l'historique", \
                                        icon='trash', \
                                        css_class="btn-danger")}
                                    </td>
                                </tr>
                            % endif
                        % endfor
                        % if len(request.context.template_history) == 0:
                            <tr><td colspan='4'>Aucun document n'a été généré pour ce compte</td></tr>
                        % endif
                    </tbody>
                </table>
            </div>
            </%doc>
        </div>
    </div>
    % endif
    % if user is not None:
        <div class='tab-pane row' id='tab5'>
            <table class="table table-striped table-condensed table-hover">
                <thead>
                    <th>Nom</th>
                    <th>Adresse e-mail</th>
                    <th>Entrepreneur(s)</th>
                    <th style="text-align:center">Actions</th>
                </thead>
                <tbody>
                    % for company in user.companies:
                        <% url = request.route_path('company', id=company.id) %>
                        <% onclick = "document.location='{url}'".format(url=url) %>
                        % if not company.enabled():
                            <tr class="danger">
                        % else:
                            <tr>
                        % endif
                            <td onclick="${onclick}" class="rowlink">
                                ${company.name}
                                % if not company.enabled():
                                    <span class='label label-danger'>
                                        Cette entreprise a été désactivée
                                    </span>
                                % endif
                            </td>
                            <td onclick="${onclick}" class="rowlink">
                                ${company.email}
                            </td>
                            <td onclick="${onclick}" class="rowlink">
                                <ul>
                                    % for employee in company.employees:
                                        <li>
                                        <a href="${request.route_path('user', id=employee.id)}">
                                            ${api.format_account(employee)}
                                            </a>
                                        </li>
                                    % endfor
                                </ul>
                            </td>
                            <td class='actions'>
                                ${table_btn(url, u"Voir", u"Modifier l'entreprise", icon='glyphicon glyphicon-search')}
                                <% url = request.route_path('company', id=company.id, _query=dict(action='edit')) %>
                                ${table_btn(url, u"Modifier", u"Modifier l'entreprise", icon='glyphicon glyphicon-pencil')}

                                % if len(company.employees) > 1:
                                    <% url = request.route_path('company', id=company.id, _query=dict(action="remove", uid=user.id)) %>
                                    <% msg = u"{0} n\\'aura plus accès aux données de l\\'entreprise {1}. Êtes-vous sûr de vouloir continuer ?".format(api.format_account(user), company.name) %>

                                    ${table_btn(url, \
                                    u"Enlever",
                                    u"Enlever cet utilisateur de cette entreprise",
                                    onclick="return confirm('%s');" % msg,
                                    icon="link",
                                    css_class="btn-warning")}

                                % endif

                                % if company.enabled():
                                    <% url = request.route_path('company', id=company.id, _query=dict(action="disable")) %>
                                    <% msg = u"Cette entreprise n\\'apparaîtra plus dans les listings de factures. Êtes-vous sûr de vouloir continuer ?" %>
                                    ${table_btn(url, \
                                    u"Désactiver", \
                                    u"désactiver l'entreprise", \
                                    icon='glyphicon glyphicon-book', \
                                    onclick="return confirm('%s');" % msg,
                                    css_class="btn-danger")}
                                % else:
                                    <% url = request.route_path('company', id=company.id, _query=dict(action="enable")) %>
                                    ${table_btn(url, \
                                    u"Activer", \
                                    u"Activer l'entreprise", \
                                    icon='glyphicon glyphicon-book', \
                                    css_class="btn-success")}
                                % endif
                            </td>
                        </tr>
                    % endfor
                </tbody>
            </table>
            <a href="${request.route_path('companies', _query=dict(action='add', user_id=user.id))}"
                class='btn btn-info'>
                <i class="glyphicon glyphicon-plus"></i>
                Associer à une nouvelle entreprise
            </a>
            <a href="${request.route_path('userdata', id=request.context.id, _query=dict(action='associate'))}"
                class='btn btn-info'>
                <i class="glyphicon glyphicon-link"></i>
                Associer à une entreprise existante
            </a>
        </div>

        <div role="tabpanel" class="tab-pane row" id="tab-accompagnement">
            <% url = request.route_path('activities', _query={'action':'new', 'user_id': user.id}) %>
                <a href='${url}' class='btn btn-info'>
                    <i class="glyphicon glyphicon-plus"></i>
                    Prendre un rendez-vous
                </a>
        </div>
    % endif
</div>
</div>
</div>
</%block>
<%block name="footerjs">
setAuthCheckBeforeSubmit('#userdatas_edit');
% if request.context.__name__ == 'userdatas':
    disableForm("#userdatas_edit");
% endif
</%block>
