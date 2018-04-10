# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import os

from autonomie.models.user.userdatas import (
    ZoneOption,
    ZoneQualificationOption,
    StudyLevelOption,
    SocialStatusOption,
    EmployeeQualityOption,
    ActivityTypeOption,
    PcsOption,
    PrescripteurOption,
    NonAdmissionOption,
    ParcoursStatusOption,
    MotifSortieOption,
    SocialDocTypeOption,
    CaeSituationOption,
    TypeSortieOption,
    AntenneOption,
)
from autonomie.views.admin.tools import (
    get_model_admin_view,
)
from autonomie.views.admin.userdatas import (
    USERDATAS_URL,
    UserDatasIndexView,
)


def includeme(config):
    """
    Configure route and views for userdatas management
    """
    for model in (
        CaeSituationOption,
        AntenneOption,
        ZoneOption,
        ZoneQualificationOption,
        StudyLevelOption,
        SocialStatusOption,
        EmployeeQualityOption,
        ActivityTypeOption,
        PcsOption,
        PrescripteurOption,
        NonAdmissionOption,
        ParcoursStatusOption,
        MotifSortieOption,
        SocialDocTypeOption,
        TypeSortieOption,
    ):
        view = get_model_admin_view(model, r_path=USERDATAS_URL)
        config.add_route(view.route_name, view.route_name)
        config.add_admin_view(view, parent=UserDatasIndexView)
