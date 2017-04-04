# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
import bleach
from copy import deepcopy


ALLOWED_HTML_TAGS = bleach.ALLOWED_TAGS + [
    'font', 'br', 'p', 'span', 'h1', 'h2', 'h3', 'h4', 'h5', 'hr', 'img',
    'div', 'pre', 'sup', 'u', 'strike', 'sub',
]
ALLOWED_HTML_ATTRS = deepcopy(bleach.ALLOWED_ATTRIBUTES)
ALLOWED_HTML_ATTRS['font'] = ['color']
ALLOWED_HTML_ATTRS['*'] = ['class', 'style']
ALLOWED_HTML_ATTRS['img'] = ['src', 'width', 'height', 'alt']
ALLOWED_CSS_STYLES = [
    'color', 'text-align', 'font-weight', 'font-family', 'text-decoration',
]


VOID_TAGS = ('<br />', '<br/>', )
TAGS_TO_CHECK = (('<p>', '</p>'), ('<div>', '</div>'),)


def remove_tag(text, tag):
    """
    Remove the tag from the beginning of the given text

    :param str text: The text with the tag
    :param str tag: The tag to remove
    :rtype: str
    """
    return text[0:-1*len(tag)].strip()


def strip_whitespace(value):
    """
    Strip whitespace and tabs at the beginning/end of a string

    :param str value: The value to clean
    :rtype: str
    """
    if hasattr(value, 'strip'):
        value = value.strip(' \t')
    return value


def strip_linebreaks(value):
    """
    Strip linebreaks

    :param str value: The value to clean
    :rtype: str
    """
    # we don't use rstrip since it's used for character stripping
    # (not chain)
    if hasattr(value, 'strip'):
        value = value.strip('\n\r')
        for tag in '<br />', '<br>', '<br/>':
            if value.endswith(tag):
                value = remove_tag(value, tag)
                return strip_linebreaks(value)

    return value


def strip_void_lines(value):
    """
    RStrip value ending with void html tags

    :param str value: The value to clean
    :rtype: str
    """
    if hasattr(value, 'strip'):
        for tag, close_tag in TAGS_TO_CHECK:
            if value.endswith(close_tag):
                prec_value = remove_tag(value, close_tag)
                prec_value = strip_whitespace(prec_value)
                prec_value = strip_linebreaks(prec_value)
                if prec_value.endswith(tag):
                    value = remove_tag(prec_value, tag)
                    value = strip_whitespace(value)
                    value = strip_linebreaks(value)
                    return strip_void_lines(value)

    return value


def strip_html(value):
    """
    Strip html void lines
    """
    value = strip_whitespace(value)
    value = strip_linebreaks(value)
    return strip_void_lines(value)


def clean_html(text):
    """
        Return a sanitized version of an html code keeping essential html tags
        and allowing only a few attributes
    """
    text = strip_html(text)
    return bleach.clean(
        text,
        tags=ALLOWED_HTML_TAGS,
        attributes=ALLOWED_HTML_ATTRS,
        styles=ALLOWED_CSS_STYLES,
        strip=True,
    )
