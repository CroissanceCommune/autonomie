# -*- coding: utf-8 -*-
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * TJEBBES Gaston <g.t@majerti.fr>
"""
Py3o exporters
"""
from __future__ import absolute_import

from sqlalchemy.orm import (
    ColumnProperty,
    RelationshipProperty,
)

from .sqla import BaseSqlaExporter


class SqlaContext(BaseSqlaExporter):
    """
    Provide a tool to build a context dict based on a given model. The datas are
    built following the informations retrieved from the model's declaration.
    Custom configuration can be achieved by customizing the info dict attribute from each column.

        config_key

            The key in the info dict we will look for.

            Actually handles the following informations :
                exclude : should the column be excluded from the output
                name : the key in the resulting dict


    >>> serializer = SqlaContext(Company)
    >>> company = Company.get(263)
    >>> res = s.compile_obj(company)


    :param model: a SQLA model
    """
    config_key = 'py3o'

    def __init__(self, model, rels=None):
        BaseSqlaExporter.__init__(self, model)
        # We store the relations already treated by storing the primaryjoin that
        # they use, since the backref uses the same join string, we can avoid
        # recursive collection
        self.rels = rels or []
        self.columns = self.collect_columns()

    def collect_columns(self):
        """
        Collect columns information from a given model.

        a column info contains

            the py3 informations

                exclude

                    Should the column be excluded from the current context ?

                name

                    the name of the key in the resulting py3o context of the
                    column

            __col__

                The original column object

            __prop__

                In case of a relationship, the SqlaContext wrapping the given
                object

        """
        res = []
        for prop in self.get_sorted_columns():

            info_dict = self.get_info_field(prop)
            main_infos = info_dict.get(self.config_key, {}).copy()

            if main_infos.get('exclude', False):
                continue

            # Si la clé name n'est pas définit on la met au nom de la colonne
            # par défaut
            main_infos.setdefault('name', prop.key)
            main_infos['__col__'] = prop
            if isinstance(prop, RelationshipProperty):
                join = str(prop.primaryjoin)
                if join in self.rels:
                    continue
                else:
                    self.rels.append(str(join))
                    main_infos['__prop__'] = SqlaContext(
                        prop.mapper,
                        rels=self.rels[:]
                    )

            res.append(main_infos)
        return res

    def compile_obj(self, obj):
        """
        generate a context based on the given obj

        :param obj: an instance of the model
        """
        res = {}
        for column in self.columns:
            if isinstance(column['__col__'], ColumnProperty):
                value = getattr(obj, column['__col__'].key)

            elif isinstance(column['__col__'], RelationshipProperty):
                # 1- si la relation est directe (une AppOption), on override le
                # champ avec la valeur (pour éviter des profondeurs)
                # 2- si l'objet lié est plus complexe, on lui fait son propre
                # chemin
                # 3- si la relation est uselist, on fait une liste d'élément
                # liés
                related = getattr(obj, column['__col__'].key)
                if related is None:
                    continue
                if column['__col__'].uselist:
                    value = []
                    for rel_obj in related:
                        value.append(column['__prop__'].compile_obj(rel_obj))
                else:

                    value = column['__prop__'].compile_obj(related)

            res[column['name']] = value

        return res
