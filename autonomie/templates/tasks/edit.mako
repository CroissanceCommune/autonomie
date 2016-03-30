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

<%doc>
    Template for estimation and invoice edition/creation
</%doc>
<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/utils.mako" import="esc"/>
<%namespace file="/base/utils.mako" import="address"/>
<%namespace file="/base/utils.mako" import="format_filelist" />


<%block name='css'>
<link href="${request.static_url('autonomie:static/css/task.css')}" rel="stylesheet"  type="text/css" />
</%block>

<%block name='content'>
% if request.context.type_ in ('cancelinvoice', 'estimation', 'invoice'):
     <div class='well'>
     <strong>Fichiers attachés à ce document</strong>
     ${format_filelist(request.context)}
     % if hasattr(request.context, 'estimation'):
         ${format_filelist(request.context.estimation)}
     % elif hasattr(request.context, 'invoice'):
            ${format_filelist(request.context.invoice)}
        % endif
    </div>
% endif
    <dl class="dl-horizontal">
        <dt>Prestataire</dt>
        <dd>${address(company, 'company')}</dd>
        </dl>
${form|n}
    <div style="display:none;" id='discount_popup'>
        <form id="discount_temp">
            <div class="form-group">
                <select id="discount_type_select" class='form-control'>
                    <option value="value" selected="true">En montant fixe</option>
                    <option value="percent">En pourcentage</option>
                </select>
            </div>
            <div class="form-group">
                <label for="discount_temp_description">Description</label>
                <textarea
                    class='form-control'
                    name="discount_temp_description"
                    rows="2">
                </textarea>
            </div>
            <div id='value_configuration'>
                <div class="form-group">
                    <label for="discount_temp_value">Montant</label>
                    <div class="input-group">
                        <input type="text" class='form-control' name="discount_temp_value">
                        <span class="input-group-addon">€</span>
                    </div>
                </div>
                <div class="form-group">
                    <label for="discount_temp_tva">Tva</label>
                    <select
                        name="discount_temp_tva"
                        class='form-control'
                        >
                        % for tva in tvas:
                            <option value="${tva.value}"
                            % if tva.default == 1:
                                selected="on"
                            % endif
                            >${tva.name}</option>
                        % endfor
                    </select>
                </div>
            </div>
            <div id='percent_configuration' style='display:none'>
                <div class="form-group">
                    <label for="discount_temp_percent">Pourcentage</label>
                    <div class="input-group">
                        <input type="text" name="discount_temp_percent" class='form-control'>
                        <span class="input-group-addon">%</span>
                    </div>
                </div>
            </div>
        </form>
        <div class='form-group'>
            <div class="text-right">
                <button
                    class='btn btn-success'
                    type='button'
                    onclick="discount.validate()"
                    >
                    Valider
                </button>
                <button
                    class='btn btn-danger'
                    type='button'
                    onclick="discount.close()"
                    >
                    Annuler
                </button>
            </div>
        </div>
    </div>
    <div id='catalog_popup'>
        <input class='form-control' type="text" name="catalog_search" placeholder="Nom ou référence"></input>
        <div class='tree-container' style='min-height: 250px;'>
        </div>
        <div class='form-group'>
            <div class="text-right">
                <button
                    class='btn btn-success'
                    type='button'
                    >
                    Insérer les éléments sélectionnés
                </button>
                <button
                    class='btn btn-danger'
                    type='button'
                    >
                    Annuler
                </button>
            </div>
        </div>
    </div>
    <script type='text/javascript'>
        $(function(){
            setPopUp('discount_popup', "Remise");
        });
    </script>
</%block>
<%block name="footerjs">
AppOptions = {};
AppOptions['loadurl'] = "${load_options_url}";
AppOptions['load_catalog_url'] = "${load_catalog_url}";
% if request.has_permission('admin_treasury'):
    AppOptions['manager'] = true;
% else:
    AppOptions['manager'] = false;
% endif
% if edit:
    AppOptions['edit'] = true;
% else:
    AppOptions['edit'] = false;
% endif
</%block>

