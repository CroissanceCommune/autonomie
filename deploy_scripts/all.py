#!/usr/bin/python
"""
    Handle the installation of a new vm with all the necessary stuff
"""
import sys

from .mysql import gen_database
from .utils import gen_random_str
from .tmplengine import process_templates

DEFAULT_CONF = dict(url="autonomie.majerti.fr",
                            secret="95959ded46ce44aPdpkepkPMAlpdeplp",
                            db=dict(password="toBeSet",
                                     user="autonomie",
                                     name="autonomie"),
                            mail=dict(host="smtp.google.fr",
                                      port="567",
                                      username="nill",
                                      password="nopass"))
def addsite(server_conf):
    """
        Add a site's configuration
    """
    params = DEFAULT_CONF
    params.update(server_conf)
    params['db']['password'] = gen_database()
    params['secret'] = gen_random_str(25)
    process_templates(params)

if __name__ == '__main__':
    addsite({'url':sys.argv[1]})
