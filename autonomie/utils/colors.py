# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2014 Croissance Commune
# * Authors:
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
"""
Color utilities
"""
from colorsys import hsv_to_rgb
from random import uniform


COLORS_SET = (
    '#20d21e', '#d6d506', '#fbe300', '#1795d9', '#b1d31c', '#b231fc',
    '#d79e0c', '#2877d9', '#b618e7', '#1cf1a8', '#0ef016', '#b5ea22',
    '#7eda21', '#0843cc', '#2caaed', '#0d64fb', '#91f003', '#16ee6b',
    '#00d5e5', '#9327fb', '#03def4', '#8b0bd1', '#0e5ad7', '#28d2d2',
    '#26b5ea', '#f9c61e', '#117cef', '#8806ee', '#4e16ef', '#75e11c',
    '#02ee41', '#1ee855', '#04e5af', '#0fcc58', '#48f714', '#02fe12',
    '#87d202', '#6bce1d', '#5dfb0f', '#faad20', '#56f82d', '#07df3a',
    '#db9828', '#dc951f', '#01f856', '#00fbec', '#1def3c', '#15d3a4',
    '#1bd677', '#18b0dd', '#bb2efa', '#0337f9', '#59ea13', '#17e3a8',
    '#59d015', '#f1e017', '#99e62c', '#287ce0', '#662ad8', '#5606cd',
    '#b9ea13', '#1228f1', '#0631d6', '#0cd688', '#13ed02', '#4ddf03',
    '#07abe4', '#eff62f', '#0ce2d8', '#1c35fd', '#0bbfee', '#08ee53',
    '#1c04cd', '#3fe026', '#1416f5', '#03cfee', '#1624d6', '#72d31c',
    '#7610e8', '#17dde3', '#94e919', '#54cf23', '#11ce87', '#1c17ec',
    '#09df6d', '#1ebad7', '#cd900b', '#e8c521', '#e8ce05', '#aaf50c',
    '#08d4d0', '#0ede29', '#0cec08', '#1650dd', '#07cf06', '#feeb1a',
    '#d6ed04', '#b8e321', '#29de75', '#8707e7', '#340dfd', '#d5b516',
    '#2acdfe', '#930fdf', '#0d9be1', '#15d266', '#4211d2', '#4908f6',
    '#9221dd', '#1a19d2', '#d3f52b', '#2f0ee3', '#0ce4e7', '#20f68e',
    '#1d93d3', '#d6962a', '#891bcf', '#632dfa', '#d0a029', '#0d28fb',
    '#8f1afd', '#5dd127', '#fcdd04', '#0721e6', '#44e315', '#2990d1',
    '#ccdb21', '#931dd2', '#a1e82c', '#8e0ed3', '#5022d9', '#06f249',
    '#14f105', '#2ff562', '#daa61e', '#531bf0', '#17f8f0', '#92f30f',
    '#570fd5', '#1de2c9', '#63e806', '#41d70f', '#2ccef1', '#21d670',
    '#1419fc', '#1cce97', '#2298e0', '#6411f6', '#f0e510', '#00eb1f',
    '#e18f12', '#2c7bf8', '#0be92c', '#2791d7', '#6c24f8', '#751ad8',
    '#05b5e2', '#3d01e3', '#078edc', '#4412eb', '#d6aa1c', '#6ced0f',
    '#2918de', '#0f22d7', '#2772d6', '#0fe3b0', '#6f0bee', '#3efd27',
    '#1ccdf2', '#170ad8', '#a12ff5', '#80cc1b', '#15dfe9', '#63ef0c',
    '#5908db', '#8c0bfb', '#78d628', '#0c71d2', '#4b25f8', '#cff52c',
    '#6827d2', '#2ef14f', '#23c6eb', '#eaee10', '#d6f70d', '#46db1a',
    '#20fa35', '#5aea19', '#84dd0e', '#1ee960', '#11c6ea', '#cffa16',
    '#1bd9de', '#7fd123', '#dccf17', '#2ff397', '#2dcdf3', '#14e091',
    '#e0c709', '#0bc7fd')


def rgb_to_hex(rgb):
    """
        return an hexadecimal version of the rgb tuple
        for css rendering
    """
    return '#%02x%02x%02x' % rgb


def get_color():
    """
        return a random color
    """
    h = uniform(0.1, 0.8)
    s = uniform(0.8, 1)
    v = uniform(0.8, 1)
    return rgb_to_hex(tuple(255 * c for c in hsv_to_rgb(h, s, v)))
