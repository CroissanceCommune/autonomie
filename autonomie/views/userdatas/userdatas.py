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
    Load,
    joinedload,
)
from autonomie.models.user.userdatas import (
    UserDatas,
    SocialDocTypeOption,
    UserDatasSocialDocTypes,
    get_default_cae_situation,
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
from autonomie.views.user.routes import USER_ITEM_URL
from autonomie.views.userdatas.routes import (
    USERDATAS_URL,
    USERDATAS_ITEM_URL,
    USERDATAS_EDIT_URL,
    USERDATAS_DOCTYPES_URL,
    USERDATAS_PY3O_URL,
    USERDATAS_MYDOCUMENTS_URL,
    USER_USERDATAS_URL,
    USER_USERDATAS_ADD_URL,
    USER_USERDATAS_EDIT_URL,
    USER_USERDATAS_DOCTYPES_URL,
    USER_USERDATAS_PY3O_URL,
)
from autonomie.views.admin.userdatas.templates import TEMPLATE_URL
from autonomie.views.user.tools import UserFormConfigState


logger = logging.getLogger(__name__)


USERDATAS_MENU = AttrMenuDropdown(
    name='userdatas',
    label=u'Gestion sociale',
    default_route=USER_USERDATAS_URL,
    icon=u'fa fa-id-card-o',
    hidden_attribute='userdatas',
    perm='edit.userdatas',
)
USERDATAS_MENU.add_item(
    name="userdatas_view",
    label=u'Fiche du porteur',
    route_name=USER_USERDATAS_EDIT_URL,
    icon=u'fa fa-user-circle-o',
    perm='view.userdatas',
)
USERDATAS_MENU.add_item(
    name="userdatas_parcours",
    label=u'Parcours',
    route_name=u'/users/{id}/userdatas/career_path',
    other_route_name=u'career_path',
    icon=u'fa fa-history',
    perm='view.userdatas',
)
USERDATAS_MENU.add_item(
    name="userdatas_doctypes",
    label=u'Documents sociaux',
    route_name=USER_USERDATAS_DOCTYPES_URL,
    icon=u'fa fa-check-square-o',
    perm='doctype.userdatas',
)
USERDATAS_MENU.add_item(
    name="userdatas_py3o",
    label=u'Génération de documents',
    route_name=USER_USERDATAS_PY3O_URL,
    icon=u'fa fa-puzzle-piece',
    perm='py3o.userdatas',
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
    config.set_steps([USER_USERDATAS_ADD_URL])
    config.add_defaults({'primary_group': 'contractor'})
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
    user_datas.situation_situation_id = get_default_cae_situation()
    request.dbsession.add(user_datas)
    request.dbsession.flush()
    return HTTPFound(
        request.route_path(
            USER_USERDATAS_EDIT_URL,
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
    add_template_vars = ("current_userdatas", "delete_url")

    @property
    def title(self):
        return u"Fiche de gestion sociale de {0}".format(
            format_account(self.current_userdatas.user, False)
        )

    @property
    def current_userdatas(self):
        return self.context

    @property
    def delete_url(self):
        return self.request.route_path(
            USERDATAS_ITEM_URL,
            id=self.current_userdatas.id,
            _query={'action': 'delete'}
        )

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
            self.request.route_path(USER_ITEM_URL, id=self.context.user_id)
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

    @property
    def admin_url(self):
        return self.request.route_path(TEMPLATE_URL)

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
            )


class UserUserDatasFileGeneration(UserDatasFileGeneration):
    @property
    def current_userdatas(self):
        return self.context.userdatas


def add_views(config):
    """
    Add module related views
    """
    config.add_view(
        userdatas_add_view,
        route_name=USER_USERDATAS_ADD_URL,
        permission="add.userdatas",
    )
    config.add_view(
        UserDatasEditView,
        route_name=USERDATAS_EDIT_URL,
        permission="edit.userdatas",
        renderer="/base/formpage.mako",
    )
    config.add_view(
        UserUserDatasEditView,
        route_name=USER_USERDATAS_URL,
        permission="edit.userdatas",
        renderer="/userdatas/edit.mako",
        layout='user',
    )
    config.add_view(
        UserUserDatasEditView,
        route_name=USER_USERDATAS_EDIT_URL,
        permission="edit.userdatas",
        renderer="/userdatas/edit.mako",
        layout='user',
    )
    config.add_view(
        UserDatasDeleteView,
        route_name=USERDATAS_ITEM_URL,
        permission="delete.userdatas",
        request_param="action=delete",
    )
    config.add_view(
        userdatas_add_entry_point,
        route_name=USERDATAS_URL,
        request_param="action=add",
        permission="add.userdatas",
    )
    config.add_view(
        UserDatasDocTypeView,
        route_name=USERDATAS_DOCTYPES_URL,
        permission="doctypes.userdatas",
        renderer="/base/formpage.mako",
    )
    config.add_view(
        UserUserDatasDocTypeView,
        route_name=USER_USERDATAS_DOCTYPES_URL,
        permission="doctypes.userdatas",
        renderer="/userdatas/doctypes.mako",
        layout='user',
    )
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


def register_menus():
    from autonomie.views.user.layout import UserMenu
    UserMenu.add_after('companies', USERDATAS_MENU)


def includeme(config):
    """
    Pyramid main entry point

    :param obj config: The current application config object
    """
    add_views(config)
    register_menus()
