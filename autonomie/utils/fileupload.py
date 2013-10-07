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
    Fileupload temp store
    store the file and the main information used to handle it
    Usefull for preview_urls
"""
import StringIO
import os
import logging
from datetime import datetime
from datetime import timedelta

log = logging.getLogger(__name__)


def pop_absolute_urls(filepath):
    """
        pop all directories informations included in a filename
        used to avoid problems with IE who's sending absolute filepaths
    """
    filepath = filepath.replace('\\', '/')
    return os.path.basename(filepath)


class FileTempStore(dict):
    """
        Temporary stores files at a given location
        implements deform.interfaces.FileUploadTempStore

        default_filename : if provided, name used to store and access the
                           uploaded file
        session : pyramid session
        path : the path to store (retrieve) the file from
        url : the base url used to access the file
        filters : list of callables that take a file object as parameter
        Example :
            to upload a file to /tmp/logo/ and access it through /assets/logo
            FileTempStore(session, "/tmp/logo", "/assets/logo/")
            if you want to force the logo file to be called logo.png
            FileTempStore(session, "/tmp/logo", "/assets/logo/", "logo.png")
            if you want to pass the logo file through a resize function
            FileTempStore(session, "/tmp/logo", "/assets/logo/", [resize])
    """
    session_key = 'deform_uploads'

    def __init__(self, session, path, url, default_filename=None, filters=None):
        self.session = session
        self.store_directory = path
        self.store_url = url
        self.default_filename = default_filename

        if not os.path.isdir(self.store_directory):
            os.system("mkdir -p %s" % self.store_directory)

        if not self.session_key in self.session:
            self.session[self.session_key] = {}

        if filters and not hasattr(filters, '__iter__'):
            filters = [filters]
        self.filters = filters or []

    def preview_url(self, uid, filename=None):
        """
            Returns the url for the preview
        """
        log.debug(u"Asking for a preview URl")
        log.debug(u" + uid : %s" % uid)
        filepath = None
        if self.default_filename:
            filename = self.default_filename
        elif not filename:
            filename = self.get(uid, {}).get('filename')

        if filename:
            log.debug(u" + filename : %s" % filename)
            filepath = os.path.join(self.store_url, filename)
        else:
            filepath = None
        log.debug(u" -> The filepath where to find our file is : %s"
                  % filepath)
        return filepath

    def get(self, uid, default=None):
        """
            Tries to get a element given by name,
            or default when it doesn't exists
        """
        try:
            return self.__getitem__(uid)
        except AttributeError:
            return default

    def __getitem__(self, uid):
        """
            Retrieves the file contents of a given file
        """
        log.debug(u"In __getitem__")
        log.debug(u" + uid %s" % uid)

        # We erase elements in the for loop
        items = self.session[self.session_key].items()
        # Check old items
        for key, value in items:
            if value['time'] + timedelta(minutes=15) < datetime.now():
                log.debug(u"  + Expiring %s" % key)
                del self.session[self.session_key][key]

        if not uid in self.session[self.session_key]:
            raise AttributeError(u"Name '{0}' does not exists".format(uid))

        # reset last timestamp
        self.session[self.session_key][uid]['time'] = datetime.now()
        self.session.persist()

        value = self.session[self.session_key][uid]['value']
        log.debug(u" + Value : %s" % value)
        value['uid'] = uid
        return value

    def write_file(self, fpath, fdata):
        """
            Writes file datas to a file
        """
        log.debug(u"Writing file datas to : %s" % fpath)
        with file(fpath, 'w') as fbuf:
            fbuf.write(fdata.read())

    def filter_data(self, fbuf):
        """
            Pass file datas through filters
        """
        log.debug(u"Filtering out image datas")
        if self.filters:
            # Use an intermediary buffer
            fdata = StringIO.StringIO()
            fdata.write(fbuf.read())
            for filter_ in self.filters:
                fdata = filter_(fdata)
                fdata.seek(0)
            return fdata
        else:
            return fbuf

    def get_filepath(self, filename):
        """
            Return the destination file path
        """
        return os.path.join(self.store_directory, filename)

    def __setitem__(self, uid, value):
        """
            Saves the file contents to a file
        """
        log.debug(u"In __setitem__")
        log.debug(u" + uid : %s" % uid)
        log.debug(u" + value : %s" % value)

        filename = self.default_filename or value['filename']
        filename = pop_absolute_urls(filename)

        filedata = value.pop('fp', None)
        if filedata is not None:
            filedata = self.filter_data(filedata)
            filepath = self.get_filepath(filename)
            self.write_file(filepath, filedata)
        else:
            log.debug(u"No file data where transmitted")

        if filename:
            value['preview_url'] = self.preview_url(uid, filename)

        self.session.setdefault(self.session_key, {})[uid] = {
            'time': datetime.now(),
            'value': {
                'filename': filename,
                'mimetype': value.get('mimetype'),
                'size': value.get('size'),
                'preview_url': value.get('preview_url')
                }
            }
        self.session.persist()
