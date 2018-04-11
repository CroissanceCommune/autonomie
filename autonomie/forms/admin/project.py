# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.project.types import ProjectType


def get_admin_project_type_schema():
    schema = SQLAlchemySchemaNode(
        ProjectType,
        includes=(
            "label", "private", "default",
        )
    )
    return schema
