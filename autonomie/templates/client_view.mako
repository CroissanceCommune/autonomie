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
<div class="row">
    <div class='span4 offset3'>
        <h3>Entreprise</h3>
        <dl>
            % for label, value in ((u"Nom de l'entreprise", client.name), (u"Code", client.id), (u"TVA intracommunautaire", client.intraTVA)):
                %if value:
                    <dt>${label}</dt>
                    <dd>${value}</dd>
                % endif
            % endfor
        </dl>
    </div>
    <div class="span4 offset1">
        <h3>Contact principal</h3>
        <strong>${client.contactLastName} ${client.contactFirstName}</strong>
        <br />
        % if client.address:
            <address>
                ${client.address}<br />
                ${client.zipCode} ${client.city}
                % if client.country and client.country!= 'France':
                    <br />${client.country}
                % endif
            </address>
        %else:
            Aucun adresse connue
            <br />
        %endif
        <dl>
            <dt>E-mail</dt>
            <dd>
                %if client.email:
                    <address>
                        ${client.email}
                    </address>
                % else:
                    Aucune adresse connue
                % endif
            </dd>
            <dt>Téléphone</dt>
            <dd>
                %if client.phone:
                    ${client.phone}
                %else:
                    Aucun numéro connu
                %endif
            </dd>
        </dl>
    </div>
</div>
<div class='row'>
    <div class='span9 offset3'>
        % if client.comments:
            <h3>Commentaires</h3>
            <blockquote style='padding:15px;margin-top:25px;border:1px solid #eee;'>
                ${client.comments}
            </blockquote>
        %else :
            Aucun commentaire
        % endif
    </div>
</div>
</%block>
