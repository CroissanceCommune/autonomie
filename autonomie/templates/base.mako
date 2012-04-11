<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <%block name="header">
    <title>${title}</title>
    <link rel="shortcut icon" href="" type="image/x-icon" />
    <meta name="description" comment="">
    <meta name="KEYWORDS" CONTENT="">
    <meta NAME="ROBOTS" CONTENT="INDEX,FOLLOW,ALL">
    </%block>
    <!--[if lt IE 9]>
    <script src="http://html5shim.googlecode.com/svn/trunk/html5.js"></script>
    <![endif]-->

    <!--    <script type="text/javascript" src="${request.static_url('autonomie:static/js/jquery-1.7.2.min.js')}"></script>-->
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/jquery-1.7.1.min.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform:static/scripts/jquery.form.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/jquery-ui-1.8.18.custom.min.js')}"></script>
    <!--    <script type="text/javascript" src="${request.static_url('deform:static/scripts/jquery-ui-timepicker-addon.js')}"></script>-->
    <script type="text/javascript" src="${request.static_url('deform:static/scripts/deform.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/deform_bootstrap.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/bootstrap.min.js')}"></script>
    <!--    <script type="text/javascript" src="${request.static_url('autonomie:static/js/bootstrap-datepicker.js')}"></script>-->
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/bootstrap-typeahead.js')}"></script>
    <script type="text/javascript" src="${request.static_url('deform_bootstrap:static/jquery_chosen/chosen.jquery.js')}"></script>
    <script type="text/javascript" src="${request.static_url('autonomie:static/js/jquery.ui.datepicker-fr.js')}"></script>
    <%block name="headjs" />

    <link href="${request.static_url('autonomie:static/css/default.css')}" rel="stylesheet"  type="text/css" />
    <link href="${request.static_url('deform:static/css/form.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform:static/css/beautify.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform_bootstrap:static/deform_bootstrap.css')}" rel="stylesheet"  type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform_bootstrap:static/jquery_chosen/chosen.css')}" rel="stylesheet"  type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform_bootstrap:static/chosen_bootstrap.css')}" rel="stylesheet"  type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('autonomie:static/css/theme/jquery-ui-1.8.16.custom.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('autonomie:static/css/main.css')}" rel="stylesheet"  type="text/css" />
    <%block name="css" />
  </head>
  <body>
    <header>
    <div class="navbar">
      <div class="navbar-inner">
          <a class="brand" href='/'>Autonomie</a>
          <div class="container">
            <div class="nav-collapse">
        % if menu is not UNDEFINED:
              <ul class='nav'>
                % for item in menu:
                  <li>
                  <a href="${item['url']}">${item['label']}</a>
                  </li>
                  <li class='divider-vertical'>
                % endfor
              </ul>
        % endif
        %if request.session.has_key('user'):
        <ul class='nav pull-right' id='logout_link'>
          <li>
          <a href="/account">${request.session['user'].lastname} ${request.session['user'].firstname}</a>
            </li>
            <li>
            <a href="/logout">Déconnexion</a>
            </li>
          </ul>
        % endif
            </div>
          </div>
      </div>
    </div>
    </header>
    <%block name="headtitle">
    <div id='pagetitle' class='well'>
        <h2>${title}</h2>
        <%block name="actionmenu" />
      </div>
    </%block>
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
      <a href="#" onclick="$('#main_message_${num}').hide();" id="main_message_${num}">
        <div class="message ui-widget">
        <div class="ui-state-highlight ui-corner-all">
          <p>
            <span class="ui-icon ui-icon-check">
            </span>
            ${message|n}
          </p>
        </div>
      </div>
      </a>
    % endfor
    </%block>
        <%block name='content' />
        <script type='text/javascript'>
          <%block name='footerjs' />
          </script>
  </body>
</html>
