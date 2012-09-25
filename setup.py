#!/usr/bin/env python
from setuptools import setup

entry_points = {
    "paste.app_factory": ["main=autonomie:main",],
    "console_scripts": ["autonomie-migrate = autonomie.scripts:migrate"]
}

setup(
    setup_requires=['d2to1'],
    d2to1=True,

    # This ensures that the MANIFEST.in is read, but it will become implicit
    # in distutils2.
    include_package_data=True,

    # This is setuptools specific, will not work with distutils2.
    entry_points=entry_points,
    test_suite="autonomie.tests"
)
