==========
Autonomie
==========

.. image::
    https://secure.travis-ci.org/CroissanceCommune/autonomie.png?branch=master
   :target: http://travis-ci.org/CroissanceCommune/autonomie
   :alt: Travis-ci: continuous integration status.


Un progiciel de gestion pour CAE -Coopérative d'activité et d'emploi.

Licence
-------

Ceci est un logiciel libre, pour les conditions d'accès, d'utilisation, de copie et d'exploitation, voir LICENSE.txt

Nouvelles fonctionnalités/Anomalies
-----------------------------------

Site officiel : http://autonomie.coop

L'essentiel du développement est réalisé sur financement de Coopérer pour
entreprendre.

Si vous rencontrez un bogue, ou avez une idée de fonctionnalité, il est possible
de signaler cela aux développeurs directement ou en utilisant le système de
tickets de github.
Exception : pour les bogues de sécurité, merci d'écrire un courriel à autonomie@majerti.fr.

Instructions pour l'installation du logiciel
--------------------------------------------

Installation des paquets (nécessaire pour l'installation dans un environnement
virtuel):

Sous Debian:

.. code-block:: console

    apt-get install virtualenvwrapper libmysqlclient-dev build-essential libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev python-mysqldb redis-server

Sous Fedora:

.. code-block:: console

    dnf install virtualenvwrapper mardiadb-devel python-devel libxslt-devel libxml2-devel libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel gcc redis-server

Création d'un environnement virtuel Python.

.. code-block:: console

    mkvirtualenv autonomie

Téléchargement et installation de l'application

.. code-block:: console

    git clone https://github.com/CroissanceCommune/autonomie.git
    cd autonomie
    python setup.py install
    cp development.ini.sample development.ini

Éditer le fichier development.ini et configurer votre logiciel (Accès à la base
de données, différents répertoires de ressources statiques ...).

Puis lancer l'application web

.. code-block:: console

    pserve development.ini

Éxécution des tâches asynchrones
---------------------------------

Un service de tâches asynchrones basé sur celery et redis est en charge de
l'éxécution des tâches les plus longues.

Voir :
https://github.com/CroissanceCommune/autonomie_celery

pour plus d'informations.

.. note::

    L'application synchronise automatiquement les modèles de données.

Puis créer un compte administrateur

.. code-block:: console

    autonomie-admin development.ini useradd [--user=<user>] [--pwd=<password>] [--firstname=<firstname>] [--lastname=<lastname>] [--group=<group>] [--email=<email>]


N.B : pour un administrateur, préciser

.. code-block:: console

    --group=admin


Développement
-------------

Dans un contexte de développement, installez autonomie avec les commandes
suivantes

.. code-block:: console

    git clone https://github.com/CroissanceCommune/autonomie.git
    cd autonomie
    pip install libsass pytest sphinx pyramid_debugtoolbar
    # Ici on install autonomie en mode developpement
    python setup.py develop
    cp development.ini.sample development.ini
