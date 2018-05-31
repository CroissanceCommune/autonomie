# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import deform
from colanderalchemy import SQLAlchemySchemaNode

from autonomie.models.task.mentions import TaskMention

from autonomie.forms import (
    customize_field,
)


def get_admin_task_mention_schema():
    """
    Build the task mentions admin schema
    """
    schema = SQLAlchemySchemaNode(
        TaskMention,
        includes=(
            "label", "help_text", "title", "full_text", "order",
        )
    )
    customize_field(
        schema,
        "label",
        title=u"Libellé",
        description=u"Libellé utilisé dans l'interface",
    )
    customize_field(
        schema,
        "full_text",
        widget=deform.widget.TextAreaWidget(cols=80, rows=4),
    )
    customize_field(schema, "order", widget=deform.widget.HiddenWidget())
    return schema
