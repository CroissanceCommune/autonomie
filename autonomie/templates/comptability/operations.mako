<%inherit file="/base.mako"></%inherit>
<%namespace file="/base/pager.mako" import="pager"/>
<%namespace file="/base/pager.mako" import="sortable"/>
<%namespace file="/base/utils.mako" import="searchform"/>
<%namespace file="/base/utils.mako" import="print_date" />
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a title='Référencer une nouvelle opération comptable' href='#new' onclick="$('#addform').dialog('open');">
        Ajouter une opération
    </a>
    </li>
    <li>
    </li>
</ul>
<div class='row'>
    <div class='span12'>
        <form class='navbar-form form-search form-horizontal' id='search_form' method='GET'>
            <div class='floatted' style="margin-top:5px;margin-right:5px;">
            <select id='company-select' name='company' data-placeholder="Sélectionner une entreprise">
                <option value=''></option>
                %for id, name in companies:
                    %if unicode(id) == request.params.get('company'):
                        <option selected="" value='${id}'>${name}</option>
                    %else:
                        <option value='${id}'>${name}</option>
                    %endif
                %endfor
            </select>
            <select name='year' id='year-select' class='span2' data-placeholder="Année">
                <option value=''></option>
                %for year in years:
                    %if unicode(current_year) == unicode(year):
                        <option selected="1" value='${year}'>${year}</option>
                    %else:
                        <option value='${year}'>${year}</option>
                    %endif
                %endfor
            </select>
        </div>
        <div class='floatted' style="margin-right:5px">
                <input type='text' name='search' class='input-medium search-query' value="${request.params.get('search', '')}"/>
                <span class="help-block">Montant ou libellé</span>
            </div>
            <div class="floatted" style="margin-right:5px">
            <select class="span1" name="nb">
                <option selected="true" value="10">10 par page</option>
                <option value="20">20 par page</option>
                <option value="30">30 par page</option>
                <option value="40">40 par page</option>
                <option value="50">50 par page</option>
                <option value="1000">Tous</option>
            </select>
            <button type="submit" class="btn btn-primary">Filtrer</button>
        </div>
        </form>
    </div>
</div>
</%block>
<%block name='content'>
<table class="table table-condensed table-bordered">
    <% columns = ((u'Identifiant', None), (u'Compagnie', None), (u"Montant", 'montant'), (u"Libellé", 'libelle'), (u"Annee", 'year'), (u"Date d'import", "date"),(u'Actions', None)) %>
    <thead>
        %for column in columns:
            <th>
                %if column[1]:
                    ${sortable(column[0], column[1])}
                %else:
                    ${column[0]}
                %endif
            </th>
        %endfor
    </thead>
    <tbody>
        % if operations:
            % for operation in operations:
                <tr>
                    <td>${operation.id}</td>
                    <td>${operation.company.name}</td>
                    <td>${operation.amount}</td>
                    <td>${operation.label}</td>
                    <td>${operation.year}</td>
                    <td>${print_date(operation.date)}</td>
                    <td>
                        <div class='btn-group'>
                            <a class='btn' href='${request.route_path("operation", id=operation.id, _query=dict(action="edit"))}' title="Éditer">
                                <i class='icon-pencil'></i>
                            </a>
                            <a class='btn'
                               href='${request.route_path("operation", id=operation.id, _query=dict(action="delete"))}'
                               title="Supprimer"
                               onclick="return confirm('Êtes-vous sûr de vouloir supprimer cette opération ?');">
                                <i class='icon-remove'></i>
                            </a>
                        </div>
                    </td>
                </tr>
            % endfor
        % else:
            <tr>
                <td colspan='${len(columns)}'>
                    Aucune opération comptable n'a pu être retrouvée
                </td>
            </tr>
        % endif
    </tbody>
</table>
${pager(operations)}
% if html_form is not UNDEFINED:
    <div id='addform'>
        ${html_form|n}
    </div>
% endif
</%block>
<%block name='footerjs'>
% if html_form is not UNDEFINED:
    $( function() {
    $("#addform").dialog({ autoOpen: false,
    modal:true,
    width:"auto",
    title:"Ajouter une opération",
    open: function(event, ui){
    $('.ui-widget-overlay').css('width','100%');
    $('.ui-widget-overlay').css('height','100%');
    }
    });
    });
% endif
$('#company-select').chosen({allow_single_deselect: true});
$('#company-select').change(function(){$(this).closest('form').submit()});
$('#year-select').chosen({allow_single_deselect: true});
$('#year-select').change(function(){$(this).closest('form').submit()});
</%block>
