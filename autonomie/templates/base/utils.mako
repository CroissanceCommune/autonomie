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
    <form class='navbar-form pull-right form-search' id='search_form' method='GET'>
        <input type='text' name='search' class='input-medium search-query' value="${request.params.get('search', '')}">
        ${html|n}
        <button type="submit" class="btn">${label}</button>
    </form>
</%def>
<%def name="urlbuild(args_dict)">
<%doc>Returns an url preserving actual get args</%doc>
<%
get_args = request.GET
get_args.update(args_dict)
path = request.current_route_path()
if get_args:
    path = "{0}?{1}".format(path, '&'.join("{0}={1}".format(key, value)
                                for key, value in get_args.items()))
%>${path}</%def>
<%def name="print_date(timestamp)">
<% import datetime %>
${datetime.datetime.fromtimestamp(float(timestamp)).strftime("%d/%m/%Y %H:%M")}
</%def>
<%def name="print_str_date(timestamp)">
    <% import datetime %>
    % if isinstance(timestamp, datetime.date):
        ${timestamp.strftime("%A %d %B %Y").capitalize()}
    %else:
        ${datetime.datetime.fromtimestamp(float(timestamp)).strftime("%A %d %B %Y").capitalize()}
    %endif
</%def>
