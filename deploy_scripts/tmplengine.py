#!/usr/bin/python
# -*- coding: utf-8 -*-
# * File Name : tmplengine.py
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
    Templating machinery
"""
import os
from mako.template import Template

HERE = os.path.abspath(__file__)
TMPL_DIR = os.path.join(HERE, "deploy_files/")
DEST_DIR = "/tmp/garbage/"

def mkdir_p(dirname):
    """
        mkdir -p behaviour
    """
    try:
        os.makedirs(dirname)
    except:
        pass


def get_tmpls(root=TMPL_DIR):
    """
        yield tmpls abs and relative path
    """
    for path, subdir, files in os.walk(root):
        rel_dir = os.path.relpath(path, root)
        for file_ in files:
            filepath = os.path.join(path, file_)
            rel_path = os.path.relpath(filepath, root)
            yield (rel_dir, filepath, rel_path)


def templatize(params):
    """
        Gen the files
    """
    for rel_dir, tmpl_path, rel_path in get_tmpls():
        mkdir_p(os.path.join(DEST_DIR, rel_dir))
        print "Template : {0}".format(tmpl_path)
        tmpl = Template(filename=tmpl_path)
        datas = tmpl.render(app=params)
        dest_file = os.path.join(DEST_DIR, rel_path)
        print "Writing to dest file : {0}".format(dest_file)
        a = file(dest_file, 'w')
        a.write(datas)
        a.close()
    return "All is all_right"

class obj(object):
    """
        Object allowing simple dict to object conversion
        used to pass attributes to the templates
    """
    def __init__(self, d):
        for a, b in d.items():
            if isinstance(b, (list, tuple)):
                setattr(self, a, [obj(x) if isinstance(x, dict) else x for x in b])
            else:
                setattr(self, a, obj(b) if isinstance(b, dict) else b)

def process_templates(conf):
    """
        templatize all the stuff
    """
    all_params = obj(conf)
    templatize(all_params)
