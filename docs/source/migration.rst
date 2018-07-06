Guide de migration
==================

Ce document reprend des éléments aidant à la réalisation de migrations de
données depuis un autre système, par exemple depuis WinScop.

Numéros de facture
------------------

Par défaut (sur les nouvelles installations), les factures sont numérotés avec
une séquence chronologique globale, non liée ni à une année, ni à une activité,
et sans préfixe (1, 2, 3…).

Gabarit de n° de facture
^^^^^^^^^^^^^^^^^^^^^^^

Il est possible de configurer l'usage de séquences plus complexes, pour
s'adapter au schéma de numérotation existant ou décidé au sein de la CAE. La
liste des variables et séquences disponibles et leur configuration se passe
depuis l'écran ``/admin/sales/numbering``.

.. note::

   Le gabarit de n° de facture utilise la `syntaxe de formatage Python`_, il est
   donc possible d'en utiliser les options avancées (remplissage, alignement…).


   .. _`syntaxe de formatage Python`:
      https://docs.python.org/2.7/library/string.html#format-specification-mini-language

Initialisation des séquences
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Dans le cas d'une reprise de séquence en cours (migration d'un autre système
vers autonomie sans remettre les compteurs à zéro), il est possible
d'initialiser les différentes séquences manuellement. Cela se passe également
depuis l'écran ``/admin/sales/numbering``.


Il convient d'initialiser les séquences avec **le dernier index déjà
utilisé**. Ex : si on initialise une séquence à *42*, le premier numéro
attribué par autonomie sera le *43*.

.. note::

   Les séquences par mois et par enseigne (``{SEQMONTHANA}``) font exception :
   elles ne disposent pas d'écran permettant de les initialiser,
   l'initialisation se fait directement en base, pour chaque activité : table
   ``company``, colonne ``month_company_sequence_init_value``.

Exemple : migration depuis WinScop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Configurer le gabarit de numéro de facture à
  ``FC{SEQYEAR:0>4}-{YY}{MM}{SEQMONTHANA:0>3}-{ANA}`` (interface d'admin)
- Initialiser la séquences ``SEQYEAR`` (interface d'admin)
- Initialiser pour chaque activité sa séquence mensuelle (en base)
- S'assurer que chaque activité a bien son code analytique renseigné (depuis
  l'annuaire des entreprises)


Migration des libellés d'écriture comptables
--------------------------------------------

Avec une logique similaire à celle des numéros de facture, il est possible
de paramétrer, pour chaque type d'écriture comptable, le libellé qui apparaitra
dans les exports CSV opérés depuis autonomie, et ainsi de conserver le même
format qu'avec l'ERP précédent. Ces paramètres se trouvent dans les différents
modules de configuration :

- *Module Notes de dépenses → Export comptable des notes de dépense*
- *Module Notes de dépenses → Export comptable des décaissements*
- *Module Ventes → Configuration comptable du module Vente → Configuration des informations générales et des modules prédéfinis*
- *Module Ventes → Configuration comptable du module Vente → Modules de contribution personnalisés*

 .. note:: Penser également à configurer la troncature des libellés en fonction
           du logiciel de compta utilisé dans *Module Comptabilité → Logiciel
           de comptabilité*

 .. note:: Pour migrer depuis WinScop, penser à utiliser une troncature du
           numéro de facture à 9 caractères (cf exemple sur les formulaire de
           configuration), les n° de facture WinScop étant assez longs.
