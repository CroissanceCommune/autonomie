# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import json
import datetime

from autonomie.scripts.utils import (
    command,
    get_value,
)


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


def _find_start_situation(userdatas, refdate):
    """
    Find the situation of the user at refdate

    :param obj userdatas: The object to check
    :param obj refdate: The reference date (datetime.date object
    :returns: A label
    """
    res = ""
    for situation in userdatas.situation_history:
        if situation.date > refdate:
            break
        else:
            res = situation.situation.label

    if not res:
        if userdatas.created_at.date() < refdate and \
                userdatas.situation_situation:
            res = userdatas.situation_situation.label

    return res


def _stream_csv_rows(model, query, fields):
    """
    Stream the rows contained in query
    """
    from sqla_inspect.csv import SqlaCsvExporter
    from autonomie_celery.tasks.export import _add_o2m_headers_to_writer
    writer = SqlaCsvExporter(model)
    writer = _add_o2m_headers_to_writer(writer, query, 'userdatas_id')

    for field in (
        {'name': 'status_start_year', "label": "Statut début année"},
        {'name': 'status_end_year', "label": "Statut fin d'année"},
        {'name': "was_cape", "label": "Était sous cape au premier janvier"},
        {'name': 'had_cape',
         'label': "Avait déjà signé un cape avant cette année"},
        {'name': 'cape_this_year', 'label': "A signé un Cape cette année"},
        {
            'name': 'was_contract',
            'label': 'Était déjà sous contrat au premier janvier de cette année'
        },
        {'name': 'contract', 'label': 'A signé un contrat cette année'},
    ):
        writer.add_extra_header(field)

    refdate = datetime.date(2017, 1, 1)

    _filter_headers(writer, fields)
    for id, item in query.all():
        writer.add_row(item)
        datas = []

        # start_situation
        datas.append(_find_start_situation(item, refdate).encode('utf-8'))

        # end situation
        if item.situation_situation is not None:
            datas.append(item.situation_situation.label.encode('utf-8'))
        else:
            datas.append('')

        # CAPE
        before = "Non"
        start_year = "Non"
        this_year = "Non"
        for cape in item.parcours_convention_cape:
            if cape.date:
                if cape.date < refdate:
                    if not cape.end_date or cape.end_date >= refdate:
                        start_year = "Oui"
                    else:
                        before = "Oui"

                else:
                    this_year = "Oui"
                    break

        datas.append(before)
        datas.append(start_year)
        datas.append(this_year)

        # contract
        start_year = "Non"
        this_year = "Non"

        if item.parcours_start_date:
            if item.parcours_start_date >= refdate:
                this_year = "Oui"
            elif not item.parcours_end_date or item.parcours_end_date >= refdate:
                start_year = "Oui"

        datas.append(start_year)
        datas.append(this_year)

        writer.add_extra_datas(datas)
    print(writer.render().read())


def _export_user_datas(args, env):
    """
    Export userdatas as csv format

    Streams the output in stdout

    autonomie-export app.ini userdatas \
    --fields=coordonnees_address,coordonnees_zipcode,coordonnees_city,\
        coordonnees_sex,coordonnees_birthday,statut_social_status,\
        coordonnees_study_level,parcours_date_info_coll,parcours_prescripteur,\
        parcours_convention_cape,activity_typologie,sortie_date,sortie_motif \
    --where='[{"key":"created_at","method":"dr","type":"date",\
        "search1":"1999-01-01","search2":"2016-12-31"}]'\
    > /tmp/toto.csv

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


def _export_cpe(args, env):
    """
    Generate the cpe export


    :param dict args: The arguments coming from the command line
    :param dict env: The environment bootstraped when setting up the pyramid app
    """
    pass


def export_cmd():
    """Export utilitiy tool, stream csv datas in stdout
    Usage:
        autonomie-export <config_uri> userdatas [--fields=<fields>] [--where=<where>]

    Options:
        -h --help             Show this screen
        --fields=<fields>     Export the comma separated list of fields
        --where=<where>       Query parameters in json format

    o userdatas : Export userdatas as csv format

    Streams the output in stdout

    autonomie-export app.ini userdatas \
    --fields=coordonnees_address,coordonnees_zipcode,coordonnees_city,\
        coordonnees_sex,coordonnees_birthday,statut_social_status,\
        coordonnees_study_level,parcours_date_info_coll,parcours_prescripteur,\
        parcours_convention_cape,activity_typologie,sortie_date,sortie_motif \
    --where='[{"key":"created_at","method":"dr","type":"date",\
        "search1":"1999-01-01","search2":"2016-12-31"}]'\
    > /tmp/toto.csv
    """
    def callback(arguments, env):
        if arguments['userdatas']:
            func = _export_user_datas
        return func(arguments, env)

    try:
        return command(callback, export_cmd.__doc__)
    finally:
        pass
