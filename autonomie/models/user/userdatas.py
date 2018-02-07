# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import datetime
import deform

from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
    Boolean,
    Text,
)

from sqlalchemy.orm import (
    relationship,
    backref,
)
from sqlalchemy.event import listen
from sqlalchemy.orm.base import NO_VALUE

from autonomie_base.consts import (
    SEX_OPTIONS,
    CIVILITE_OPTIONS,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie_base.utils.date import str_to_date
from autonomie.models.tools import get_excluded_colanderalchemy
from autonomie.models.node import Node
from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)
from autonomie.models.user.user import User
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


logger = logging.getLogger(__name__)


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
            'colanderalchemy': {
                'widget': deform.widget.HiddenWidget(),
                'missing': None
            },
            'export': {'exclude': True},
        },
    )

    doctype_id = Column(
        ForeignKey('social_doc_type_option.id'),
        primary_key=True,
        info={
            'colanderalchemy': {
                'widget': deform.widget.HiddenWidget(),
                'missing': None
            },
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
                'colanderalchemy': {'exclude': True},
                "export": {
                    'exclude': True,
                    'stats': {
                        'exclude': False,
                        'label': u"Documents sociaux - ",
                    }
                }
            },
        ),
        info={
            'colanderalchemy': {'exclude': True},
            "export": {'exclude': True}
        },
    )

    doctype = relationship(
        "SocialDocTypeOption",
        backref=backref(
            'registration',
            cascade='all, delete-orphan',
            info={'colanderalchemy': {'exclude': True}},
        ),
        info={
            'colanderalchemy': {'exclude': True},
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
            'export': {'exclude': True},
        }
    )
    user = relationship(
        "User",
        primaryjoin='User.id==UserDatas.user_id',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u'Compte utilisateur'
            ),
            'export': {'exclude': True},
        }
    )

    # INFORMATIONS GÉNÉRALES : CF CAHIER DES CHARGES #
    situation_history = relationship(
        "CaeSituationChange",
        order_by="CaeSituationChange.date",
        info={
            'colanderalchemy': {'exclude': True},
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
            }
        }
    )

    situation_situation = relationship(
        "CaeSituationOption",
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u'Situation dans la CAE'
            ),
            'export': {'related_key': 'label'},
        },
    )

    situation_antenne_id = Column(
        ForeignKey('antenne_option.id'),
        info={
            'colanderalchemy': {
                'title': u"Antenne de rattachement",
                "section": u"Synthèse",
            }
        }
    )
    situation_antenne = relationship(
        "AntenneOption",
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u"Antenne de rattachement"
            ),
            'export': {'related_key': 'label'},
        },
    )

    situation_follower_id = Column(
        ForeignKey('accounts.id'),
        info={
            'colanderalchemy': {
                'title': u'Accompagnateur',
                'section': u'Synthèse',
            },
        },
    )

    situation_follower = relationship(
        "User",
        primaryjoin='User.id==UserDatas.situation_follower_id',
        backref=backref(
            "followed_contractors",
            info={
                'colanderalchemy': {'exclude': True},
                'export': {'exclude': True},
            },
        ),
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u'Conseiller'),
            'export': {
                'related_key': 'lastname',
                'label': u"Conseiller",
            },
            'import': {
#                'related_retriever': User.find_user
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
            },
        }
    )

    coordonnees_zone = relationship(
        'ZoneOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u"Zone d'habitation"
            ),
            'export': {'related_key': 'label'},
        },
    )

    coordonnees_zone_qual_id = Column(
        ForeignKey('zone_qualification_option.id'),
        info={
            'colanderalchemy': {
                'title': u"Qualification de la zone d'habitation",
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_zone_qual = relationship(
        'ZoneQualificationOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
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
            }
        }
    )

    coordonnees_study_level_id = Column(
        ForeignKey('study_level_option.id'),
        info={
            'colanderalchemy': {
                'title': u"Niveau d'études",
                'section': u'Coordonnées',
            }
        }
    )

    coordonnees_study_level = relationship(
        'StudyLevelOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u"Niveau d'études"),
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
            }
        }
    )

    statut_social_status = relationship(
        'SocialStatusOption',
        primaryjoin='UserDatas.statut_social_status_id==SocialStatusOption.id',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u"Statut social à l'entrée"
            ),
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
            },
        }
    )
    statut_social_status_today = relationship(
        'SocialStatusOption',
        primaryjoin='UserDatas.statut_social_status_today_id==\
SocialStatusOption.id',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u"Statut social actuel"
            ),
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
                    "stats": {'exclude': True},
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
            }
        }
    )

    activity_typologie = relationship(
        'ActivityTypeOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
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
            }
        }
    )

    activity_pcs = relationship(
        'PcsOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u"PCS"),
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
                    "stats": {'exclude': True},
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
            }
        }
    )

    parcours_prescripteur = relationship(
        "PrescripteurOption",
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u"Prescripteur"),
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
                    "stats": {'exclude': True},
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
            }
        }
    )

    parcours_non_admission = relationship(
        "NonAdmissionOption",
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
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
                    "stats": {'exclude': True},
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
                    "stats": {'exclude': True},
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
        info={'colanderalchemy': {'exclude': True}},
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
            }
        }
    )
    parcours_employee_quality = relationship(
        'EmployeeQualityOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u"Qualité du salarié"
            ),
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
            }
        }
    )
    parcours_status = relationship(
        "ParcoursStatusOption",
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u"Aptitude"),
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
            }
        }
    )

    sortie_motif = relationship(
        'MotifSortieOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u"Motif de sortie"),
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
            }
        }
    )

    sortie_type = relationship(
        'TypeSortieOption',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(u"Type de sortie"),
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


# multi-valued user-datas
class ExternalActivityDatas(DBBASE):
    """
    Datas related to external activities
    """
    __colanderalchemy_config__ = {
        'title': u"une activité Externe à la CAE",
    }
    __tablename__ = 'external_activity_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': {
                'widget': deform.widget.HiddenWidget(),
                'missing': None
            },
            'export': {'exclude': True},
        }
    )
    type = Column(
        String(50),
        info={
            'colanderalchemy': {
                'title': u"Type de contrat",
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
            'colanderalchemy': {'exclude': True},
            'export': {
                'label': u"Identifiant Autonomie",
                'stats': {'exclude': True},
            }
        },
    )


class CompanyDatas(DBBASE):
    __colanderalchemy_config__ = {
        'title': u"une activité",
    }
    __tablename__ = 'company_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': {
                'widget': deform.widget.HiddenWidget(),
                'missing': None
            },
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
            }
        }
    )

    activity = relationship(
        "CompanyActivity",
        info={
            'colanderalchemy': {'exclude': True},
            'export': {'related_key': 'label'},
        }
    )
    userdatas_id = Column(
        ForeignKey("user_datas.id"),
        info={
            'colanderalchemy': {'exclude': True},
            'export': {
                'label': u"Identifiant Autonomie",
                'stats': {'exclude': True},
            }
        }
    )


