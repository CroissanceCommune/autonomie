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
import datetime
import logging
import os
import mimetypes

from pyramid.httpexceptions import (
    HTTPForbidden,
    HTTPNotFound,
    HTTPFound,
)

from autonomie.models.files import MailHistory
from autonomie.forms.lists import BaseListsSchema
from autonomie.views import (
    BaseView,
    BaseListView,
)
from autonomie.mail import send_salary_sheet
from autonomie.utils.ascii import force_ascii
from autonomie.utils.files import (
    encode_path,
    decode_path,
    issubdir,
    filesizeformat,
)


log = logging.getLogger(__name__)


def get_root_directory(request):
    """
        get the root directory of files handled in this module
    """
    absdir = request.registry.settings.get('autonomie.ftpdir')
    if not absdir:
        raise Exception(u"The ftpdirectory could not be found, \
            please set it up.")
    return absdir


_NULLCODES = ["0", 0, "", None]

def code_is_not_null(code):
    """
        Return True if the given code is not null
    """
    return code not in _NULLCODES

def isprefixed(filename, prefix='___'):
    """
        Return True if the filename startswith prefix + '_'
    """
    prefix += '_'
    if prefix == '____':
        return True
    else:
        return filename.startswith(prefix)


def current_years():
    """
        return a list of the years that should be considered as currents
    """
    today = datetime.date.today()
    result = [str(today.year)]
    if today.month == 1:
        result.append(str(today.year - 1))
    return result



class File(object):
    """
        File object abstraction
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

    def url(self, request):
        """
            return the url to fetch the given file
        """
        root_directory = get_root_directory(request)
        relpath = self.path.replace(root_directory, "", 1)
        return request.route_path("treasury_files",
                id=request.context.id,
                _query=dict(name=encode_path(relpath)))

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
        return "<File : %s %s>" % (self.name, self.path)


def digit_subdirs(path):
    """
        Return subdirectories of path which names are composed of digits
    """
    for name in os.listdir(path):
        spath = os.path.join(path, name)
        if os.path.isdir(spath) and name.isdigit():
            yield name, spath



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

    @staticmethod
    def list_files(path, prefix='___'):
        """
            Return files in path that are prefixed with prefix
        """
        # prefix has a strange form since the prefix is a security point and a
        # void one could lead to security issues
        result = []
        for name in os.listdir(path):
            filepath = os.path.join(path, name)
            if os.path.isfile(filepath):
                if isprefixed(name, prefix):
                    file_obj = File(name, filepath)
                    result.append(file_obj)
        result.sort(key=lambda f:f.path)
        return result

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
                    result_dict[year][month] = self.list_files(month_path,
                                                                    prefix)
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
        log.warn("Current context has no code")
        return HTTPForbidden()

    if not isprefixed(filename, company_code):
        log.warn("Current context has no code")
        return HTTPForbidden()

    if not issubdir(root_path, filepath):
        log.warn("Given filepath is not a subdirectory")
        log.warn(filepath)
        log.warn(root_path)
        return HTTPForbidden()

    if os.path.isfile(filepath):
        file_obj = File(filename, filepath)
        file_obj.as_response(request)
        return request.response

    log.warn("File not found")
    log.warn(filepath)
    return HTTPNotFound()



class Treasury(DisplayDirectoryView):
    """
        List the Treasury directory
    """
    title = u"Trésorerie"
    _root_directory = "tresorerie"


class IncomeStatement(DisplayDirectoryView):
    """
        List the Income Statements
    """
    title = u"Compte de résultat"
    _root_directory = "resultat"

class SalarySheet(DisplayDirectoryView):
    """
        List the salary sheets
    """
    title = u"Bulletin de salaire"
    _root_directory = "salaire"


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
        result = BaseListView._build_return_value(self, schema, appstruct, query)

        for obj in result['records']:
            splitted = obj.filepath.split('/')
            filename = splitted[-1]
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
    from autonomie.tasks import mail
    mail.delay(
        request.registry.settings
    )

    #history_entry = MailHistory.get(request.matchdict['id'])
    #send_salary_sheet(
    #    request,
    #    history_entry.company,
    #    history_entry.filename,
    #    history_entry.filepath,
    #    True,
    #)

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
    for key, view in ("treasury", Treasury), \
                     ("incomestatement", IncomeStatement), \
                     ("salarysheet", SalarySheet):
        config.add_route(key, "/company/{id:\d+}/%s" % key, traverse=traverse)
        config.add_view(view, route_name=key,
                renderer="treasury/documents.mako", permission="edit")
    config.add_route("treasury_files", "/company/{id:\d+}/files/",
                        traverse=traverse)
    config.add_view(file_display, route_name="treasury_files",
                    request_param='name')

    # mail history
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
