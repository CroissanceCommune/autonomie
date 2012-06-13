<%inherit file="base.mako"></%inherit>
<%block name='content'>
<div class='row'>
    <div class="span6 offset3">
        <h3>Entreprise ${company.name}</h3>
        ${company.goal}
        <br />
        <br />
        %for link in link_list:
            <p>${link.render(request)|n}</p>
        %endfor
        <br />
        %if len(company.employees) > 1:
            <h3>Employé(s)</h3>
        %elif len(company.employees) == 1:
            <h3>Employé</h3>
        %else:
            <h3>Il n'y a aucun compte associé à cette entreprise</h3>
        %endif

        % for empl in company.employees:
            <a href="${request.route_path('user', id=empl.id)}" title='Voir ce compte'>
                <i class='icon-user'></i>${empl.lastname} ${empl.firstname}
            </a>
            <br />
            <br />
        % endfor
    </div>
</div>
</%block>
