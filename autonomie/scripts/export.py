# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import datetime
import json

from autonomie.scripts.utils import (
    command,
    get_value,
)
from autonomie.models.base import DBSESSION as db


def _get_query(model, where):
    """
    Return a query on the given model

    :param cls model: The model to get items from
    :param list where: List of criteria in dict form
    :returns: A SQLA query
    :rtype: obj
    """
    from autonomie.models.statistics import StatisticEntry
    from autonomie.views.statistics import (
        CRITERION_MODELS,
        get_inspector,
    )
    from autonomie.statistics import EntryQueryFactory

    entry = StatisticEntry(title="script related entry", description="")

    for criterion_dict in where:
        criterion_factory = CRITERION_MODELS[criterion_dict['type']]
        entry.criteria.append(criterion_factory(**criterion_dict))

    inspector = get_inspector()
    query_factory = EntryQueryFactory(model, entry, inspector)
    return query_factory.query()


def _filter_headers(writer, fields):
    """
    ensure only the fields we wanted are effectively returned by the writer
    """
    headers = []
    all_headers = writer.headers
    for field in fields:
        for header in all_headers:
            hname = header["key"]
            if field == hname:
                headers.append(header)
    writer.headers = headers


def _stream_csv_rows(model, query, fields):
    """
    Stream the rows contained in query
    """
    from sqla_inspect.csv import SqlaCsvExporter
    from autonomie.views.user import add_o2m_headers_to_writer
    writer = SqlaCsvExporter(model)
    writer = add_o2m_headers_to_writer(writer, query)

    _filter_headers(writer, fields)
    for id, item in query.all():
        writer.add_row(item)
    print(writer.render().read())


def _export_user_datas(args, env):
    """
    Export userdatas as csv format

    Streams the output in stdout

    autonomie-export app.ini userdatas --fields=coordonnees_address,coordonnees_zipcode,coordonnees_city,coordonnees_sex,coordonnees_birthday,statut_social_status,coordonnees_study_level,parcours_date_info_coll,parcours_prescripteur,parcours_convention_cape,activity_typologie,sortie_date,sortie_motif --where='[{"key":"created_at","method":"dr","type":"date","search1":"1999-01-01","search2":"2016-12-31"}]' > /tmp/toto.csv

    :param dict args: The arguments coming from the command line
    :param dict env: The environment bootstraped when setting up the pyramid app
    """
    from autonomie.models.user import UserDatas

    logger = logging.getLogger(__name__)
    fields = get_value(args, "fields", "").split(',')
    where_str = get_value(args, "where", "{}")
    try:
        where = json.loads(where_str)
        if isinstance(where, dict):
            where = [where]
    except:
        logger.exception("Where should be in json format")
        where = []

    logger.debug("Fields : {0}".format(fields))
    logger.debug("Where : {0}".format(where))

    if where:
        query = _get_query(UserDatas, where)
    else:
        query = UserDatas.query()

    _stream_csv_rows(UserDatas, query, fields)


def export_cmd():
    """Export utilitiy tool, stream csv datas in stdout

    Usage:
        autonomie-export <config_uri> userdatas [--fields=<fields>] [--where=<where>]

    o userdatas : export userdatas

    Options:
        -h --help             Show this screen
        --fields=<fields>     Export the comma separated list of fields
        --where=<where>       Query parameters in json format
    """
    def callback(arguments, env):
        args = ()
        if arguments['userdatas']:
            func = _export_user_datas
        return func(arguments, env)

    try:
        return command(callback, export_cmd.__doc__)
    finally:
        pass
