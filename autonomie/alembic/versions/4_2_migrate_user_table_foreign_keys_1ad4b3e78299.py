"""4.2 : Migrate user table foreign keys

Revision ID: 1ad4b3e78299
Revises: 4299e583631c
Create Date: 2017-11-08 10:47:31.126072

"""

# revision identifiers, used by Alembic.
revision = '1ad4b3e78299'
down_revision = '13a25f46e412'

from alembic import op
import sqlalchemy as sa
from autonomie.alembic.utils import (
    disable_constraints,
    enable_constraints,
)


user_helper = sa.Table(
    'accounts',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('login', sa.String(255)),
    sa.Column('password', sa.String(255)),
    sa.Column('active', sa.String(1)),
)


userdatas_helper = sa.Table(
    'user_datas',
    sa.MetaData(),
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('user_id', sa.Integer),
    sa.Column('coordonnees_civilite', sa.String(15)),
    sa.Column('coordonnees_lastname', sa.String(255)),
    sa.Column('coordonnees_firstname', sa.String(255)),
    sa.Column('coordonnees_email1', sa.String(255)),
)


def update_database_structure():
    # Migrate the foreignkey
    op.drop_constraint('fk_user_groups_user_id', 'user_groups', type_='foreignkey')
    op.add_column(
        'user_groups',
        sa.Column(
            'login_id', sa.Integer, sa.ForeignKey('login.id')
        )
    )
    op.add_column(
        'accounts',
        sa.Column(
            'civilite', sa.String(10)
        )
    )
    for index in ('egw_accounts_account_lid', 'login', 'uq_accounts_login'):
        op.execute('ALTER TABLE accounts DROP INDEX IF EXISTS %s' % index)


def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from alembic.context import get_bind
    connection = get_bind()

    from autonomie.models.user.login import Login
    op.execute('update accounts set civilite="Monsieur"')

    for user in connection.execute(user_helper.select()):
        login = Login(
            user_id=user.id,
            login=user.login,
        )
        login.pwd_hash = user.password,
        login.active = user.active == 'Y'
        session.add(login)
        session.flush()
        op.execute(
            'UPDATE user_groups set login_id="%s" where user_id=%s' % (
                login.id, user.id
            )
        )


    from autonomie.models.user.user import User
    for userdatas in connection.execute(userdatas_helper.select()):
        if userdatas.user_id is None:
            user = User(
                lastname=userdatas.coordonnees_lastname,
                firstname=userdatas.coordonnees_firstname,
                email=userdatas.coordonnees_email1,
                civilite=userdatas.coordonnees_civilite or 'Monsieur',
            )
            session.add(user)
            session.flush()
            connection.execute(
                userdatas_helper.update().where(
                    userdatas_helper.c.id == userdatas.id
                ).values(user_id=user.id)
            )
        else:
            user = User.get(userdatas.user_id)
            user.civilite = userdatas.coordonnees_civilite or 'Monsieur'
            session.merge(user)
            session.flush()

    op.execute('update accounts set civilite="Monsieur" where civilite is NULL')



def clean_database():
    op.execute("ALTER TABLE user_groups DROP INDEX IF EXISTS `user_id`")
    op.drop_column('user_groups', 'user_id')
    op.drop_column("accounts", "login")
    op.drop_column("accounts", "password")
    op.drop_column("accounts", "active")
    op.drop_column('invoice', 'deposit')


def upgrade():
    disable_constraints()
    update_database_structure()
    migrate_datas()
    clean_database()
    enable_constraints()


def downgrade():
    pass
