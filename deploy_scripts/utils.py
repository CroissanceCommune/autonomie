# -*- coding: utf-8 -*-
# * File Name : utils.py
#
# * Copyright (C) 2010 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 10-07-2012
# * Last Modified :
#
# * Project :
#
"""
    Main functions
"""
import os
import random
import string

def gen_random_str(length=10):
    """
        Return a random string
    """
    return ''.join(random.choice(string.letters) for i in xrange(length))

def launch_cmd(cmd):
    """
        Entry point used to launch commands
    """
    print "Launching command : {0}".format(cmd)
    os.system(cmd)


