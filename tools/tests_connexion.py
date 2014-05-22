# -*- coding: utf-8 -*-
# * File Name : testit.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 05-02-2013
# * Last Modified :
#
# * Project :
#
import logging
import sys
import mechanize

def getlogger():
    logging.basicConfig(level=logging.DEBUG,
            format="[%(filename)s:%(lineno)s]%(message)s\n",
            filename="/tmp/testlog.log")

    logger = logging.getLogger("testautonomie")
    return logger


class Tester(object):
    def __init__(self, url, login):
        self.br = mechanize.Browser()
        self.br.set_handle_robots(False)
        self.url = url
        self.login = login
        self.password = "o"
        self.domain = self.remove_port_and_http(url)
        self.login_url = self.get_login_url(url)
        self.account_url = self.get_account_url(url)
        self.log = getlogger().info

    def remove_port_and_http(self, url):
        url = url[7:]
        return url.split(':')[0]

    def get_login_url(self, url):
        return '%s/login' % (url,)

    def get_account_url(self, url):
        return '%s/account' % (url,)

    def connect(self):
        self.br.open(self.login_url)
        # First form
        self.br.select_form(nr=0)
        self.br.form['login'] = self.login
        self.br.form['password'] = self.password
        self.br.submit()
        cookies = self.br._ua_handlers['_cookies'].cookiejar.__dict__
        return cookies['_cookies'][self.domain]['/']['beaker.session.id'].value

    def is_login_in_account_page(self):
        resp = self.br.open(self.account_url)
        page = resp.read()
        if self.login in page:
            return True, "OK, it's the good page"
        else:
            self.log("***********************************")
            self.log(self.login)
            self.log(page.replace('  ', ''))
            return False, "ERROR : wrong page fetched watch testlog.log"

    def run(self):
        session_id = self.connect()
        result, msg = self.is_login_in_account_page()
        if not result:
            print "%s : %s -> %s" % (self.login, session_id, msg)


def main():
    url = sys.argv[1]
    login = sys.argv[2]
    test_obj = Tester(url, login)
    test_obj.run()


if __name__ == '__main__':
    main()
