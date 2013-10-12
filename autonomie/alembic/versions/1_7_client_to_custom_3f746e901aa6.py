"""1.7 : Client to Customer

Revision ID: 3f746e901aa6
Revises: 2b29f533fdfc
Create Date: 2010-10-14 14:47:39.964827

"""

# revision identifiers, used by Alembic.
revision = '3f746e901aa6'
down_revision = '29299007fe7d'

from alembic import op
import sqlalchemy as sa

foreign_key_names = (
            ("invoice", "invoice_ibfk_4",),
            ("estimation", "estimation_ibfk_3",),
            ("cancelinvoice", "cancelinvoice_ibfk_4",),
            ("manualinv", "manualinv_ibfk_2",),
            )

def remove_foreign_key(table, key):
    query = "alter table %s drop foreign key %s;" % (table, key)
    try:
        op.execute(query)
        has_key =  True
    except:
        import traceback
        traceback.print_exc()
        print "An error occured dropping foreign key"
        has_key = False
    return has_key

def upgrade():
    from autonomie.alembic.utils import force_rename_table
    from autonomie.alembic.utils import rename_column
    has_fkey = {
            'estimation':False,
            "invoice": False,
            "cancelinvoice": False,
            "manualinv": False
            }


    # Remove foreign keys to be able to rename columns
    for table, fkey in foreign_key_names:
        has_fkey[table] = remove_foreign_key(table, fkey)

    # Rename columns
    for table in (
            'estimation',
            'invoice',
            'cancelinvoice',
            'manualinv',
            ):
        rename_column(table, 'client_id', 'customer_id')
        op.execute("delete from %s where customer_id=0;" % table)

    # Add the foreign key constraint again
    for table, fkey in foreign_key_names:
        if has_fkey[table]:
            op.create_foreign_key(
                fkey,
                table,
                'customer',
                ['customer_id'],
                ['id'])

    remove_foreign_key("project_client", "project_client_ibfk_2")
    # Rename the project client
    force_rename_table('project_client', 'project_customer')


    # Rename the column
    rename_column('project_customer', 'client_id', 'customer_id')

    op.create_foreign_key(
        "project_customer_ibfk_2",
        'project_customer',
        'customer',
        ['customer_id'],
        ['id'])


def downgrade():
    from autonomie.alembic.utils import force_rename_table
    from autonomie.alembic.utils import rename_column

    for table, key in foreign_key_names:
        remove_foreign_key(table, key)

    for table in ('estimation', 'invoice', 'cancelinvoice', 'manualinvoice'):
        fkey = "%s_ibfk_1" % table
        query = "alter table %s drop foreign key %s;" % (table, fkey)
        op.execute(query)
        rename_column(table, 'customer_id', 'client_id')

    for table, key in foreign_key_names:
        op.create_foreign_key(
            fkey,
            table,
            'customer',
            ['client_id'],
            ['id'])
    force_rename_table('project_customer', 'project_client')
    # Rename the column
    fkey = "project_client_ibfk_2"
    remove_foreign_key("project_client", "project_customer_ibfk_2")

    rename_column('project_client', 'customer_id', 'client_id')

    op.create_foreign_key(
        "project_client_ibfk_2",
        'project_client',
        'customer',
        ['client_id'],
        ['id'])

