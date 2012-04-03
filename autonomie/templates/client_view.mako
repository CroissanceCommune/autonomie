<%inherit file="base.mako"></%inherit>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a class="btn-primary" title='Éditer les informations de ce client' style='margin:0px 10px 0px 250px;'
        href='${request.route_path("company_client", cid=company.id, id=client.id, _query=dict(edit=True))}'>
        Éditer
    </a>
    </li>
</ul>
</%block>
<%block name='content'>
<div style="margin-left:20%;width:60%; font-size:1.3em;">
    <table class='table table-bordered'>
        <tr><td>
                Nom de l'entreprise :
            </td><td>
            ${client.name}
    </td></tr>
    <tr><td>
            Code :
            </td><td>
            ${client.id}

% if client.intraTVA:
        <tr><td>
    TVA intracommunautaire :
            </td><td>
    ${client.intraTVA}
    </td></tr>
% endif
<tr><td colspan='2' style="background-color:#EEE"></td></tr>
        <tr><td>
Contact principal :
            </td><td>
${client.contactLastName} ${client.contactFirstName}
    </td></tr>
        <tr><td>
Adresse :
            </td><td>
        % if client.address:
            ${client.address}<br /> ${client.zipCode} ${client.city}
            % if client.country and client.country!= 'France':
                <br />${client.country}
            % endif
        %else:
            Aucun adresse connue
        %endif
    </td></tr>
    <tr><td colspan='2' style="background-color:#EEE"></td></tr>
        <tr><td>
    Téléphone :
            </td><td>
        %if client.phone:
            ${client.phone}
        %else:
            Aucun numéro connu
        %endif
    </td></tr>
    <br />
        <tr><td>
    E-mail :
            </td><td>
            %if client.email:
                ${client.email}
            % else:
                Aucune adresse connue
            % endif
    </td></tr>
</table>
    <br />
% if client.comments:
    <b>Commentaires :</b>
    <blockquote style='padding:15px;margin-top:25px;border:1px solid #eee;'>
        ${client.comments}
    </blockquote>
%else :
Aucun commentaire
% endif
    <br />
</div>
</%block>
