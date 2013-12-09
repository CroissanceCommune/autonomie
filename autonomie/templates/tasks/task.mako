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

<%doc>
    Base template for task rendering
</%doc>
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="shortcut icon" href="" type="image/x-icon" />
        <meta name="description" comment="">
        <meta name="KEYWORDS" CONTENT="">
        <meta NAME="ROBOTS" CONTENT="INDEX,FOLLOW,ALL">
        <link href="${request.static_url('autonomie:static/css/pdf.css', _app_url='')}" rel="stylesheet"  type="text/css" />
        <% task = tasks[0] %>
        <style>
            % if task.type_ == 'estimation':
                <% watermark = 'watermark_estimation.jpg' %>
            % else:
                <% watermark = 'watermark_invoice.jpg' %>
            % endif
            @page {
                size: a4 portrait;
                margin:1cm;
                margin-bottom:3.5cm;
                % if not task.has_been_validated() and not task.is_cancelled():
                    background-image: url("${request.static_url('autonomie:static/{0}'.format(watermark), _app_url='')}");
                % endif
                @frame footer {
                    -pdf-frame-content: footer;
                    bottom: 0cm;
                    margin-left: 1cm;
                    margin-right: 1cm;
                    % if hasattr(task, "course") and task.course == 1 and request.config.has_key('coop_pdffootercourse'):
                        height:4cm;
                    % else:
                        height:3cm;
                    % endif
                }
            }
        </style>
    </head>
    <body>
        % for task in tasks:
            ${request.layout_manager.render_panel('{0}_html'.format(task.type_), task=task)}
            % if not loop.last:
                <pdf:nextpage />
            % endif
        % endfor
    </body>
</html>
