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
from datetime import datetime
from datetime import timedelta

log = logging.getLogger(__name__)

class FileTempStore(dict):
    """
        Temporary stores files at a given location
        implements deform.interfaces.FileUploadTempStore

        default_filename : if provided, name used to store and access the
                           uploaded file
        session : pyramid session
        path : the path to store (retrieve) the file from
        url : the base url used to access the file
        Example :
            to upload a file to /tmp/logo/ and access it through /assets/logo
            FileTempStore(session, "/tmp/logo", "/assets/logo/")
            if you want to force the logo file to be called logo.png
            FileTempStore(session, "/tmp/logo", "/assets/logo/", "logo.png")
    """
    session_key = 'deform_uploads'
    def __init__(self, session, path, url, default_filename=None):
        self.session = session
        self.store_directory = path
        self.store_url = url
        self.default_filename = default_filename
        if not os.path.isdir(self.store_directory):
            os.system("mkdir -p %s" % self.store_directory)
        if not self.session.has_key(self.session_key):
            self.session[self.session_key] = {}

    def preview_url(self, uid, filename=None):
        """
            Returns the url for the preview
        """
        log.debug("Asking for a preview URl")
        log.debug(" + uid : %s" % uid)
        filepath = None
        if self.default_filename:
            filename = self.default_filename
        elif not filename:
            filename = self.get(uid, {}).get('filename')

        if filename:
            log.debug(" + filename : %s" % filename)
            filepath = os.path.join(self.store_url, filename)
        else:
            filepath = None
        log.debug(" -> The filepath where to find our file is : %s" % filepath)
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
        log.debug("In __getitem__")
        log.debug(" + uid %s" % uid)

        # We erase elements in the for loop
        items = self.session[self.session_key].items()
        # Check old items
        for key, value in items:
            if value['time'] + timedelta(minutes=15) < datetime.now():
                log.debug("  + Expiring %s" % key)
                del self.session[self.session_key][key]

        if not uid in self.session[self.session_key]:
            raise AttributeError, "Name '{0}' does not exists".format(uid)

        # reset last timestamp
        self.session[self.session_key][uid]['time'] = datetime.now()
        self.session.persist()

        value = self.session[self.session_key][uid]['value']
        log.debug(" + Value : %s" % value)
        value['uid'] = uid
        return value

    def __setitem__(self, uid, value):
        """
            Saves the file contents to a file
        """
        log.debug("In __setitem__")
        log.debug(" + uid : %s" % uid)
        log.debug(" + value : %s" % value)
        filedata = value.get('fp')
        filename = self.default_filename or value['filename']
        if filedata:
            filepath = os.path.join(self.store_directory, filename)
            log.debug("Writing file datas to : %s" % filepath)
            with file(filepath, 'w') as fbuf:
                if isinstance(filedata, file):
                    fbuf.write(filedata.read())
                else:
                    fbuf.write(filedata)
            del value['fp']
        else:
            log.debug("No file data where transmitted")
        if filename:
            value['preview_url'] = self.preview_url(uid, filename)

        self.session.setdefault(self.session_key, {})[uid] = {
            'time': datetime.now(),
            'value': {
                'filename': filename,
                'mimetype': value.get('mimetype'),
                'size': value.get('size'),
                'preview_url':value.get('preview_url')
                }
            }
        self.session.persist()
