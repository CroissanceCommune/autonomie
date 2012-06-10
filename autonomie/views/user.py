# -*- coding: utf-8 -*-
# * File Name : user.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-06-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    User related views
"""
import logging

from sqlalchemy import or_
from pyramid.view import view_config

from deform import Form
from deform import ValidationFailure

from autonomie.models.model import User
from autonomie.models.model import Company
from autonomie.views.forms import pwdSchema
from autonomie.views.forms import userSchema

from .base import ListView

log = logging.getLogger(__name__)

@view_config(route_name='account', renderer='account.mako')
def account(request):
    """
        Account handling page
    """
    avatar = request.user
    pwdformschema = pwdSchema.bind(check=True)
    pwdform = Form(pwdformschema, buttons=("submit",))
    html_form = pwdform.render({'login':avatar.login})
    if "submit" in request.params:
        controls = request.params.items()
        try:
            datas = pwdform.validate(controls)
        except ValidationFailure, e:
            html_form = e.render()
        else:
            log.debug("# User {0} has changed his password #")
            dbsession = request.dbsession()
            new_pass = datas['pwd']
            avatar.set_password(new_pass)
            dbsession.merge(avatar)
            dbsession.flush()
            request.session.flash(u"Votre mot de passe a bien été modifié",
                                                                    'main')

    return dict(title="Mon compte",
                html_form=html_form,
                account=avatar
                )

def _get_user_form(edit=False):
    """
        Return the user add form
    """
    schema = userSchema.bind(edit=edit)
    form = Form(schema, buttons=('submit',))
    return form

class UserView(ListView):
    """
        User related views
    """
    columns = ("account_lastname", "account_email", )
    default_sort = 'account_lastname'
    default_direction = 'asc'

    @view_config(route_name='user_directory', renderer='directory.mako')
    def directory(self):
        """
            User directory
        """
        search, sort, direction, current_page, items_per_page = \
                                                self._get_pagination_args()
        query = self._get_users()
        if search:
            #FIXME :
            query = self._filter_search(query, search)
        users = query.order_by(sort + " " + direction).all()

        records = self._get_pagination(users, current_page, items_per_page)
        # Add user form
        form = _get_user_form(edit=False)
        return dict(title=u"Annuaire des utilisateurs",
                    users=records,
                    html_form=form.render())

    def _get_users(self):
        """
            return the user query
        """
        return self.dbsession.query(User).join(User.companies)

    def _filter_search(self, query, search):
        """
            Return a filtered query
        """
        return query.filter( or_(User.lastname.like("%"+search+"%"),
                     User.companies.any(Company.name.like("%"+search+"%"))))
