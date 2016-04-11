"""3.2 : passage 5 chiffres

Revision ID: 3c1321f40c0c
Revises: 58df01afdaad
Create Date: 2016-04-08 13:59:10.943692

"""

# revision identifiers, used by Alembic.
revision = '3c1321f40c0c'
down_revision = '58df01afdaad'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from autonomie.models.task import (
        DiscountLine,
        TaskLine,
        Task,
        PaymentLine,
    )
    from autonomie.models.base import DBSESSION as db
    models = (
        (DiscountLine, ("amount",),),
         (TaskLine, ("cost",),),
          (Task, ('ht', 'tva', 'ttc', 'expenses_ht', 'expenses', ),),
           (PaymentLine, ('amount',),)
           )
    for model, keys in models:
        for key in keys:
            op.execute(
                u"Alter table {table} CHANGE {key} {key} BIGINT(20)".format(
                    table=model.__tablename__, key=key
                )
            )

    for model, keys in models:
        attrs = [getattr(model, 'id')]
        attrs.extend([getattr(model, key) for key in keys])
        query = db().query(*attrs)
        if model == Task:
            query = query.filter(
                Task.type_.in_(('invoice', 'estimation', 'cancelinvoice'))
            )
        for entry in query:
            id_ = entry[0]
            vals = entry[1:]
            f_keys = ["%s=%s" % (keys[index], 1000 * value)
                      for index,value in enumerate(vals)
                      if value is not None]
            key_query = ','.join(f_keys)
            if key_query.strip():
                query = "update {table} set {key_query} where id={id}".format(
                    table=model.__tablename__,
                    key_query=key_query,
                    id=id_
                )
                op.execute(query)


def downgrade():
    pass
