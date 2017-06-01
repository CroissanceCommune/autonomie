# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

from alembic import context
import traceback
import transaction

from autonomie_base.models.base import DBSESSION
from autonomie.models import DBBASE


def run_migrations_online():
    if DBSESSION.bind is None:
        raise ValueError(
"\nYou must do Autonomie migrations using the 'autonomie-migrate' script"
"\nand not through 'alembic' directly."
            )

    transaction.begin()
    connection = DBSESSION.connection()

    context.configure(
        connection=connection,
        target_metadata=DBBASE.metadata,
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
