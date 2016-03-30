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
<%namespace file="/base/utils.mako" import="searchform"/>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <%block name="header">
    <title>${title}</title>
    <link rel="shortcut icon" href="${request.static_url('autonomie:static/img/favicon.ico')}" type="image/x-icon" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" comment="">
    <meta name="KEYWORDS" CONTENT="">
    <meta NAME="ROBOTS" CONTENT="INDEX,FOLLOW,ALL">
    <link  rel="stylesheet" type="text/css" href="${request.static_url('autonomie:static/css/print.css')}" media="print" />
    </%block>
    <!--[if lt IE 9]>
    <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <%block name="headjs" />

    <%block name="css" />
  </head>
  <body>
    ${request.layout_manager.render_panel('menu')}
    ${request.layout_manager.render_panel('submenu')}
    <%block name="headtitle">
    <div class='pagetitle visible-lg hidden-sm hidden-print'>
      <h2 >
        ${title}
      </h2>
    </div>
    </%block>
    <div class="container-fluid">
        <div class='subnav hidden-print'>
        <%block name="actionmenu">
        % if action_menu is not UNDEFINED and not action_menu.void():
            ${action_menu.render(request)|n}
        % elif not request.actionmenu.void():
            ${request.actionmenu.render(request)|n}
        % endif
        </%block>
      </div>
      <%block name='pop_message'>
      % for message in request.session.pop_flash(queue=""):
          <div class='row hidden-print'>
          <div class='col-md-6 col-md-offset-3'>
            <div class="alert alert-success">
              <button class="close" data-dismiss="alert" type="button">×</button>
              ${api.clean_html(message)|n}
            </div>
          </div>
        </div>
      % endfor
      % for message in request.session.pop_flash(queue="error"):
          <div class='row hidden-print'>
          <div class='col-md-6 col-md-offset-3'>
            <div class="alert alert-danger">
              <button class="close" data-dismiss="alert" type="button">×</button>
              <i class='fa fa-warning'></i>
              ${api.clean_html(message)|n}
            </div>
          </div>
        </div>
      % endfor
      </%block>
      <%block name='content' />
      % if request.popups is not UNDEFINED:
          % for name, popup in request.popups.items():
              <div id="${name}" style="display:none;" class="hidden-print">
                ${popup.html|n}
              </div>
        % endfor
      % endif
    </div>
    <div id='loading-box'>
        <i class="fa fa-spinner fa-spin"></i>
    </div>
    <div id='login_form' style='display:none'></div>
    <script type='text/javascript'>
      $('#company-select-menu').change(function(){window.location = $(this).val();});
      % if request.popups is not UNDEFINED:
        $( function() {
          % for name, popup in request.popups.items():
            setPopUp("${name}", "${popup.title}");
          % endfor
        });
      % endif
      <%block name='footerjs' />
    </script>
  </body>
</html>
