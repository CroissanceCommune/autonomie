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
% if info_message != UNDEFINED:
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Message
    </div>
    <div class='panel-body'>
        <div class="alert alert-success">
            ${info_message|n}
        </div>
    </div
</div>
% endif
% if warn_message != UNDEFINED:
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Message
    </div>
    <div class='panel-body'>
        <div class="alert alert-warn">
            <i class='fa fa-warning'></i>
            ${warn_message|n}
        </div>
    </div>
</div>
% endif
% if help_message != UNDEFINED:
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Message
    </div>
    <div class='panel-body'>
        <div class='alert alert-info'>
        <i class='fa fa-question-circle fa-2x'></i>
        ${help_message|n}
        </div>
    </div>
</div>
% endif
<div class="col-md-12">
    <h3>${title}</h3>
    ${form|n}
</div>
</%block>
