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

    apt-get install virtualenvwrapper libmariadbclient-dev build-essential libjpeg-dev libfreetype6 libfreetype6-dev libxml2-dev zlib1g-dev python-mysqldb redis-server libxslt1-dev


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

Initialiser la base de données

.. code-block:: console

    autonomie-admin development.ini syncdb

.. note::

    L'application synchronise automatiquement les modèles de données.

Puis créer un compte administrateur

.. code-block:: console

    autonomie-admin development.ini useradd [--user=<user>] [--pwd=<password>] [--firstname=<firstname>] [--lastname=<lastname>] [--group=<group>] [--email=<email>]

N.B : pour un administrateur, préciser

.. code-block:: console

    --group=admin


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

Mise à jour
-----------

La mise à jour d'Autonomie s'effectue en deux temps (il est préférable de
sauvegarder vos données avant de lancer les commandes suivantes)

Mise à jour de la structure de données

.. code-block:: console

    autonomie-migrate app.ini upgrade

Configuration des données par défaut dans la base de données

.. code-block:: console

    autonomie-admin app.ini syncdb


Développement
-------------

Dans un contexte de développement, installez autonomie avec les commandes
suivantes

.. code-block:: console

    git clone https://github.com/CroissanceCommune/autonomie.git
    cd autonomie
    pip install pyramid_debugtoolbar
    # Ici on install autonomie en mode developpement
    python setup.py develop
    cp development.ini.sample development.ini


Base de données avec Vagrant
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Pour héberger la base de données dans une machine virtuelle jettable et
reproductible sans toucher à la machine hôte, une configuration Vagrant est
disponible. Pour l'utiliser :

.. code-block:: console

    apt install virtualbox vagrant

Et pour lancer cette machine :

.. code-block:: console

    vagrant up

Un serveur MariaDB est alors installé et configuré (port local 13306 de l'hôte
local, base: autonomie, login: autonomie, password: autonomie).

Des configurations adaptées à vagrant sont commentées dans ``test.ini.sample`` et
``developement.ini.sample``.

Au besoin, la base peut être remise à zéro avec :

.. code-block:: console

    vagrant provision


Tests
------

Installer les dépendances de test

.. code-block:: console

    pip install -r test_requirements.txt

Copier et personaliser le fichier de configuration

.. code-block:: console
    cp test.ini.sample test.ini

Lancer les tests

.. code-block:: console

   py.test autonomie/tests
   
Documentation utilisateur
--------------------------

Le guide d'utilisation se trouve à cette adresse :
https://docerp.cooperer.coop
