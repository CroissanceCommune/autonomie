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

"""
    This view displays the documents of the current company
"""
import os
import re
import datetime
import logging
import mimetypes
import colander
import redis.exceptions

import peppercorn
from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPNotFound,
    HTTPFound,
)

from autonomie.models.files import (
    MailHistory,
    check_if_mail_sent,
)
from autonomie.forms.lists import BaseListsSchema
from autonomie.forms.treasury_files import MailSendingSchema
from autonomie.views import (
    BaseView,
    BaseListView,
)
from autonomie.models.company import Company
from autonomie.models.job import MailingJob
from autonomie.views.render_api import month_name
from autonomie.mail import send_salary_sheet
from autonomie.task import async_mail_salarysheets
from autonomie.utils.ascii import force_ascii
from autonomie.utils.files import (
    encode_path,
    decode_path,
    issubdir,
    filesizeformat,
)

DEFAULT_MAIL_OBJECT = {
    'salaire': u"""Votre bulletin de salaire"""
}


DEFAULT_MAIL_MESSAGE = {
    'salaire': u"""Bonjour {company.name},
Vous trouverez ci-joint votre bulletin de salaire pour la période {month}/{year}.
""",
}

# Regexp permettant de récupérer le code analytique depuis le nom d'un fichier
REGEXP = re.compile('(?P<code_compta>[^_]+).')


_NULLCODES = ["0", 0, "", None]


logger = logging.getLogger(__name__)


def is_valid_year(year_str):
    """
    Return True if the given string seems to be a valid year
    """
    return year_str.isdigit() and len(year_str) == 4


def get_root_directory(request):
    """
        get the root directory of files handled in this module
    """
    absdir = request.registry.settings.get('autonomie.ftpdir')
    if not absdir:
        raise Exception(u"The ftpdirectory could not be found, \
            please set it up.")
    return absdir


def get_code_compta(filename):
    """
    Get the code compta extracted from the given filename
    :param str filename: A filename in which we should find the code
    """
    groups = REGEXP.match(filename)
    if groups is None:
        raise Exception(
            "The given filepath doesn't match the regexp : %s" % (
                filename
            )
        )
    return groups.group("code_compta")


def belongs_to_company(filename):
    """
    Check if a file belongs to a company

    :param str filename: The filename we want to check
    """
    code_compta = get_code_compta(filename)
    return Company.query().filter(Company.code_compta==code_compta).count() > 0


def get_company_by_code(code_compta):
    """
    Return the company associated to this code_compta
    :param str code_compta: The analytic code of the company to find
    """
    query = Company.query().filter(Company.code_compta==code_compta)
    return query.first()


def code_is_not_null(code):
    """
    Return True if the given code is not null
    :param str code: The code to check
    """
    return code not in _NULLCODES


def isprefixed(filename, prefix='___'):
    """
    Return True if the filename startswith prefix + '_'
    return False if bool(prefix) is False
    """
    prefix += '_'
    if prefix == '____':
        return True
    else:
        return filename.startswith(prefix)


def current_years():
    """
    return a list of the years that should be considered as currents
    :returns: The current year and the precedent one if we're in january
    """
    today = datetime.date.today()
    result = [str(today.year)]
    if today.month == 1:
        result.append(str(today.year - 1))
    return result


def digit_subdirs(path):
    """
    Return subdirectories of path which names are composed of digits
    """
    for name in os.listdir(path):
        spath = os.path.join(path, name)
        if os.path.isdir(spath) and name.isdigit():
            yield name, spath


def list_files(path, prefix='___'):
    """
    Return files in path that are prefixed with prefix

    :param str prefix: the prefix of the file
        (e.g : 125 for a file starting by 125_)
    :returns: A sorted list of abstract file objects
    """
    # prefix has a strange form since the prefix is a security point and a
    # void one could lead to security issues
    result = []
    for name in os.listdir(path):
        filepath = os.path.join(path, name)
        if os.path.isfile(filepath):
            if prefix and not isprefixed(name, prefix):
                continue
            file_obj = AbstractFile(name, filepath)
            result.append(file_obj)
    result.sort(key=lambda f:f.path)
    return result


