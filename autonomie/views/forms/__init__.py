# -*- coding: utf-8 -*-
# * File Name : __init__.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 10-04-2012
# * Last Modified :
#
# * Project : Autonomie
#
"""
    Form Schemas for autonomie
"""
from .user import get_auth_schema
from .user import get_password_change_schema
from .user import get_user_schema
from .user import get_user_del_schema
from .client import ClientSchema
from .project import ProjectSchema
from .project import phaseSchema
from .admin import MainConfig
from .admin import TvaConfig
from .comptability import OperationSchema
from .utils import BaseFormView

