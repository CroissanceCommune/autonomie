# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


class MenuItem(object):
    __type__ = 'item'

    def __init__(self, name, route_name, icon, label, title=None, perm=None):
        self.name = name

        if title is None:
            self.title = label
        else:
            self.title = title

        self.icon = icon
        self.label = label
        self.route_name = route_name
        self.perm = perm

    def url(self, context, request):
        return request.route_path(
            self.route_name,
            id=context.id
        )

    def enabled(self, context, request):
        return True

    def selected(self, context, request):
        return request.matched_route.name == self.route_name

    def has_permission(self, context, request):
        if self.perm is not None:
            return request.has_permission(self.perm)
        return True


class MenuDropdown(object):
    """
    Dropdown menu

    icon

        An icon

    label

        A label (will be used as title on smaller viewports

    title

        The title shown on hovering the menu entry

    default_route

        If the menu is disabled, a link to that route will be provided instead
    """
    __type__ = 'dropdown'

    def __init__(
        self, name, icon, label, title=None, default_route=None, perm=None
    ):
        self.name = name
        if title is None:
            self.title = label
        else:
            self.title = title

        self.icon = icon
        self.label = label
        self.items = []
        self.default_route = default_route
        self.perm = perm

    def add_item(self, name, route_name, icon, label, title=None, perm=None):
        self.items.append(
            MenuItem(name, route_name, icon, label, title, perm=perm)
        )

    def enabled(self, context, request):
        return True

    def url(self, context, request):
        if self.default_route:
            return request.route_path(
                self.default_route,
                id=context.id
            )

    def selected(self, context, request):
        res = False
        for item in self.items:
            if item.selected(context, request):
                res = True
                break
        return res

    def has_permission(self, context, request):
        if self.perm is not None:
            return request.has_permission(self.perm)
        return True


class AttrMenuItem(MenuItem):
    """
    A menu item that is condionnaly shown regarding a model's attribute

    If the context's attribute is None, the menu is not shown
    """
    def __init__(self, *args, **kw):
        self.model_attribute = kw.pop('model_attribute')
        MenuItem.__init__(self, **kw)

    def enabled(self, context, request):
        return getattr(context, self.model_attribute, None) is not None


class AttrMenuDropdown(MenuDropdown):
    def __init__(self, *args, **kw):
        self.model_attribute = kw.pop('model_attribute')
        MenuDropdown.__init__(self, **kw)

    def enabled(self, context, request):
        return getattr(context, self.model_attribute, None) is not None


class Menu(object):
    def __init__(self, name):
        self.name = name
        self.items = []

    def add(self, item):
        self.items.append(item)

    def add_before(self, name, new_item):
        """
        Add an item before the item named name
        """
        for index, item in enumerate(self.items[:]):
            if item.name == name:
                self.items.insert(index, new_item)
                return
        raise KeyError(u"Unknown node : %s" % name)

    def add_after(self, name, new_item):
        """
        Add an item after the item named name
        """
        for index, item in enumerate(self.items[:]):
            if item.name == name:
                self.items.insert(index + 1, new_item)
                return
        raise KeyError(u"Unknown node : %s" % name)
