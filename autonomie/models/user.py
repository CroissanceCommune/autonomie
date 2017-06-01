# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
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
#

"""
    User models
"""
import logging
import datetime
import colander
import deform

from hashlib import md5

from sqlalchemy import (
    Table,
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
    Boolean,
    Text,
    not_,
)

from sqlalchemy.orm import (
    relationship,
    backref,
    deferred,
)
from sqlalchemy.event import listen
from sqlalchemy.ext.associationproxy import association_proxy

from autonomie.views import render_api

from autonomie_base.models.base import (
    DBBASE,
    DBSESSION,
    default_table_args,
)
from autonomie.models.node import Node
from autonomie.models.company import CompanyActivity
from autonomie.forms import (
    get_hidden_field_conf,
    get_excluded,
    EXCLUDED,
    get_select,
    get_select_validator,
    get_deferred_select,
    mail_validator,
)
from autonomie_base.models.types import (
    JsonEncodedDict,
    PersistentACLMixin,
)
from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)
from autonomie_base.utils.date import str_to_date


ADMIN_PRIMARY_GROUP = 1
MANAGER_PRIMARY_GROUP = 2
CONTRACTOR_PRIMARY_GROUP = 3


# We need to store this datas here (before we find a solution to place a
# hashbang in an alembic migratino script)


