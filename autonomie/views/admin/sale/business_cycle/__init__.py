# -*-coding:utf-8-*-
import os


from autonomie.views.admin.sale import (
    SaleIndexView,
    SALE_URL
)
from autonomie.views.admin.tools import BaseAdminIndexView


BUSINESS_URL = os.path.join(SALE_URL, "business_cycle")


class BusinessCycleIndexView(BaseAdminIndexView):
    title = u"Cycle d'affaires"
    description = u"Configurer les typologies de projet (Chantiers, \
Formations ... ) et leurs pré-requis (mentions, documents...)"
    route_name = BUSINESS_URL


def includeme(config):
    config.add_route(BUSINESS_URL, BUSINESS_URL)
    config.add_admin_view(
        BusinessCycleIndexView,
        parent=SaleIndexView,
    )
    config.include('.project_type')
    config.include('.mentions')
    config.include('.file_types')
