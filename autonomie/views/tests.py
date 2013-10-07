"""
    View for testing js scripts with qunit
    It's not really automated, but it's better than nuts
"""
from autonomie.resources import test_js


def testjs(request):
    """
        Only the template is interesting in this view
    """
    test_js.need()
    return dict(title=u"Page de test pour les composantes javascript")


def includeme(config):
    """
        Adding route and view for js tests usefull to test browser problems
    """
    config.add_route("testjs", "/testjs")
    config.add_view(testjs,
                    route_name='testjs',
                    permission="admin",
                    renderer='/tests/base.mako')