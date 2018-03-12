# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    ForeignKey,
)
from sqlalchemy.orm import (
    relationship,
    deferred,
)

from autonomie_base.models.base import (
    DBBASE,
    DBSESSION,
    default_table_args,
)
from autonomie.forms import (
    EXCLUDED,
)

logger = logging.getLogger(__name__)


USER_GROUPS = Table(
    'user_groups',
    DBBASE.metadata,
    Column('login_id', Integer, ForeignKey('login.id')),
    Column('group_id', Integer, ForeignKey('groups.id')),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


class Group(DBBASE):
    """
    Available groups used in autonomie
    """
    __tablename__ = 'groups'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': EXCLUDED}
    )
    name = Column(
        String(30),
        nullable=False,
        info={'colanderalchemy': {'title': u"Nom du groupe"}}
    )
    label = deferred(
        Column(
            String(255),
            nullable=False,
            info={'colanderalchemy': {'title': u"Libellé"}},
        ),
        group="edit"
    )
    users = relationship(
        'Login',
        secondary=USER_GROUPS,
        back_populates='_groups',
    )

    @classmethod
    def _find_one(cls, name_or_id):
        """
        Used as a creator for the initialization proxy
        """
        with DBSESSION.no_autoflush:
            res = DBSESSION.query(cls).get(name_or_id)
            if res is None:
                # We try with the id
                res = DBSESSION.query(cls).filter(
                    cls.name == name_or_id
                ).one()

        return res

    def __json__(self, request):
        return dict(name=self.name, label=self.label)
