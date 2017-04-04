#!/usr/bin/env python
import os
from setuptools import setup
from setuptools import find_packages


here = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(here, 'README.rst')) as f:
    README = f.read()

with open(os.path.join(here, 'requirements.txt')) as f:
    install_reqs = f.read()

entry_points = {
    "paste.app_factory": ["main=autonomie:main", ],
    "console_scripts": [
        "autonomie-migrate = autonomie.scripts:migrate",
        "autonomie-admin = autonomie.scripts:autonomie_admin_cmd",
        "autonomie-mail = autonomie.scripts.mail_files:mail_cmd",
        "autonomie-fake = autonomie.scripts:populate_fake",
        "autonomie-cache = autonomie.scripts:cache_cmd",
        "autonomie-export = autonomie.scripts:export_cmd",
    ],
    "fanstatic.libraries": ["autonomie = autonomie.resources:lib_autonomie"]
}

setup(
    name='autonomie',
    version='3.3.0',
    description="Progiciel de gestion pour CAE",
    long_description=README,
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python",
        "Framework :: Pyramid",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: WSGI :: Application",
    ],
    author='Majerti',
    author_email="tech@majerti.fr",
    url="http://autonomie.coop",
    keywords="pyramid,business,web",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=install_reqs,
    tests_require=['pytest', 'WebTest', "Mock"],
    extras_require={
        'dev': ['libsass', 'sphinx'],
    },
    setup_requires=[],
    test_suite="autonomie.tests",
    entry_points=entry_points,
)
