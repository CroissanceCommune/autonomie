# -*- coding: utf-8 -*-
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
    Static div container used to display the list of tva amounts
</%doc>
<%def name='esc(datas)'><%text>${</%text>${datas}<%text>}</%text>\
</%def>
<script id="tvaTmpl" type="text/x-jquery-tmpl">
<div class='control-label'>
TVA à ${esc('label')}
</div>
<div class='controls'>
    <div class='input'>${esc('value')}</div>
</div>
</script>
<div class='control-group estimationamounts offset8' id='total_ht'>
    <div class='control-label'>
        Total HT
    </div>
    <div class='controls'>
        <div class='input'></div>
    </div>
</div>
<div class='control-group estimationamounts offset8' id='tvalist'>
</div>
<div class='control-group estimationamounts offset8' id='total_ttc'>
    <div class='control-label'>
        Total TTC
    </div>
    <div class='controls'>
        <div class='input'></div>
    </div>
</div>
