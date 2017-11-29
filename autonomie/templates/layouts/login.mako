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
<!DOCTYPE html>
<html lang="fr">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <%block name="header">
    % if not title is UNDEFINED:
    <title>${title}</title>
    % endif
    <link rel="shortcut icon" href="${request.static_url('autonomie:static/img/favicon.ico')}" type="image/x-icon" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" comment="">
    <meta name="KEYWORDS" CONTENT="">
    <meta NAME="ROBOTS" CONTENT="INDEX,FOLLOW,ALL">
    </%block>
  </head>
  <body
      class="${request.matched_route.name}-view"
      >
    <div class="page-content-wrapper">
        <div class="container-fluid">
          <%block name='pop_message'>
          % for message in request.session.pop_flash(queue=""):
            % if message is not None:
              <div class='row hidden-print'>
              <div class='col-md-6 col-md-offset-3'>
                <div class="alert alert-success">
                  <button class="close" data-dismiss="alert" type="button">×</button>
                  ${api.clean_html(message)|n}
                </div>
              </div>
            </div>
            % endif
          % endfor
          % for message in request.session.pop_flash(queue="error"):
            % if message is not None:
              <div class='row hidden-print'>
              <div class='col-md-6 col-md-offset-3'>
                <div class="alert alert-danger">
                  <button class="close" data-dismiss="alert" type="button">×</button>
                  <i class='fa fa-warning'></i>
                  ${api.clean_html(message)|n}
                </div>
              </div>
            </div>
            % endif
          % endfor
          </%block>
          <%block name='content' />
        </div>
    </div>
    <footer id='page-footer-block'>
        Autonomie v${layout.autonomie_version}
        <%block name='footer' />
    </footer>
  </body>
</html>
