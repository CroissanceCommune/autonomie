<%inherit file="${context['main_template'].uri}" />

<%block name="content">
    <%block name="before_details"></%block>

    <% workshop = request.context %>
    <div class='panel panel-default page-block'>
    <div class='panel-heading'>
    Détails
    </div>
    <div class='panel-body'>
        % if workshop.description != '':
                <h4>Description</h4>
                <p>${workshop.description}</p>
        % endif

        <h4>Personnes</h4>
        <dl class="dl-horizontal">
            <dt>
                <i class="fa fa-key"></i>
                Gère :
            </dt>
            <dd>
                % if workshop.owner:
                    ${workshop.owner.label}
                % else:
                    Non renseigné
                % endif
            </dd>

            <dt>
                Anime(nt) :
            </dt>
            <dd>
                % if workshop.trainers:
                    ${', '.join([i.label for i in workshop.trainers])}
                % else:
                    Non renseigné
                % endif
            </dd>

            <dt>
                Participent :
            <dd>${', '.join([i.label for i in workshop.participants])}</dd>
            </dd>
        </dl>
    </div>
    </div>

<%block name="after_details"></%block>
</%block>
