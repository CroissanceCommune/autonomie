"""4.2.0 add_filetype_table

Revision ID: 11a62732db65
Revises: 44f964dc36a2
Create Date: 2018-06-05 16:27:08.014127

"""

# revision identifiers, used by Alembic.
revision = '11a62732db65'
down_revision = '44f964dc36a2'

import logging
from alembic import op
import sqlalchemy as sa


def update_database_structure():
    op.add_column(
        'file',
        sa.Column(
            "file_type_id",
            sa.Integer,
            sa.ForeignKey('file_type.id'),
            nullable=True,
        )
    )


def migrate_datas():
    logger = logging.getLogger("alembic.autonomie")
    from autonomie_base.models.base import DBSESSION
    session = DBSESSION()
    from autonomie.models.config import Config
    import json

    from autonomie.models.files import (
        File,
        FileType,
    )
    json_str = Config.get_value("attached_filetypes", "[]")
    try:
        configured_filetypes = json.loads(json_str)
    except:
        logger.exception(u"Error in json str : %s" % json_str)
        configured_filetypes = []
    if configured_filetypes:
        result = []
        for filetype_label in configured_filetypes:
            if filetype_label:
                filetype = FileType(label=filetype_label)
                session.add(filetype)
                session.flush()
                result.append(filetype)

        for typ_ in result:
            query = File.query().filter_by(label=typ_.label)
            for file_ in query:
                file_.file_type_id = typ_.id
                session.merge(file_)
        session.flush()



def upgrade():
    update_database_structure()
    migrate_datas()


def downgrade():
    op.drop_constraint('file', 'fk_file_file_type_id')
    op.drop_column("file", "file_type_id")
