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

# -*- coding: utf-8 -*-
<%doc>
    input for estimation/invoice lines
</%doc>
<input class='input-mini' type='text' readonly='true' name="${field.name}" value="${cstruct}" ></input>
<script type="text/javascript">
    deform.addCallback(
        "${field.oid}",
        function (oid) {
            $('#' + oid + " input").blur(function(){
                var row = $(this).parent().parent();
                $(Facade).trigger("amountchange", row);
            }
        )});
</script>
