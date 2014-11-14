"""2.4 : userdatas_is_node

Revision ID: 46beb4c6f140
Revises: 40c1f95213d0
Create Date: 2014-11-11 19:30:39.741070

"""

# revision identifiers, used by Alembic.
revision = '46beb4c6f140'
down_revision = '40c1f95213d0'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('node', sa.Column('_acl', sa.Text()))

    from autonomie.models.base import DBSESSION
    from autonomie.models.node import Node
    session = DBSESSION()
    from alembic.context import get_bind
    conn = get_bind()
    req = "select max(id) from node"
    result = conn.execute(req).fetchall()
    max_id = result[0][0]

    print("The new max_id is : %s" % max_id)

    request = "select id, coordonnees_lastname from user_datas"
    result = conn.execute(request)

    op.execute("SET FOREIGN_KEY_CHECKS=0;")

    for index, (id, lastname) in enumerate(result):
        max_id += 1
        new_id = max_id
        node = Node(
            id=new_id,
            name=lastname,
            type_='userdata',
        )
        session.add(node)
        # Update des relations
        for table in "userdatas_socialdocs", "external_activity_datas", \
                     "company_datas", "date_diagnostic_datas", \
                     "date_convention_cape_datas", "date_dpae_datas":
            op.execute("update {0} set userdatas_id={1} where userdatas_id={2}".format(table, new_id,  id))
        # Update de la table node
        op.execute("update user_datas set id={0} where id={1};".format(new_id, id))
        if index % 50 == 0:
            session.flush()

    op.execute("SET FOREIGN_KEY_CHECKS=1;")


def downgrade():
    op.execute("delete from node where type_='userdata'")
    op.drop_column('node', '_acl')
