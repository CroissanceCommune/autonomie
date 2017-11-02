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
    <!--[if lt IE 9]>
    <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <%block name="headjs" />

    <%block name="css" />
    <link  rel="stylesheet" type="text/css" href="${request.static_url('autonomie:static/css/print.css')}" media="print" />
  </head>
  <body
      class="${request.matched_route.name}-view"
      >
    % if 'popup' not in request.GET:
        ${request.layout_manager.render_panel('menu')}
        ${request.layout_manager.render_panel('submenu')}
        <%block name="headtitle">
        % if title is not UNDEFINED:
        <div class='pagetitle visible-lg hidden-print hidden-sm'>
          <h2 >
            ${title}
          </h2>
        </div>
        % endif
        </%block>
        % if not request.actionmenu.void():
        <div class='hidden-print'>
            <div class='subnav'>
                ${request.actionmenu.render(request)|n}
            </div>
        </div>
        % endif
    % endif

    <%block name='afteractionmenu' />

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
          <%block name='beforecontent' />
          <%block name='content' />
          % if request.popups is not UNDEFINED:
              % for name, popup in request.popups.items():
                  <div id="${name}" style="display:none;" class="hidden-print">
                    ${popup.html|n}
                  </div>
            % endfor
          % endif
        </div>
    </div>
    <div id='loading-box' style='display:none'>
        <i class="fa fa-circle-o-notch fa-spin"></i>
    </div>
    <div id='login_form' style='display:none'></div>
    <footer id='page-footer-block'>
    Autonomie v${layout.autonomie_version}
    <%block name='footer' />
    </footer>
    <script type='text/javascript'>
        $( function() {
            console.log("In the js func");
            % if request.popups is not UNDEFINED:
            % for name, popup in request.popups.items():
                setPopUp("${name}", "${popup.title}");
            % endfor
            % endif
            var company_select_tag = $('#company-select-menu');
            if (!_.isUndefined(company_select_tag)){
                $('#company-select-menu').select2();
                $('#company-select-menu').change(
                  function(){window.location = $(this).val();}
                );
            }
        });
      <%block name='footerjs' />
    </script>
  </body>
</html>
