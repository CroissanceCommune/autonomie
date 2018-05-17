# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


class NavigationHandler:
    """
    Class used to manage the navigation history of a user

    request

        Current pyramid request

    keyword

        The history keyword e.g: project

    Usage 1 : remember the current page

        >>> nav_handler = NavigationHandler(request, "project")
        >>> nav_handler.remember()

    Usage 2 : retrieve the last visited page

        >>> nav_handler = NavigationHandler(request, "project")
        >>> nav_handler.last()

    """
    def __init__(self, request, keyword, clean_query=True):
        self.keyword = keyword
        self.request = request
        self.clean_query = clean_query

        session_datas = self.request.user.session_datas or {}
        key_datas = session_datas.get(self.keyword, {})
        self.history = key_datas.get('history')

    def last(self):
        return self.history

    def remember(self):
        if self.clean_query:
            _query = {}
        else:
            _query = None
        path = self.request.current_route_path(_query=_query)
        if path != self.history:
            self.history = path
            self._save()

    def _save(self):
        session_datas = self.request.user.session_datas or {}
        session_datas.setdefault(self.keyword, {})['history'] = self.history
        if self.request.user.session_datas is None:
            self.request.user.session_datas = {}

        # NOte : Here we ensure passing through the __setitem__ method of our
        # MutableDict (see models.types for more informations)
        self.request.user.session_datas[self.keyword] = \
            session_datas[self.keyword]
        self.request.dbsession.merge(self.request.user)
        self.request.dbsession.flush()