COMPANY_EMPLOYEE = Table(
    'company_employee',
    DBBASE.metadata,
    Column("company_id", Integer, ForeignKey('company.id'), nullable=False),
    Column("account_id", Integer, ForeignKey('accounts.id'), nullable=False),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


USER_GROUPS = Table(
    'user_groups',
    DBBASE.metadata,
    Column('user_id', Integer, ForeignKey('accounts.id')),
    Column('group_id', Integer, ForeignKey('groups.id')),
    mysql_charset=default_table_args['mysql_charset'],
    mysql_engine=default_table_args['mysql_engine'],
)


SEX_OPTIONS = (
    ('', '', ),
    ('M', 'Homme', ),
    ('F', 'Femme', ),
)


CIVILITE_OPTIONS = (
    ('', u'Non renseigné', ),
    ('Monsieur', u'Monsieur',),
    ('Madame', u'Madame',),
)
# (célibataire, marié, veuf, divorcé, séparé, vie maritale, pacsé) .

STATUS_OPTIONS = (
    ('', '',),
    ('single', u"Célibataire", ),
    ('maried', u'Marié(e)', ),
    ('widow', u"Veuf(ve)", ),
    ('divorced', u"Divorcé(e)", ),
    ('isolated', u"Séparé(e)", ),
    ("free_union", u"Vie maritale", ),
    ('pacsed', u"Pacsé(e)", ),
)


CONTRACT_OPTIONS = (
    ('', '',),
    ('cdd', u'CDD',),
    ('cdi', u'CDI',),
)


log = logging.getLogger(__name__)


TEMPLATES_URL = 'autonomie:deform_templates/'
CLEAN_MAPPING_WIDGET = deform.widget.MappingWidget(
    template=TEMPLATES_URL + 'clean_mapping.pt'
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
    label = Column(
        String(255),
        nullable=False,
        info={'colanderalchemy': {'title': u"Libellé"}},
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


class User(DBBASE, PersistentACLMixin):
    """
        User model
    """
    __tablename__ = 'accounts'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': EXCLUDED},
    )

    login = deferred(
        Column(
            String(64),
            unique=True,
            nullable=False,
            info={'colanderalchemy': {'title': u'Identifiant'}}
        ),
        group='edit',
    )

    lastname = Column(
        String(50),
        info={'colanderalchemy': {'title': u'Nom'}},
        nullable=False,
    )

    firstname = Column(
        String(50),
        info={'colanderalchemy': {'title': u'Prénom'}},
        nullable=False,
    )

    active = deferred(
        Column(
            String(1),
            info={'colanderalchemy': EXCLUDED, 'export': EXCLUDED},
            default='Y',
            nullable=False,
        ),
        group='edit',
    )

    email = deferred(
        Column(
            String(100),
            info={
                'colanderalchemy': {
                    'title': u"Adresse e-mail",
                    'section': u'Coordonnées',
                    'validator': mail_validator(),
                }
            },
            nullable=False,
        ),
        group='edit',
    )

    pwd = deferred(
        Column(
            "password",
            String(100),
            info={
                'colanderalchemy':
                {
                    'title': u'Mot de passe',
                    'widget': deform.widget.CheckedPasswordWidget(),
                },
                'export': EXCLUDED,
            },
            nullable=False,
        ),
        group='edit',
    )

    companies = relationship(
        "Company",
        secondary=COMPANY_EMPLOYEE,
        backref=backref(
            "employees",
            info={
                'colanderalchemy': get_excluded(u'Employés'),
                'export': EXCLUDED
            },
        ),
        info={
            'colanderalchemy': get_excluded(u'Entreprises'),
            'export': EXCLUDED
        },
    )
    _groups = relationship(
        "Group",
        secondary=USER_GROUPS,
        backref=backref(
            "users",
            info={'colanderalchemy': EXCLUDED, 'export': EXCLUDED},
        ),
        info={'colanderalchemy': EXCLUDED, 'export': EXCLUDED},
    )
    groups = association_proxy(
        "_groups",
        "name",
        creator=Group._find_one
    )

    compte_tiers = deferred(
        Column(
            String(30),
            info={
                'colanderalchemy':
                {
                    'title': u'Compte tiers pour note de dépense',
                }
            },
            default="",
        ),
        group="edit",
    )

    session_datas = deferred(
        Column(
            JsonEncodedDict,
            info={'colanderalchemy': EXCLUDED, 'export': EXCLUDED},
            default=None,
        ),
        group="edit"
    )

    userdatas = relationship(
        "UserDatas",
        primaryjoin='User.id==UserDatas.user_id',
        back_populates='user',
        uselist=False,
        cascade='all, delete-orphan',
        info={
            'colanderalchemy': EXCLUDED,
            'export': {'exclude': True},
        }
    )

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
        log.info(u"Modifying password : '{0}'".format(self.login))
        self.pwd = self._encode_pass(password)

    def auth(self, password):
        """
            Authentify the current record with password
        """
        if password:
            return self.pwd == self._encode_pass(password)
        return False

    def get_company(self, cid):
        """
            Return the company
        """
        if not isinstance(cid, int):
            cid = int(cid)
        for company in self.companies:
            if company.id == cid:
                return company
        raise KeyError

    def has_userdatas(self):
        """
        Return True if the current object has userdatas associated to it
        """
        query = DBSESSION().query(UserDatas.id)
        query = query.filter(UserDatas.user_id == self.id)
        count = query.count()
        return count >= 1

    @classmethod
    def query(cls, ordered=True, only_active=True):
        """
            Query users
        """
        query = super(User, cls).query()
        if only_active:
            query = query.filter(User.active == 'Y')

        if ordered:
            query = query.order_by(User.lastname)

        return query

    @classmethod
    def unique_login(cls, login, user_id=None):
        """
        check that the given login is not yet in the database

            login

                A string for a login candidate

            user_id

                Optionnal user_id, if given, we will check all logins except
                this user's
        """
        query = cls.query(only_active=False)
        if user_id:
            query = query.filter(not_(cls.id == user_id))

        result = query.filter(cls.login == login).first()
        if result is not None:
            return False
        else:
            return True

    def disable(self):
        """
            disable a user
        """
        self.active = "N"

    def enable(self):
        """
            enable a user
        """
        self.active = "Y"

    def enabled(self):
        """
            is he enabled ?
        """
        return self.active == 'Y'

    def __unicode__(self):
        return u"<User {s.id} '{s.lastname} {s.firstname}'>".format(s=self)

    def __repr__(self):
        return self.__unicode__().encode('utf-8')

    def __json__(self, request):
        return dict(
            lastname=self.lastname,
            firstname=self.firstname,
        )

    @property
    def label(self):
        return u"{0} {1}".format(self.lastname, self.firstname)


def get_user_by_roles(roles):
    """
    Return user by primary roles
    """
    if len(roles) > 1:
        from sqlalchemy import or_
        clauses = []
        for role in roles:
            clauses.append(User.groups.contains(role))

        return User.query().filter(or_(*clauses))
    else:
        return User.query().filter(User.groups.contains(roles))


def get_users_options(roles=None):
    """
    Return the list of active users from the database formatted as choices:
        [(user_id, user_label)...]

    :param role: roles of the users we want
        default:  all
        values : ('contractor', 'manager', 'admin'))
    """
    if roles and not hasattr(roles, "__iter__"):
        roles = [roles]
    if roles:
        query = get_user_by_roles(roles)
    else:
        query = User.query()
    return [(unicode(u.id), render_api.format_account(u)) for u in query]


def get_deferred_user_choice(roles=None, widget_options=None):
    """
        Return a colander deferred for users selection options
    """
    widget_options = widget_options or {}
    default_option = widget_options.pop("default_option", None)

    @colander.deferred
    def user_select(node, kw):
        """
            Return a user select widget
        """
        choices = get_users_options(roles)
        if default_option:
            choices.insert(0, default_option)
        return deform.widget.Select2Widget(
            values=choices,
            **widget_options
            )
    return user_select


def user_node(roles=None, **kw):
    """
    Return a schema node for user selection
    roles: allow to restrict the selection to the given roles
        (to select between admin, contractor and manager)
    """
    widget_options = kw.pop('widget_options', {})
    return colander.SchemaNode(
        colander.Integer(),
        widget=get_deferred_user_choice(roles, widget_options),
        **kw
    )


class ZoneOption(ConfigurableOption):
    """
    Different type of geographical zones
    """
    __colanderalchemy_config__ = {
        'title': u"Zone d'habitation",
        'validation_msg': u"Les zones urbaines ont bien été configurées",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class ZoneQualificationOption(ConfigurableOption):
    """
    Different possible values to qualify a zone
    """
    __colanderalchemy_config__ = {
        'title': u"Qualificatif des zones d'habitation",
        'validation_msg': u"Les qualificatifs de zones urbaines ont bien \
été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class StudyLevelOption(ConfigurableOption):
    """
    Different values for study level
    """
    __colanderalchemy_config__ = {
        'title': u"Niveau d'étude",
        'validation_msg': u"Les niveaux d'étude ont bien été configurées",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class SocialStatusOption(ConfigurableOption):
    """
    Different values for social status
    """
    __colanderalchemy_config__ = {
        'title': u"Statut social à l'entrée dans la CAE",
        'validation_msg': u"Les statuts sociaux ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class EmployeeQualityOption(ConfigurableOption):
    """
    Different values for employee quality
    """
    __colanderalchemy_config__ = {
        'title': u"Qualité du salarié",
        'validation_msg': u"Les qualité du salarié ont bien été configurées",
        "help_msg": u"Configurer les options possibles pour définir la qualité\
 d'un salarié (cadre, employé ...)",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class ActivityTypeOption(ConfigurableOption):
    """
    Different possible values for activity type
    """
    __colanderalchemy_config__ = {
        'title': u"Typologie des métiers/secteurs d'activité",
        'validation_msg': u"Les typologie des métiers ont bien été configurées",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class PcsOption(ConfigurableOption):
    """
    Different possible value for Pcs
    """
    __colanderalchemy_config__ = {
        'title': u"Pcs",
        'validation_msg': u"Les options pour 'PCS' ont bien été configurées",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class PrescripteurOption(ConfigurableOption):
    """
    Different values for prescripteur
    """
    __colanderalchemy_config__ = {
        'title': u"Prescripteur",
        'validation_msg': u"Les différents prescripteurs ont bien \
été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class NonAdmissionOption(ConfigurableOption):
    """
    Possible values for refusing admission
    """
    __colanderalchemy_config__ = {
        'title': u"Motif de non admission",
        'validation_msg': u"Les motifs de non admission ont bien \
été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class ParcoursStatusOption(ConfigurableOption):
    """
    Possible values for status
    """
    __colanderalchemy_config__ = {
        'title': u"Statut du parcours",
        'validation_msg': u"Les statuts de parcours ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class CaeSituationOption(ConfigurableOption):
    """
    Possible values for the cae status "Situation actuelle dans la cae"
    """
    __colanderalchemy_config__ = {
        'title': u"Situation dans la CAE",
        'validation_msg': u"Les types de situations ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')
    # Is this element related to the integration process of a PP
    is_integration = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u'Donne droit à un compte Autonomie',
                'description': u"Si un porteur de projet a ce statut, \
un compte Autonomie lui sera automatiquement associé"
            }
        },
    )


class MotifSortieOption(ConfigurableOption):
    """
    Possible values for exit motivation
    """
    __colanderalchemy_config__ = {
        'title': u"Motif de sortie",
        'validation_msg': u"Les motifs de sortie ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class TypeSortieOption(ConfigurableOption):
    """
    Possible values for exit form
    """
    __colanderalchemy_config__ = {
        'title': u"Type de sortie",
        'validation_msg': u"Les types de sortie ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class SocialDocTypeOption(ConfigurableOption):
    """
    Different social doc types
    """
    __colanderalchemy_config__ = {
        "title": u"Type de document sociaux",
        'validation_msg': u"Les types de documents sociaux ont \
bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class AntenneOption(ConfigurableOption):
    """
    Different antenne
    """
    __colanderalchemy_config__ = {
        "title": u"Antennes de la CAE",
        'validation_msg': u"Les antennes ont bien été configurées",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class UserDatasSocialDocTypes(DBBASE):
    """
    relationship table used between social document types and user datas set
    """
    __tablename__ = 'userdatas_socialdocs'
    __table_args__ = default_table_args
    __colanderalchemy_config__ = {
        'css': "text-right",
    }
    userdatas_id = Column(
        ForeignKey('user_datas.id'),
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {'exclude': True},
        },
    )

    doctype_id = Column(
        ForeignKey('social_doc_type_option.id'),
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {
                'exclude': True,
                'stats': {'exclude': False, 'label': u"Type de documents"},
            }
        },
    )

    status = Column(
        Boolean(),
        default=False,
        info={
            'export': {
                'exclude': True,
                'stats': {'exclude': False, 'label': u"A été fourni ?"},
            }
        },
    )
    userdatas = relationship(
        'UserDatas',
        backref=backref(
            'doctypes_registrations',
            cascade='all, delete-orphan',
            info={
                'colanderalchemy': EXCLUDED,
                "export": {
                    'exclude': True,
                    'stats': {
                        'exclude': False,
                        'label': u"Documents sociaux - ",
                    }
                }
            },
        ),
        info={'colanderalchemy': EXCLUDED, "export": EXCLUDED},
    )

    doctype = relationship(
        "SocialDocTypeOption",
        backref=backref(
            'registration',
            cascade='all, delete-orphan',
            info={'colanderalchemy': EXCLUDED},
        ),
        info={
            'colanderalchemy': EXCLUDED,
            "export": {
                'exclude': True,
                'stats': {
                    'exclude': False,
                }
            }
        },
    )


def get_dict_key_from_value(val, dict_):
    for key, value in dict_.items():
        if value == val:
            return key
    raise KeyError()


class UserDatas(Node):
    __tablename__ = 'user_datas'
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'userdata'}

    id = Column(
        ForeignKey('node.id'),
        primary_key=True,
        info={
            'colanderalchemy': {
                'exclude': True,
                'title': u"Identifiant Autonomie"
            },
        }
    )

    # User account associated with this dataset
    user_id = Column(
        ForeignKey('accounts.id'),
        info={
            'colanderalchemy': EXCLUDED,
            'export': {'exclude': True},
        }
    )
    user = relationship(
        "User",
        primaryjoin='User.id==UserDatas.user_id',
        info={
            'colanderalchemy': get_excluded(u'Compte utilisateur'),
            'export': {'exclude': True},
        }
    )

    # INFORMATIONS GÉNÉRALES : CF CAHIER DES CHARGES #
    situation_history = relationship(
        "CaeSituationChange",
        order_by="CaeSituationChange.date",
        info={
            'colanderalchemy': EXCLUDED,
            'export': {
                "flatten": [
                    ('date', u'Date'),
                    ('situation.label', u"Situation"),
                ],
                'label': u"Changement de situation",
            },
        },
    )
    situation_situation_id = Column(
        ForeignKey("cae_situation_option.id"),
        nullable=False,
        info={
            'colanderalchemy':
            {
                'title': u"Situation actuelle dans la CAE",
                'section': u'Synthèse',
                'widget': get_deferred_select(CaeSituationOption),
            }
        }
    )

    situation_situation = relationship(
        "CaeSituationOption",
        info={
            'colanderalchemy': get_excluded(u'Situation dans la CAE'),
            'export': {'related_key': 'label'},
        },
    )

    situation_antenne_id = Column(
        ForeignKey('antenne_option.id'),
        info={
            'colanderalchemy': {
                'title': u"Antenne de rattachement",
                "section": u"Synthèse",
                'widget': get_deferred_select(AntenneOption),
            }
        }
    )
    situation_antenne = relationship(
        "AntenneOption",
        info={
            'colanderalchemy': get_excluded(u"Antenne de rattachement"),
            'export': {'related_key': 'label'},
        },
    )

    situation_follower_id = Column(
        ForeignKey('accounts.id'),
        info={
            'colanderalchemy': {
                'title': u'Accompagnateur',
                'section': u'Synthèse',
                'widget': get_deferred_user_choice(
                    roles=['admin', 'manager'],
                    widget_options={
                        'default_option': ('', ''),
                    }
                ),
            },
            # 'export': {'exclude': True},
        },
    )

    situation_follower = relationship(
        "User",
        primaryjoin='User.id==UserDatas.situation_follower_id',
        backref=backref(
            "followed_contractors",
            info={
                'colanderalchemy': EXCLUDED,
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': get_excluded(u'Conseiller'),
            'export': {
                'related_key': 'lastname',
                'label': u"Conseiller",
            },
            'import': {
                'related_key': 'login',
            }
        }
    )

    situation_societariat_entrance = Column(
        Date(),
        info={
            'colanderalchemy': {
                'title': u"Date d'entrée au sociétariat",
                'section': u'Synthèse',
            },
        },
        default=None,
    )

    # COORDONNÉES : CF CAHIER DES CHARGES #
    coordonnees_civilite = Column(
        String(10),
        info={
            'colanderalchemy': {
                'title': u'Civilité',
                'section': u"Coordonnées",
                'widget': get_select(CIVILITE_OPTIONS),
            },
            'export': {
                'formatter': lambda val: dict(CIVILITE_OPTIONS).get(val),
                'stats': {'options': CIVILITE_OPTIONS},
            }
        },
        default=CIVILITE_OPTIONS[0][0],
        nullable=False,
    )

    coordonnees_lastname = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u"Nom",
                'section': u'Coordonnées',
            },
        },
        nullable=False,
    )

    coordonnees_firstname = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u"Prénom",
                'section': u'Coordonnées',
            },
        },
        nullable=False,
    )

    coordonnees_ladies_lastname = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u"Nom de jeune fille",
                'section': u'Coordonnées',
            },
        },
    )

    coordonnees_email1 = Column(
        String(100),
        info={
            'colanderalchemy': {
                'title': u"E-mail 1",
                'section': u'Coordonnées',
                'validator': mail_validator(),
            }
        },
        nullable=False,
    )

    coordonnees_email2 = Column(
        String(100),
        info={
            'colanderalchemy': {
                'title': u"E-mail 2",
                'section': u'Coordonnées',
                'validator': mail_validator(),
            }
        }
    )

    coordonnees_tel = Column(
        String(14),
        info={
            'colanderalchemy': {
                'title': u"Tél. fixe",
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_mobile = Column(
        String(14),
        info={
            'colanderalchemy': {
                'title': u"Tél. mobile",
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_address = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u'Adresse',
                'section': u'Coordonnées',
                'widget': deform.widget.TextAreaWidget(),
            }
        }
    )

    coordonnees_zipcode = Column(
        String(7),
        info={
            'colanderalchemy': {
                'title': u'Code postal',
                'section': u'Coordonnées',
            },
            'py3o': {
                'formatter': lambda z: u"%05d" % z
            }
        }
    )

    coordonnees_city = Column(
        String(100),
        info={
            'colanderalchemy': {
                'title': u"Ville",
                'section': u'Coordonnées',
            }
        },
    )

    coordonnees_zone_id = Column(
        ForeignKey('zone_option.id'),
        info={
            'colanderalchemy': {
                'title': "Zone d'habitation",
                'section': u'Coordonnées',
                'widget': get_deferred_select(
                    ZoneOption
                ),
            },
        }
    )

    coordonnees_zone = relationship(
        'ZoneOption',
        info={
            'colanderalchemy': get_excluded(u"Zone d'habitation"),
            'export': {'related_key': 'label'},
        },
    )

    coordonnees_zone_qual_id = Column(
        ForeignKey('zone_qualification_option.id'),
        info={
            'colanderalchemy': {
                'title': u"Qualification de la zone d'habitation",
                'section': u'Coordonnées',
                'widget': get_deferred_select(
                    ZoneQualificationOption
                ),
            }
        }
    )

    coordonnees_zone_qual = relationship(
        'ZoneQualificationOption',
        info={
            'colanderalchemy': get_excluded(
                u"Qualification de la zone d'habitation"
            ),
            'export': {'related_key': 'label'},
        },
    )

    coordonnees_sex = Column(
        String(1),
        info={
            'colanderalchemy': {
                'title': u'Sexe',
                'section': u'Coordonnées',
                'widget': get_select(SEX_OPTIONS),
                'validator': get_select_validator(SEX_OPTIONS),
            },
            'export': {'stats': {'options': SEX_OPTIONS}},
        }
    )

    coordonnees_birthday = Column(
        Date(),
        info={
            'colanderalchemy': {
                'title': u'Date de naissance',
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_birthplace = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u'Lieu de naissance',
                'section': u'Coordonnées',
                'widget': deform.widget.TextAreaWidget(),
            }
        }
    )

    coordonnees_birthplace_zipcode = Column(
        String(7),
        info={
            'colanderalchemy': {
                'title': u'Code postal de naissance',
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_nationality = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u'Nationalité',
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_resident = Column(
        Date(),
        info={
            'colanderalchemy': {
                'title': u'Carte de séjour (fin de validité)',
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_secu = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u'Numéro de sécurité sociale',
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_family_status = Column(
        String(20),
        info={
            'colanderalchemy': {
                'title': u'Situation de famille',
                'section': u'Coordonnées',
                'widget': get_select(STATUS_OPTIONS),
                'validator': get_select_validator(STATUS_OPTIONS),
            },
            'export': {
                'formatter': lambda val: dict(STATUS_OPTIONS).get(val),
                'stats': {'options': STATUS_OPTIONS},
            }
        }
    )

    coordonnees_children = Column(
        Integer(),
        default=0,
        info={
            'colanderalchemy': {
                'title': u"Nombre d'enfants",
                'section': u'Coordonnées',
                'widget': get_select(zip(range(20), range(20))),
            }
        }
    )

    coordonnees_study_level_id = Column(
        ForeignKey('study_level_option.id'),
        info={
            'colanderalchemy': {
                'title': u"Niveau d'études",
                'section': u'Coordonnées',
                'widget': get_deferred_select(StudyLevelOption),
            }
        }
    )

    coordonnees_study_level = relationship(
        'StudyLevelOption',
        info={
            'colanderalchemy': get_excluded(u"Niveau d'études"),
            'export': {'related_key': 'label'},
        },
    )
    coordonnees_emergency_name = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u"Contact urgent : Nom",
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_emergency_phone = Column(
        String(14),
        info={
            'colanderalchemy': {
                'title': u'Contact urgent : Téléphone',
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_identifiant_interne = Column(
        String(20),
        info={
            'colanderalchemy': {
                'title': u'Identifiant interne',
                'description': u"Identifiant interne propre à la CAE \
(facultatif)",
                'section': u'Coordonnées',
            }
        }
    )

    # STATUT
    statut_social_status_id = Column(
        ForeignKey('social_status_option.id'),
        info={
            'colanderalchemy':
            {
                'title': u"Statut social à l'entrée",
                'section': u'Statut',
                'widget': get_deferred_select(SocialStatusOption),
            }
        }
    )

    statut_social_status = relationship(
        'SocialStatusOption',
        primaryjoin='UserDatas.statut_social_status_id==SocialStatusOption.id',
        info={
            'colanderalchemy': get_excluded(u"Statut social à l'entrée"),
            'export': {'related_key': 'label'},
        },
    )

    statut_social_status_today_id = Column(
        ForeignKey('social_status_option.id'),
        info={
            'colanderalchemy':
            {
                'title': u"Statut social actuel",
                'section': u'Statut',
                'widget': get_deferred_select(SocialStatusOption),
            },
        }
    )
    statut_social_status_today = relationship(
        'SocialStatusOption',
        primaryjoin='UserDatas.statut_social_status_today_id==\
SocialStatusOption.id',
        info={
            'colanderalchemy': get_excluded(u"Statut social actuel"),
            'export': {
                'related_key': 'label',
            },
        },
    )

    statut_handicap_allocation_expiration = Column(
        Date(),
        default=None,
        info={
            'colanderalchemy':
            {
                'title': u"Allocation adulte handicapé - échéance (expiration)",
                'section': u'Statut',
            }
        }
    )

    statut_external_activity = relationship(
        "ExternalActivityDatas",
        cascade="all, delete-orphan",
        info={
            'colanderalchemy':
            {
                'title': u'Activité externe',
                'section': u'Statut',
            },
            'export': {
                'flatten': [
                    ('type', u"Type de contrat"),
                    ('hours', u'Heures'),
                    ('brut_salary', u"Salaire brut"),
                    ('employer_visited', u"Visite employeur"),
                ],
            }
        },
        backref=backref(
            'userdatas',
            info={
                'export': {
                    'related_key': u"export_label",
                    "keep_key": True,
                    "label": u"Porteur de projet",
                    "stats": EXCLUDED,
                }
            }
        ),
    )

    statut_end_rights_date = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u'Date de fin de droit',
                'section': u'Statut',
            }
        }
    )

    # ACTIVITÉ : cf cahier des charges
    activity_typologie_id = Column(
        ForeignKey('activity_type_option.id'),
        info={
            'colanderalchemy':
            {
                'title': u"Typologie des métiers/secteurs d'activités",
                'section': u'Activité',
                'widget': get_deferred_select(ActivityTypeOption),
            }
        }
    )

    activity_typologie = relationship(
        'ActivityTypeOption',
        info={
            'colanderalchemy': get_excluded(
                u"Typologie des métiers/secteurs d'activités"
            ),
            'export': {'related_key': 'label'},
        },
    )
    activity_pcs_id = Column(
        ForeignKey('pcs_option.id'),
        info={
            'colanderalchemy':
            {
                'title': u"PCS",
                'section': u'Activité',
                'widget': get_deferred_select(PcsOption),
            }
        }
    )

    activity_pcs = relationship(
        'PcsOption',
        info={
            'colanderalchemy': get_excluded(u"PCS"),
            'export': {'related_key': 'label'},
        },
    )
    activity_companydatas = relationship(
        "CompanyDatas",
        cascade="all, delete-orphan",
        backref=backref(
            'userdatas',
            info={
                'export': {
                    'related_key': u"export_label",
                    "keep_key": True,
                    "label": u"Porteur de projet",
                    "stats": EXCLUDED,
                }
            }
        ),
        info={
            'colanderalchemy':
            {
                'title': u'Activités',
                'section': u'Activité',
            },
            'export': {
                'flatten': [
                    ('title', u"Titre de l'activité"),
                    ('name', u"Nom commercial"),
                    ('website', u"Site internet"),
                ]
            }
        }
    )

    # PARCOURS : cf cahier des charges
    parcours_prescripteur_id = Column(
        ForeignKey('prescripteur_option.id'),
        info={
            'colanderalchemy':
            {
                'title': u'Prescripteur',
                'section': u'Parcours',
                'widget': get_deferred_select(PrescripteurOption),
            }
        }
    )

    parcours_prescripteur = relationship(
        "PrescripteurOption",
        info={
            'colanderalchemy': get_excluded(u"Prescripteur"),
            'export': {'related_key': 'label'},
        },
    )
    parcours_prescripteur_name = Column(
        String(50),
        info={
            'colanderalchemy':
            {
                'title': u'Nom du prescripteur',
                'section': u'Parcours',
            }
        }
    )

    parcours_date_info_coll = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u'Date info coll',
                'section': u'Parcours',
            }
        }
    )

    parcours_date_diagnostic = relationship(
        "DateDiagnosticDatas",
        cascade="all, delete-orphan",
        backref=backref(
            'userdatas',
            info={
                'export': {
                    'related_key': u"export_label",
                    "keep_key": True,
                    "label": u"Porteur de projet",
                    "stats": EXCLUDED,
                }
            }
        ),
        info={
            'colanderalchemy':
            {
                'title': u'Date diagnostic',
                'section': u'Parcours',
            },
            'import': {
                "related_key": "date",
                "formatter": str_to_date
            },
            'export': {
                'flatten': [('date', u"Date")],
            }
        }
    )

    parcours_non_admission_id = Column(
        ForeignKey('non_admission_option.id'),
        info={
            'colanderalchemy':
            {
                'title': u'Motif de non admission en CAE',
                'section': u'Parcours',
                'widget': get_deferred_select(NonAdmissionOption)
            }
        }
    )

    parcours_non_admission = relationship(
        "NonAdmissionOption",
        info={
            'colanderalchemy': get_excluded(
                u'Motif de non admission en CAE'
            ),
            'export': {'related_key': 'label'},
        },
    )

    parcours_convention_cape = relationship(
        "DateConventionCAPEDatas",
        cascade='all, delete-orphan',
        backref=backref(
            'userdatas',
            info={
                'export': {
                    'related_key': u"export_label",
                    "keep_key": True,
                    "label": u"Porteur de projet",
                    "stats": EXCLUDED,
                }
            }
        ),
        info={
            'colanderalchemy': {
                "title": u"Date convention CAPE",
                'section': u'Parcours',
            },
            'import': {
                'related_key': 'date',
                "formatter": str_to_date
            },
            'export': {
                'flatten': [('date', u"Date")],
            }
        }
    )

    parcours_dpae = relationship(
        "DateDPAEDatas",
        cascade='all, delete-orphan',
        backref=backref(
            'userdatas',
            info={
                'export': {
                    'related_key': u"export_label",
                    "keep_key": True,
                    "label": u"Porteur de projet",
                    "stats": EXCLUDED,
                }
            }
        ),
        info={
            'colanderalchemy': {
                "title": u"Date DPAE",
                'section': u'Parcours',
            },
            'import': {
                'related_key': 'date',
                "formatter": str_to_date
            },
            'export': {
                'flatten': [('date', u"Date")],
            }
        }
    )

    parcours_contract_type = Column(
        String(4),
        info={
            'colanderalchemy':
            {
                'title': u'Type de contrat',
                'section': u'Parcours',
                'widget': get_select(CONTRACT_OPTIONS)
            },
            'export': {
                'formatter': lambda val: dict(CONTRACT_OPTIONS).get(val),
                'stats': {'options': CONTRACT_OPTIONS},
            }
        }
    )

    parcours_start_date = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u"Date de début de contrat",
                'description': u'Date du Cdi ou du début de Cdd',
                "section": u"Parcours",
            }
        }
    )

    parcours_end_date = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u"Date de fin de contrat",
                'description': u'Date de fin de Cdd',
                "section": u"Parcours",
            }
        }
    )

    parcours_contract_history = relationship(
        "ContractHistory",
        cascade='all, delete-orphan',
        info={
            'colanderalchemy': {
                "title": u"Avenants au contrat de travail",
                'section': u'Parcours',
            },
            'export': {
                'flatten': [
                    ('date', u"Date"),
                    ('number', u"Numéro d'avenant"),
                ],
            }
        }
    )

    # To be removed in version > 3.3.0
    parcours_last_avenant = Column(
        Date(),
        info={'colanderalchemy': EXCLUDED},
    )

    parcours_taux_horaire = Column(
        Float(),
        info={
            'colanderalchemy':
            {
                'title': u'Taux horaire',
                'section': u'Parcours',
            }
        }
    )

    parcours_taux_horaire_letters = Column(
        String(250),
        info={
            'colanderalchemy':
            {
                'title': u'Taux horaire (en lettres)',
                'section': u'Parcours',
            }
        }
    )

    parcours_num_hours = Column(
        Float(),
        info={
            'colanderalchemy':
            {
                'title': u"Nombre d'heures",
                "section": u"Parcours",
            }
        }
    )

    parcours_salary = Column(
        Float(),
        info={
            'colanderalchemy':
            {
                'title': u"Salaire brut",
                'section': u'Parcours',
                'widget': deform.widget.TextInputWidget(readonly=True),
                'description': u"Ce champ est rempli automatiquement",
            }
        }
    )

    parcours_salary_letters = Column(
        String(100),
        info={
            'colanderalchemy':
            {
                'title': u"Salaire en lettres",
                'section': u'Parcours',
            }
        }
    )

    parcours_employee_quality_id = Column(
        ForeignKey('employee_quality_option.id'),
        info={
            'colanderalchemy':
            {
                'title': u"Qualité du salarié",
                'section': u'Parcours',
                'widget': get_deferred_select(EmployeeQualityOption),
            }
        }
    )
    parcours_employee_quality = relationship(
        'EmployeeQualityOption',
        info={
            'colanderalchemy': get_excluded(u"Qualité du salarié"),
            'export': {'related_key': 'label'},
        }
    )

    parcours_goals = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Objectifs",
                "section": u"Parcours",
                "widget": deform.widget.TextAreaWidget(),
            }
        }
    )

    parcours_status_id = Column(
        ForeignKey("parcours_status_option.id"),
        info={
            'colanderalchemy':
            {
                'title': u"Aptitude",
                'section': u'Parcours',
                'widget': get_deferred_select(ParcoursStatusOption),
            }
        }
    )
    parcours_status = relationship(
        "ParcoursStatusOption",
        info={
            'colanderalchemy': get_excluded(u"Aptitude"),
            'export': {'related_key': 'label'},
        },
    )
    parcours_medical_visit = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u"Date de la visite médicale",
                'section': u'Parcours',
            }
        }
    )

    parcours_medical_visit_limit = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u"Date limite",
                'section': u'Parcours',
            }
        }
    )

    # SORTIE
    sortie_date = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u"Date de sortie",
                'section': u'Sortie',
            }
        }
    )

    sortie_motif_id = Column(
        ForeignKey('motif_sortie_option.id'),
        info={
            'colanderalchemy':
            {
                'title': u"Motif de sortie",
                'section': u'Sortie',
                'widget': get_deferred_select(MotifSortieOption),
            }
        }
    )

    sortie_motif = relationship(
        'MotifSortieOption',
        info={
            'colanderalchemy': get_excluded(u"Motif de sortie"),
            'export': {'related_key': 'label'},
        },
    )

    sortie_type_id = Column(
        ForeignKey('type_sortie_option.id'),
        info={
            'colanderalchemy':
            {
                'title': u"Type de sortie",
                'section': u'Sortie',
                'widget': get_deferred_select(TypeSortieOption),
            }
        }
    )

    sortie_type = relationship(
        'TypeSortieOption',
        info={
            'colanderalchemy': get_excluded(u"Type de sortie"),
            'export': {'related_key': 'label'},
        },
    )

    @property
    def export_label(self):
        return u"{0} {1}".format(
            self.coordonnees_lastname,
            self.coordonnees_firstname,
        )

    def __unicode__(self):
        return u"<Userdatas : {0} {1} {2}>".format(
            self.id,
            self.coordonnees_lastname,
            self.coordonnees_firstname
        )

    @property
    def age(self):
        birthday = self.coordonnees_birthday
        now = datetime.date.today()
        years = now.year - birthday.year
        # We translate the "now" date to know if his birthday has passed or not
        translated_now = datetime.date(birthday.year, now.month, now.day)
        if translated_now < birthday:
            years -= 1
        return years

    def gen_user_account(self):
        """
        Generate a user account for the given model
        """
        from autonomie_base.utils.ascii import gen_random_string
        if self.situation_situation.is_integration:
            if self.user_id is None:
                login = self.coordonnees_email1
                index = 0
                # Fix #165: check login on account generation
                while User.query().filter(User.login == login).count() > 0:
                    login = u"{0}_{1}".format(index, login)
                    index += 1

                password = gen_random_string(6)
                user = User(
                    login=login,
                    firstname=self.coordonnees_firstname,
                    lastname=self.coordonnees_lastname,
                    email=self.coordonnees_email1,
                )
                user.set_password(password)
                self.user = user
                return user, login, password
            else:
                return self.user, self.user.login, None
        return None, None, None

    def gen_companies(self):
        """
        Generate companies as expected
        """
        from autonomie.models.company import Company
        companies = []
        if self.situation_situation.is_integration:
            if self.user_id is None:
                for data in self.activity_companydatas:
                    # Try to retrieve an existing company (and avoid duplicates)
                    company = Company.query().filter(
                        Company.name == data.name
                    ).first()
                    if company is None:
                        company = Company(
                            name=data.name,
                            goal=data.title,
                            email=self.coordonnees_email1,
                            phone=self.coordonnees_tel,
                            mobile=self.coordonnees_mobile,
                        )
                        if data.activity is not None:
                            company.activities.append(data.activity)
                    companies.append(company)
            else:
                pass
        return companies


