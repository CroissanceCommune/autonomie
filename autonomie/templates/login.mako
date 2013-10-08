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

<%inherit file="base.mako" ></%inherit>
<%block name='content'>
<style>
    .form-horizontal .form-actions{
        padding:15px 30px;
    }
    .form-actions .btn{
        width:100%;
        padding:5px;
    }
    .loginbox{
        border:1px solid #ddd;
        overflow:hidden;
        border-radius: 4px 4px 4px 4px;
        margin-top:10px;
        background-color:#efefef;
        padding-top:5px;
    }
    .loginbox legend{
        text-align:center;
    }
</style>
<div class='row'>
    <div class='span6 offset3 loginbox'>
        <div style='text-align:center;'>
            <img src="/assets/main/logo.png" alt='Votre CAE' />
        </div>
        ${html_form|n}
    </div>
</div>
</%block>
