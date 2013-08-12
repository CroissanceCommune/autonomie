<%inherit file="base.mako"></%inherit>
<%block name='content'>
% if companies:
    <ul class="thumbnails">
        % for company in companies:
        <li class="span4">
        <div class="thumbnail">
            <img src="/assets/${company.get_logo_filepath()}" title="${company.name}" alt="" style="max-height:200px;"/>
            <div class="caption">
                <h3>${company.name}</h3>
                <p>
                    ${company.goal}
                </p>
                <a class="btn btn-primary" href="${company.url}" title="Accéder au gestionnaire de ${company.name}">
                    Accéder au gestionnaire de ${company.name} >>>
                </a>
            </div>
        </div>
        </li>
    % endfor
</ul>
%else:
    <strong>Aucune entreprise n'a été configurée pour ce compte</strong>
% endif
</%block>
