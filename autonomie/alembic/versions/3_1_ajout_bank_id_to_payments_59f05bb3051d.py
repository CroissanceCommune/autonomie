"""3.1 : Ajout de champs aux paiements

Revision ID: 59f05bb3051d
Revises: 54de05a93319
Create Date: 2015-08-19 13:09:12.384701

"""

# revision identifiers, used by Alembic.
revision = '59f05bb3051d'
down_revision = '54de05a93319'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('payment', sa.Column('created_at', sa.DateTime()))
    op.add_column('payment', sa.Column('updated_at', sa.DateTime()))
    op.add_column('payment', sa.Column('bank_id', sa.Integer(), nullable=True))
    op.add_column('payment', sa.Column('exported', sa.Boolean(), default=False))
    op.add_column('payment', sa.Column(
        'tva_id',
        sa.Integer(),
        sa.ForeignKey('tva.id'),
        nullable=True,
    ))
    op.add_column(
        'payment',
        sa.Column('remittance_amount', sa.Integer(), nullable=True)
    )
    op.add_column(
        'tva',
        sa.Column('compte_a_payer', sa.String(125), default='')
    )
    from autonomie_base.models.base import DBSESSION
    from autonomie.models.task import Payment

    session = DBSESSION()

    for payment in Payment.query():
        payment.remittance_amount = payment.amount
        payment.exported = True
        payment.created_at = payment.updated_at = payment.date
        session.merge(payment)


def downgrade():
    op.drop_column('payment', 'bank_id')
    op.drop_column('payment', 'remittance_amount')
