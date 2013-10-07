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
    utilities for image handling
"""
from PIL import Image
from StringIO import StringIO


class ImageResizer(object):
    """
        Allows to resize images regarding given proportions
        r = ImageResize(height_proportion, width_proportion, default_color)
        resized_image_buffer = r.complete(image_buffer)

        resized_image_buffer will respect the given proportions and
        will be filed with the default color
    """
    def __init__(self, width, height, color=(255, 255, 255,)):
        self.proportions = float(width)/float(height)
        self.color = color

    def get_white_layer(self, width, height):
        """
            Returns a white layer that will be our image background
        """
        size = (width, height)
        return Image.new('RGB', size, self.color)

    def complete(self, img_buf):
        """
            Complete the image to get at last my proportions, not more
        """
        img_buf.seek(0)
        img_obj = Image.open(img_buf)

        width, height = img_obj.size
        img_proportions = float(width)/float(height)

        if img_proportions >= self.proportions:
            return img_buf
        else:
            new_width = int(height * self.proportions)
            new_height = height
            padding = (new_width - width) / 2
            layer = self.get_white_layer(new_width, new_height)
            layer.paste(img_obj, (padding, 0))
            mybuffer = StringIO()
            layer.save(mybuffer, format="PNG")
            mybuffer.seek(0)
            return mybuffer
