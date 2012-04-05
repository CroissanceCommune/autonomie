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
import os
import logging
from deform.interfaces import FileUploadTempStore
from datetime import datetime, timedelta
from pyramid.threadlocal import get_current_request

import pickle
from cStringIO import StringIO

log = logging.getLogger(__file__)

class BeakerTempStore(FileUploadTempStore):
    """
            Temporary stores files at a given location
    """
    session_key = 'deform_upload_tempstore'

    def set_session(self, session):
        self.session = session

    def preview_url(self, name):
        return None

    def get(self, name, default=None):
        """
            Tries to get a element given by name, or default when it doesn't exists
        """
        try:
            return self.__getitem__(name)
        except AttributeError:
            return default

    def __getitem__(self, name):
        """
            Retreives the file contents of a given file
        """
        log.debug("In __getitem__")
        request = get_current_request()
        self.set_session(request.session)
        log.debug(" + name %s" % name)
        # We erase elements in the for loop
        items = self.session[self.session_key].items()
        # Check old items
        for key, value in items:
            if value['time'] + timedelta(minutes=15) < datetime.now():
                del self.session[self.session_key][key]

        if not name in self.session[self.session_key]:
            raise AttributeError, "Name '{0}' does not exists".format(name)

        # reset last timestamp
        self.session[self.session_key][name]['time'] = datetime.now()
        self.session.persist()

        value = self.session[self.session_key][name]['value']
        value['fp'] = StringIO(value['fp'])

        log.debug(" + Value : %s" % value)
        value['uid'] = name

        return value

    def __setitem__(self, name, value):
        """
            Saves the file contents to a file
        """
        log.debug("In __setitem__")
        request = get_current_request()
        self.set_session(request.session)
        log.debug(" + name : %s" % name)
        log.debug(" + value : %s" % value)

        if value.has_key('fp') and value['fp']:
            filebuf = value['fp'].read()
        else:
            filebuf = ""
        self.session.setdefault(self.session_key, {})[name] = {
                'time': datetime.now(),
                'value': {
                    'fp': filebuf,
                    'filename': value['filename'],
                    'mimetype': value['mimetype'],
                    'size': value['size']
                    }
                }

        self.session.persist()

