"""3.1 : move to filedepot

Revision ID: 4cb8e3e01f36
Revises: 39c70a8da291
Create Date: 2015-10-10 10:05:44.476390

"""

# revision identifiers, used by Alembic.
revision = '4cb8e3e01f36'
down_revision = '39c70a8da291'

import sys
import time
from alembic import op
import logging
import sqlalchemy as sa


def upgrade():
    logger = logging.getLogger('autonomie')
    logger.addHandler(logging.StreamHandler(sys.stdout))
    logger.setLevel(logging.INFO)
    from depot.fields.upload import UploadedFile
    from sqlalchemy import bindparam

    from autonomie.models.base import DBSESSION, METADATA

    try:
        op.add_column("file", sa.Column('depot', sa.Unicode(4096)))
    except:
        pass

    session = DBSESSION()

    def process(thing, store):
        id, data, filename, mimetype = thing
        logger.debug("Handling file with id %s" % id)
        uploaded_file = UploadedFile(
            {'depot_name': "local", 'files': []}
        )
        uploaded_file._thaw()
        uploaded_file.process_content(
            data, filename=filename, content_type=mimetype
        )
        store.append(
            {
                'nodeid': thing.id,
                'depot_datas': uploaded_file.encode(),
            }
        )
        logger.info("Saved data for node id {}".format(id))

    window_size = 10
    window_idx = 0

    logger.info("# Starting migration of blob datas #")
    from alembic.context import get_bind
    conn = get_bind()

    # Processing the file table
    logger.debug("  + Processing files")
    files = sa.Table('file', METADATA)
    processed_files = []
    count = session.query(files.c.id).count()

    logger.debug(u"   + Moving the files on disk")
    now = time.time()
    while True:
        start = window_size * window_idx
        if start >= count:
            break
        logger.debug("Slicing from %s" % (start,))

        req = "select distinct(file.id), data, node.name, mimetype from file join node on file.id=node.id LIMIT %s, %s" % (start, window_size)
        things = conn.execute(req)
        if things is None:
            break

        for thing in things:
            process(thing, processed_files)

        window_idx += 1
    logger.debug(u"-> Done")

    logger.debug(u"Migrating the 'data' column")
    op.drop_column('file', 'data')
    op.add_column('file', sa.Column('data', sa.Unicode(4096)))
    files.c.data.type = sa.Unicode(4096)

    update = files.update().where(files.c.id == bindparam('nodeid')).\
        values({files.c.data: bindparam('depot_datas')})

    def chunks(l, n):
        for i in xrange(0, len(l), n):
            yield l[i:i + n]

    for cdata in chunks(processed_files, 10):
        session.execute(update, cdata)

    logger.debug("  + Processing config files")
    logger.debug(u"   + Moving the files on disk")
    config_files = sa.Table('config_files', METADATA)
    processed_config_files = []
    req = "select id, data, name, mimetype from config_files"
    for thing in conn.execute(req):
        process(thing, processed_config_files)

    op.drop_column('config_files', 'data')
    op.add_column('config_files', sa.Column('data', sa.Unicode(4096)))
    files.c.data.type = sa.Unicode(4096)
    update = config_files.update().where(files.c.id == bindparam('nodeid')).\
        values({files.c.data: bindparam('depot_datas')})

    session.execute(update, processed_config_files)

    logger.debug(u"-> Done")

    from zope.sqlalchemy import mark_changed
    mark_changed(session)

    logger.info("Blob migration completed in {} seconds".format(
        int(time.time() - now)))


def downgrade():
    pass
