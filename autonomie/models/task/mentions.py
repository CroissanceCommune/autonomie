# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
"""
Modèle pour les mentions dans les devis et factures
"""
import sqlalchemy as sa

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
    DBSESSION,
)
from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)

TASK_MENTION = sa.Table(
    'task_mention_rel',
    DBBASE.metadata,
    sa.Column('task_id', sa.Integer, sa.ForeignKey('task.id')),
    sa.Column('mention_id', sa.Integer, sa.ForeignKey('task_mention.id')),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)
MANDATORY_TASK_MENTION = sa.Table(
    'mandatory_task_mention_rel',
    DBBASE.metadata,
    sa.Column('task_id', sa.Integer, sa.ForeignKey('task.id')),
    sa.Column('mention_id', sa.Integer, sa.ForeignKey('task_mention.id')),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


class TaskMention(ConfigurableOption):
    __colanderalchemy_config__ = {
        "title": u"Mentions facultatives des devis/factures",
        "description": u"Configurer les mentions que les entrepreneurs \
peuvent faire figurer dans leurs devis/factures",
    }
    id = get_id_foreignkey_col('configurable_option.id')
    title = sa.Column(
        sa.String(255),
        default="",
        info={
            'colanderalchemy': {
                "title": u"Titre à afficher dans les PDF",
                "description": u"Texte apparaissant sous forme de titre \
dans la sortie PDF (facultatif)"
            }
        }
    )
    full_text = sa.Column(
        sa.Text(),
        info={
            'colanderalchemy': {
                "title": u"Texte à afficher dans les PDF",
                "description": u"Si cette mention a été ajoutée à \
un devis/facture, ce texte apparaitra dans la sortie PDF",
            }
        },
    )
    help_text = sa.Column(
        sa.String(255),
        info={
            "colanderalchemy": {
                "title": u"Texte d'aide à l'utilisation",
                "description": u"Aide fournie à l'entrepreneur dans l'interface"
            }
        }
    )

    @property
    def is_used(self):
        task_query = DBSESSION().query(TASK_MENTION.c.task_id).filter(
            TASK_MENTION.c.mention_id == self.id
        )

        mandatory_query = DBSESSION().query(
            MANDATORY_TASK_MENTION.c.task_id
        ).filter(
            MANDATORY_TASK_MENTION.c.mention_id == self.id
        )

        return DBSESSION().query(task_query.exists()).scalar() or \
            DBSESSION().query(mandatory_query.exists()).scalar()
