# -*- coding: utf-8 -*-
# * File Name : avatar.py
#
# * Copyright (C) 2010 Gaston TJEBBES <tonthon21@gmail.com>
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 07-02-2012
# * Last Modified : mer. 28 mars 2012 10:00:50 CEST
#
# * Project : Autonomie
#
import logging

log = logging.getLogger(__name__)

def get_build_avatar(dbsession):
    def build_avatar(login, request):
        """
            Stores the avatar object in the session
        """
        log.debug("# Building avatar")
        from autonomie.models.model import User
        avatar = dbsession.query(User).filter_by(login=login).first()
        request.session['user'] = avatar
        if avatar:
            return []
    return build_avatar
