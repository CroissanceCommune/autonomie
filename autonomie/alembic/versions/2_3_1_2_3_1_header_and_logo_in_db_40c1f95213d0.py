"""2.3.1 : 2.3.1 header and logo in db

Revision ID: 40c1f95213d0
Revises: 42c3d2634645
Create Date: 2014-10-13 10:45:40.840370

"""

# revision identifiers, used by Alembic.
revision = '40c1f95213d0'
down_revision = '42c3d2634645'

import os
import mimetypes
from alembic import op
import sqlalchemy as sa
import logging
logger = logging.getLogger("alembic.migrate_company_header")


BASEFILEPATH = u"/var/intranet_files/"


def load_file_struct(filepath, filename):
    res = dict()
    if os.path.isfile(filepath):
        data = open(filepath, "rb").read()
        res['data'] = data
        res['mimetype'] = mimetypes.guess_type(filepath)[0] or 'text/plain'
        res['size'] = len(data)
        res['name'] = filename
    else:
        logger.warn("Unknown file %s" % filepath)
    return res


def upgrade():
    from autonomie.models.company import Company
    from autonomie.models.files import File
    from autonomie_base.models.base import DBSESSION
    from alembic.context import get_bind
    from autonomie.models.config import ConfigFiles

    for i in ('header_id', 'logo_id',):
        col = sa.Column(i, sa.Integer, sa.ForeignKey('file.id'))
        op.add_column('company', col)

    query = "select id, header, logo from company;"
    conn = get_bind()
    result = conn.execute(query)

    session = DBSESSION()

    for id_, header, logo in result:
        company = Company.get(id_)
        basepath = u"%scompany/%s" % (BASEFILEPATH, id_,)

        if header:
            header_path = u"%s/header/%s" % (basepath, header)
            try:
                file_datas = load_file_struct(header_path, header)
            except:
                print("Error while loading a header")
                print(id_)
                file_datas = None
            if file_datas:
                company.header = file_datas
                session.add(company.header_file)
                session.flush()

        if logo:
            logo_path = u"%s/logo/%s" % (basepath, logo)
            try:
                file_datas = load_file_struct(logo_path, logo)
            except:
                print("Error while loading a logo")
                print(id_)
                file_datas = None
            if file_datas:
                company.logo = file_datas
                company = session.merge(company)
                session.flush()

    filepath = u"%s/main/logo.png" % BASEFILEPATH
    if os.path.isfile(filepath):
        ConfigFiles.set('logo.png', load_file_struct(filepath, 'logo.png'))

    filepath = u"%s/main/accompagnement_header.png" % BASEFILEPATH
    if os.path.isfile(filepath):
        ConfigFiles.set(
            'accompagnement_header.png',
            load_file_struct(filepath, 'accompagnement_header.png')
        )

def downgrade():
    for query in ("alter table company DROP FOREIGN KEY company_ibfk_1",
                  "alter table company DROP FOREIGN KEY company_ibfk_2",):
        op.execute(query)
    op.drop_column('company', 'logo_id')
    op.drop_column('company', 'header_id')
    op.drop_table('config_files')
