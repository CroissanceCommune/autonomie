<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<%namespace file="/base/utils.mako" import="searchform"/>
<html>
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
    <%block name="header">
    <title>${title}</title>
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

    <link href="${request.static_url('autonomie:static/css/default.css')}" rel="stylesheet"  type="text/css" />
    <link href="${request.static_url('autonomie:static/css/shadow.css')}" rel="stylesheet"  type="text/css" />
    <link href="${request.static_url('deform:static/css/form.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform:static/css/beautify.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform_bootstrap:static/jquery_chosen/chosen.css')}" rel="stylesheet"  type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('deform_bootstrap:static/chosen_bootstrap.css')}" rel="stylesheet"  type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('autonomie:static/css/theme/jquery-ui-1.8.16.custom.css')}" type="text/css" rel="stylesheet"/>
    ##<link href="${request.static_url('autonomie:static/css/bootstrap-responsive.css')}" type="text/css" rel="stylesheet"/>
    <link href="${request.static_url('autonomie:static/css/main.css')}" rel="stylesheet"  type="text/css" />
    <%block name="css" />
  </head>
  <body>
    <header>
            ${request.layout_manager.render_panel('menu')}
            ${request.layout_manager.render_panel('submenu')}
    </header>
    <%block name="headtitle">
    <div class='pagetitle visible-desktop hidden-tablet'>
      <h2 >
        ${title}
      </h2>
    </div>
    </%block>
    <div class='container'>
      <div class='subnav'>
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
        <div class='row'>
          <div class='span6 offset3'>
            <div class="alert alert-success">
              <button class="close" data-dismiss="alert" type="button">×</button>
              ${message|n}
            </div>
          </div>
        </div>
      % endfor
      % for message in request.session.pop_flash(queue="error"):
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
      % if request.popups is not UNDEFINED:
          % for name, popup in request.popups.items():
              <div id="${name}" style="display:none;">
                ${popup.html|n}
              </div>
        % endfor
      % endif
    </div>
    <script type='text/javascript'>
      <%block name='footerjs' />
      $('#company-select-menu').change(function(){window.location = $(this).val();});
      % if request.popups is not UNDEFINED:
        $( function() {
          % for name, popup in request.popups.items():
            setPopUp("${name}", "${popup.title}");
          % endfor
        });
      % endif
    </script>
  </body>
</html>
