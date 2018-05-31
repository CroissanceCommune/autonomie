# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging

from hashlib import md5

from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    not_,
)
from sqlalchemy.orm import (
    relationship,
    load_only,
)
from sqlalchemy.ext.associationproxy import association_proxy

from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
    DBSESSION,
)
from autonomie.models.user.group import (
    USER_GROUPS,
    Group,
)

logger = logging.getLogger(__name__)


class Login(DBBASE):
    """
    Datas table containing login informations

    username/password
    """
    __tablename__ = 'login'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'exclude': True}}
    )
    login = Column(
        String(64),
        unique=True,
        nullable=False,
        info={'colanderalchemy': {'title': u'Identifiant'}}
    )

    pwd_hash = Column(
        String(100),
        info={
            'colanderalchemy':
            {
                'title': u'Mot de passe',
            },
            'export': {'exclude': True},
        },
        nullable=False,
    )
    active = Column(
        Boolean(),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
        default=True,
    )
    _groups = relationship(
        "Group",
        secondary=USER_GROUPS,
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'exclude': True}
        },
    )
    groups = association_proxy(
        "_groups",
        "name",
        creator=Group._find_one
    )
    user_id = Column(
        Integer,
        ForeignKey('accounts.id')
    )
    user = relationship(
        'User',
        info={'colanderalchemy': {'exclude': True}}
    )

    def __init__(self, user_id=None, login=None, password=None, groups=()):
        if user_id is not None:
            self.user_id = user_id
        if login is not None:
            self.login = login
        if password is not None:
            self.set_password(password)
        if groups:
            self.groups = groups
        self.active = True

    @staticmethod
    def _encode_pass(password):
        """
            Return a md5 encoded password
        """
        if isinstance(password, unicode):
            password = password.encode('utf-8')
        return md5(password).hexdigest()

    def set_password(self, password):
        """
            Set the user's password
        """
        logger.info(u"Modifying password : '{0}'".format(self.login))
        self.pwd_hash = self._encode_pass(password)

    def auth(self, password):
        """
        Auth a user

        :param str password: The password to check
        :returns: True or False
        :rtype: bool
        """
        if password and self.active:
            return self.pwd_hash == self._encode_pass(password)
        return False

    def primary_group(self):
        """
        Find a group that should be primary in the login's groups

        :returns: The group name
        :rtype: str
        """
        result = ""
        for group in self._groups:
            if group.primary:
                result = group.name
        return result

    @classmethod
    def query(cls, only_active=True):
        """
            Query users
        """
        query = super(Login, cls).query()
        if only_active:
            query = query.filter_by(active=True)

        return query

    @classmethod
    def unique_login(cls, login, login_id=None):
        """
        check that the given login is not yet in the database

            login

                A string for a login candidate

            login_id

                Optionnal login_id, if given, we will check all logins except
                this one (in case of edition)
        """
        query = cls.query(only_active=False)
        if login_id:
            query = query.filter(not_(cls.id == login_id))

        count = query.filter(cls.login == login).count()
        return count == 0

    @classmethod
    def unique_user_id(cls, user_id, login_id=None):
        """
        Check that no Login object is already associated to a User account with
        id user_id

            user_id

                A user id

            login_id

                Optionnal id, if given, we will check all logins except
                this one (in case of edition)
        """
        query = cls.query(only_active=False)
        if login_id:
            query = query.filter(not_(cls.id == login_id))

        return query.filter(cls.user_id == user_id).count() == 0

    @classmethod
    def id_from_login(cls, login):
        """
        Retrieve the Login instance matching with 'login'

        :param str login: The login string
        :returns: An id
        :rtype: int
        :raises: Error when no Login instance could be found
        """
        return cls.query().options(
            load_only('id')
        ).filter_by(login=login).one().id

    @classmethod
    def find_by_login(cls, login, active=True):
        query = DBSESSION().query(cls)
        query = query.options(load_only('pwd_hash'))
        query = query.filter_by(login=login)
        if active:
            query = query.filter_by(active=True)
        return query.first()