# One to one test relationship

# class ExtendedUserDatas(DBBASE):
#    """
#    Datas extension
#    """
#    id = Column(
#        ForeignKey(UserDatas.id),
#        primary_key=True,
#        info={
#            'colanderalchemy': EXCLUDED,
#            'export': {'label': 'Extension'},
#        }
#    )
#    test_value = Column(
#        String(255),
#        info={
#            'colanderalchemy': {
#                'section': 'Custom datas',
#                'title': u"Valeur test"
#            }
#        }
#    )
#    userdata = relationship(
#        UserDatas,
#        backref=backref(
#            'extension',
#            uselist=False,
#            info={
#                'colanderalchemy': {'section': 'Custom datas',},
#                'export': {'label': 'Extension', }
#            }
#        ),
#        uselist=False,
#    )
#

# multi-valued user-datas
class ExternalActivityDatas(DBBASE):
    """
    Datas related to external activities
    """
    __colanderalchemy_config__ = {
        'title': u"une activité Externe à la CAE",
        'widget': CLEAN_MAPPING_WIDGET,
    }
    __tablename__ = 'external_activity_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {'exclude': True},
        }
    )
    type = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u"Type de contrat",
                'widget': get_select(CONTRACT_OPTIONS),
            },
            'export': {'stats': {'options': CONTRACT_OPTIONS}},
        }
    )
    hours = Column(
        Float(),
        info={
            'colanderalchemy': {
                'title': u"Nombre d'heures",
            }
        }
    )
    brut_salary = Column(
        Float(),
        info={
            'colanderalchemy': {
                'title': u'Salaire brut',
            }
        }
    )
    employer_visited = Column(
        Boolean(),
        default=False,
        info={
            'colanderalchemy': {
                'title': u'Visite autre employeur',
            }
        }
    )
    userdatas_id = Column(
        ForeignKey('user_datas.id'),
        info={
            'colanderalchemy': EXCLUDED,
            'export': {
                'label': u"Identifiant Autonomie",
                'stats': EXCLUDED,
            }
        },
    )


