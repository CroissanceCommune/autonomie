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
<%namespace file="/base/utils.mako" import="dropdown_item"/>
<%block name='afteradminmenu'>
</%block>
<%block name='content'>
<div class='row'>
    <div class='col-xs-12'>
        <div class='panel panel-default'>
            <div class='panel-heading'>
            </div>
            <div class='panel-body'>
                <form method='POST'
                    class="deform  deform" accept-charset="utf-8"
                    enctype="multipart/form-data">
                    <input type='hidden' name='__start__' value='items:sequence' />
                    % for business_type in business_types:
                    <h2 class='text-center'>${business_type.label}</h2>
                    <table class='table table-bordered table-striped'>
                        <thead>
                            <th>Types de fichier</th>
                            % if business_type.name != 'default':
                                <th>Affaire</th>
                            % endif
                            <th>Devis</th>
                            <th>Factures</th>
                            <th>Avoirs</th>
                            </tr>
                        </thead>
                        <tbody>
                        % for file_type in file_types:
                            <% file_type_items = items.get(file_type.id, {}) %>
                            <tr>
                            <td><b>${file_type.label}</b></td>
                                <% btype_items = file_type_items.get(business_type.id, {}) %>
                                % for doctype in ('business', 'estimation', 'invoice', 'cancelinvoice'):
                                    % if business_type.name == 'default' and doctype == 'business':
                                    <% continue %>
                                    % endif
                                <% requirement_type = btype_items.get(doctype, {}).get('requirement_type', -1) %>
                                <% validation = btype_items.get(doctype, {}).get('validation') %>
                                <% tag_id = "requirement_type_%s_%s_%s" % (file_type.id, business_type.id, doctype) %>
                                <td>
                                <input type='hidden' name='__start__' value='item:mapping' />
                                    <input type='hidden' name='file_type_id' value='${file_type.id}' />
                                    <input type='hidden' name='business_type_id' value='${business_type.id}'/>
                                    <input type='hidden' name='doctype' value='${doctype}' />
                                     <input type='hidden' name='__start__' value='requirement_type:rename'>
                                     <label for='${tag_id}'>Ce type de fichier : </label>
                                    <div class='radio'>
                                    <label>
                                        <input type='radio' name='${tag_id}' value=''
                                        % if requirement_type == -1:
                                        checked
                                        % endif
                                        />&nbsp;N'est pas proposé dans le formulaire de dépot de fichier
                                    </label>
                                    </div>
                                    % for option, label in (\
                                        ('optionnal', u'Est Proposé dans le formulaire de dépot de fichier'), \
                                        ('recommended', u'Recommandé'), \
                                        ('mandatory', u'Requis systématiquement pour la validation'), \
                                        ('business_mandatory', u"Globalement requis dans le/la {0} pour la validation".format(business_type.label)), \
                                        ('project_mandatory', u"Globalement requis dans le projet pour la validation")):
                                        % if doctype == 'business' and option == 'mandatory':
                                        <% continue %>
                                        % endif

                                        <div class='radio'>
                                        <label>
                                            <input type='radio' name='${tag_id}' value='${option}'
                                            % if requirement_type == option:
                                            checked
                                            % endif
                                            />&nbsp;${label}
                                        </label>
                                        </div>
                                    % endfor
                                    <input type='hidden' name='__end__' value='requirement_type:rename'>
                                    <hr />
                                    <div class="checkbox">
                                    <label>
                                      <input type="checkbox" name="validation"
                                      % if validation:
                                      checked
                                      % endif
                                      >&nbsp;Ce type de fichier exige une validation par l'équipe d'appui ?
                                    </label>
                                    </div>
                                <input type='hidden' name='__end__' value='item:mapping' />
                                </td>
                            % endfor
                            </tr>
                            % endfor
                        </tbody>
                    </table>
                    <hr />
                    % endfor
                    <input type='hidden' name='__end__' value='items:sequence' />
                    <div class='form-actions'>
                       <button id="deformsubmit" class="btn btn-primary " value="submit" type="submit" name="submit"> Enregistrer </button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</div>
</%block>
