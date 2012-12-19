#-*-coding:utf-8-*-

from autonomie import models
import logging

log = logging.getLogger(__name__)


def includeme(config):
    settings = config.registry.settings.get('autonomie.fa_config', {})

    # Example to add a specific model
    config.formalchemy_model("tva",
                             model='autonomie.models.tva.Tva',
                             **settings)
    config.formalchemy_model("user",
                            model='autonomie.models.user.User',
                                **settings)


    log.info('autonomie.faroutes loaded')
