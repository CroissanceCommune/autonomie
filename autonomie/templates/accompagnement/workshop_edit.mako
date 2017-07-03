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
<%inherit file="${context['main_template'].uri}" />
<%block name="content">
<div class='row'>
    <div class='col-md-12'>
        <button class='btn btn-primary' data-toggle='collapse' data-target='#edition_form'>
            <i class="fa fa-pencil"></i> Modifier les données relatives à l'atelier
        </button>
        <a class='btn btn-default'
            href='${request.route_path("workshop", id=request.context.id, _query=dict(action="duplicate"))}' >
            <i class='fa fa-copy'></i>
            Dupliquer cet atelier
        </a>
        <a class='btn btn-default' href='${request.route_path("workshop.pdf", id=request.context.id)}' >
            <i class='fa fa-download'></i>
            Télécharger la feuille d'émargement globale
        </a>
        <div
            % if formerror is not UNDEFINED:
                class='section-content'
            % else:
                class='section-content collapse'
            % endif
            id='edition_form'>
            <button class="close" data-toggle="collapse" data-target='#edition_form' type="button">×</button>
            ${form|n}
        </div>
    </div>
</div>

    <h3>Émargement</h3>
    <form method='POST'
        class="deform  deform" accept-charset="utf-8"
        enctype="multipart/form-data" action="${request.route_path('workshop',\
        id=request.context.id, _query=dict(action='record'))}">

        <input type="hidden" name="__start__" value="attendances:sequence" />
            <ul class='nav nav-tabs'>
                % for timeslot in request.context.timeslots:
                    <li \
                    % if loop.first:
                        class='active' \
                    % endif
                    >
                        <a href='#tab_${timeslot.id}' data-toggle='tab'>
                            ${timeslot.name}
                        </a>
                    </li>
                % endfor
            </ul>
            <div class='tab-content'>
                % for timeslot in request.context.timeslots:
                    <div class='tab-pane \
                        % if loop.first:
                            active \
                        % endif
                            ' id='tab_${timeslot.id}'>
                            <h4>Émargement de la tranche horaire ${timeslot.name}</h4>
                            <p>
                            <b>Horaires : </b>  de ${api.format_datetime(timeslot.start_time, timeonly=True)} \
à ${api.format_datetime(timeslot.end_time, timeonly=True)} \
(${timeslot.duration[0]}h${timeslot.duration[1]})
</p>
<div>
    <a class='btn btn-default' href='${request.route_path("timeslot.pdf", id=timeslot.id)}' >
        <i class='fa fa-download'></i>
        Télécharger la feuille d'émargement pour cette tranche horaire
    </a>
</div>
                            % for attendance in timeslot.sorted_attendances:
                                <input type="hidden" name="__start__" value="attendance:mapping" />
                                <% participant = attendance.user %>
                                <% participant_url = request.route_path('user', id=participant.id) %>
                                <% status = attendance.status %>

                               <% tag_id = "presence_%s_%s" % (timeslot.id, participant.id) %>
                               <input type='hidden' name='account_id' value='${participant.id}' />
                               <input type='hidden' name='timeslot_id' value='${timeslot.id}' />
                               <div class='row form-group'>
                                   <label class="col-sm-2" for="${tag_id}">
                                        <a href='${participant_url}' title='Voir le compte de ce participant'>
                                            ${api.format_account(participant)}
                                        </a>
                                   </label>
                                       <input type='hidden' value='status:rename' name='__start__' />
                                       % for index, value  in enumerate(available_status):
                                           <% val, label = value %>
                                           <label class='radio-inline' >
                                               <input id='${tag_id}' name='${tag_id}' type='radio' \
                                               % if status == val:
                                                   checked \
                                                % endif
                                                value='${val}' />${label}
                                           </label>
                                       % endfor
                                       <input type='hidden' name='__end__' />
                               </div>
                               <input type='hidden' name='__end__' value='attendance:mapping' />
                           % endfor
                       </div>
                   % endfor
               </div>
               <input type="hidden" name="__end__" value='attendances:sequence'/>
               <div class='form-actions'>
                   <button id="deformsubmit" class="btn btn-primary " value="submit" type="submit" name="submit"> Enregistrer </button>
               </div>
        </form>
</%block>
