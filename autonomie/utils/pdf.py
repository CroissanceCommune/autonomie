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
    Tools for handling pdf files

    write_pdf(request, filename, html)

"""
import logging
import base64
import re
import pkg_resources
import cStringIO as StringIO
from os.path import join

from xhtml2pdf import pisa

from pyramid.renderers import render
from pyramid.threadlocal import get_current_request

from autonomie.export.utils import write_file_to_request


logger = logging.getLogger(__name__)


def render_html(request, template, datas):
    """
        Compile the current template with the given datas
    """
    return render(template, datas, request)


def write_pdf(request, filename, html):
    """
        Write a pdf in a pyramid request
    """
    result = buffer_pdf(html)
    write_file_to_request(request, filename, result)
    return request


def buffer_pdf(html):
    """
        Return a cstringio datas containing a pdf
    """
    result = StringIO.StringIO()
    pisa.pisaDocument(html,
                      result,
                      link_callback=fetch_resource,
                      encoding='utf-8', html_encoding="utf-8")
    return result


DATAURI_TMPL = u"data:{0};base64,{1}"
FILEPATH_REGX = re.compile("^/files/(?P<fileid>[0-9]+).png")
PUBLIC_FILES_REGX = re.compile("^/public/(?P<filekey>.+)")


def get_db_file_resource(fileobj):
    """
    Return a resource string usable by Pisa for dynamically db loaded resources

    :param obj fileobj: a file object with a mimetype attr and a get_value
    method

    :returns: a resource string (default : with a void png)
    """
    if fileobj is not None:
        try:
            b64_str = base64.encodestring(fileobj.getvalue())
        except IOError:  # In case the file isn't on disk anymore
            logger.exception(u"File does not exist")
            b64_str = base64.encodestring('')
        mimetype = fileobj.mimetype
    else:
        b64_str = ""
        mimetype = "image/png"
    return DATAURI_TMPL.format(mimetype, b64_str)


def fetch_resource(uri, rel):
    """
        Callback used by pisa to locally retrieve ressources
        giving the uri
        if the uri starts with /files : we're looking for a db file
        else we're looking for a static resource
    """
    f_regex_group = FILEPATH_REGX.match(uri)
    pf_regex_group = PUBLIC_FILES_REGX.match(uri)

    if f_regex_group is not None:
        # C'est un modèle File que l'on doit renvoyer
        filename = f_regex_group.group('fileid')
        # On récupère l'objet fichier
        from autonomie.models.files import File
        fileobj = File.get(filename)
        resource = get_db_file_resource(fileobj)

    elif pf_regex_group is not None:
        key = pf_regex_group.group('filekey')
        from autonomie.models.config import ConfigFiles
        fileobj = ConfigFiles.get(key)
        resource = get_db_file_resource(fileobj)

    else:
        # C'est un fichier statique
        request = get_current_request()
        introspector = request.registry.introspector
        if uri.startswith('/'):
            uri = uri[1:]
        mainuri, sep, relative_filepath = uri.partition('/')
        mainuri = mainuri + '/'
        resource = ''
        for staticpath in introspector.get_category('static views'):
            if mainuri == staticpath['introspectable']['name']:
                basepath = staticpath['introspectable']['spec']
                resource = join(basepath, relative_filepath).encode('utf-8')
                if ':' in resource:
                    package, filename = resource.split(':')
                    resource = pkg_resources.resource_filename(
                        package,
                        filename,
                    )
                break
    return resource
