"""4.2.0a : add multiple social status on userdatas

Revision ID: 18591428772b
Revises: 1ad4b3e78299
Create Date: 2018-03-27 17:22:34.722509

"""

# revision identifiers, used by Alembic.
revision = '18591428772b'
down_revision = '1ad4b3e78299'

from alembic import op
import sqlalchemy as sa

def update_database_structure():
    pass

def migrate_datas():
    from autonomie_base.models.base import DBSESSION
    from alembic.context import get_bind
    from autonomie.models.user.userdatas import SocialStatusDatas
    session = DBSESSION()
    connection = get_bind()
    userdatas_helper = sa.Table(
        'user_datas',
        sa.MetaData(),
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('statut_social_status_id', sa.Integer()),
        sa.Column('statut_social_status_today_id', sa.Integer()),
    )
    for userdata in connection.execute(userdatas_helper.select()):
        if userdata.statut_social_status_id:
            social_status_entry = SocialStatusDatas(
                step='entry', 
                userdatas_id=userdata.id, 
                social_status_id=userdata.statut_social_status_id
            )
            session.add(social_status_entry)
        if userdata.statut_social_status_today_id:
            social_status_today = SocialStatusDatas(
                step='today', 
                userdatas_id=userdata.id, 
                social_status_id=userdata.statut_social_status_today_id
            )
            session.add(social_status_today)
    session.flush()

def clean_database():
    op.execute("ALTER TABLE `user_datas` DROP FOREIGN KEY IF EXISTS `fk_user_datas_statut_social_status_id`")
    op.execute("ALTER TABLE `user_datas` DROP INDEX IF EXISTS `fk_user_datas_statut_social_status_id`")
    op.execute("ALTER TABLE `user_datas` DROP FOREIGN KEY IF EXISTS `fk_user_datas_statut_social_status_today_id`")
    op.execute("ALTER TABLE `user_datas` DROP INDEX IF EXISTS `fk_user_datas_statut_social_status_today_id`")
    op.drop_column('user_datas', 'statut_social_status_id')
    op.drop_column('user_datas', 'statut_social_status_today_id')

def upgrade():
    update_database_structure()
    migrate_datas()
    clean_database()

def downgrade():
    pass