class CompanyDatas(DBBASE):
    __colanderalchemy_config__ = {
        'title': u"une activité",
        'widget': CLEAN_MAPPING_WIDGET,
    }
    __tablename__ = 'company_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {'exclude': True},
        }
    )
    title = Column(
        String(250),
        info={
            "colanderalchemy":
            {
                'title': u"Titre de l'activité",
            }
        },
        nullable=False,
    )
    name = Column(
        String(100),
        info={
            "colanderalchemy":
            {
                'title': u"Nom commercial",
            }
        },
        nullable=False,
    )
    website = Column(
        String(100),
        info={
            "colanderalchemy":
            {
                'title': u"Site internet",
            }
        }
    )
    activity_id = Column(
        ForeignKey("company_activity.id"),
        info={
            'colanderalchemy': {
                'title': u"Domaine d'activité",
                "widget": get_deferred_select(
                    CompanyActivity
                ),
            }
        }
    )

    activity = relationship(
        "CompanyActivity",
        info={
            'colanderalchemy': EXCLUDED,
            'export': {'related_key': 'label'},
        }
    )
    userdatas_id = Column(
        ForeignKey("user_datas.id"),
        info={
            'colanderalchemy': EXCLUDED,
            'export': {
                'label': u"Identifiant Autonomie",
                'stats': EXCLUDED,
            }
        }
    )


