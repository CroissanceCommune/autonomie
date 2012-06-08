<%inherit file="/base.mako"></%inherit>
<%block name='actionmenu'>
<ul class='nav nav-pills'>
    <li>
    <a href="${request.route_path('admin_main')}" title="Configuration générale de votre installation d'autonomie">
        <div class="hcentered">
            Configuration générale
        </div>
    </a>
    </li>
    <li>
    <a href="${request.route_path('admin_tva')}" title="Configuration des taux de TVA proposés dans les devis et factures">
        <div class="hcentered">
            Configuration des taux de TVA
        </div>
    </a>
    </li>
</ul>
</%block>
