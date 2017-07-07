# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from sqlalchemy import (
    Column,
    Integer,
    Boolean,
    String,
)
from sqlalchemy.orm import (
    relationship,
)
from autonomie_base.models.base import (
    DBBASE,
    default_table_args,
)
from autonomie.models.options import (
    ConfigurableOption,
    get_id_foreignkey_col,
)
from autonomie import forms


class PaymentMode(DBBASE):
    """
        Payment mode entry
    """
    __colanderalchemy_config__ = {
        "title": u"un mode de paiement",
        "help_msg": u"Configurer les modes de paiement pour la saisie des \
encaissements des factures",
        "validation_msg": u"Les modes de paiement ont bien été configurés"
    }
    __tablename__ = "paymentmode"
    __table_args__ = default_table_args
    id = Column(
        Integer,
        primary_key=True,
        info={'colanderalchemy': forms.get_hidden_field_conf()},
    )
    label = Column(
        String(120),
        info={'colanderalchemy': {'title': u"Libellé"}}
    )


class BankAccount(ConfigurableOption):
    """
    Bank accounts used for payment registry
    """
    __colanderalchemy_config__ = {
        "title": u"un compte banque",
        'validation_msg': u"Les comptes banques ont bien été configurés",
    }
    id = get_id_foreignkey_col('configurable_option.id')
    code_journal = Column(
        String(120),
        info={
            "colanderalchemy": {
                'title': u"Code journal Banque",
                'description': u"""Code journal utilisé pour les exports
                des encaissements et des règlements des notes de dépense""",
            }
        },
        nullable=False,
    )

    compte_cg = Column(
        String(120),
        info={
            "colanderalchemy": {'title': u"Compte CG Banque"}
        },
        nullable=False,
    )
    default = Column(
        Boolean(),
        default=False,
        info={
            "colanderalchemy": {'title': u"Utiliser ce compte par défaut"}
        }
    )
    payments = relationship(
        'Payment',
        order_by="Payment.date",
        info={'colanderalchemy': {'exclude': True}},
    )
