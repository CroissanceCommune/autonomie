# -*- coding: utf-8 -*-
# * File Name : pdf.py
#
# * Copyright (C) 2010 Majerti <tech@majerti.fr>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 06-02-2012
# * Last Modified : jeu. 26 avril 2012 15:45:11 CEST
#
# * Project : coopagestv2
#
"""
    Tools for handling pdf files

    write_pdf(request, filename, template, datas)

"""
import os
import pkg_resources
import cStringIO as StringIO

from xhtml2pdf import pisa

from pyramid.renderers import render

HERE = os.path.dirname(__file__)
def render_html(request, template, datas):
    """
        Compile the current template with the given datas
    """
    return render( template, datas, request )

def write_pdf(request, filename, template, datas):
    """
        Write a pdf in a pyramid request
    """
    request = write_pdf_headers(request, filename)

    html = render_html(request, template, datas)
    result = buffer_pdf(html)
    request.response.write( result.getvalue() )
    return request

def write_pdf_headers(request, filename):
    """
        write the headers for the pdf file 'filename'
    """
    request.response.content_type = 'application/pdf'
    request.response.headerlist.append(
                ('Content-Disposition',
                 'attachment; filename={0}'.format(filename)))
    return request

def buffer_pdf(html):
    """
        Return a cstringio datas containing a pdf
    """
    result = StringIO.StringIO()
    pisa.pisaDocument(html,
                      result,
                      link_callback=fetch_resource,
                     encoding='utf-8')
    return result

def fetch_resource(uri, rel):
    """
        Callback used by pisa to locally retrieve ressources
        giving the uri
    """
    if ':' in uri:
        package, filename = uri.split(':')
    else:
        package = "autonomie"
        filename = uri
    filepath = pkg_resources.resource_filename(package, filename)

    return filepath
