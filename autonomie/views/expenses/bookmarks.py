# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


class BookMarkHandler(object):
    """
        Wrapper for expense bookmarks
    """
    def __init__(self, request):
        self.request = request
        self.bookmarks = {}
        self.load_bookmarks_from_current_request()

    def load_bookmarks_from_current_request(self):
        session_datas = self.request.user.session_datas or {}
        expense_datas = session_datas.get('expense', {})
        self.bookmarks = expense_datas.get('bookmarks', {})

    def refresh(self):
        self.load_bookmarks_from_current_request()

    def store(self, item):
        """
            Store a bookmark (add/edit)
            :@param item: a dictionnary with the bookmark informations
        """
        id_ = item.get('id')
        if not id_:
            id_ = self._next_id()
            item['id'] = id_

        self.bookmarks[id_] = item
        self._save()
        return item

    def delete(self, id_):
        """
            Removes a bookmark
        """
        item = self.bookmarks.pop(id_, None)
        if item is not None:
            self._save()
        return item

    def _next_id(self):
        """
            Return the next available bookmark id
        """
        id_ = 1
        if self.bookmarks.keys():
            all_keys = [int(key) for key in self.bookmarks.keys()]
            id_ = max(all_keys) + 1
        return id_

    def _save(self):
        """
            Persist the bookmarks in the database
        """
        session_datas = self.request.user.session_datas or {}
        session_datas.setdefault('expense', {})['bookmarks'] = self.bookmarks
        if self.request.user.session_datas is None:
            self.request.user.session_datas = {}

        # NOte : Here we ensure passing through the __setitem__ method of our
        # MutableDict (see models.types for more informations)
        self.request.user.session_datas['expense'] = session_datas['expense']
        self.request.dbsession.merge(self.request.user)
        self.request.dbsession.flush()


def get_bookmarks(request):
    """
        Return the user's bookmarks
    """
    return BookMarkHandler(request).bookmarks.values()
