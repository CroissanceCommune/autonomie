"""3.2 : Add mention to tva

Revision ID: 1cf6d10d40cf
Revises: 3c1321f40c0c
Create Date: 2016-04-12 15:26:57.422710

"""

# revision identifiers, used by Alembic.
revision = '1cf6d10d40cf'
down_revision = '3c1321f40c0c'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.execute(u"Alter table tva modify name VARCHAR(15)")
    op.execute(u"Alter table tva modify active tinyint(1)")
    op.add_column('tva', sa.Column('mention', sa.Text(), default=''))

    from autonomie.models.tva import Tva
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    for tva in session.query(Tva):
        if tva.value <= 0:
            tva.mention = u"TVA non applicable selon l'article 259b du CGI."
            session.merge(tva)
        else:
            tva.mention = u"TVA {0} %".format(tva.value / 100.0)
            session.merge(tva)


def downgrade():
    op.drop_column('tva', 'mention')
