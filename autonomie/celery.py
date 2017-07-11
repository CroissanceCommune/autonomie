# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

from autonomie.models.user import UserDatas
from autonomie.models.customer import Customer


def includeme(config):
    config.register_import_model(
        key='userdatas',
        model=UserDatas,
        label=u"Données de gestion sociale",
        permission='admin_userdatas',
        excludes=(
            'name',
            'created_at',
            'updated_at',
            'type_',
            '_acl',
            'parent_id',
            'parent',
        )
    )
    config.register_import_model(
        key='customer',
        model=Customer,
        label=u"Clients",
        permission='add_customer',
        excludes=(
            'created_at',
            'updated_at',
            'company_id',
            'company',
        ),
    )
