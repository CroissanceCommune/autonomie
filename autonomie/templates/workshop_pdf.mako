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
<%doc>
Attendance sheet for a given timeslot (the current context)
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
        <div>
        <img src="/assets/main/accompagnement_header.png" />
        </div>
        % for index, i in enumerate(('info1', 'info2', 'info3')):
            % if getattr(workshop, i):
                <h${index + 1}>${getattr(workshop, i)} </h${index + 1}>
            % endif
        % endfor

        % if timeslots[0].start_time.day == timeslots[-1].end_time.day:
            <h3>
                Émargement du ${api.format_date(timeslots[0].start_time)}
                de ${api.format_datetime(timeslots[0].start_time, timeonly=True)}
                à ${api.format_datetime(timeslots[-1].end_time, timeonly=True)}
            </h3>
        % else:
            <h3>
                Émargement du ${api.format_datetime(timeslots[0].start_time)}
                au ${api.format_datetime(timeslots[-1].end_time)}
            </h3>
        % endif
        <div>
            <b>Nom du (des) formateur(s)</b> : ${' '.join(workshop.leaders)}&nbsp;&nbsp;&nbsp; <b>Signature(s)</b> :
        </div>
        <br />
        <div>
            <div>
                <img src="${request.static_url('autonomie:static/img//pdf_checkbox.png', _app_url='')}" />
                Atelier
            </div>
            <div>
                <img src="${request.static_url('autonomie:static/img//pdf_checkbox.png', _app_url='')}" />
                Formation
            </div>
        </div>
        <br />
        <div><b>Titre de l'atelier ou de la formation</b> : ${workshop.name}</div>
        <div class='row'>
            <table class="lines span12">
                <thead>
                    <tr>
                        <th class="description">Participants</th>
                        % for timeslot in timeslots:
                            <th class='price'>${timeslot.name}</th>
                        % endfor
                    </tr>
                </thead>
                <tbody>
                    % for user in participants:
                        <tr>
                            <td>
                                ${api.format_account(user)} ( ${"'".join([c.name for c in user.companies])} )
                            </td>
                            % for timeslot in timeslots:
                                <td><br /></td>
                            % endfor
                        </tr>
                    % endfor
                </tbody>
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

