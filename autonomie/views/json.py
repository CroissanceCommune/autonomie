"""
    Json API views
"""

def json_project(request):
    """
        Return a json representation of the project
    """
    return request.context.todict()

def includeme(config):
    """
        Configure the views for this module
    """
    for route_name in "project", "company", "client":
        config.add_view(json_project,
                        route_name=route_name,
                        renderer='json',
                        request_method='GET',
                        xhr=True,
                        permission='edit')