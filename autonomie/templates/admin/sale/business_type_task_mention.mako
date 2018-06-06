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
                            <tr>
                            <th>Mentions</th>
                            <th>Devis</th>
                            <th>Factures</th>
                            <th>Avoirs</th>
                            </tr>
                        </thead>
                        <tbody>
                        % for mention in mentions:
                            <% mention_items = items.get(mention.id, {}) %>
                            <tr>
                            <td><b>${mention.label}</b></td>
                            <% btype_items = mention_items.get(business_type.id, {}) %>
                            % for doctype in ('estimation', 'invoice', 'cancelinvoice'):
                            <% mandatory = btype_items.get(doctype, -1) %>
                            <% tag_id = "mandatory_%s_%s_%s" % (mention.id, business_type.id, doctype) %>
                            <td>
                            <input type='hidden' name='__start__' value='item:mapping' />
                                <input type='hidden' name='task_mention_id' value='${mention.id}' />
                                <input type='hidden' name='business_type_id' value='${business_type.id}'/>
                                <input type='hidden' name='doctype' value='${doctype}' />
                                 <input type='hidden' name='__start__' value='mandatory:rename'>
                                <div class='radio'>
                                <label>
                                    <input type='radio' name='${tag_id}' value=''
                                    % if mandatory == -1:
                                    checked
                                    % endif
                                    />&nbsp;Non utilisée
                                </label>
                                </div>
                                <div class='radio'>
                                <label>
                                    <input type='radio' name='${tag_id}' value='false'
                                    % if not mandatory:
                                    checked
                                    % endif
                                    />&nbsp;Facultative
                                </label>
                                </div>
                                <div class='radio'>
                                <label>
                                    <input type='radio' name='${tag_id}' value='true'
                                    % if mandatory == True:
                                    checked
                                    % endif
                                    />&nbsp;Obligatoire
                                </label>
                                </div>
                                 <input type='hidden' name='__end__' value='mandatory:rename'>
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
