# -*- coding: utf-8 -*-
# * File Name : fileupload.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 05-04-2012
# * Last Modified :
#
# * Project :
#
"""
    Fileupload temp store
    store the file and the main information used to handle it
    Usefull for preview_urls
"""
import os
import logging
from deform.interfaces import FileUploadTempStore
from datetime import datetime, timedelta
from pyramid.threadlocal import get_current_request

from cStringIO import StringIO

log = logging.getLogger(__name__)

class FileTempStore(FileUploadTempStore):
    """
        Temporary stores files at a given location
    """
    session_key = 'deform_uploads'
    def __init__(self, session, path, default_filename=None):
        self.session = session
        self.store_directory = path
        self.default_filename = default_filename
        if not os.path.isdir(self.store_directory):
            os.system("mkdir -p %s" % self.store_directory)

    def preview_url(self, name):
        """
            Returns the url for the preview
        """
        #TODO : overwrite deform's templates to add a preview link

        #filepath = os.path.join(self.store_directory, filename)
        #if os.path.isfile(filepath):
        #    filedata = file(filepath, 'r').read()
        #    value['fp'] = filedata
        return None

    def get(self, name, default=None):
        """
            Tries to get a element given by name,
            or default when it doesn't exists
        """
        try:
            return self.__getitem__(name)
        except AttributeError:
            return default

    def __getitem__(self, name):
        """
            Retrieves the file contents of a given file
        """
        log.debug("In __getitem__")
        log.debug(" + name %s" % name)

        # We erase elements in the for loop
        items = self.session[self.session_key].items()
        # Check old items
        for key, value in items:
            if value['time'] + timedelta(minutes=15) < datetime.now():
                log.debug("  + Expiring %s" % key)
                del self.session[self.session_key][key]

        if not name in self.session[self.session_key]:
            raise AttributeError, "Name '{0}' does not exists".format(name)

        # reset last timestamp
        self.session[self.session_key][name]['time'] = datetime.now()
        self.session.persist()

        value = self.session[self.session_key][name]['value']
        log.debug(" + Value : %s" % value)
        value['uid'] = name
        return value

    def __setitem__(self, name, value):
        """
            Saves the file contents to a file
        """
        log.debug("In __setitem__")
        log.debug(name)
        log.debug(value)
        filedata = value.get('fp')
        if filedata:
            filename = self.default_filename or value['filename']
            filepath = os.path.join(self.store_directory, filename)
            log.debug("Writing file datas to : %s" % filepath)
            with file(filepath, 'w') as fbuf:
                if isinstance(filedata, file):
                    fbuf.write(filedata.read())
                else:
                    fbuf.write(filedata)
            del value['fp']

        session_fo = self.session.get(self.session_key, {})

        self.session.setdefault(self.session_key, {})[name] = {
            'time': datetime.now(),
            'value': {
                'filename': value['filename'],
                'mimetype': value.get('mimetype'),
                'size': value.get('size')
                }
            }
        log.debug("The session")
        log.debug(self.session)
        self.session.persist()
