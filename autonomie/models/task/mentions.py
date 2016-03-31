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
import deform
import sqlalchemy as sa

from autonomie.models.base import (
    DBBASE,
    default_table_args,
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


class TaskMention(ConfigurableOption):
    __colanderalchemy_config__ = {
        "title": u"mention facultative",
        "help_msg": u"Configurer des mentions facultatives pour les devis et \
factures, celles-ci sont proposées aux entrepreneurs dans les formulaires et \
insérées dans les sorties PDF.<br /> \
<b>Libellé</b>: Libellé dans le formulaire<br />\
<b>Titre</b>: Le titre du bloc contenant les mentions dans le PDF <br />\
<b>Texte à afficher dans les PDF</b>: Texte affiché dans la sortie PDF \
si l'entrepreneur a ajouté cette mention à son devis/sa facture<br />."
        "validation_msg": u"Les mentions facultatives ont bien été configurées"
    }
    id = get_id_foreignkey_col('configurable_option.id')
    title = sa.Column(
        sa.String(255),
        info={
            'colanderalchemy': {
                "title": u"Titre",
                "description": u"Titre du bloc contenant les mentions dans \
la sortie pdf",
            }
        }
    full_text = sa.Column(
        sa.Text(),
        info={
            'colanderalchemy': {
                "title": u"Texte à afficher dans les PDF",
                "description": u"Si l'entrepreneur a ajouté cette mention à \
son devis/sa facture, ce texte apparaitra dans la sortie PDF",
                'widget': deform.widget.RichTextWidget(
                    options={
                        'language': "fr_FR",
                        'content_css': "/fanstatic/fanstatic/css/richtext.css",
                    },
                )
            }
        },
    )
    tasks = sa.orm.relationship(
        "Task",
        secondary=TASK_MENTION,
        back_populates="mentions",
        info={
            'colanderalchemy': {
                'exclude': True
            }
        }
    )
