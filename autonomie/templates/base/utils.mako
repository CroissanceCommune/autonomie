<%def name='esc(datas)'><%text>${</%text>${datas}<%text>}</%text>\
</%def>
<%def name='address(datas, _type)'>
    %if _type == 'client':
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
    <form class='navbar-form pull-right form-search offset3 form-inline' id='search_form' method='GET'>
        <div class='floatted' style='padding-right:3px'>
            <input type='text' name='search' class='input-medium search-query' value="${request.params.get('search', '')}">
        % if helptext:
            <span class="help-block">${helptext}</span>
        %endif
        </div>
        ${html|n}
        <select class='span1' name='nb'>
            % for text, value in (('10 par page', u'10'), ('20 par page', u'20'), ('30 par page', u'30'), ("40 par page", u'40'), ('50 par page', u'50'), ('Tous', u'1000'),):
                <% nb_item = request.GET.get("nb") %>
                % if nb_item == value or request.cookies.get('items_per_page') == value:
                    <option value="${value}" selected='true'>${text}</option>
                %else:
                    <option value="${value}">${text}</option>
                %endif
            % endfor
        </select>
        <button type="submit" class="btn">${label}</button>
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
<%def name="format_text(data)">
    <%doc>
        Replace \n with br for html output
    </%doc>
    %if data is not UNDEFINED and data is not None:
        ${data.replace(u'\n', u'<br />')|n}
    %endif
</%def>
<%def name="format_client(client)">
    <%doc>
        Render a client
    </%doc>
    %if client is not UNDEFINED and client is not None:
        <a href="${request.route_path('client', id=client.id)}"
           title="Voir le client ${client.name}">
            ${client.name}
        </a>
    %endif
</%def>
<%def name="format_project(project)">
    <%doc>
        Render a project
    </%doc>
    %if project is not UNDEFINED and project is not None:
        <a href="${request.route_path('project', id=project.id)}"
            title="Voir le projet ${project.name}">
            ${project.name}
        </a>
    %endif
</%def>
<%def name="format_mail(mail)">
    <%doc>
        Render an email address
    </%doc>
    % if mail is not UNDEFINED and mail is not None:
        <a href="mailto:${mail}"><span class="ui-icon ui-icon-mail-closed"></span>${mail}</a>
    % endif
</%def>
<%def name="format_phone(phone)">
    <%doc>
        Render a phone with a phone link
    </%doc>
    % if phone is not UNDEFINED and phone is not None:
        <a class="visible-mobile hidden-desktop" href="tel://${phone}">${phone}</a>
        <span class="hidden-mobile visible-desktop">${phone}</span>
    % endif
</%def>
<%def name="table_btn(href, label, title, icon=None, onclick=None, icotext=None)">
    <a class='btn' href='${href}' title="${title}"
        % if onclick:
            onclick="${onclick}"
        % endif
        >
        %if icotext:
            <span>${icotext|n}</span>
        % endif
        %if icon:
            <i class='icon ${icon}'></i>
        %endif
        <span class="visible-desktop hidden-tablet" style="display:inline">
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
        %if company.get_logo_filepath():
          <img src="/assets/${company.get_logo_filepath()}" alt=""  width="250px" />
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
        </dl>
</%def>
