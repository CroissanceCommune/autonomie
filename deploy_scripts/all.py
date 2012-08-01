#!/usr/bin/python
"""
    Handle the installation of a new vm with all the necessary stuff
"""
import sys
import os
import sys
import inspect
# realpath() with make your script run, even if you symlink it :)
cmd_folder = os.path.realpath(os.path.abspath(os.path.split(inspect.getfile( inspect.currentframe() ))[0]))
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

from ConfigParser import RawConfigParser
from mysql import gen_database
from utils import gen_random_str
from tmplengine import process_templates

USAGE = """
Usage : install.py INIFILE TEMPLATEFILE
Description : installs autonomie with the options given in the provided inifile

Example:
    all.py /tmp/mywebsite.ini

Inifile format :
    Expected:

    [main]
    hostname=intranet.site.com

    Optionnal :

    [mail]
    host=localhost (default)
    port=25 (default)
    user=autonomie@site.com (default None)
    password=pass (default None)
    tls=True (default False)
"""

def usage(err_msg=""):
    print err_msg
    print "\n"
    print USAGE

def handle_args(args):
    if not args:
        usage("ERROR : An inifile is excepted as argument")
        sys.exit(1)
    else:
        inifile = args[0]
        if not os.path.isfile(inifile):
            usage("ERROR : The inifile doesn't exists")
            sys.exit(1)
    return inifile

class Parser(RawConfigParser):
    """
        DEFAULT_CONF = dict(url="autonomie.majerti.fr",
                            secret="95959ded46ce44aPdpkepkPMAlpdeplp",
                            mail=dict(host="localhost",
                                      port=25,
                                      username=None,
                                      password=None))
    """
    def __init__(self, inifile):
        RawConfigParser.__init__(self)
        self.read(inifile)

    def get_hostname(self):
        return self.get('main', 'hostname')

    def has_mail(self):
        return self.has_section('mail')

    def get_mail_conf(self):
        dico = {}
        for option in self.options('mail'):
            if option == 'tls':
                dico[option] = self.getboolean('mail', option)
            elif option == 'port':
                dico[option] = self.getint('mail', option)
            else:
                dico[option] = self.get('mail', option)
        return dico

    def get_db_conf(self):
        return dict(password="",
                    user="autonomie",
                    name="autonomie"),

    def has_dict(self):
        ret_dict = dict(db=self.get_db_conf())
        if self.has_mail():
            ret_dict['mail'] = self.get_mail_conf()
        ret_dict['url'] = self.get_hostname()
        return ret_dict

def addsite(cfgparser_obj):
    """
        Add a site's configuration
    """
    params = cfgparser_obj.has_dict()
    params['db']['password'] = gen_database()
    params['secret'] = gen_random_str(25)
    process_templates(params)

def main():
    args = sys.argv[1:]
    inifile = handle_args(args)
    cfgparser_obj = Parser(inifile)
    addsite(cfgparser_obj)

if __name__ == '__main__':
    main()