class AbstractFile(object):
    """
    File object abstraction used to easily handle treasury files
    Provides :
        * meta informations
        * urls generation
        * other infos
    """
    def __init__(self, name, path):
        self.name = name
        self.path = path
        self._mod_time = os.path.getatime(path)
        self._size = os.path.getsize(path)

    @property
    def mod_date(self):
        """
        return a datetime object for the atime of the file
        """
        return datetime.datetime.fromtimestamp(self._mod_time)

    @property
    def size(self):
        """
        Return a pretty printing value of the file
        """
        return filesizeformat(self._size)

    @property
    def mimetype(self):
        """
        Return the mimetype of the file, "text/plain"
        if None could be found
        """
        mtype = mimetypes.guess_type(self.path)[0]
        if mtype is None:
            mtype = "text/plain"
        return mtype

    @property
    def datas(self):
        """
        Return the content of the file
        """
        return open(self.path).read()

    @property
    def code(self):
        """
        The code compta found in the filename
        """
        try:
            res = get_code_compta(self.name)
        except Exception:
            res = None
        return res

    def url(self, request, company_id=None):
        """
        return the url to fetch the given file

        :param obj request: The current request object
        :param int company_id: The id of the company owning the document
            (default: the current request context)
        """
        if company_id is None:
            company_id = request.context.id

        root_directory = get_root_directory(request)
        relpath = self.path.replace(root_directory, "", 1)

        return request.route_path(
            "treasury_files",
            id=company_id,
            _query=dict(name=encode_path(relpath))
        )

    def as_response(self, request):
        """
        Stream the file in the current request's response
        """
        request.response.content_type = self.mimetype
        request.response.headerlist.append(
                ('Content-Disposition',
                'attachment; filename={0}'.format(force_ascii(self.name))))
        request.response.write(self.datas)
        return request

    def __repr__(self):
        return "<AbstractFile : %s %s>" % (self.name, self.path)

    def is_in_mail_history(self, company):
        """
        Return True if this file is already in the mail history
        (based on the md5 sum of the content)
        :param obj company: The company to which this file should have been sent
        """
        return check_if_mail_sent(
            open(self.path, 'r').read(),
            company.id,
        )


class DisplayDirectoryView(BaseView):
    """
    Base view for document directory display
    Given a directory, it looks up for all subdirectories of the form :
        <root_dir>/<year>/<month>
    to find files of the form
    <code analytique>_annee_mois_semaine
    """
    title = u""
    _root_directory = None

    @property
    def root_directory(self):
        """
            return the abspath of the root_directory
        """
        return os.path.join(get_root_directory(self.request),
                                            self._root_directory)

    def collect_documents(self, prefix):
        """
            collect all documents restricted to the given prefix
        """
        result_dict = {}
        if self.root_directory is not None and \
                os.path.isdir(self.root_directory):
            for year, year_path in digit_subdirs(self.root_directory):
                result_dict[year] = {}
                for month, month_path in digit_subdirs(year_path):
                    result_dict[year][month] = list_files(
                        month_path,
                        prefix,
                    )
        return result_dict

    def __call__(self):
        company_code = self.request.context.code_compta
        if code_is_not_null(company_code):
            documents = self.collect_documents(company_code)
        else:
            documents = {}
        return dict(title=self.title,
                documents=documents,
                current_years=current_years()
                )


class TreasuryFilesView(DisplayDirectoryView):
    """
        List the Treasury directory
    """
    title = u"Trésorerie"
    _root_directory = "tresorerie"


class IncomeStatementFilesView(DisplayDirectoryView):
    """
        List the Income Statements
    """
    title = u"Compte de résultat"
    _root_directory = "resultat"


class SalarySheetFilesView(DisplayDirectoryView):
    """
        List the salary sheets
    """
    title = u"Bulletin de salaire"
    _root_directory = "salaire"


class AdminTreasuryView(BaseView):
    """
    Admin View for documents supervision (mailing ...)
    """
    title = u"Administration des fichiers"
    filetypes = ('salaire', ) #'trésorerie', 'resultat')

    def __init__(self, context, request):
        BaseView.__init__(self, context, request)
        self.root_directory = get_root_directory(request)

    def get_entry(self, result, year, month, month_dir, type_):
        """
        Return an entry for the listing for admin files
        """
        result = None
        label = month_name(month)
        if label:
            all_files = [filename for filename in os.listdir(month_dir)\
                            if belongs_to_company(filename)]
            if len(all_files) > 0:
                url = self.request.route_path(
                    'admin_treasury_files',
                    filetype=type_,
                    year=year,
                    month=month,
                )
                result = {
                    "label": label,
                    "url": url,
                    "nbfiles": len(all_files),
                }
        return result

    def collect_years_and_months(self):
        """
        Collect years and months for which we have files
        """
        result = {}
        for type_ in self.filetypes:
            type_dir = os.path.join(self.root_directory, type_)
            for year, year_dir in digit_subdirs(type_dir):
                result[year] = {}
                for month, month_dir in digit_subdirs(year_dir):
                    if month in result[year]:
                        continue

                    entry = self.get_entry(
                        result,
                        year,
                        month,
                        month_dir,
                        type_
                    )
                    if entry is not None:
                        result[year][month] = entry
        return result

    def __call__(self):
        return dict(
            title=self.title,
            datas=self.collect_years_and_months(),
            current_years=current_years()
        )


