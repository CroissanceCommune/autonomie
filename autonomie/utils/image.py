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
import pkg_resources
from PIL import (
    Image,
    ImageDraw,
    ImageFont,
)
from StringIO import StringIO


def ensure_rgb(image):
    """
    Ensure the image is in RGB format
    """
    if image.mode != 'RGB':
        image = image.convert('RGB')
    return image


class ImageRatio(object):
    """
    Ensure images respect the given proportions by adding white spaces

    r = ImageRatio(height_proportion, width_proportion, default_color)
    resized_image_buffer = r.complete(image_buffer)

    resized_image_buffer will respect the given proportions and
    will be filed with the given color


    height

        The destination height used to compile the dest ratio

    width

        The destination width used to compile the dest ratio

    color

        The RGB tuple describing the filling color to use
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
        img_obj = ensure_rgb(img_obj)

        width, height = img_obj.size
        img_proportions = float(width)/float(height)

        if img_proportions >= self.proportions:
            mybuffer = StringIO()
            img_obj.save(mybuffer, format="PNG", mode="RGB")
            mybuffer.seek(0)
            return mybuffer
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


class ImageResizer(object):
    """
    Ensure image fit inside the given box

    if the image's width or height are larger than the provided one, the image
    is resized accordingly
    """
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def complete(self, img_buf):
        result = img_buf
        result.seek(0)
        img_obj = Image.open(result)
        img_obj = ensure_rgb(img_obj)
        width, height = img_obj.size

        img_obj.thumbnail((self.width, self.height), Image.ANTIALIAS)
        result = StringIO()
        img_obj.save(result, format='PNG')
        result.seek(0)
        return result


def build_header(text, size=(1000, 250)):
    """
    Build a header image containing text

    :param str text: The text to write
    :returns: The header image
    :rtype: StrinIO instance populated with the image datas in PNG Format
    """
    img = Image.new('RGB', size, (255, 255, 255))
    fontpath = pkg_resources.resource_filename(
        'autonomie',
        'static/fonts/playfair_display_regular.ttf'
    )
    font = ImageFont.truetype(fontpath, 30)

    d = ImageDraw.Draw(img)
    d.text((100, 100), text, font=font, fill=(0, 0, 0))
    mybuffer = StringIO()
    img.save(mybuffer, 'PNG')
    mybuffer.seek(0)
    return mybuffer
