<%inherit file="base.mako"></%inherit>
<%block name='content'>
<div class='container' style='overflow:hidden'>
        %if task.statusPersonAccount  is not UNDEFINED and task.statusPersonAccount:
            <strong>${task.get_status_str().format(genre='', firstname=task.statusPersonAccount.firstname, lastname=task.statusPersonAccount.lastname)}</strong>
        %else:
            <strong>Aucune information d'historique ou de statut n'a pu être retrouvée</strong>
        %endif
        <div style='border:1px solid #888'>
            ${html_datas|n}
        </div>
</div>
</%block>
