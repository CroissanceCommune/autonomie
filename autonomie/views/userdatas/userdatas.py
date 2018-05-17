# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
UserDatas add edit views
"""
import logging
from pyramid.httpexceptions import HTTPFound

from deform_extensions import AccordionFormWidget
from js.deform import auto_need
from genshi.template.eval import UndefinedError
from sqlalchemy.orm import (
    load_only,
    Load,
    joinedload,
)

from autonomie.models.user.userdatas import (
    UserDatas,
    SocialDocTypeOption,
    UserDatasSocialDocTypes,
    CaeSituationChange,
)
from autonomie.models import files
from autonomie.forms.user.userdatas import (
    get_add_edit_schema,
    USERDATAS_FORM_GRIDS,
    get_doctypes_schema,
)
from autonomie.utils.strings import (
    format_account,
)
from autonomie.utils.menu import (
    AttrMenuDropdown,
)
from autonomie.views import (
    BaseFormView,
    submit_btn,
    cancel_btn,
    BaseView,
    DeleteView,
)
from autonomie.views.userdatas.py3o import (
    add_response_to_request,
    record_compilation,
    get_key_from_genshi_error,
)
from autonomie.views.user.tools import UserFormConfigState


logger = logging.getLogger(__name__)


USERDATAS_MENU = AttrMenuDropdown(
    name='userdatas',
    label=u'Gestion sociale',
    default_route=u'/users/{id}/userdatas',
    icon=u'fa fa-id-card-o',
    model_attribute='userdatas',
    perm='view.userdatas',
)
USERDATAS_MENU.add_item(
    name="userdatas_view",
    label=u'Fiche du porteur',
    route_name=u'/users/{id}/userdatas/edit',
    icon=u'fa fa-user-circle-o',
    perm='view.userdatas',
)
USERDATAS_MENU.add_item(
    name="userdatas_parcours",
    label=u'Parcours',
    route_name=u'/users/{id}/userdatas/history',
    icon=u'fa fa-history',
    perm='edit.userdatas',
)
USERDATAS_MENU.add_item(
    name="userdatas_doctypes",
    label=u'Documents sociaux',
    route_name=u'/users/{id}/userdatas/doctypes',
    icon=u'fa fa-check-square-o',
    perm='edit.userdatas',
)
USERDATAS_MENU.add_item(
    name="userdatas_py3o",
    label=u'Génération de documents',
    route_name=u'/users/{id}/userdatas/py3o',
    icon=u'fa fa-puzzle-piece',
    perm='edit.userdatas',
)
USERDATAS_MENU.add_item(
    name="userdatas_filelist",
    label=u'Portefeuille de documents',
    route_name=u'/users/{id}/userdatas/filelist',
    icon=u'fa fa-briefcase',
    perm='view.userdatas',
)


def userdatas_add_entry_point(context, request):
    """
    Entry point for userdatas add
    Record the userdatas form as next form urls

    The add process follows this stream :
        1- entry point
        2- user add form
        3- userdatas form
    """
    config = UserFormConfigState(request.session)
    config.set_steps(['/users/{id}/userdatas/add'])
    config.add_defaults({'groups': ['contractor']})
    return HTTPFound(
        request.route_path(
            "/users",
            _query={'action': 'add'}
        )
    )


def userdatas_add_view(context, request):
    """
    Add userdatas to an existing User object

    :param obj context: The pyramid context (User instance)
    :param obj request: The pyramid request
    """
    logger.debug(u"Adding userdatas for the user %s" % context.id)
    user_datas = UserDatas()
    user_datas.user_id = context.id
    user_datas.coordonnees_civilite = context.civilite
    user_datas.coordonnees_lastname = context.lastname
    user_datas.coordonnees_firstname = context.firstname
    user_datas.coordonnees_email1 = context.email
    request.dbsession.add(user_datas)
    request.dbsession.flush()
    return HTTPFound(
        request.route_path(
            '/users/{id}/userdatas/edit',
            id=context.id,
        )
    )


def ensure_doctypes_rel(userdatas_id, request):
    """
    Ensure there is a UserDatasSocialDocTypes instance attaching each social doc
    type with the userdatas

    :param int userdatas_id: The id of the userdatas instance
    :param obj request: The request object
    """
    for doctype in SocialDocTypeOption.query():
        doctype_id = doctype.id
        rel = UserDatasSocialDocTypes.get((userdatas_id, doctype_id,))
        if rel is None:
            rel = UserDatasSocialDocTypes(
                userdatas_id=userdatas_id,
                doctype_id=doctype_id,
            )
            request.dbsession.add(rel)
    request.dbsession.flush()


class UserDatasEditView(BaseFormView):
    """
    User datas edition view
    """
    schema = get_add_edit_schema()
    validation_msg = u"Les informations sociales ont bien été enregistrées"
    buttons = (submit_btn, cancel_btn,)

    @property
    def title(self):
        return u"Fiche de gestion sociale de {0}".format(
            format_account(self.current_userdatas.user, False)
        )

    @property
    def current_userdatas(self):
        return self.context

    def before(self, form):
        auto_need(form)
        form.widget = AccordionFormWidget(named_grids=USERDATAS_FORM_GRIDS)
        form.set_appstruct(self.schema.dictify(self.current_userdatas))

    def submit_success(self, appstruct):
        model = self.schema.objectify(appstruct, self.current_userdatas)
        model = self.dbsession.merge(model)
        self.dbsession.flush()

        self.session.flash(
            u"Vos modifications ont été enregistrées"
        )
        return HTTPFound(self.request.current_route_path())


class UserUserDatasEditView(UserDatasEditView):
    @property
    def current_userdatas(self):
        return self.context.userdatas


class UserDatasDeleteView(DeleteView):
    def redirect(self):
        return HTTPFound(
            self.request.route_path('/users/{id}', id=self.context.user_id)
        )


class UserDatasDocTypeView(BaseFormView):
    _schema = None
    title = u"Liste des documents fournis par l'entrepreneur"
    form_options = (('formid', 'doctypes-form'),)
    add_template_vars = ('current_userdatas',)

    def __init__(self, *args, **kwargs):
        BaseFormView.__init__(self, *args, **kwargs)
        ensure_doctypes_rel(self.current_userdatas.id, self.request)

    @property
    def current_userdatas(self):
        return self.context

    @property
    def schema(self):
        if self._schema is None:
            self._schema = get_doctypes_schema(self.current_userdatas)

        return self._schema

    @schema.setter
    def schema(self, schema):
        self._schema = schema

    def before(self, form):
        appstruct = {}
        for index, entry in enumerate(
            self.current_userdatas.doctypes_registrations
        ):
            appstruct['node_%s' % index] = {
                'userdatas_id': entry.userdatas_id,
                'doctype_id': entry.doctype_id,
                'status': entry.status,
            }
        form.set_appstruct(appstruct)
        return form

    def submit_success(self, appstruct):
        node_schema = self.schema.children[0]
        for key, value in appstruct.items():
            logger.debug(value)
            model = node_schema.objectify(value)
            self.dbsession.merge(model)

        self.request.session.flash(
            u"Vos modifications ont été enregistrées"
        )

        return HTTPFound(self.request.current_route_path())


class UserUserDatasDocTypeView(UserDatasDocTypeView):
    @property
    def current_userdatas(self):
        return self.context.userdatas


class UserDatasFileGeneration(BaseView):
    """
    Base view for file generation
    """
    title = u"Génération de documents sociaux"

    @property
    def current_userdatas(self):
        return self.context

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
                add_response_to_request(
                    self.request,
                    template,
                    model,
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
            return dict(
                templates=available_templates.all(),
                title=self.title,
                current_userdatas=self.current_userdatas
            )


class UserUserDatasFileGeneration(UserDatasFileGeneration):
    @property
    def current_userdatas(self):
        return self.context.userdatas


class UserDatasFileList(BaseView):
    @property
    def current_userdatas(self):
        return self.context

    def __call__(self):
        query = files.File.query().options(load_only(
            "description",
            "name",
            "updated_at",
            "id",
        ))
        query = query.filter_by(parent_id=self.current_userdatas.id)

        return dict(
            title=u"Portefeuille de documents",
            files=query,
            current_userdatas=self.current_userdatas,
        )


class UserUserDatasFileList(UserDatasFileList):
    @property
    def current_userdatas(self):
        return self.context.userdatas


class UserDatasHistory(BaseView):

    @property
    def current_userdatas(self):
        return self.context

    def __call__(self):
        status_query = CaeSituationChange.query()
        status_query = status_query.options(
            Load(CaeSituationChange).load_only("date", "id"),
            joinedload("situation").load_only("label"),
        )
        status_query = status_query.filter_by(
            userdatas_id=self.current_userdatas.id
        )
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
            status_history=status_query.all(),
            user=self.current_userdatas.user,
            template_history=template_query.all(),
            title=u"Parcours de {0}".format(
            	format_account(self.current_userdatas.user, False)
        	)
        )


class UserUserDatasHistory(UserDatasHistory):
    @property
    def current_userdatas(self):
        return self.context.userdatas


def mydocuments_view(context, request):
    """
    View callable collecting datas for showing the social docs associated to the
    current user's account
    """
    if context.userdatas is not None:
        query = files.File.query()
        documents = query.filter(
            files.File.parent_id == context.userdatas.id
        ).all()
    else:
        documents = []
    return dict(
        title=u"Mes documents",
        documents=documents,
    )


def add_routes(config):
    """
    Add module related routes
    """
    config.add_route(
        '/users/{id}/userdatas',
        '/users/{id}/userdatas',
        traverse='/users/{id}',
    )
    config.add_route(
        '/users/{id}/userdatas/add',
        '/users/{id}/userdatas/add',
        traverse='/users/{id}',
    )
    config.add_route(
        '/userdatas/{id}',
        '/userdatas/{id}',
        traverse='/userdatas/{id}',
    )

    for view in (
        'edit', 'doctypes', 'py3o', 'mydocuments', "filelist", "history"
    ):
        config.add_route(
            '/userdatas/{id}/%s' % view,
            '/userdatas/{id}/%s' % view,
            traverse='/userdatas/{id}',
        )
        config.add_route(
            '/users/{id}/userdatas/%s' % view,
            '/users/{id}/userdatas/%s' % view,
            traverse='/users/{id}',
        )


def add_views(config):
    """
    Add module related views
    """
    config.add_view(
        userdatas_add_view,
        route_name='/users/{id}/userdatas/add',
        permission="add.userdatas",
    )
    config.add_view(
        UserDatasEditView,
        route_name='/userdatas/{id}',
        permission="edit.userdatas",
        renderer="/base/formpage.mako",
    )
    config.add_view(
        UserUserDatasEditView,
        route_name='/users/{id}/userdatas',
        permission="edit.userdatas",
        renderer="/userdatas/edit.mako",
        layout='user',
    )
    config.add_view(
        UserUserDatasEditView,
        route_name='/users/{id}/userdatas/edit',
        permission="edit.userdatas",
        renderer="/userdatas/edit.mako",
        layout='user',
    )
    config.add_view(
        UserDatasDeleteView,
        route_name='/userdatas/{id}',
        permission="delete.userdatas",
        request_param="action=delete",
    )
    config.add_view(
        userdatas_add_entry_point,
        route_name='/userdatas',
        request_param="action=add",
        permission="add.userdatas",
    )
    config.add_view(
        UserDatasDocTypeView,
        route_name='/userdatas/{id}/doctypes',
        permission="edit.userdatas",
        renderer="/base/formpage.mako",
    )
    config.add_view(
        UserUserDatasDocTypeView,
        route_name='/users/{id}/userdatas/doctypes',
        permission="edit.userdatas",
        renderer="/userdatas/doctypes.mako",
        layout='user',
    )
    config.add_view(
        UserDatasFileGeneration,
        route_name='/userdatas/{id}/py3o',
        permission="edit.userdatas",
        renderer="/userdatas/py3o.mako",
    )
    config.add_view(
        UserUserDatasFileGeneration,
        route_name='/users/{id}/userdatas/py3o',
        permission="edit.userdatas",
        renderer="/userdatas/py3o.mako",
        layout='user',
    )
    config.add_view(
        UserDatasFileList,
        route_name="/userdatas/{id}/filelist",
        permission="view.userdatas",
        renderer="/userdatas/filelist.mako",
        layout="user"
    )
    config.add_view(
        UserUserDatasFileList,
        route_name="/users/{id}/userdatas/filelist",
        permission="view.userdatas",
        renderer="/userdatas/filelist.mako",
        layout="user"
    )
    config.add_view(
        UserDatasHistory,
        route_name="/userdatas/{id}/history",
        permission="view.userdatas",
        renderer="/userdatas/history.mako",
        layout="user"
    )
    config.add_view(
        UserUserDatasHistory,
        route_name="/users/{id}/userdatas/history",
        permission="view.userdatas",
        renderer="/userdatas/history.mako",
        layout="user"
    )
    config.add_view(
        mydocuments_view,
        route_name='/users/{id}/userdatas/mydocuments',
        permission="view.documents",
        renderer="/userdatas/mydocuments.mako",
        layout='user',
    )


def register_menus():
    from autonomie.views.user.layout import UserMenu
    UserMenu.add_after('companies', USERDATAS_MENU)


def includeme(config):
    """
    Pyramid main entry point

    :param obj config: The current application config object
    """
    add_routes(config)
    add_views(config)

    register_menus()