class DateDiagnosticDatas(DBBASE):
    __colanderalchemy_config__ = {
        'title': u"une date de diagnostic",
        'widget': CLEAN_MAPPING_WIDGET,
    }
    __tablename__ = 'date_diagnostic_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {'exclude': True},
        }
    )
    date = Column(
        Date(),
        info={
            'colanderalchemy': {
                "title": u'Date du diagnostic',
            }
        },
        nullable=False
    )
    userdatas_id = Column(
        ForeignKey("user_datas.id"),
        info={
            'colanderalchemy': EXCLUDED,
            'export': {
                'label': u"Identifiant Autonomie",
                'stats': EXCLUDED,
            }
        }
    )


class DateConventionCAPEDatas(DBBASE):
    __colanderalchemy_config__ = {
        'title': u"une date de convention CAPE",
        'widget': CLEAN_MAPPING_WIDGET,
    }
    __tablename__ = 'date_convention_cape_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {'exclude': True},
        }
    )
    date = Column(
        Date(),
        info={
            "colanderalchemy": {
                "title": u'Date de la convention',
            }
        },
        nullable=False,
    )
    end_date = Column(
        Date(),
        info={
            "colanderalchemy": {
                "title": u'Date de fin de la convention',
            }
        }
    )
    userdatas_id = Column(
        ForeignKey("user_datas.id"),
        info={
            'colanderalchemy': EXCLUDED,
            'export': {
                'label': u"Identifiant Autonomie",
                'stats': EXCLUDED,
            }
        }
    )


