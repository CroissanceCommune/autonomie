# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;

import logging


logger = logging.getLogger(__name__)


class FileAdded(object):
    """
    Event to be fired on new file download

    >>> request.registry.notify(FileAdded(request, file_object))
    """
    action = "add"

    def __init__(self, request, file_object):
        self.request = request
        self.file_object = file_object
        self.parent = self.file_object.parent


class FileUpdated(FileAdded):
    """
    Event to be fired on file update

    >>> request.registry.notify(FileUpdated(request, file_object))
    """
    action = "update"


class FileDeleted(FileAdded):
    """
    Event fired when a file was deleted
    >>> request.registry.notify(FileDeleted(request, file_object))
    """
    action = "delete"


def on_file_change(event):
    if hasattr(event.parent, "file_requirement_service"):
        logger.info(u"+ Calling the parent's file requirement service")
        event.parent.file_requirement_service.register(
            event.parent, event.file_object, action=event.action
        )
        if hasattr(event.parent, "status_service"):
            event.parent.status_service.update_status(
                event.parent,
            )


def includeme(config):
    config.add_subscriber(on_file_change, FileAdded)
    config.add_subscriber(on_file_change, FileUpdated)
    config.add_subscriber(on_file_change, FileDeleted)
