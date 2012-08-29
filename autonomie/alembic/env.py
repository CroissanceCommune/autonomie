from alembic import context
import traceback
import transaction

from autonomie.models import DBSESSION
from autonomie.models import DBMETADATA

def run_migrations_online():
    if DBSESSION.bind is None:
        raise ValueError(
            "\nYou must Autonomie's migration using the 'autonomie-migrate' \
            script"
            "\nand not through 'alembic' directly."
            )

    transaction.begin()
    connection = DBSESSION.connection()

    context.configure(
        connection=connection,
        target_metadata=DBMETADATA,
        )

    try:
        context.run_migrations()
    except:
        traceback.print_exc()
        transaction.abort()
    else:
        transaction.commit()
    finally:
        #connection.close()
        pass

run_migrations_online()
