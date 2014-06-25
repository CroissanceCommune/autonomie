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
    </head>
    <body>
        <% config = request.config %>

        <img src="/assets/main/accompagnement_header.png" />

        <div class='text12'><b>Date : </b> le ${api.format_date(activity.date)}</div>
        <div class='text12'><b>Durée : </b> ${activity.duration}</div>
        <div><b>Date : </b> le ${api.format_date(activity.datetime)}</div>
        <div><b>Durée : </b> ${activity.duration}</div>

        <center>
            <div class='text12 upper'><b>${activity.action_label}</b></div>
            <div class='text9'>${activity.subaction_label}</div>
            <br />
            <div class='text14'><b>${activity.type_object.label}</b></div>

        </center>
        <div class='text12'>Conseiller : ${', '.join([api.format_account(conseiller) for conseiller in activity.conseillers])}</div>
        <% companies = set() %>
        <div class='text12'>Participants :
            % for user in activity.participants:
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
            <br />
            <div class='text12' ><b>${label}</b></div>
            <hr />
            ${api.clean_html(getattr(activity, attr))|n}
        % endfor
        <br />
        <br />
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
    <div class='row' id='footer'>
        % if config.has_key('coop_pdffootertitle'):
            <b>${format_text(config.get('coop_pdffootertitle'))}</b><br />
        %endif
        % if config.has_key('coop_pdffootertext'):
            ${format_text(config.get('coop_pdffootertext'))}
        % endif
</div>
</body>
</html>
