"""2.3 : add userdatas

Revision ID: 591c8309dc2b
Revises: 15d4152bd5d6
Create Date: 2014-07-07 17:35:26.009603

"""

# revision identifiers, used by Alembic.
revision = '591c8309dc2b'
down_revision = '15d4152bd5d6'

from alembic import op
import sqlalchemy as sa


def upgrade():
    from autonomie.models import user
    from autonomie.models.base import DBSESSION

    db = DBSESSION()

    for u in db.query(user.User)\
             .filter(user.User.active=='Y')\
             .filter(user.User.primary_group==3):
        situation = "integre"
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
