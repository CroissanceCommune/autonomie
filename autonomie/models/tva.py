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
    Model for tva amounts
"""
import colander
import deform
import deform_extensions
from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    Boolean,
    Text,
    not_,
)
from sqlalchemy.orm import (
    relationship,
)

from autonomie.utils.html import clean_html
from autonomie.forms.custom_types import AmountType
from autonomie.models.base import DBBASE
from autonomie.models.base import default_table_args


TVA_GRID = (
    (('active', 6,),),
    (('name', 6,), ('value', 6),),
    (('mention', 12),),
    (('compte_cg', 3), ('code', 3), ('compte_a_payer', 3)),
    (('default', 6),),
    (('products', 12),),
)


class Tva(DBBASE):
    """
        `id` int(2) NOT NULL auto_increment,
        `name` varchar(8) NOT NULL,
        `value` int(5)
        `default` int(2) default 0 #rajouté par mise à jour 1.2
    """
    __colanderalchemy_config__ = {
        "title": u"un taux de TVA",
        "validation_msg": u"Les taux de Tva ont bien été configurés",
        "help_msg": u"""Configurez les taux de Tva disponibles utilisés dans \
Autonomie, ainsi que les produits associés.<br /> \
        Une Tva est composée :<ul><li>D'un libellé (ex : TVA 20%)</li> \
        <li>D'un montant (ex : 20)</li> \
        <li>D'un ensemble d'informations comptables</li> \
        <li>D'un ensemble de produits associés</li> \
        <li> D'une mention : si elle est renseignée, celle-ci viendra se placer
        en lieu et place du libellé (ex : Tva non applicable en vertu ...)
        </ul><br /> \
        <b>Note : les montants doivent tous être distincts, si vous utilisez \
        plusieurs Tva à 0%, utilisez des montants négatifs pour les \
        différencier. \
        """,
        'widget': deform_extensions.GridFormWidget(named_grid=TVA_GRID)
    }
    __tablename__ = 'tva'
    __table_args__ = default_table_args
    id = Column(
        'id',
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}},
    )
    active = Column(
        Boolean(),
        default=True,
        info={
            'colanderalchemy': {'exclude': True}
        },
    )
    name = Column(
        "name",
        String(15),
        nullable=False,
        info={
            'colanderalchemy': {
                'title': u'Libellé du taux de TVA',
                }
        },
    )
    value = Column(
        "value",
        Integer,
        info={
            "colanderalchemy": {
                'title': u'Valeur',
                'typ': AmountType(),
                'description': u"Le pourcentage associé (ex : 19.6)",
            }
        },
    )
    compte_cg = Column(
        "compte_cg",
        String(125),
        default="",
        info={'colanderalchemy': dict(title=u"Compte CG de Tva")}
    )
    code = Column(
        "code",
        String(125),
        default="",
        info={'colanderalchemy': dict(title=u"Code de Tva")}
    )
    compte_a_payer = Column(
        String(125),
        default='',
        info={'colanderalchemy': dict(
            title=u"Compte de Tva à payer",
            description=u"Utilisé dans les exports comptables des \
encaissements",
        )}
    )
    mention = Column(
        Text,
        info={
            'colanderalchemy': {
                'title': u"Mentions spécifiques à cette TVA",
                'description': u"""Si cette Tva est utilisée dans un
devis/une facture,la mention apparaitra dans la sortie PDF
(ex: Mention pour la tva liée aux formations ...)""",
                'widget': deform.widget.TextAreaWidget(rows=1),
                'preparer': clean_html,
                'missing': colander.drop,
            }
        }
    )
    default = Column(
        "default",
        Boolean(),
        info={
            "colanderalchemy": {
                'title': u'Cette tva doit-elle être proposée par défaut ?'
            }
        },
    )
    products = relationship(
        "Product",
        cascade="all, delete-orphan",
        info={
            'colanderalchemy': {
                'title': u"Comptes produit associés",
                "widget": deform.widget.SequenceWidget(
                    add_subitem_text_template=u"Ajouter un compte produit",
                )
            },
        },
        back_populates='tva',
    )

    @classmethod
    def query(cls, include_inactive=False):
        q = super(Tva, cls).query()
        if not include_inactive:
            q = q.filter(Tva.active == True)
        return q.order_by('value')

    @classmethod
    def by_value(cls, value):
        """
        Returns the Tva matching this value
        """
        return super(Tva, cls).query().filter(cls.value == value).one()

    @classmethod
    def get_default(cls):
        return cls.query().filter_by(default=True).first()

    def __json__(self, request):
        return dict(
            id=self.id,
            value=self.value,
            name=self.name,
            default=self.default == 1,
            products=[product.__json__(request) for product in self.products],
        )

    @classmethod
    def unique_value(cls, value, tva_id=None):
        """
        Check that the given value has not already been attributed to a tva
        entry

        :param int value: The value currently configured
        :param int tva_id: The optionnal id of the current tva object (edition
        mode)
        :returns: True/False
        :rtype: bool
        """
        query = cls.query(include_inactive=True)
        if tva_id:
            query = query.filter(not_(cls.id == tva_id))

        return query.filter_by(value=value).count() == 0


class Product(DBBASE):
    __colanderalchemy_config__ = {
        'title': u"Compte produit",
        'widget': deform_extensions.InlineMappingWidget(),
    }
    __tablename__ = 'product'
    __table_args__ = default_table_args
    id = Column(
        'id',
        Integer,
        primary_key=True,
        info={'colanderalchemy': {'widget': deform.widget.HiddenWidget()}},
    )
    name = Column(
        "name",
        String(125),
        nullable=False,
        info={'colanderalchemy': {'title': u'Libellé', 'width': 6}}
    )
    compte_cg = Column(
        "compte_cg",
        String(125),
        info={'colanderalchemy': {'title': u'Compte CG', 'width': 6}}
    )
    active = Column(
        Boolean(),
        default=True,
        info={'colanderalchemy': {'exclude': True}},
    )
    tva_id = Column(
        Integer,
        ForeignKey("tva.id", ondelete="cascade"),
        info={'colanderalchemy': {'exclude': True}}
    )
    tva = relationship(
        "Tva",
        back_populates="products",
        info={'colanderalchemy': {'exclude': True}}
    )

    def __json__(self, request):
        return dict(
            id=self.id,
            name=self.name,
            compte_cg=self.compte_cg
        )

    @classmethod
    def query(cls, include_inactive=False):
        q = super(Product, cls).query()
        if not include_inactive:
            q = q.join(cls.tva)
            q = q.filter(Product.active == True)
            q = q.filter(Tva.active == True)
        return q.order_by('name')
