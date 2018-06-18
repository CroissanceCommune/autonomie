Guide de migration
==================

Ce document reprend des éléments aidant à la réalisation de migrations de
données depuis un autre système, par exemple depuis WinScop.

Numéros de facture
------------------

Par défaut (sur les nouvelles installations), les factures sont numérotés avec
une séquence chronologique globale, non liée ni à une année, ni à une activité,
et sans préfixe (1, 2, 3…).

Schéma de n° de facture
^^^^^^^^^^^^^^^^^^^^^^^

Il est possible de configurer l'usage de séquences plus complexes, pour
s'adapter au schéma de numérotation existant ou décidé au sein de la CAE. La
liste des variables et séquences disponibles et leur configuration se passe
depuis l'écran ``/admin/sales/numbering``.

.. note::

   Le format de n° de facture utilise la `syntaxe de formatage Python`_, il est
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

   Les séquences par mois et par activité (``{SEQMONTHANA}``) font exception :
   elles ne disposent pas d'écran permettant de les initialiser,
   l'initialisation se fait directement en base, pour chaque activité : table
   ``company``, colonne ``month_company_sequence_init_value``.

Exemple : migration depuis WinScop
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

- Configurer le format de numéro de facture à
  ``FC{SEQYEAR:0>4}-{YY}{MM}{SEQMONTHANA:0>3}-{ANA}`` (interface d'admin)
- Initialiser la séquences ``SEQYEAR`` (interface d'admin)
- Initialiser pour chaque activité sa séquence mensuelle (en base)
- S'assurer que chaque activité a bien son code analytique renseigné (depuis
  l'annuaire des entreprises)
