# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2013 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#       * Pettier Gabriel;
#       * TJEBBES Gaston <g.t@majerti.fr>
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    Filesystem abstraction
"""
import os
import datetime
import math

from urllib import pathname2url, url2pathname


UNITIES = ['o', 'ko', 'Mo']

def filesizeformat(value, precision=2):
    """
        Returns a humanized string for a given amount of bytes
    """
    if value == 0:
        return '0 o'
    log = math.floor(math.log(value, 1024))
    unity = UNITIES[int(log)]
    return "%.*f%s" % ( precision, value / math.pow(1024, log), unity )

def encode_path(path):
    """
        format a filepath as a dict key
    """
    if type(path) == unicode:
        path = path.encode('utf-8')
    return pathname2url(path)


def decode_path(path):
    """
        decode a filepath
    """
    if type(path) == unicode:
        path = path.encode('utf-8')
    return url2pathname(path).decode('utf-8')


def issubdir(root_path, path):
    """
        Return True if path is a subdirectory of root_path
    """
    root = os.path.realpath(root_path)
    path = os.path.realpath(path)
    return os.path.commonprefix([root, path]) == root


class Base(dict):
    """
        Base resource object for directory representation
    """
    def __init__(self, path, parent, **args):
        dict.__init__(self, **args)
        self.parent = parent
        self.path = path
        self.name = os.path.basename(path)
        self.__name__ = os.path.basename(path)

    def get_path(self):
        path = self.get_keyname()
        if self.parent and hasattr(self.parent, "get_path"):
            path = os.path.join(self.parent.get_path(), path)
        return path

    def get_keyname(self):
        return encode_path(self.path)


class File(Base):
    """
        File resource object
    """
    def __init__(self, path, parent, **args):
        Base.__init__(self, path, parent, **args)
        self.mod_time = os.path.getatime(path)
        self.size = os.path.getsize(path)

    def get_mod_date(self):
        """
            return a datetime object for the atime of the file
        """
        return datetime.datetime.fromtimestamp(self.mod_time)

    def get_size(self):
        """
            Return a pretty printing value of the file
        """
        return filesizeformat(self.size)

    def isdir(self):
        return False


class Directory(Base):
    """
        Directory resource object
    """
    def __init__(self, path, parent=None, **args):
        Base.__init__(self, path, parent, **args)
        self.children = self.build_children()

    def build_children(self):
        """
            Populate the resource's dict
        """
        for child in os.listdir(self.path):
            child_path = os.path.join(self.path, child)
            if os.path.isfile(child_path):
                element = File(child_path, self)
            else:
                element =  Directory(child_path, self)
            self.add_child(child, element)

    def add_child(self, name, element):
        """
            Add a child element
        """
        key = encode_path(name)
        self[key] = element

    def isdir(self):
        return True



def get_timestamped_filename(root_name, extension):
    """
    Build a filename with timestamp info

    :param str root_name: The filename prefix
    :param str extension: The extension of the destination file

    :returns: a filename with a timestamp
    :rtype: str
    """
    today = datetime.date.today()
    return u"{0}_{1}.{2}".format(
        root_name,
        today.strftime("%d%m%Y"),
        extension,
    )
