==========
Autonomie
==========

.. image::
    https://secure.travis-ci.org/CroissanceCommune/autonomie.png?branch=master
   :target: http://travis-ci.org/#!/CroissanceCommune/autonomie
      :alt: Travis-ci: continuous integration status.


Un progiciel de gestion pour CAE -Coopérative d'activité et d'emploi.

Licence
-------

Ceci est un logiciel libre, pour les conditions d'accès, d'utilisation, de copie et d'exploitation, voir LICENSE.txt

Nouvelles fonctionnalités/Anomalies
-----------------------------------

Site officiel : http://autonomie.coop

L'essentiel du développement est réalisé sur financement de Croissance Commune.

Si vous rencontrez un bogue, ou avez une idée de fonctionnalité, il est possible
de signaler cela aux développeurs directement ou en utilisant le système de
tickets de github.
Exception : pour les bogues de sécurité, merci d'écrire un courriel à autonomie@majerti.fr.

Instructions pour l'installation du logiciel
--------------------------------------------

Installation des paquets (nécessaire pour l'installation dans un environnement
virtuel):

.. code-block:: console

    apt-get install virtualenvwrapper libmysqlclient-dev build-essential libjpeg-dev libfreetype6 libfreetype6-dev zlib1g-dev python-mysqldb

Création d'un environnement virtuel Python.

.. code-block:: console

    mkvirtualenv autonomie

Téléchargement et installation de l'application

.. code-block:: console

    git clone https://github.com/Croissance_Commune/autonomie.git
    cd autonomie
    pip -r requirements.txt
    python setup.py install
    cp development.ini.sample development.ini

Éditer le fichier development.ini et configurer votre logiciel (Accès à la base
de données, différents répertoires de ressources statiques ...).

Puis lancer l'application

.. code-block:: console

    pserve development.ini

L'application synchronise automatiquement les modèles de données.

Puis créer un compte administrateur

.. code-block:: console

    autonomie-admin development.ini add [--user=<user>] [--pwd=<password>] [--firstname=<firstname>] [--lastname=<lastname>]
