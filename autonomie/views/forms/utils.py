# -*- coding: utf-8 -*-
# * File Name :
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 17-10-2012
# * Last Modified :
#
# * Project :
#
"""
    Form view tool to easily build form views
"""
from pyramid_deform import FormView
from autonomie.utils.views import submit_btn

class BaseFormView(FormView):
    """
        Allows to easily build form views
    """
    add_template_vars = ('title',)
    buttons = (submit_btn,)

    def __init__(self, request):
        super(BaseFormView, self).__init__(request)
        self.dbsession = self.request.dbsession
        self.session = self.request.session

    def __call__(self):
        result = super(BaseFormView, self).__call__()
        if isinstance(result, dict):
            result.update(self.more_template_vars())
        return result

    def more_template_vars(self):
        """
            Add template vars to the response dict
        """
        result = {}
        for name in self.add_template_vars:
            result[name] = getattr(self, name)
        return result