class DateDiagnosticDatas(DBBASE):
    __colanderalchemy_config__ = {
        'title': u"une date de diagnostic",
    }
    __tablename__ = 'date_diagnostic_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': {
                'widget': deform.widget.HiddenWidget(),
                'missing': None
            },
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
            'colanderalchemy': {'exclude': True},
            'export': {
                'label': u"Identifiant Autonomie",
                'stats': {'exclude': True},
            }
        }
    )


class DateConventionCAPEDatas(DBBASE):
    __colanderalchemy_config__ = {
        'title': u"une date de convention CAPE",
    }
    __tablename__ = 'date_convention_cape_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': {
                'widget': deform.widget.HiddenWidget(),
                'missing': None
            },
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
            'colanderalchemy': {'exclude': True},
            'export': {
                'label': u"Identifiant Autonomie",
                'stats': {'exclude': True},
            }
        }
    )


class DateDPAEDatas(DBBASE):
    __colanderalchemy_config__ = {
        'title': u"une date de DPAE",
    }
    __tablename__ = 'date_dpae_datas'
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': {
                'widget': deform.widget.HiddenWidget(),
                'missing': None
            },
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
            'colanderalchemy': {'exclude': True},
            'export': {
                'label': u"Identifiant autonomie",
                'stats': {'exclude': True},
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
            'colanderalchemy': {
                'widget': deform.widget.HiddenWidget(),
                'missing': None
            },
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
            'colanderalchemy': {'exclude': True},
            'export': {
                'label': u"Identifiant autonomie",
                'stats': {'exclude': True},
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
            }
        }
    )
    situation = relationship(
        "CaeSituationOption",
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u"Situation dans la CAE"
            ),
            'export': {'related_key': 'label'},
        },
    )


class ContractHistory(DBBASE):
    """
    Used to store history of contract updates
    """
    __colanderalchemy_config__ = {
        'title': u"un avenant",
    }
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={
            'colanderalchemy': {
                'widget': deform.widget.HiddenWidget(),
                'missing': None
            },
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
            'colanderalchemy': {'exclude': True},
            'export': {
                'label': u"Identifiant autonomie",
                'stats': {'exclude': True},
            }
        }
    )
    userdatas = relationship(
        "UserDatas",
        back_populates='parcours_contract_history',
        info={
            'colanderalchemy': {'exclude': True},
            'export': {
                'related_key': u"export_label",
                "keep_key": True,
                "label": u"Historique des avenants",
                "stats": {'exclude': True},
            }
        }
    )


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


def add_situation_change_handler(target, value, oldvalue, initiator):
    """
    Handler for the situation Change handling
    """
    if value != oldvalue:
        if value is not NO_VALUE and value is not None:
            target.situation_history.append(
                CaeSituationChange(
                    date=datetime.date.today(),
                    situation_id=value,
                )
            )


listen(UserDatas.situation_situation_id, "set", add_situation_change_handler)
