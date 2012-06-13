<%doc>
Template used to render a search form
</%doc>
<form class='navbar-form pull-right form-search offset3 form-inline' id='${elem.id_}' method='GET'>
    <div class='floatted' style='padding-right:3px'>
        <input type='text' name='search' class='input-medium search-query' value="${request.params.get('search', '')}">
        % if elem.helptext:
            <span class="help-block">${elem.helptext}</span>
        %endif
    </div>
    ##${elem.html|n}
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
    <button type="submit" class="btn">${elem.submit_text}</button>
</form>