class DateDPAEDatas(DBBASE):
    __colanderalchemy_config__ = {
        'title': u"une date de DPAE",
        'widget': CLEAN_MAPPING_WIDGET,
    }
    __tablename__ = 'date_dpae_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {'exclude': True},
        }
    )
    date = Column(
        Date(),
        info={
            'colanderalchemy': {
                "title": u'Date de la DPAE',
            }
        },
        nullable=False,
    )
    userdatas_id = Column(
        ForeignKey("user_datas.id"),
        info={
            'colanderalchemy': EXCLUDED,
            'export': {
                'label': u"Identifiant autonomie",
                'stats': EXCLUDED,
            }
        }
    )


class CaeSituationChange(DBBASE):
    """
    Used to store cae status change
    """
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {'exclude': True},
        }
    )
    date = Column(
        Date(),
        info={
            'colanderalchemy': {
                "title": u'Date du changement de situation',
            }
        },
        nullable=False,

    )
    userdatas_id = Column(
        ForeignKey("user_datas.id"),
        info={
            'colanderalchemy': EXCLUDED,
            'export': {
                'label': u"Identifiant autonomie",
                'stats': EXCLUDED,
            }
        }
    )
    situation_id = Column(
        ForeignKey("cae_situation_option.id"),
        nullable=False,
        info={
            'colanderalchemy':
            {
                'title': u"Situation dans la CAE",
                'widget': get_deferred_select(CaeSituationOption),
            }
        }
    )
    situation = relationship(
        "CaeSituationOption",
        info={
            'colanderalchemy': get_excluded(u"Situation dans la CAE"),
            'export': {'related_key': 'label'},
        },
    )


