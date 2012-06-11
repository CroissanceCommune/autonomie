<%inherit file="base.mako"></%inherit>
<%block name='content'>
% for company in companies:
   <div class="item drop-shadow round floatted">
       <a href="${company.url}" title="Accéder au gestionnaire de ${company.name}">
        <div class="hcentered">
            <h3>${company.name}</h3>
            <img src="${company.get_logo_filepath}" title="${company.name}" alt=""/>
        </div>
       </a>
    </div>
%else:
    <strong>Aucune entreprise n'a été configurée pour ce compte</strong>
% endfor
</%block>
