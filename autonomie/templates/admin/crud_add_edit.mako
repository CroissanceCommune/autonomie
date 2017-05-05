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
    :param str form: Html formatted form

    :param str warn_msg: optionnal warning message
    :param str help_msg: optionnal help message
</%doc>
<%inherit file="/admin/index.mako"></%inherit>
<%block name='content'>
<h3 class='text-center'>${title}</h3>
    <hr>
    <div class='row'>
        <div class='col-md-8 col-md-offset-2'>
            % if warn_msg is not UNDEFINED:
                <div class="alert alert-warning">
                    <i class='glyphicon glyphicon-warning-sign'></i>
                    ${warn_msg|n}
                </div>
            % endif
            % if help_msg is not UNDEFINED:
                <div class="alert alert-info">
                    <i class='glyphicon glyphicon-question-sign'></i>
                    ${help_msg|n}
                </div>
            % endif
            ${form|n}
        </div>
    </div>
</%block>
