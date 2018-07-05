# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def get_post_int(request, key, default):
    """
        Retrieve an int from the post datas
        :param key: the key the data should be retrieved from
        :param default: a default value
    """
    val = default
    if key in request.POST:
        try:
            val = int(request.POST[key])
        except ValueError:
            val = default
    return val


def get_page_number(request, post_arg):
    """
        Return the page number the user is asking
    """
    return get_post_int(request, post_arg, 0)


def make_get_list_url(listname):
    """
    Return a url builder for the pagination
        :param listname: the name of the list
    """
    tmpl = "#{listname}/{option}".format(listname=listname, option="{0}")

    def _get_list_url(page):
        """
            Return a js url for a list pagination
            :param page: page number
        """
        return tmpl.format(page)
    return _get_list_url


def get_items_per_page(request, cookie_name):
    """
    Infers the nb of items per page from a request.
    If value supplied in POST, we redefine it in a cookie.

    cookie_name is a string representation of a base 10 int
        expected to be 5, 15 or 50.

    """
    default = 5

    post_value = get_post_int(request, cookie_name, None)
    if post_value is not None:
        request.response.set_cookie(cookie_name, '%d' % post_value)
        return post_value

    if cookie_name in request.cookies:
        raw_nb_per_page = request.cookies[cookie_name]
        try:
            return int(raw_nb_per_page)
        except ValueError:
            # Not an int, setting it again and going on
            request.response.set_cookie(cookie_name, '%d' % default)

    # fall back to base value
    return default
