<%doc>
    Template for estimation readonly display
</%doc>
<%inherit file="/base.mako"></%inherit>
<%block name='content'>
<div class='container' style='overflow:hidden'>
<div>
    %if task.statusPersonAccount  is not UNDEFINED and task.statusPersonAccount:
        <strong>${task.get_status_str("estimation")}</strong>
        <br />
    %else:
        <strong>Aucune information d'historique ou de statut n'a pu être retrouvée pour ce devis.</strong>
        <br />
    %endif
        Vous ne pouvez plus modifier ce document car il a déjà été validé.
        <br />
    <a class='btn btn-primary' href='${request.route_path("estimation", cid=company.id, id=task.IDProject, taskid=task.IDTask, _query=dict(view="pdf"))}' title="Télécharger la version PDF">
        Télécharger la version PDF
    </a>
    %if task.CAEStatus in ('sent', 'valid'):
        <a class='btn btn-primary'
            href='${request.route_path("estimation", cid=company.id, id=task.IDProject, taskid=task.IDTask, _query=dict(action="geninv"))}'
            title="Générer les factures correspondantes">
            Générer les factures
        </a>
        <a class='btn btn-primary'
            href='${request.route_path("estimation", cid=company.id, id=task.IDProject, taskid=task.IDTask, _query=dict(action="geninv"))}'
            title="Annuler ce devis">
            Indiquer sans suite
        </a>
    %endif
    <br />

</div>

        <div style='border:1px solid #888'>
            ${html_datas|n}
        </div>
</div>
</%block>
