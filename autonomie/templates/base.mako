<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%namespace file="/base/utils.mako" import="searchform"/>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <%block name="header">
    <title>${title}</title>
    <link rel="shortcut icon" href="" type="image/x-icon" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" comment="">
    <meta name="KEYWORDS" CONTENT="">
    <meta NAME="ROBOTS" CONTENT="INDEX,FOLLOW,ALL">
    </%block>
    <!--[if lt IE 9]>
    <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/jquery-1.7.1.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform:static/scripts/jquery.form.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/jquery-ui-1.8.18.custom.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform:static/scripts/deform.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/deform_bootstrap.js')}"></script>
    ##    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/bootstrap.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('autonomie:static/js/bootstrap.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/bootstrap-typeahead.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/jquery_chosen/chosen.jquery.js')}"></script>
    <script type="text/javascript" src="${request.static_url('autonomie:static/js/jquery.ui.datepicker-fr.js')}"></script>
    <%block name="headjs" />

    <link href="${request.static_url('autonomie:static/css/default.css')}" rel="stylesheet"  type="text/css" />
    <link href="${request.static_url('autonomie:static/css/shadow.css')}" rel="stylesheet"  type="text/css" />
    <link href="${request.static_url('deform:static/css/form.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform:static/css/beautify.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform_bootstrap:static/jquery_chosen/chosen.css')}" rel="stylesheet"  type="text/css" rel="stylesheet"/>
##    <link href="${request.static_url('deform_bootstrap:static/deform_bootstrap.css')}" rel="stylesheet"  type="text/css" rel="stylesheet"/>
<link href="${request.static_url('autonomie:static/css/bootstrap.min.css')}" rel="stylesheet"  type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform_bootstrap:static/chosen_bootstrap.css')}" rel="stylesheet"  type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('autonomie:static/css/theme/jquery-ui-1.8.16.custom.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('autonomie:static/css/bootstrap-responsive.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('autonomie:static/css/main.css')}" rel="stylesheet"  type="text/css" />
    <%block name="css" />
  </head>
  <body>
    <header>
    <div class="navbar">
      <div class="navbar-inner">
        <div class="container">
          <a class="brand" href='/'>Autonomie</a>
          <a class="btn btn-navbar" data-target=".menu" data-toggle="collapse">
            >>>
          </a>
          <div class="nav-collapse menu">
            % if menu is not UNDEFINED and menu:
              ${menu.render(request)|n}
            % endif
            %if request.user:
              <div class="btn-group pull-right">
                <a class="btn dropdown-toggle" href="#" data-toggle="dropdown">
                  <i class="icon-user"></i>
                  ${request.user.lastname} ${request.user.firstname}
                  <span class="caret"></span>
                </a>

                <ul class='dropdown-menu'>
                <li>
                  <a href="${request.route_path('account')}">
                    <span class='ui-icon ui-icon-gear'></span>
                    Mon compte
                  </a>
                  </li>
                  <li>
                  <a href="${request.route_path('holliday')}">
                    <span class='icon-plane'></span>
                    Mes congés
                    </a>
                  </li>
                  <li class="divider"></li>
                <li>
                <a href="/logout">
                  <span class='ui-icon ui-icon-close'></span>
                  Déconnexion</a>
                </li>
              </ul>
            % endif
          </div>
        </div>
      </div>
    </div>
    </div>
    % if submenu is not UNDEFINED and submenu:
    <div class="navbar">
      <div class="navbar-inner">
        <div class="container">
          <a class="btn btn-navbar" data-target=".submenu" data-toggle="collapse">
            >>>
          </a>
          <div class='nav-collapse submenu'>
        ${submenu.render(request)|n}
      </div>
      </div>
    </div>
    </div>
    % endif
    </header>
    <%block name="headtitle">
    <div class='pagetitle visible-desktop hidden-tablet'>
      <h2 >${title}</h2>
    </div>
    </%block>
    <div class='container'>
      <div class='subnav'>
        <%block name="actionmenu">
          % if action_menu is not UNDEFINED:
            ${action_menu.render(request)|n}
          % endif
        </%block>
      </div>
      <%block name="breadcrumb_block">
      % if breadcrumb is not UNDEFINED:
        <ul class="breadcrumb">
          % for link in breadcrumb.links:
            % if link['active']:
              <li class='active'>
              ${link['label']}
            % else:
              <li>
              <a href="${link['url']}">${link['label']}<a>
                  ${link['label']}
                  <span class='delimiter'>></span>
                % endif
                </li>
              % endfor
            </ul>
          % endif
          </%block>
          <%block name='pop_message'>
          % for num, message in enumerate(request.session.pop_flash(queue="main")):
            <div class='row'>
              <div class='span6 offset3'>
            <div class="alert alert-success">
              <button class="close" data-dismiss="alert" type="button">×</button>
               ${message|n}
             </div>
              </div>
              </div>
          % endfor
          % for num, message in enumerate(request.session.pop_flash(queue="error")):
            <div class='row'>
              <div class='span6 offset3'>
              <div class="alert alert-error">
                <button class="close" data-dismiss="alert" type="button">×</button>
                ${message|n}
              </div>
              </div>
              </div>
          % endfor
          </%block>
          <%block name='content' />
     </div>
        <script type='text/javascript'>
          <%block name='footerjs' />
          $('#company-select-menu').change(function(){window.location = $(this).val();});
        </script>
      </body>
    </html>
