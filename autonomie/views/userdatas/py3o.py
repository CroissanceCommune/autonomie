# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import os
import datetime

from sqla_inspect import py3o

from pyramid.httpexceptions import HTTPFound

from autonomie.export.utils import write_file_to_request
from autonomie.models import files


logger = logging.getLogger(__name__)


def record_compilation(context, request, template):
    """
    Record the compilation of a template to be able to build an history
    """
    history = files.TemplatingHistory(
        user_id=request.user.id,
        userdatas_id=context.id,
        template_id=template.id
    )
    logger.debug(u"Storing an history object")
    request.dbsession.add(history)


def get_filename(template_name):
    """
    Return the filename to use to store
    """
    now = datetime.datetime.now()
    name = os.path.splitext(template_name)[0]
    return u"{0}_{1}.odt".format(name, now.strftime('%d-%m-%Y-%Hh-%M'))


def store_compiled_file(context, request, output, template):
    """
    Stores the compiled datas in the user's environment

    :param context: The context of the
    """
    logger.debug(u"Storing the compiled file")
    name = get_filename(template.name)
    output.seek(0)
    datas = output.getvalue()
    file_obj = files.File(
        name=name,
        description=template.description,
        data=output,
        mimetype="application/vnd.oasis.opendocument.text",
        size=len(datas),
        parent_id=context.id
    )
    request.dbsession.add(file_obj)
    return file_obj


def delete_templating_history_view(context, request):
    userdatas = context.userdatas
    request.dbsession.delete(context)
    request.session.flash(u"L'élément a bien été supprimé de l'historique")
    return HTTPFound(
        request.route_path(
            'userdata',
            id=userdatas.id,
            _anchor='tab4'
        )
    )


def get_key_from_genshi_error(err):
    """
    Genshi raises an UndefinedError, but doesn't store the key name in the
    Exception object
    We get the missing key from the resulting message
    """
    msg = err.message
    if " not defined" in msg:
        return msg.split(" not defined")[0]
    else:
        return msg


def add_response_to_request(request, template, context):
    """
    Build a templated file response, write it in the request
    and record compilation

    :param obj request: The current request object
    :param obj template: A Template object
    :param obj context: The context to use for templating
    :returns: The request object
    """
    output = py3o.compile_template(
        context,
        template.data_obj,
        request.config
    )
    write_file_to_request(
        request,
        template.name,
        output,
    )
    store_compiled_file(context, request, output, template)
    return request