class MailTreasuryFilesView(BaseView):
    """
    View used to mail salary sheets

    Following url parameters are mandatory :

        filetype

            The filetype we'd like to list

        year

        month
    """
    title = u"Envoi de fichiers par e-mail"

    def collect_files(self, path):
        """
        Collect files and associated companies for the given view
        """
        datas = {}
        files = list_files(path, prefix=None)

        for abstract_file in files:

            code = abstract_file.code
            if code is None:
                continue
            company = get_company_by_code(code)
            if company is None:
                continue

            datas.setdefault(company.id, []).append(
                {
                    'file': abstract_file,
                    'company': company,
                }
            )
        return datas

    def _prepare_mails(self, datas, form_datas, root_path, year, month):
        """
        Prepare the emails adding some informations in it

        :param dict datas: The file listing datas
        :param dict form_datas: The validated submitted datas
        :param str root_path: The absolute root_path to the files
        :param int year: The year associated to the files
        :param int month: The month associated to the files
        """
        force = form_datas.get('force', False)
        message_tmpl = form_datas['mail_message']
        subject = form_datas['mail_subject']

        mails = []
        for mail_dict in form_datas['mails']:
            # Le form renvoie des couples (company_id, attachment), on
            # enlève ceux pour lesquels aucune pièce jointe n'est
            # remplie (la case n'a pas été cochée)
            if "attachment" not in mail_dict.keys():
                continue

            filedatas = self._get_file_datas_entry(datas, mail_dict)
            company = filedatas['company']

            # Si on ne force pas l'envoi, on va enlever les documents
            # qui ont déjà été envoyé
            if not force:
                if filedatas['file'].is_in_mail_history(company):
                    continue

            mail_dict['attachment_path'] = self._prepare_attachment(
                root_path,
                mail_dict,
            )
            mail_dict['message'] = self._prepare_message(
                message_tmpl, company, year, month)
            mail_dict['subject'] = subject
            mail_dict['email'] = company.email

            mails.append(mail_dict)
        return mails


    def _prepare_attachment(self, root_path, mail):
        """
        Return the attachment absolute filepath
        :param str root_path: The directory we manage
        :param dict mail_dicts: The dict representing a mail
        :returns: The full file path
        """
        # On ajoute le filepath aux dict des mails à envoyer
        return os.path.join(root_path, mail['attachment'])

    def _prepare_message(self, message_tmpl, company, year, month):
        """
        Format the mail content
        """
        return message_tmpl.format(company=company, year=year, month=month)


    def _send_mails(self, mails, force):
        """
        Launch the task for mail sending
        """
        job = MailingJob()
        self.request.dbsession.add(job)
        self.request.dbsession.flush()

        try:
            celery_job = async_mail_salarysheets.delay(
                job.id,
                mails,
                force,
            )
            logger.info(u" * The Celery Task {0} has been delayed, its result \
should be retrieved from the MailingJob : {1}".format(celery_job.id, job.id)
                    )
        except redis.exceptions.ConnectionError:
            logger.exception(u"La connexion redis à la base de données n'est \
pas possible")
            self.request.session.flash(
                u"Un problème de connexion a été rencontré, l'outil d'envoi \
de mail n'est pas disponible", 'error')

        return HTTPFound(self.request.route_path('job', id=job.id))

    def _base_result_dict(self, filetype):
        """
        Returns the base view result dict
        """
        return dict(
            title=self.title,
            mail_subject=DEFAULT_MAIL_OBJECT[filetype],
            mail_message=DEFAULT_MAIL_MESSAGE[filetype],
            mails=(),
            force=False,
            errors={},
        )

    def _get_file_datas_entry(self, datas, mail):
        """
        Return the file datas entry corresponding to the submitted mail datas
        :param dict datas: The collected datas about all handled files
        :param dict mail: The submitted datas corresponding to a mail that
        should be sent
        """
        company_id = mail['company_id']
        filename = mail['attachment']
        company_files_datas = datas[company_id]
        for file_datas in company_files_datas:
            if file_datas['file'].name == filename:
                return file_datas
        raise KeyError(u"The submitted datas are invalid, we can't retrieve \
the informations")

    def __call__(self):
        """
        The main entry for our view
        """
        logger.info("Calling the treasury files view")
        filetype = self.request.matchdict['filetype']
        year = self.request.matchdict['year']
        month = self.request.matchdict['month']
        root_directory = get_root_directory(self.request)
        root_path = os.path.join(root_directory, filetype, year, month)

        result = self._base_result_dict(filetype)
        datas = self.collect_files(root_path)
        result['datas'] = datas

        if 'submit' in self.request.params:
            logger.info(" -> Datas were submitted")
            # L'utilisateur a demandé l'envoi de mail
            try:
                appstruct = peppercorn.parse(self.request.params.items())
                form_datas = MailSendingSchema().deserialize(appstruct)

            except colander.Invalid as e:
                logger.exception(u" - Submitted datas are invalid")
                result.update(self.request.params)
                result['errors'] = e.asdict()

            else:
                logger.info(" + Submitted datas are valid")
                mails = self._prepare_mails(
                    datas,
                    form_datas,
                    root_path,
                    year,
                    month,
                )

                # On check qu'il y a au moins une entrée pour laquelle on va
                # envoyer un mail
                if len(mails) == 0:

                    result['errors'] = {
                        'companies': u"Veuillez sélectionner au moins \
    une entreprise"}
                    result.update(form_datas)
                    return result

                force = form_datas.get('force', False)
                return self._send_mails(mails, force)

        return result


