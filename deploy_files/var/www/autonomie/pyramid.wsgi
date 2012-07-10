import os

from pyramid.paster import get_app
from pyramid.paster import setup_logging

HERE = os.path.dirname(__file__)
APP_INIFILE = os.path.join(HERE, 'autonomie', 'production.ini')

setup_logging(APP_INIFILE)

application = get_app(APP_INIFILE, 'main')
