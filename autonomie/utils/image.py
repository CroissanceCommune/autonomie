# -*- coding: utf-8 -*-
# * File Name : image.py
#
# * Copyright (C) 2012 Gaston TJEBBES <g.t@majerti.fr>
# * Company : Majerti ( http://www.majerti.fr )
#
#   This software is distributed under GPLV3
#   License: http://www.gnu.org/licenses/gpl-3.0.txt
#
# * Creation Date : 08-01-2013
# * Last Modified :
#
# * Project :
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