def file_display(request):
    """
    Stream a file
    """
    root_path = get_root_directory(request)
    rel_filepath = decode_path(request.params['name'])
    # remove the leading slash to be able to join
    rel_filepath = rel_filepath.strip('/')
    filepath = os.path.join(root_path, rel_filepath)
    filename = os.path.basename(filepath)
    company_code = request.context.code_compta

    if not code_is_not_null(company_code):
        logger.warn("Current context has no code")
        return HTTPForbidden()

    if not isprefixed(filename, company_code):
        logger.warn("Current context has no code")
        return HTTPForbidden()

    if not issubdir(root_path, filepath):
        logger.warn("Given filepath is not a subdirectory")
        logger.warn(filepath)
        logger.warn(root_path)
        return HTTPForbidden()

    if os.path.isfile(filepath):
        file_obj = AbstractFile(filename, filepath)
        file_obj.as_response(request)
        return request.response

    logger.warn("AbstractFile not found")
    logger.warn(filepath)
    return HTTPNotFound()


class MailHistoryView(BaseListView):
    """
    A view showing the history of sent emails
    """
    schema = BaseListsSchema()
    default_sort = 'send_at'
    default_direction = 'desc'
    sort_columns = {'send_at': 'send_at'}
    title = u"Historique des mails envoyés"

    def query(self):
        return MailHistory.query()

    def _build_return_value(self, schema, appstruct, query):
        """
        add month and years attribute to each file record
        """
        result = BaseListView._build_return_value(
            self,
            schema,
            appstruct,
            query
        )

        for obj in result['records']:
            splitted = obj.filepath.split('/')
            month = splitted[-2]
            year = splitted[-3]

            obj.month = month
            obj.year = year

        return result

    def filter_company_id(self, query, appstruct):
        search = appstruct.get('search')
        if search:
            query = query.filter(MailHistory.company_id==search)
        return query


def mailagain(request):
    """
    Send an email again based on its history entry
    """
    history_entry = MailHistory.get(request.matchdict['id'])
    send_salary_sheet(
        request,
        history_entry.company,
        history_entry.filename,
        history_entry.filepath,
        True,
    )

    request.session.flash(u"Le mail a bien été envoyé")
    url = request.route_path('mailhistory')
    return HTTPFound(url)


def includeme(config):
    """
        View and route inclusions
    """
    # traverse is the path in the resource tree we provide to add a context to
    # our view
    traverse = '/companies/{id}'

    # Add the file listing route/views
    for key, view in ("treasury", TreasuryFilesView), \
                     ("incomestatement", IncomeStatementFilesView), \
                     ("salarysheet", SalarySheetFilesView):
        config.add_route(
            key,
            "/company/{id:\d+}/%s" % key,
            traverse=traverse
        )
        config.add_view(
            view,
            route_name=key,
            renderer="treasury/documents.mako",
            permission="edit",
        )

    # Add the file display view
    config.add_route(
        "treasury_files",
        "/company/{id:\d+}/files/",
        traverse=traverse,
    )
    config.add_view(
        file_display,
        route_name="treasury_files",
        request_param='name',
    )


    # Add the mail history views
    config.add_route("mailhistory", '/mailhistory')
    config.add_view(
        MailHistoryView,
        route_name='mailhistory',
        renderer='mailhistory.mako',
        permission="admin",
    )
    config.add_route("mail", "/mail/{id:\d+}")
    config.add_view(
        mailagain,
        route_name="mail",
        permission="admin",
    )

    # Add the admin files view
    config.add_route(
        "admin_treasury_all",
        "/treasury_files/",
    )
    config.add_route(
        "admin_treasury_files",
        "/treasury_files/{filetype}/{year}/{month}/",
    )
    config.add_view(
        AdminTreasuryView,
        route_name="admin_treasury_all",
        renderer="/treasury/admin_treasury_all.mako",
        permission="admin",
    )
    config.add_view(
        MailTreasuryFilesView,
        route_name="admin_treasury_files",
        renderer="/treasury/admin_treasury_files.mako",
        permission="admin",
    )
