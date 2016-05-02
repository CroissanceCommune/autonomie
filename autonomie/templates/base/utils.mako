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

<%def name='esc(datas)'><%text>${</%text>${datas}<%text>}</%text>\
</%def>
<%def name='address(datas, _type)'>
    %if _type == 'customer':
            <address>
                <b>${datas.name}</b><br />
                ${datas.address}<br />
                ${datas.zipCode} ${datas.city}
                % if datas.country and datas.country!= 'France':
                    <br />${datas.country}
                % endif
            </address>
    %elif _type == 'company':
        <address>
            <b>${datas.name}</b><br />
        </address>
    %endif
</%def>
<%def name="format_text(data, breaklines=True)">
    <%doc>
        Replace \n with br for html output
    </%doc>
    <% text = data %>
    %if data is not UNDEFINED and data is not None and breaklines:
        <% text = text.replace(u'\n', u'<br />') %>
    %endif
    ${api.clean_html(text)|n}
</%def>
<%def name="format_customer(customer, link=True)">
    <%doc>
        Render a customer
    </%doc>
    %if customer is not UNDEFINED and customer is not None:
        % if link:
        <a href="${request.route_path('customer', id=customer.id)}"
            title="Voir le client ${customer.name}">
        % endif
        ${customer.name}
        % if link:
        </a>
    %endif
    %endif
</%def>
<%def name="format_project(project, link=True)">
    <%doc>
        Render a project
        link : should we generate an html link
    </%doc>
    %if project is not UNDEFINED and project is not None:
        % if link:
        <a href="${request.route_path('project', id=project.id)}"
            title="Voir le projet ${project.name}">
        % endif
        ${project.name}
        % if link:
            </a>
        % endif
    %endif
</%def>
<%def name="format_mail(mail)">
    <%doc>
        Render an email address
    </%doc>
    % if mail is not UNDEFINED and mail is not None:
        <a href="mailto:${mail}">${mail}&nbsp;<i class="glyphicon glyphicon-envelope"></i></a>
    % endif
</%def>
<%def name="format_phone(phone)">
    <%doc>
        Render a phone with a phone link
    </%doc>
    % if phone is not UNDEFINED and phone is not None:
        <a class="visible-mobile hidden-lg" href="tel://${phone}">${phone}</a>
        <span class="hidden-mobile visible-lg">${phone}</span>
    % endif
</%def>
<%def name="table_btn(href, label, title, icon=None, onclick=None, icotext=None, css_class='')">
    <a class='btn btn-default btn-sm ${css_class}' href='${href}' title="${title}"
        % if onclick:
            onclick="${onclick}"
        % endif
        >
        %if icotext:
            <span>${api.clean_html(icotext)|n}</span>
        % endif
        %if icon:
            % if not icon.startswith('glyph') and not icon.startswith('fa'):
                <i class='glyphicon glyphicon-${icon}'></i>
            % else:
                <i class='${icon}'></i>
            % endif
        %endif
        <span class="visible-lg-inline-block hidden-sm" style="display:inline">
            ${label}
        </span>
    </a>
</%def>
<%def name="format_company(company)">
    <h3>
        <a href="${request.route_path('company', id=company.id)}">Entreprise ${company.name}</a>
    </h3>
        <p>
          ${company.goal}
        </p>
        %if company.logo_id:
            <img src="${api.img_url(company.logo_file)}" alt=""  width="250px" />
        %endif
        <dl>
            % if company.email:
                <dt>E-mail</dt>
                <dd>${format_mail(company.email)}</dd>
            % endif
            % for label, attr in ((u'Téléphone', 'phone'), (u"Téléphone portable", "mobile"),):
                %if getattr(company, attr):
                    <dt>${label}</dt>
                    <dd>${format_phone(getattr(company, attr))}</dd>
                % endif
            % endfor
            % if request.has_permission('admin_treasury'):
                % for label, key in ((u'Code comptable', 'code_compta'),\
                                     (u'Contribution à la CAE (en %)', 'contribution'),\
                                     ):
                    <dt>${label}</dt>
                    <dd>${getattr(company, key) or u"Non renseigné"}</dd>
                % endfor
            % endif
            % if company.activities:
                <dt>Domaine(s) d'activité</dt>
                <dd>
                    <ul>
                        % for activity in company.activities:
                            <li>${activity.label}</li>
                        % endfor
                    </ul>
                </dd>
            % endif
        </dl>
</%def>
<%def name="format_filelist(parent_node, delete=False)">
 % if parent_node is not None:
      % for child in parent_node.children:
          % if loop.first:
              <ul class='list-unstyled'>
          % endif
              % if child.type_ == 'file':
                  <li>
                  <a href="${request.route_path('file', id=child.id)}">${child.label}</a>
                    % if delete:
                        <a class='btn btn-small btn-danger' href="${request.route_path('file', id=child.id, _query=dict(action='delete'))}">
                          <i class='glyphicon glyphicon-trash'></i>
                      </a>
                  % endif
                  <a class='' href="${request.route_path('file', id=file.id, _query=dict(action='download'))}"><i class='glyphicon glyphicon-download'></i>Télécharger le fichier</a>
                  </li>
              % endif
          % if loop.last:
              </ul>
          % endif
      % endfor
  % endif
</%def>
<%def name="format_filetable(documents)">
    <table class="table table-striped table-hover">
        <thead>
            <th>Description</th>
            <th>Nom du fichier</th>
            <th>Déposé le</th>
            <th class="actions">Actions</th>
        </thead>
        <tbody>
            % for child in documents:
              <tr>
                  <td>${child.description}</td>
                  <td>${child.name}</td>
                  <td>${api.format_date(child.updated_at)}</td>
                  <td class="actions">
                      % if api.has_permission('edit', child):
                        ${table_btn(request.route_path('file', id=child.id),
                            u"Voir/Modifier",
                            u"Voir/Modifier ce document",
                            icon="pencil")}
                      % endif
                      ${table_btn(request.route_path('file', id=child.id, _query=dict(action='download')),
                      u"Télécharger",
                      u"Télécharger ce document",
                      icon="download-alt")}
                      % if api.has_permission('delete', child):
                          <% message = u"Ce fichier sera supprimer de la base de gestion sociale. Êtes-vous sûr de vouloir continuer ?" %>
                          ${table_btn(request.route_path('file', id=child.id, _query=dict(action='delete')),
                                u"Supprimer",
                                u"Supprimer ce document",
                                onclick=u"return confirm('%s')" % message,
                                icon="trash",
                                css_class='btn-danger')}
                      % endif

                  </td>
              </tr>
            % endfor
            % if documents == []:
                <tr><td colspan='6'>Aucun document social n'est disponible</td></tr>
            % endif
        </tbody>
  </table>
</%def>
<%def name="definition_list(items)">
    <%doc>
        render a list of elements as a definition_list
        items should be an iterator of (label, values) 2-uple
    </%doc>
    <dl class="dl-horizontal">
        % for label, value in items:
            <dt>${label}</dt>
            <dd>${value}</dd>
        % endfor
    </dl>
</%def>

