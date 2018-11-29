# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import logging
import os
import datetime

from pyramid.httpexceptions import HTTPFound
from genshi.template.eval import UndefinedError
from sqla_inspect import py3o
from sqlalchemy.orm import (
    Load,
    joinedload,
)

from autonomie.export.utils import write_file_to_request
from autonomie.models import files
from autonomie.utils.widgets import Link
from autonomie.views import (
    BaseView,
    DeleteView,
)
from autonomie.views.userdatas.routes import (
    USERDATAS_PY3O_URL,
    USER_USERDATAS_PY3O_URL,
    TEMPLATING_ITEM_URL,
)
from autonomie.views.admin.userdatas.templates import TEMPLATE_URL


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
    logger.debug(u"Storing the compiled file {}".format(template.name))
    name = get_filename(template.name)
    output.seek(0)
    datas = output.getvalue()
    file_obj = files.File(
        name=name,
        description=template.description,
        mimetype="application/vnd.oasis.opendocument.text",
        size=len(datas),
        parent_id=context.id
    )
    file_obj.data = output
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


def get_userdatas_py3o_stage_datas(userdatas):
    """
    Generate additionnal datas that can be used for the py3o compiling context

    :param obj userdatas: The UserDatas instance
    """
    compatibility_keys = {
        u'Contrat CAPE': 'parcours_convention_cape',
        u'Avenant contrat': "parcours_contract_history",
        u"Contrat DPAE": "parcours_dpae",
    }
    res = {}
    context = None
    for stage, paths in userdatas.get_career_path_by_stages().items():
        num_path = len(paths)
        for index, path in enumerate(paths):
            if context is None:
                context = py3o.SqlaContext(path.__class__)
            path_as_dict = context.compile_obj(path)

            key = stage.replace(' ', '')
            datas = res.setdefault(key, {})

            datas["l%s" % index] = path_as_dict

            if index == 0:
                datas['last'] = path_as_dict
            if index == num_path - 1:
                datas['first'] = path_as_dict

            # On veut garder les clés que l'on avait dans le passé
            if stage in compatibility_keys:
                res[compatibility_keys[stage]] = datas.copy()

    return res


def get_userdatas_company_datas(userdatas):
    """
    Generate additionnal_context datas that can be used for the py3o compiling
    context

    :param obj userdatas: The UserDatas instance
    :returns: a dict with company_datas
    """
    result = {'companydatas': {}}
    if userdatas.user:
        datas = result['companydatas']
        context = None
        num_companies = len(userdatas.user.companies)
        for index, company in enumerate(userdatas.user.companies):
            if context is None:
                context = py3o.SqlaContext(company.__class__)
            company_dict = context.compile_obj(company)
            company_dict['title'] = company_dict['name']
            datas["l%s" % index] = company_dict
            if index == 0:
                datas['first'] = company_dict

            if index == num_companies:
                datas['last'] = company_dict

    return result


def get_template_output(request, template, context):
    """
    Compile the template/datas and generate the output file

    Workflow :

        - The context (model) is serialized to a dict
        - py3o is used to compile the template using the given dict

    :param obj request: The current request object
    :param obj template: A Template object
    :param obj context: The context to use for templating (must be an instance
    inheriting from Node)
    :returns: The request object
    :returns: StringIO.StringIO
    """
    additionnal_context = get_userdatas_py3o_stage_datas(context)
    additionnal_context.update(get_userdatas_company_datas(context))
    additionnal_context.update(request.config)
    return py3o.compile_template(
        context,
        template.data_obj,
        additionnal_context=additionnal_context,
    )


class UserDatasFileGeneration(BaseView):
    """
    Base view for file generation
    """
    title = u"Génération de documents sociaux"

    @property
    def current_userdatas(self):
        return self.context

    @property
    def admin_url(self):
        return self.request.route_path(TEMPLATE_URL)

    def stream_actions(self, item):
        """
        Stream actions on TemplatingHistory instances

        :param obj item: A TemplatingHistory instance
        :returns: A generator producing Link instances
        """
        yield Link(
            self.request.route_path(
                "/templatinghistory/{id}",
                id=item.id,
                _query={'action': 'delete'}
            ),
            u"Supprimer",
            icon="fa fa-trash",
        )

    def py3o_action_view(self, doctemplate_id):
        """
        Answer to simple GET requests
        """
        model = self.current_userdatas
        template = files.Template.get(doctemplate_id)
        if template:
            logger.debug(
                " + Templating (%s, %s)" % (template.name, template.id)
            )
            try:
                compiled_output = get_template_output(
                    self.request, template, model
                )
                write_file_to_request(
                    self.request, template.name, compiled_output
                )
                store_compiled_file(
                    model,
                    self.request,
                    compiled_output,
                    template,
                )
                record_compilation(model, self.request, template)
                return self.request.response
            except UndefinedError, err:
                key = get_key_from_genshi_error(err)
                msg = u"""Erreur à la compilation du modèle la clé {0}
n'est pas définie""".format(key)
                logger.exception(msg)

                self.session.flash(msg, "error")
            except IOError:
                logger.exception(u"Le template n'existe pas sur le disque")
                self.session.flash(
                    u"Erreur à la compilation du modèle, le modèle de fichier "
                    u"est manquant sur disque. Merci de contacter votre "
                    u"administrateur.",
                    "error",
                )
            except Exception:
                logger.exception(
                    u"Une erreur est survenue à la compilation du template \
%s avec un contexte de type %s et d'id %s" % (
                        template.id,
                        model.__class__,
                        model.id,
                    )
                )
                self.session.flash(
                    u"Erreur à la compilation du modèle, merci de contacter \
votre administrateur",
                    "error"
                )
        else:
            self.session.flash(
                u"Erreur : ce modèle est manquant",
                "error"
            )

        return HTTPFound(self.request.current_route_path(_query={}))

    def __call__(self):
        doctemplate_id = self.request.GET.get('template_id')
        if doctemplate_id:
            return self.py3o_action_view(doctemplate_id)
        else:
            available_templates = files.Template.query()
            available_templates = available_templates.filter_by(active=True)
            template_query = files.TemplatingHistory.query()
            template_query = template_query.options(
                Load(files.TemplatingHistory).load_only('id', 'created_at'),
                joinedload("user").load_only('firstname', 'lastname'),
                joinedload('template').load_only('name'),
            )
            template_query = template_query.filter_by(
                userdatas_id=self.current_userdatas.id
            )
            return dict(
                templates=available_templates.all(),
                template_history=template_query.all(),
                title=self.title,
                current_userdatas=self.current_userdatas,
                admin_url=self.admin_url,
                stream_actions=self.stream_actions,
            )


class UserUserDatasFileGeneration(UserDatasFileGeneration):
    @property
    def current_userdatas(self):
        return self.context.userdatas


class TemplatingHistoryDeleteView(DeleteView):
    def redirect(self):
        return HTTPFound(
            self.request.route_path(
                USER_USERDATAS_PY3O_URL,
                id=self.context.user.id
            )
        )


def includeme(config):
    config.add_view(
        UserDatasFileGeneration,
        route_name=USERDATAS_PY3O_URL,
        permission="py3o.userdatas",
        renderer="/userdatas/py3o.mako",
    )
    config.add_view(
        UserUserDatasFileGeneration,
        route_name=USER_USERDATAS_PY3O_URL,
        permission="py3o.userdatas",
        renderer="/userdatas/py3o.mako",
        layout='user',
    )
    config.add_view(
        TemplatingHistoryDeleteView,
        route_name=TEMPLATING_ITEM_URL,
        request_param="action=delete",
        permission="delete"
    )
