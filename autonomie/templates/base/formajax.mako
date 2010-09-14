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
% if not form is UNDEFINED:
    ${form|n}
    <script>
        ## fix a deform bug : when sending a form through ajax response, the
        ## 'ajaxification' of the form is not fired in a full html page, this
        ## firing is ensured by the deform.js script, here we force this
        deform.loaded = false;
        $(function(){
            deform.load()
        });
    </script>
% endif
% if not message is UNDEFINED:
    <div>${message|n}</div>
% endif
