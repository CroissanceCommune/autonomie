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
            Port Parallèle<br />
            70, rue Amelot<br />
            75011 Paris
        </address>
    %endif
</%def>
<%def name="searchform(label='Rechercher', html='')">
    <form class='navbar-form pull-right form-search offset3' id='search_form' method='GET'>
        <input type='text' name='search' class='input-medium search-query' value="${request.params.get('search', '')}">
        ${html|n}
        <button type="submit" class="btn">${label}</button>
    </form>
</%def>
<%def name="urlbuild(args_dict)">
<%doc>Returns an url preserving actual get args</%doc>
<%
get_args = request.GET.copy()
get_args.update(args_dict)
path = request.current_route_path()
if get_args:
    path = "{0}?{1}".format(path, '&'.join("{0}={1}".format(key, value)
                                for key, value in get_args.items()))
%>${path}</%def>
<%def name="print_date(timestamp)">
<% import datetime %>
    % if isinstance(timestamp, datetime.date):
        ${timestamp.strftime("%d/%m/%Y")}
    % elif not timestamp:
        ""
    % else:
        ${datetime.datetime.fromtimestamp(float(timestamp)).strftime("%d/%m/%Y %H:%M")}
    % endif
</%def>
<%def name="print_str_date(timestamp)">
    <% import datetime %>
    % if isinstance(timestamp, datetime.date):
        ${timestamp.strftime("%A %d %B %Y").decode('utf-8').capitalize()}
    % elif not timestamp:
        ""
    %else:
        ${datetime.datetime.fromtimestamp(float(timestamp)).strftime("%A %d %B %Y").decode('utf-8').capitalize()}
    %endif
</%def>
<%def name="format_amount(data)">
    <%doc>Format an amount for display</%doc>
    %if data is not UNDEFINED and data is not None:
        <% data = "%.2f"% (int(data)/100.0,) %>
        ${data.replace('.', ',')}
    %endif
</%def>
<%def name="format_quantity(data)"><%doc>Format a quantity for display</%doc>
    %if data is not UNDEFINED and data is not None:
        <% data = "%d"% (int(data),) %>
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
<%def name="format_client(client, company)">
    <%doc>
        Render a client
    </%doc>
    %if client is not UNDEFINED and client is not None:
        <a href="${request.route_path('company_client', cid=company.id, id=client.id)}"
           title="Voir le client ${client.name}">
            ${client.name}
        </a>
    %endif
</%def>
<%def name="format_project(project, company)">
    <%doc>
        Render a project
    </%doc>
    %if project is not UNDEFINED and project is not None:
        <a href="${request.route_path('company_project', cid=company.id, id=project.id)}"
            title="Voir le projet ${project.name}">
            ${project.name}
        </a>
    %endif
</%def>
