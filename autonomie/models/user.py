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
from deform import widget as deform_widget

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
)
from sqlalchemy.util import classproperty
from sqlalchemy.event import listen

from autonomie.views import render_api

from deform_bootstrap import widget as bootstrap_widget
from autonomie.models.base import DBBASE
from autonomie.models.base import default_table_args
from autonomie.models.widgets import (
    get_hidden_field_conf,
    EXCLUDED,
    get_select,
    get_select_validator,
    get_date,
    get_deferred_select,
    mail_validator,
)
from autonomie.models.types import JsonEncodedDict
from autonomie.utils.ascii import camel_case_to_name


ADMIN_PRIMARY_GROUP = 1
MANAGER_PRIMARY_GROUP = 2
CONTRACTOR_PRIMARY_GROUP = 3


ROLES = {
    'admin': 1,
    'manager': 2,
    'contractor': 3,
    }


COMPANY_EMPLOYEE = Table('company_employee', DBBASE.metadata,
        Column("company_id", Integer, ForeignKey('company.id')),
        Column("account_id", Integer, ForeignKey('accounts.id')),
        mysql_charset=default_table_args['mysql_charset'],
        mysql_engine=default_table_args['mysql_engine'])


SITUATION_OPTIONS = (
    ('reu_info', u"Réunion d'information",),
    ("entretien", u"Entretien",),
    ("integre", u"Intégré",),
    ("sortie", u"Sortie",),
    ("refus", u"Refus",),
)


SEX_OPTIONS = (
    ('M', 'Homme', ),
    ('F', 'Femme', ),
)


CIVILITE_OPTIONS = (
    ('Monsieur', u'Monsieur',),
    ('Madame', u'Madame',),
)


STATUS_OPTIONS = (
    ('maried', u'Marié', ),
    ('pacsed', u"Pacsé", ),
    ('isolated', u"Parent isolé", ),
    ('single', u"Célibataire", ),
    ("free_union", u"union libre", ),
)


CONTRACT_OPTIONS = (
    ('cdd', u'CDD',),
    ('cdi', u'CDI',),
)


log = logging.getLogger(__name__)


def get_id_foreignkey_col(foreignkey_str):
    """
    Return an id column as a foreignkey with correct colander configuration

        foreignkey_str

            The foreignkey our id is pointing to
    """
    column = Column(
        "id",
        Integer,
        ForeignKey(foreignkey_str),
        primary_key=True,
        info={'colanderalchemy': get_hidden_field_conf()},
    )
    return column


