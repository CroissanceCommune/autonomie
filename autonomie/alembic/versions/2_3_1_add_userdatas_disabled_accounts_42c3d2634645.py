"""2.3.1 : add userdatas disabled accounts

Revision ID: 42c3d2634645
Revises: 591c8309dc2b
Create Date: 2014-09-05 11:02:29.068338

"""

# revision identifiers, used by Alembic.
revision = '42c3d2634645'
down_revision = '591c8309dc2b'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from autonomie.models import user
    from autonomie_base.models.base import DBSESSION

    db = DBSESSION()

    for u in db.query(user.User)\
             .filter(user.User.userdatas==None)\
             .filter(user.User.primary_group==3):
        situation = "sortie"
        if u.email:
            userdata = user.UserDatas(
                situation_situation=situation,
                coordonnees_firstname=u.firstname,
                coordonnees_lastname=u.lastname,
                coordonnees_email1=u.email,
                coordonnees_civilite=u'?',
            )
            userdata.user_id = u.id
            for company in u.companies:
                companydata = user.CompanyDatas(
                    title=company.goal,
                    name=company.name,
                )
                userdata.activity_companydatas.append(companydata)
            db.add(userdata)
            db.flush()


def downgrade():
    pass
