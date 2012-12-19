#-*-coding:utf-8-*-
import logging
from pyramid_formalchemy.resources import Models

from autonomie import models
from autonomie.models import tva
from autonomie.utils.security import DEFAULT_PERM

log = logging.getLogger(__name__)

class ModelsWithAcl(Models):
    __acl__ = DEFAULT_PERM[:]


class ACLProxy(object):
    def __init__(self, proxified):
        self.proxified = proxified

    def __getattr__(self, name):
        if name == "__acl__":
            return DEFAULT_PERM[:]
        return getattr(self.proxified, name)


def includeme(config):
    config.include('pyramid_formalchemy')
    config.include('fa.jquery')

    try:
        # Add fanstatic tween if available
        config.include('pyramid_fanstatic')
    except ImportError:
        log.warn('You should install pyramid_fanstatic or register a fanstatic'
                 ' middleware by hand')

    session_factory = models.DBSESSION

    # register session and model_view for later use
    settings = {'package': 'autonomie',
                'session_factory': session_factory,
                'factory':ModelsWithAcl,
               }
    config.registry.settings['autonomie.fa_config'] = settings

    config.formalchemy_admin("/adminfa",
                            view='fa.jquery.pyramid.ModelView',
                            models=[ACLProxy(tva.Tva),
                                    ACLProxy(models.project.Project)],
                             **settings)

    # Adding the package specific routes
    log.debug('formalchemy_admin registered at /adminfa')
