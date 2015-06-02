<%doc>
    * Copyright (C) 2012-2015 Croissance Commune
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
<%inherit file="/base.mako"></%inherit>
<%block name="content">
<div class='row'>
    <div class='col-sm-8 col-sm-offset-2'>
        <form method='POST' enctype="multipart/form-data" accept-charset="utf-8">
            <div class="form-group">
                <label for="contractor_id">Entrepreneur à évaluer</label>
                % if not request.user.is_contractor():
                    <select name='contractor_id' class='form-control'>
                        % for id, label in user_options:
                            <option value='${id}'>${label}</option>
                        % endfor
                    </select>
                % endif
            </div>
            <div class='row'>
                <div class='col-sm-5'>
                    <div class="form-group">
                        <div>
                            <b>Choisissez une échéance</b>
                        </div>
                        <div class='btn-group' role='group'>
                            % for deadline in deadlines:
                                <button
                                    class='btn btn-default'
                                    type='submit'
                                    name='deadline'
                                    value='${deadline.id}'>
                                    ${deadline.label}
                                </button>
                            % endfor
                        </div>
                    </div>
                </div>
                <div class='col-sm-2'>
                    OU
                </div>
                <div class='col-sm-5'>
                    <div class="form-group">
                        <button
                            class='btn btn-success'
                            type='submit'
                            name='sheet'
                            value='radar'>
                            Voir l'évaluation globale
                        </button>
                    </div>
                </div>
            </div>
        </form>
    </div>
</div>
</%block>
<%block name="footerjs">
$('select[name=contractor_id]').select2();
</%block>
