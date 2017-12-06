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
<%namespace file="autonomie:templates/base/utils.mako" import="format_text" />
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
<html>
    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="shortcut icon" href="" type="image/x-icon" />
        <meta name="description" comment="">
        <meta name="KEYWORDS" CONTENT="">
        <meta NAME="ROBOTS" CONTENT="INDEX,FOLLOW,ALL">
        <link href="${request.static_url('autonomie:static/css/pdf.css', _app_url='')}" rel="stylesheet"  type="text/css" />
        <% config = request.config %>
        <style>
                    <%
if config.has_key('activity_footer'):
    footer_height = len(config.get('activity_footer').splitlines())
    footer_height = footer_height * 0.8 + 2
else:
    footer_height = 2
%>

            @page {
                size: a4 portrait;
                @frame content_frame {
                    margin: 1cm;
                    border: 0pt solid white;
                    margin-bottom: ${footer_height}cm;
                }
                @frame footer_frame {
                    -pdf-frame-content: footer_content;
                    bottom: 0cm;
                    margin-left: 1cm;
                    margin-right: 1cm;
                    height: ${footer_height}cm;
                    border: 0pt solid white;
                    vertical-align:bottom;
                }
            }
        </style>
    </head>
    <body>
        <img src="/public/activity_header_img.png" />

        <div class='text12'><b>Date : </b> le ${api.format_date(activity.datetime)}</div>
        <div class='text12'><b>Durée : </b> ${activity.duration}</div>

        <center>
            <div class='text12 upper'><b>${activity.action_label}</b></div>
            <div class='text9'>${activity.subaction_label}</div>
            <br />
            <div class='text14'><b>${activity.type_object.label}</b></div>

        </center>
        <div class='text12'>Conseiller : ${', '.join([api.format_account(conseiller) for conseiller in activity.conseillers])}</div>
        <% companies = set() %>
        <div class='text12'>Participants :
            % for user in activity.sorted_participants:
                ${api.format_account(user)} ( ${"'".join([c.name for c in user.companies])} )
                % if not loop.last:
                    ,
                % endif
            % endfor
        </div>
        <% options = (\
            (u"Objectifs du rendez-vous", "objectifs"), \
            (u"Points abordés", "point"),\
            (u"Plan d'action et préconisations", "action" ),\
            (u"Documents produits", "documents" ),\
            )
        %>
        % for label, attr in options:
            <div class='text12 activity-title' >${label}</div>
            <div class="activity-content">
                % if getattr(activity, attr) is not None:
                ${api.clean_html(getattr(activity, attr))|n}
                % endif
            </div>
        % endfor
        <br />
        <br />
        <table>
        <tr>
            <td style="padding-bottom:50px; width:50%">
                <b>Signature Conseiller</b>
            </td>
            <td style="padding-bottom:50px; width:50%">
                <b>Signature Participant</b>
            </td>
            </tr>
            </table>

      <div id="footer_content">
        <img src="/public/activity_footer_img.png" />
        <div class='row' id='footer'>
            % if config.has_key('activity_footer'):
                ${format_text(config.get('activity_footer'))}
            % endif
        </div>
    </div>
</body>
</html>