class User(DBBASE):
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

    login = Column(
        String(64, collation="utf8_bin"),
        unique=True,
        nullable=False,
        info={'colanderalchemy': {'title': u'Identifiant'}}
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

    primary_group = Column(
        Integer,
        info={'colanderalchemy':EXCLUDED},
        default=3,
    )

    active = Column(
        String(1),
        info={'colanderalchemy':EXCLUDED},
        default='Y'
    )

    email = Column(
        String(100),
        info={
            'colanderalchemy': {
                'title': u"Adresse e-mail",
                'section': u'Coordonnées',
                'validator': mail_validator(),
            }
        },
        nullable=False,
    )

    pwd = Column(
        "password",
        String(100),
        info={'colanderalchemy':
              {
                  'title': u'Mot de passe',
                  'widget': deform_widget.CheckedPasswordWidget(),
              }
        },
        nullable=False,
    )

    companies = relationship(
        "Company",
        secondary=COMPANY_EMPLOYEE,
        backref="employees",
        info={'colanderalchemy':EXCLUDED},
    )

    compte_tiers = Column(
        String(30),
        info={
            'colanderalchemy':
            {
                'title': u'Compte tiers',
            }
        },
        default="",
    )

    session_datas = Column(
        JsonEncodedDict,
        info={'colanderalchemy':EXCLUDED},
        default=None,
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

    def is_admin(self):
        """
            return true if the user is and administrator
        """
        return self.primary_group == ADMIN_PRIMARY_GROUP

    def is_manager(self):
        """
            return True if the user is a manager
        """
        return self.primary_group == MANAGER_PRIMARY_GROUP

    def is_contractor(self):
        """
            return True if the user is a contractor
        """
        return self.primary_group == CONTRACTOR_PRIMARY_GROUP

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
            query = query.filter(not_(cls.id==user_id))

        result = query.filter(cls.login==login).first()
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

    def __repr__(self):
        return u"<User {s.id} '{s.lastname} {s.firstname}'>".format(s=self)


def get_user_by_roles(roles):
    """
        Return user by roles
    """
    roles_ids = [ROLES[role] for role in roles if role in ROLES.keys()]
    return User.query().filter(User.primary_group.in_(roles_ids))


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
        return bootstrap_widget.ChosenSingleWidget(
            values=choices,
            **widget_options
            )
    return user_select


class ConfigurableOption(DBBASE):
    """
    Base class for options
    """
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': get_hidden_field_conf()}
    )
    label = Column(
        String(100),
        info={'colanderalchemy': {'title': u'Libellé'}},
    )
    active = Column(
        Boolean(),
        default=True,
        info={'colanderalchemy': EXCLUDED}
    )
    type_ = Column(
        'type_',
        String(30),
        nullable=False,
        info={'colanderalchemy': EXCLUDED}
        )

    @classproperty
    def __mapper_args__(cls):
        name = cls.__name__
        if name == 'ConfigurableOption':
            return {
                'polymorphic_on': 'type_',
                'polymorphic_identity':'configurable_option'
            }
        else:
            return {'polymorphic_identity': camel_case_to_name(name)}

    @classmethod
    def query(cls):
        query = super(ConfigurableOption, cls).query()
        query = query.filter(ConfigurableOption.active==True)
        return query


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
        'title': u"Statut du parcour",
        'validation_msg': u"Les statuts de parcours ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')


class MotifSortieOption(ConfigurableOption):
    """
    Possible values for exit motivation
    """
    __colanderalchemy_config__ = {
        'title': u"Motif de sortie",
        'validation_msg': u"Les motifs de sortie ont bien été configurés",
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


class UserDatasSocialDocTypes(DBBASE):
    """
    relationship table used between social document types and user datas set
    """
    __tablename__ = 'userdatas_socialdocs'
    __table_args__ = default_table_args
    __colanderalchemy_config__ = {
        'css': "well text-center",
    }
    userdatas_id = Column(
        ForeignKey('user_datas.id'),
        primary_key=True,
        info={'colanderalchemy': get_hidden_field_conf() },
    )

    doctype_id = Column(
        ForeignKey('social_doc_type_option.id'),
        primary_key=True,
        info={'colanderalchemy': get_hidden_field_conf()},
    )

    status = Column(Boolean(), default=False)
    userdatas = relationship(
        'UserDatas',
        backref=backref(
            'doctypes_registrations',
            cascade='all, delete-orphan',
            info={'colanderalchemy': EXCLUDED},
        ),
        info={'colanderalchemy': EXCLUDED},
    )

    doctype = relationship(
        "SocialDocTypeOption",
        backref=backref(
            'registration',
            cascade='all, delete-orphan',
            info={'colanderalchemy': EXCLUDED},
        ),
        info={'colanderalchemy': EXCLUDED},
    )


class UserDatas(DBBASE):
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': get_hidden_field_conf(),
            'export': {'exclude': True},
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
        backref=backref(
            "userdatas",
            uselist=False,
            cascade='all, delete-orphan',
            info={
                'colanderalchemy': EXCLUDED,
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': EXCLUDED,
            'export': {'exclude': True},
        }
    )

    # INFORMATIONS GÉNÉRALES : CF CAHIER DES CHARGES #
    situation_situation = Column(
        String(20),
        info={
            'colanderalchemy': {
                'title': u"Situation actuelle dans la CAE",
                'section': u'Synthèse',
                'widget': get_select(SITUATION_OPTIONS),
                'validator': get_select_validator(SITUATION_OPTIONS),
                'default': SITUATION_OPTIONS[0][0],
            },
            'export': {
                'formatter': lambda val: dict(SITUATION_OPTIONS).get(val),
            }
        },
    )

    situation_follower_id = Column(
        ForeignKey('accounts.id'),
        info={'colanderalchemy':
              {
                  'title': u'Accompagnateur',
                  'section': u'Synthèse',
                  'widget': get_deferred_user_choice(
                      roles=['admin', 'manager']
                  ),
              },
              'export': {'exclude': True},
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
            'colanderalchemy': EXCLUDED,
            'export': {
                'related_key': 'lastname',
                'label': u"Conseiller",
            },
        }
    )

    situation_societariat_entrance = Column(
        Date(),
        info={
            'colanderalchemy': {
                'title': u"Date d'entrée au sociétariat",
                'section': u'Synthèse',
                'widget': get_date(),
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
        },
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
                'widget': deform_widget.TextAreaWidget(),
            }
        }
    )

    coordonnees_zipcode = Column(
        String(7),
        info={
            'colanderalchemy': {
                'title': u'Code postal',
                'section': u'Coordonnées',
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
        info={'colanderalchemy': EXCLUDED},
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
        info={'colanderalchemy': EXCLUDED},
    )

    coordonnees_sex = Column(
        String(1),
        info={
            'colanderalchemy': {
                'title': u'Sexe',
                'section': u'Coordonnées',
                'widget': get_select(SEX_OPTIONS),
                'validator': get_select_validator(SEX_OPTIONS),
            }
        }
    )

    coordonnees_birthday = Column(
        Date(),
        info={
            'colanderalchemy': {
                'title': u'Date de naissance',
                'section': u'Coordonnées',
                'widget': get_date(),
            }
        }
    )

    coordonnees_birthplace = Column(
        String(255),
        info={
            'colanderalchemy': {
                'title': u'Lieu de naissance',
                'section': u'Coordonnées',
                'widget': deform_widget.TextAreaWidget(),
            }
        }
    )

    coordonnees_birthplace_zipcode = Column(
        String(7),
        info={
            'colanderalchemy': {
                'title': u'Code postale',
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
                'widget': get_date(),
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
        }
    )

    coordonnees_children = Column(
        Integer(),
        default=0,
        info={
            'colanderalchemy':{
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
        info={'colanderalchemy': EXCLUDED},
    )
    coordonnees_emergency_name = Column(
        String(50),
        info={
            'colanderalchemy':{
                'title': u"Contact urgent : Nom",
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_emergency_phone = Column(
        String(14),
        info={
            'colanderalchemy':{
                'title': u'Contact urgent : Téléphone',
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_identifiant_interne = Column(
        String(20),
        info={
            'colanderalchemy':{
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
        info={'colanderalchemy': EXCLUDED},
    )
    statut_handicap_allocation_expiration = Column(
        Date(),
        default=None,
        info={
            'colanderalchemy':
            {
                'title': u"Allocation adulte handicapé - échéance (expiration)",
                'section': u'Statut',
                'widget': get_date(),
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
        }
    )

    statut_end_rights_date = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u'Date de fin de droit',
                'section': u'Statut',
                'widget': get_date(),
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
        info={'colanderalchemy': EXCLUDED},
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
        info={'colanderalchemy': EXCLUDED},
    )
    activity_companydatas = relationship(
        "CompanyDatas",
        cascade="all, delete-orphan",
        info={
            'colanderalchemy':
            {
                'title': u'Activité',
                'section': u'Activité',
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
        info={'colanderalchemy': EXCLUDED},
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
                'widget': get_date()
            }
        }
    )

    parcours_date_diagnostic = relationship(
        "DateDiagnosticDatas",
        cascade="all, delete-orphan",
        info={
            'colanderalchemy':
            {
                'title': u'Date diagnostic',
                'section': u'Parcours',
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
        info={'colanderalchemy': EXCLUDED},
    )

    parcours_convention_cape = relationship(
        "DateConventionCAPEDatas",
        cascade='all, delete-orphan',
        info={
            'colanderalchemy':{
                "title": u"Date convention CAPE",
                'section': u'Parcours',
            },
        }
    )

    parcours_dpae = relationship(
        "DateDPAEDatas",
        cascade='all, delete-orphan',
        info={
            'colanderalchemy':{
                "title": u"Date DPAE",
                'section': u'Parcours',
            },
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
                'widget': get_date(),
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
                'widget': get_date(),
            }
        }
    )

    parcours_last_avenant = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u'Dernier avenant',
                'section': u'Parcours',
                'widget': get_date(),
            }
        }
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
        Integer(),
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

    parcours_goals = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Objectifs",
                "section": u"Parcours",
                "widget": deform_widget.TextAreaWidget(),
            }
        }
    )

    parcours_status_id = Column(
        ForeignKey("parcours_status_option.id"),
        info={
            'colanderalchemy':
            {
                'title': u"Statut",
                'section': u'Parcours',
                'widget': get_deferred_select(ParcoursStatusOption),
            }
        }
    )

    parcours_status = relationship(
        "ParcoursStatusOption",
        info={'colanderalchemy': EXCLUDED},
    )
    parcours_medical_visit = Column(
        Date(),
        info={
            'colanderalchemy':
            {
                'title': u"Date de la visite médicale",
                'section': u'Parcours',
                'widget': get_date(),
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
                'widget': get_date(),
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
                'widget': get_date(),
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
        info={'colanderalchemy': EXCLUDED},
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
        from autonomie.utils.ascii import gen_random_string
        if self.situation_situation == 'integre' and self.user_id is None:
            login = self.coordonnees_email1,
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
        return None, None, None

    def gen_companies(self):
        """
        Generate companies as expected
        """
        from autonomie.models.company import Company
        companies = []
        if self.situation_situation == 'integre' and self.user_id is None:
            for data in self.activity_companydatas:
                company = Company(
                    name=data.name,
                    goal=data.title,
                    email=self.coordonnees_email1,
                    phone=self.coordonnees_tel,
                    mobile=self.coordonnees_mobile,
                )
                companies.append(company)
        return companies


# multi-valued user-datas
class ExternalActivityDatas(DBBASE):
    """
    Datas related to external activities
    """
    __tablename__ = 'external_activity_datas'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True, info={
        'colanderalchemy': get_hidden_field_conf()
        }
    )
    type = Column(String(50),
        info={'colanderalchemy':
              {
                  'title': u"Type de contrat",
                  'widget': get_select(CONTRACT_OPTIONS),
              }
             }
                 )
    hours = Column(
        Integer,
        info={'colanderalchemy':
              {
                  'title': u"Nombre d'heures",
              }
             }
    )
    brut_salary = Column(
        Integer,
        info={'colanderalchemy':
              {
                  'title': u'Salaire brut',
              }
             }
    )
    employer_visited = Column(
        Boolean(),
        default=False,
        info={'colanderalchemy':
              {
                  'title': u'Visite autre employeur',
              }
             }
    )
    userdatas_id = Column(
        ForeignKey('user_datas.id'),
        info={'colanderalchemy': EXCLUDED},
    )


class CompanyDatas(DBBASE):
    __tablename__ = 'company_datas'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True, info={
        'colanderalchemy': get_hidden_field_conf()
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
    userdatas_id = Column(ForeignKey("user_datas.id"), info={'colanderalchemy': EXCLUDED})


class DateDiagnosticDatas(DBBASE):
    __tablename__ = 'date_diagnostic_datas'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True, info={
        'colanderalchemy': get_hidden_field_conf()
    }
    )
    date = Column(
        Date(),
        info={
            "title": u'Date du diagnostic',
            "widget": get_date(),
        }
    )
    userdatas_id = Column(ForeignKey("user_datas.id"), info={'colanderalchemy': EXCLUDED})


class DateConventionCAPEDatas(DBBASE):
    __tablename__ = 'date_convention_cape_datas'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True, info={
        'colanderalchemy': get_hidden_field_conf(),
    }
    )
    date = Column(
        Date(),
        info={
            "title": u'Date de la convention',
            "widget": get_date(),
        }
    )
    userdatas_id = Column(ForeignKey("user_datas.id"), info={'colanderalchemy': EXCLUDED})


class DateDPAEDatas(DBBASE):
    __tablename__ = 'date_dpae_datas'
    __table_args__ = default_table_args
    id = Column(Integer, primary_key=True, info={
        'colanderalchemy': get_hidden_field_conf(),
    }
    )
    date = Column(
        Date(),
        info={
            "title": u'Date de la DPAE',
            "widget": get_date(),
        }
    )
    userdatas_id = Column(
        ForeignKey("user_datas.id"),
        info={'colanderalchemy': EXCLUDED}
    )


USERDATAS_FORM_GRIDS = {
    u"Synthèse": (
        ((2, True), (2, True)),
        ((2, True),)
    ),
    u"Coordonnées": (
        ((2, True), (2, True), (2, True), (2, True)),
        ((2, True), (2, True)),
        ((2, True), (2, True)),
        ((2, True), (2, True), (3, True)),
        ((2, True), (2, True)),
        ((2, True), (2, True), (2, True), (2, True)),
        ((2, True), (2, True)),
        ((3, True), ),
        ((2, True), (2, True), (2, True)),
        ((2, True), (2, True)),
    ),
    u"Parcours": (
        ((2, True), (2, True)),
        ((2, True), ),
        ((2, True), ),
        ((2, True), ),
        ((2, True), ),
        ((2, True), ),
        ((2, True), (2, True), (2, True), (2, True)),
        ((2, True), (2, True), (2, True)),
        ((2, True), (2, True), ),
        ((4, True), ),
        ((2, True), (2, True), (2, True)),
    )
}


# Registering event handlers to keep datas synchronized
def sync(key):
    def handler(target, value, oldvalue, initiator):
        if target.userdatas is not None:
            log.debug(u"Updating the {0} with {1}".format(key, value))
            setattr(target.userdatas, key, value)
    return handler

listen(User.firstname, 'set', sync('coordonnees_firstname'))
listen(User.lastname, 'set', sync('coordonnees_lastname'))
