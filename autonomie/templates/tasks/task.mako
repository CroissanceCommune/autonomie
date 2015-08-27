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
            % if task.type_ == 'estimation':
                <% watermark = 'watermark_estimation.jpg' %>
            % else:
                <% watermark = 'watermark_invoice.jpg' %>
            % endif

            <%
course_footer_height = common_footer_height = 0
if request.config.has_key('coop_pdffootertext'):
    common_footer_height = len(config.get('coop_pdffootertext').splitlines())
if request.config.has_key('coop_pdffootercourse'):
    course_footer_height = common_footer_height + len(config.get('coop_pdffootercourse').splitlines())
course_footer_height *= 0.8
common_footer_height *= 0.8
%>
<% start_with_course = getattr(tasks[0], 'course', 0) == 1 %>

        <style>
            @page {
                size: a4 portrait;
                % if not task.has_been_validated() and not task.is_cancelled():
                    background-image: url("${request.static_url('autonomie:static/{0}'.format(watermark), _app_url='')}");
                % endif
                @frame content_frame {
                    margin: 1cm;
                    margin-top: 1.5cm;
                    margin-bottom: 3.3cm;
                    border: 0pt solid white;
                }
                @frame footer {
                    % if start_with_course:
                        -pdf-frame-content: coursefooter;
                        height: ${course_footer_height}cm;
                    %else:
                        -pdf-frame-content: commonfooter;
                        height: ${common_footer_height}cm;
                    % endif
                    bottom: 0.5cm;
                    margin-left: 1cm;
                    margin-right: 1cm;
                    border: 0pt solid white;
                }
                @frame paging{
                    -pdf-frame-content: page-number;
                    bottom: 0cm;
                    height: 0.5cm;
                    font-size: 0.3cm;
                    left: 19cm;

                }
            }
            @page alternate {
                size: a4 portrait;
                % if not task.has_been_validated() and not task.is_cancelled():
                    background-image: url("${request.static_url('autonomie:static/{0}'.format(watermark), _app_url='')}");
                % endif
                @frame content_frame {
                    margin: 1cm;
                    margin-bottom: 3.8cm;
                    border: 0pt solid white;
                }
                @frame footer {
                    % if start_with_course:
                        -pdf-frame-content: commonfooter;
                        height: ${common_footer_height}cm;
                    %else:
                        -pdf-frame-content: coursefooter;
                        height: ${course_footer_height}cm;
                    % endif
                    bottom: 0cm;
                    margin-left: 1cm;
                    margin-right: 1cm;
                    border: 0pt solid white;
                }
                @frame paging{
                    -pdf-frame-content: page-number;
                    position: relative;
                    height: 0.5cm;
                    top: 1cm;
                    left: 19cm;
                }
            }
        </style>
    </head>
    <body>
        % for task in tasks:

            ${request.layout_manager.render_panel('{0}_html'.format(task.type_), task=task, bulk=bulk)}
            % if not loop.last:
                % if getattr(tasks[loop.index +1], 'course', 0) and not start_with_course:
                    <pdf:nexttemplate name="alternate"/>
                    <pdf:nextpage />
                % elif not getattr(tasks[loop.index +1], 'course', 0) and start_with_course:
                    <pdf:nexttemplate name="alternate"/>
                    <pdf:nextpage />
                %else:
                    <pdf:nexttemplate loop.index=0 />
                    <pdf:nextpage />
                % endif
            % endif
        % endfor
    </body>
</html>
