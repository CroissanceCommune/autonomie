<%doc>
Template Displaying a list of trainings
</%doc>

<%inherit file="${context['main_template'].uri}" />
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="format_text" />
<%block name='content'>
<div class='panel panel-default page-block'>
    <div class='panel-heading'>
        <a href='#filter-form'
        data-toggle='collapse'
        aria-expanded="false"
        aria-controls="filter-form">
        <i class='glyphicon glyphicon-search'></i>&nbsp;
        Filtres&nbsp;
        <i class='glyphicon glyphicon-chevron-down'></i>
        </a>
        % if '__formid__' in request.GET:
        <div class='help-text'>
        <small><i>Des filtres sont actifs</i></small>
        </div>
        <div class='help-text'>
        <a href="${request.current_route_path(_query={})}">
        <i class='glyphicon glyphicon-remove'></i> Supprimer tous les filtres
        </a>
        </div>
        % endif
    </div>
    <div class='panel-body'>
        % if '__formid__' in request.GET:
        <div class='collapse' id='filter-form'>
        % else:
        <div class='in collapse' id='filter-form'>
        % endif
            <div class='row'>
                <div class='col-xs-12'>
                    ${form|n}
                </div>
            </div>
        </div>
    </div>
</div>

<div class='panel panel-default page-block'>
    <div class='panel-heading'>
        ${records.item_count} Résultat(s)
    </div>
    <div class='panel-body'>
    <table class="table table-condensed table-bordered">
        <thead>
            <th>Statut</th>
            <th>Intitulé du projet</th>
            <th>Enseigne</th>
            <th>Client</th>
            <th class='text-center'>Actions</th>
        </thead>
        <tbody>
        % if records:
            % for id_, record in records:
                <tr>
                    <td>
                    TODO
                    </td>
                    <td>${record.name}</td>
                    <td>${record.company.name}</td>
                    <td>
                        <ul>
                            % for customer in record.customers:
                            <li>${customer.label}</li>
                            % endfor
                        </ul>
                    </td>
                    <td class='text-center'>
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
            <td colspan="4"><em>Aucun élément n'a été retrouvé</em></td>
            </tr>
        % endif
        </tbody>
    </table>
    ${pager(records)}
    </div>
</div>
</%block>
