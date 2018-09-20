# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import json
import datetime
import os

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

    inspector = get_inspector(model)
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
            elif (
                not item.parcours_end_date or
                item.parcours_end_date >= refdate
            ):
                start_year = "Oui"

        datas.append(start_year)
        datas.append(this_year)

        writer.add_extra_datas(datas)
    print(writer.render().read())


def _export_userdatas_command(args, env):
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


def _write_invoice_on_disk(request, document, destdir, prefix, key):
    """
    Write an invoice on disk

    :param obj request: The current env request instance
    :param obj document: The document instance (invoice/cancelinvoice)
    :param str destdir: An existing dest directory
    :param str prefix: The prefix to add before dest file name
    :param str key: A key used to make the name unique
    """
    from autonomie.views.task.views import (
        html,
    )
    from autonomie.utils.pdf import buffer_pdf
    from pyramid_layout.config import create_layout_manager

    class A:
        def __init__(self, req):
            self.request = req

    logger = logging.getLogger(__name__)
    dest_file = u"%s_%s_%s.pdf" % (prefix, document.official_number, key)
    filepath = os.path.join(destdir, dest_file)
    logger.debug("Writing : %s" % filepath)
    request.context = document
    create_layout_manager(A(request))

    html_str = html(request, tasks=[document], bulk=True)
    with file(filepath, 'wb') as fbuf:
        fbuf.write(buffer_pdf(html_str).read())


def _invoices_pdf_command(args, env):
    """
    export pdf of the documents matching the given parameters
    """
    request = env['request']
    from autonomie.models.task import (
        Invoice, CancelInvoice,
    )
    logger = logging.getLogger(__name__)
    destdir = get_value(args, "destdir")
    if not os.path.isdir(destdir):
        raise Exception(u"Le répertoire de destination n'existe pas")

    where_str = get_value(args, "where")
    if not where_str:
        raise Exception(u"L'argument de recherche where est requis")
    try:
        where = json.loads(where_str)
        if isinstance(where, dict):
            where = [where]
    except:
        logger.exception("Where should be in json format")
        where = []

    invoice_query = _get_query(Invoice, where)
    cinvoice_query = _get_query(CancelInvoice, where)
    invoice_query = invoice_query.filter_by(status='valid')
    cinvoice_query = cinvoice_query.filter_by(status='valid')
    logger.debug(u"Exporting %s invoices to pdf" % invoice_query.count())
    logger.debug(u"Exporting %s cancelinvoices to pdf" % cinvoice_query.count())
    index = 0
    for invoice in invoice_query:
        _write_invoice_on_disk(
            request, invoice[1], destdir, prefix=u"facture", key=str(index)
        )
        index += 1
    for cinvoice in cinvoice_query:
        _write_invoice_on_disk(
            request, cinvoice[1], destdir, prefix=u"avoir", key=str(index)
        )
        index += 1
    logger.debug(u"Export has finished, check %s" % destdir)


def export_economic_stats2018(args, env):
    """
    Exporte les données statistiques au format 2018
    """
    logger = logging.getLogger(__name__)
    destdir = get_value(args, "destdir")
    if not os.path.isdir(destdir):
        raise Exception(u"Le répertoire de destination n'existe pas")

    year = get_value(args, 'year')
    cae = get_value(args, 'cae')

    from sqlalchemy.orm import load_only
    from sqlalchemy import or_
    from autonomie.models.company import Company
    from autonomie.models.task import Task, Invoice, CancelInvoice
    from autonomie.compute.math_utils import integer_to_amount
    docs = Task.query().with_polymorphic(
        [Invoice, CancelInvoice]
    ).options(
        load_only('customer_id', 'company_id', 'id', 'ht')
    ).filter(
        Task.type_.in_(('invoice', 'cancelinvoice'))
    ).filter(
        or_(
            Invoice.financial_year == year,
            CancelInvoice.financial_year == year,
        )
    )
    datas = {}
    for i in docs:
        company_dict = datas.setdefault(i.company_id, {})
        company_dict.setdefault('ca', 0)
        company_dict['ca'] += integer_to_amount(i.ht, precision=5)
        company_dict.setdefault('customers', {}).setdefault(i.customer_id, 0)
        company_dict['customers'][i.customer_id] += 1
        company_dict.setdefault('count', 0)
        company_dict['count'] += 1
        company_dict['cae'] = cae

    for key, value in datas.items():
        value['customer_nums'] = len(value['customers'].keys())

    company_ids = datas.keys()
    if company_ids:
        companies = Company.query().filter(Company.id.in_(company_ids))
        for company in companies:
            datas[company.id]['activities'] = ""
            for a in company.activities:
                datas[company.id]['activities'] += u"{}, ".format(a.label)
            datas[company.id]['salaries'] = 0
            for user in company.employees:
                if user.userdatas is not None:
                    if user.userdatas.parcours_salary is not None:
                        datas[company.id]['salaries'] += user.userdatas.parcours_salary

    from sqla_inspect.csv import CsvWriter
    writer = CsvWriter()
    headers = [
        {'name': "cae", "label": u"CAE"},
        {'name': "activities", 'label': u"Type d'activité"},
        {'name': "ca", "label": u"Chiffre d'affaire"},
        {'name': "salaries", "label": u"Salaires produits"},
        {'name': "count", "label": u"Nombre de facture"},
        {'name': "customer_nums", "label": u"Nombre de clients"},
    ]
    writer.set_headers(headers)
    writer._datas = [writer.format_row(value) for value in datas.values()]
    dest_file = os.path.join(
        destdir,
        "export_statistic2018_{}_annee_{}.csv".format(cae.replace(' ', '_'), year)
    )
    with open(dest_file, 'w') as fbuf:
        writer.render(fbuf)
    print(dest_file)


def export_cmd():
    """Export utilitiy tool, stream csv datas in stdout
    Usage:
        autonomie-export <config_uri> userdatas [--fields=<fields>] [--where=<where>]
        autonomie-export <config_uri> invoices_pdf [--destdir=<destdir>] [--where=<where>]
        autonomie-export <config_uri> economic_statistics2018 [--cae=<destdir] [--destdir=<destdir>] [--year=<year>]

    Options:
        -h --help             Show this screen
        --fields=<fields>     Export the comma separated list of fields
        --where=<where>       Query parameters in json format descrbing
        statistic options
        --destdir=<destdir>   The directory where we output the datas

    o userdatas     : Export userdatas as csv format
    o invoices_pdf  : Export Invoices and CancelInvoices in pdf format
    o economic_statistics2018

    Streams the output in stdout

    autonomie-export app.ini userdatas \
    --fields=coordonnees_address,coordonnees_zipcode,coordonnees_city,\
        coordonnees_sex,coordonnees_birthday,statut_social_status,\
        coordonnees_study_level,parcours_date_info_coll,parcours_prescripteur,\
        parcours_convention_cape,activity_typologie,sortie_date,sortie_motif \
    --where='[{"key":"created_at","method":"dr","type":"date",\
        "search1":"1999-01-01","search2":"2016-12-31"}]'\
    > /tmp/toto.csv

    autonomie-export
    """
    def callback(arguments, env):
        if arguments['userdatas']:
            func = _export_userdatas_command
        elif arguments['invoices_pdf']:
            func = _invoices_pdf_command
        elif arguments['economic_statistics2018']:
            func = export_economic_stats2018
        return func(arguments, env)

    try:
        return command(callback, export_cmd.__doc__)
    finally:
        pass
