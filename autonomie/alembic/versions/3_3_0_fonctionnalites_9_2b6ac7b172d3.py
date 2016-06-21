"""3.3.0 : fonctionnalites_9

Revision ID: 2b6ac7b172d3
Revises: 25a21d2410b7
Create Date: 2016-06-21 11:12:57.071400

"""

# revision identifiers, used by Alembic.
revision = '2b6ac7b172d3'
down_revision = '25a21d2410b7'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column(
        "user_datas",
        sa.Column(
            'statut_social_status_today_id',
            sa.Integer,
            sa.ForeignKey('social_status_option.id'),
        )
    )
    op.add_column(
        "user_datas",
        sa.Column(
            "parcours_employee_quality_id",
            sa.Integer,
            sa.ForeignKey('employee_quality_option.id'),
        )
    )


def downgrade():
    op.execute("SET FOREIGN_KEY_CHECKS=0;")
    op.drop_table('employee_quality_option')
    op.drop_column('user_datas', 'statut_social_today_id',)
    op.drop_column('user_datas', 'parcours_employee_quality_id',)
    op.execute("SET FOREIGN_KEY_CHECKS=1;")