class ContractHistory(DBBASE):
    """
    Used to store history of contract updates
    """
    __colanderalchemy_config__ = {
        'title': u"un avenant",
        'widget': CLEAN_MAPPING_WIDGET,
    }
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {'exclude': True},
        }
    )
    date = Column(
        Date(),
        info={
            'colanderalchemy': {
                "title": u"Date d'effet",
            }
        },
        nullable=False,
    )
    number = Column(
        Integer,
        info={
            'colanderalchemy': {
                "title": u"Numéro",
            }
        },
        nullable=False,
    )
    userdatas_id = Column(
        ForeignKey("user_datas.id"),
        info={
            'colanderalchemy': EXCLUDED,
            'export': {
                'label': u"Identifiant autonomie",
                'stats': EXCLUDED,
            }
        }
    )
    userdatas = relationship(
        "UserDatas",
        back_populates='parcours_contract_history',
        info={
            'colanderalchemy': EXCLUDED,
            'export': {
                'related_key': u"export_label",
                "keep_key": True,
                "label": u"Historique des avenants",
                "stats": EXCLUDED,
            }
        }
    )


USERDATAS_FORM_GRIDS = {
    u"Synthèse": (
        (('situation_situation_id', 6),),
        (('situation_follower_id', 6), ('situation_antenne_id', 6)),
        (('situation_societariat_entrance', 6),),
    ),
    u"Coordonnées": (
        (
            ('coordonnees_civilite', 3),
            ('coordonnees_lastname', 3),
            ('coordonnees_firstname', 3),
            ('coordonnees_ladies_lastname', 3)
        ),
        (
            ('coordonnees_email1', 3),
            ('coordonnees_email2', 3),
        ),
        (
            ('coordonnees_tel', 3),
            ('coordonnees_mobile', 3),
        ),
        (
            ('coordonnees_address', 3),
            ('coordonnees_zipcode', 3),
            ('coordonnees_city', 3),
        ),
        (
            ('coordonnees_zone_id', 3),
            ('coordonnees_zone_qual_id', 3),
        ),
        (
            ('coordonnees_sex', 3),
            ('coordonnees_birthday', 3),
            ('coordonnees_birthplace', 3),
            ('coordonnees_birthplace_zipcode', 3),
        ),
        (
            ('coordonnees_nationality', 3),
            ('coordonnees_resident', 3),
        ),
        (
            ('coordonnees_secu', 3),
        ),
        (
            ('coordonnees_family_status', 3),
            ('coordonnees_children', 3),
            ('coordonnees_study_level_id', 3),
        ),
        (
            ('coordonnees_emergency_name', 3),
            ('coordonnees_emergency_phone', 3),
        ),
        (
            ('coordonnees_identifiant_interne', 3),
        ),
    ),
    u"Parcours": (
        (
            ('parcours_prescripteur_id', 3),
            ('parcours_prescripteur_name', 3),
        ),
        (
            ('parcours_date_info_coll', 3),
        ),
        (
            ('parcours_date_diagnostic', 12),
        ),
        (
            ('parcours_non_admission_id', 3),
        ),
        (
            ('parcours_convention_cape', 6),
            ('parcours_dpae', 6),
        ),
        (
            ('parcours_contract_type', 3),
            ('parcours_start_date', 3),
            ('parcours_end_date', 3),
        ),
        (
            ('parcours_taux_horaire', 3),
            ('parcours_taux_horaire_letters', 3),
            ('parcours_num_hours', 3),
            ('parcours_salary', 3),
        ),
        (
            ('parcours_salary_letters', 6),
            ('parcours_employee_quality_id', 3),
        ),
        (
            ('parcours_contract_history', 6),
        ),
        (
            ('parcours_goals', 6),
        ),
        (
            ('parcours_status_id', 6),
        ),
        (
            ('parcours_medical_visit', 3),
            ('parcours_medical_visit_limit', 3),
        ),
    ),

}


