# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Fiche formateur

Extension du module User qui vient rajouter la possibilité de stocker des
informations sur les formateurs
"""
from sqlalchemy import (
    Column,
    ForeignKey,
    String,
    Text,
    Boolean,
)
from sqlalchemy.orm import (
    relationship,
)

from autonomie_base.models.base import (
    default_table_args,
)
from autonomie.models.node import Node
from autonomie.models.tools import get_excluded_colanderalchemy


class TrainerDatas(Node):
    __tablename__ = "trainer_datas"
    __table_args__ = default_table_args
    __mapper_args__ = {'polymorphic_identity': 'trainerdata'}

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
        primaryjoin='User.id==TrainerDatas.user_id',
        info={
            'colanderalchemy': get_excluded_colanderalchemy(
                u'Compte utilisateur'
            ),
            'export': {'exclude': True},
        },
    )

    # Profil professionnel
    specialty = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Spécialité",
                "description": u"Votre spécialité - Votre cœur de métier, \
champ de compétence et domaines d'expertise (3 lignes au maximum)",
                "section": u"Profil Professionnel",
            }
        }
    )
    linkedin = Column(
        String(255),
        info={
            'colanderalchemy':
            {
                'title': u"Réseau Sociaux - Adresse du profil linkedin",
                "section": u"Profil Professionnel",
            }
        }
    )
    viadeo = Column(
        String(255),
        info={
            'colanderalchemy':
            {
                'title': u"Réseau Sociaux - Adresse du profil Viadeo",
                "section": u"Profil Professionnel",
            }
        }
    )
    career = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Votre parcours professionnel en 3 dates ou périodes",
                "description": u"Par exemple pour date : en 1991 - Par \
exemple pour période : de 1991 à 1995",
                "section": u"Profil Professionnel",
            }
        }
    )
    qualifications = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Votre qualification ou/et diplôme le plus pertinent",
                "description": u"2 lignes maximum",
                "section": u"Profil Professionnel",
            }
        }
    )
    background = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Votre formation de formateur",
                "section": u"Profil Professionnel",
            }
        }
    )
    references = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Vos références de missions de formation effectuées",
                "description": u"5 références maximum en mentionnant nom du \
client, contexte de l'intervention, année",
                "section": u"Profil Professionnel",
            }
        }
    )
    # Section "Concernant votre activité de formation"
    motivation = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Quelle est votre motivation, pourquoi faites-vous \
de la formation ?",
                "description": u"3 lignes maximum",
                "section": u"Concernant votre activité de formation",
            }
        }
    )
    approach = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Concernant votre activité de formation",
                "description": u"3 lignes maximum, ne pas entrer dans la \
méthodologie",
                "section": u"Concernant votre activité de formation",
            }
        }
    )
    # Section: Un petit peu de vous
    temperament = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Caractère",
                "description": u"1 à 3 lignes, par ex : sens de la créativité, \
aimer les gens et croire en leur potentiel, aime maîtriser son sujet \
parfaitement ...",
                "section": u"Un petit peu de vous",
            }
        }
    )
    indulgence = Column(
        Text(),
        info={
            'colanderalchemy':
            {
                'title': u"Ce qui vous inspire le plus d'indulgence",
                "description": u"1 à 3 lignes, par ex : la peur d'un \
environnement ou d'un outil, les difficultés des personnes à s'exprimer, \
l’échec lié à une prise de risque ...",
                "section": u"Un petit peu de vous",
            }
        }
    )
    sound = Column(
        Text(),
        info={
            "colanderalchemy": {
                "title": u"Le son, le bruit que vous aimez",
                "description": u"1 à 3 lignes, par ex : le café qui coule le \
matin, le son de l'élastique de ma chemise cartonnée qui contient mon \
programme de formation...",
                "section": u"Un petit peu de vous",
            }
        }
    )
    object_ = Column(
        Text(),
        info={
            "colanderalchemy": {
                "title": u"Si vous étiez un objet, vous seriez ?",
                "description": u"1 à 3 lignes, par ex : une agrafeuse pour \
faire du lien, un micro pour écouter, une lampe pour éclairer",
                "section": u"Un petit peu de vous",
            }
        }
    )

    active = Column(
        Boolean(),
        info={
            "colanderalchemy": {
                "title": u"Fiche active ?",
                "description": u"Cette fiche formateur est-elle active ?",
            }
        }
    )
