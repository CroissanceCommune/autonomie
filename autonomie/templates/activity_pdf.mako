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
<%namespace file="/base/utils.mako" import="format_text" />
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
<h1>Fiche rendez-vous</h1>
<div>Nature du rendez-vous : ${activity.type_object.label}</div>
<div>Mode d'entretien : ${activity.mode}</div>
<div>Conseiller : ${api.format_account(activity.conseiller)}</div>
<div>Participants :
% for user in activity.participants:
${api.format_account(user)}
    % if not loop.last:
    ,
    % endif
% endfor
</div>
        <% options = (\
                (u"Point de suivi", "point"),\
                (u"Définition des objectifs", "objectifs"), \
                (u"Plan d'action et préconisations", "action" ),\
                (u"Documents produits", "documents" ),\
                )
        %>
        % for label, attr in options:
            <h3>${label}</h3>
            <blockquote>
                ${format_text(getattr(activity, attr))}
            </blockquote>
        % endfor
<hr>
<div style="padding-bottom:50px">
<b>Signature Conseiller</b>
</div>
<div>
<b>Signature Participant</b>
</div>
</body>
</html>