def salary_compute(mapper, connection, target):
    """
    Compute the salary of a user
    """
    val1 = target.parcours_taux_horaire
    val2 = target.parcours_num_hours
    try:
        res = val1 * val2
    except:
        res = 0
    target.parcours_salary = res


listen(UserDatas, "before_insert", salary_compute, propagate=True)
listen(UserDatas, "before_update", salary_compute, propagate=True)


# Registering event handlers to keep datas synchronized
def sync_user_to_userdatas(key):
    def handler(target, value, oldvalue, initiator):
        if target.userdatas is not None:
            log.debug(u"Updating the {0} with {1}".format(key, value))
            setattr(target.userdatas, key, value)
    return handler


def sync_userdatas_to_user(key):
    def handler(target, value, oldvalue, initiator):
        raise Exception()
        if target.user is not None:
            log.debug(u"Updating the {0} with {1}".format(key, value))
            setattr(target.user, key, value)
    return handler


listen(User.firstname, 'set', sync_user_to_userdatas('coordonnees_firstname'))
listen(User.lastname, 'set', sync_user_to_userdatas('coordonnees_lastname'))
listen(User.email, 'set', sync_user_to_userdatas('coordonnees_email1'))


def add_situation_change_handler(target, value, oldvalue, initiator):
    """
    Handler for the situation Change handling
    """
    if isinstance(value, int) and value != oldvalue:
        target.situation_history.append(
            CaeSituationChange(
                date=datetime.date.today(),
                situation_id=value,
            )
        )


listen(UserDatas.situation_situation_id, "set", add_situation_change_handler)
