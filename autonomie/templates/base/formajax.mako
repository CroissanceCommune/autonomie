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
% if not message is UNDEFINED:
    <div class='text-center'>
        <div id='msg-div' class="alert alert-success" tabindex='1'>
          <button class="close" data-dismiss="alert" type="button">×</button>
          ${api.clean_html(message)|n}
        </div>
      </div>
% endif
% if not form is UNDEFINED:
    ${form|n}
% endif
<script type='text/javascript'>
    $('#msg-div').focus();
</script>
