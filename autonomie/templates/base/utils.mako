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
<%def name="searchform(label='Rechercher', html='', helptext=None)">
    <form class='navbar-form pull-right form-search col-md-offset-3 form-inline' id='search_form' method='GET'>
        <div class='pull-left' style='padding-right:3px'>
            <input type='text' name='search' class='input-medium search-query' value="${request.params.get('search', '')}">
        % if helptext:
            <span class="help-block">${helptext}</span>
        %endif
        </div>
        ${html|n}
        <select class='col-md-1' name='nb'>
            % for text, value in (('10 par page', u'10'), ('20 par page', u'20'), ('30 par page', u'30'), ("40 par page", u'40'), ('50 par page', u'50'), ('Tous', u'1000'),):
                <% nb_item = request.GET.get("nb") %>
                % if nb_item == value or request.cookies.get('items_per_page') == value:
                    <option value="${value}" selected='true'>${text}</option>
                %else:
                    <option value="${value}">${text}</option>
                %endif
            % endfor
        </select>
        <button type="submit" class="btn btn-default">${label}</button>
    </form>
</%def>
<%def name="urlbuild(args_dict)">
<%doc>Returns an url preserving actual get args</%doc>
<%
get_args = request.GET.copy()
get_args.update(args_dict)
path = request.current_route_path(_query=get_args)
%>${path}</%def>
<%def name="print_date(timestamp)">
<% import datetime %>
    % if isinstance(timestamp, datetime.date):
        ${timestamp.strftime("%e/%m/%Y")}
    % elif not timestamp:
        ""
    % else:
        ${datetime.datetime.fromtimestamp(float(timestamp)).strftime("%d/%m/%Y %H:%M")}
    % endif
</%def>
<%def name="print_str_date(timestamp)">
    <% import datetime %>
    % if isinstance(timestamp, datetime.date):
        Le ${timestamp.strftime("%e %B %Y").decode('utf-8').capitalize()}
    % elif not timestamp:
        ""
    %else:
        Le ${datetime.datetime.fromtimestamp(float(timestamp)).strftime("%e %B %Y").decode('utf-8').capitalize()}
    %endif
</%def>
<%def name="format_amount(data, trim=True)" filter="trim">
    <%doc>Format an amount for display</%doc>
    %if data is not UNDEFINED and data is not None:
        % if trim:
            <% data = "%.2f"% (int(data)/100.0,) %>
        % else:
            <% data = "%s" % (data/100.0,) %>
        % endif
        ${data.replace('.', ',')}
    %endif
</%def>
<%def name="format_quantity(data)"><%doc>Format a quantity for display</%doc>
    %if data is not UNDEFINED and data is not None:
        <% data = "%s"% (float(data),) %>
        ${data.replace('.', ',')}
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
    <a class='btn btn-default ${css_class}' href='${href}' title="${title}"
        % if onclick:
            onclick="${onclick}"
        % endif
        >
        %if icotext:
            <span>${api.clean_html(icotext)|n}</span>
        % endif
        %if icon:
            <i class='glyphicon glyphicon-${icon}'></i>
        %endif
        <span class="visible-lg hidden-sm" style="display:inline">
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
            % if request.user.is_manager() or request.user.is_admin():
                % for label, key in ((u'Code comptable', 'code_compta'),\
                                     (u'Contribution à la CAE (en %)', 'contribution'),\
                                     ):
                    <dt>${label}</dt>
                    <dd>${getattr(company, key) or u"Non renseigné"}</dd>
                % endfor
            % endif
        </dl>
</%def>
<%def name="format_filelist(parent_node)">
 % if parent_node is not None:
      % for child in parent_node.children:
          % if loop.first:
              <ul>
          % endif
              % if child.type_ == 'file':
                  <li>
                  <a href="${request.route_path('file', id=child.id)}">${child.label}</a>
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

