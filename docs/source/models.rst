Technique spécifique utilisées pour les modèles
===============================================

Polymorphisme
-------------

Le polymorphisme permet de fournir une structure d'héritage à nos modèles.

Duplication
...........

Le polymorphisme permet de factoriser les déclarations d'attributs. La classe Node (et la table sql correspondante) stocke par exemple la date de création.

Requêtes
.........

Grâce au polymorphisme, on peut effectuer des requêtes sur plusieurs modèles simultanément ::

.. code-block:: python

    Node.query().with_polymorphism([Invoice, File, Activity]).filter(Node.name=='Nom que l'on cherche')

Cette requête va permettre de requêter (et donc de trier/filtrer) tous les noeuds de type Invoice, File, Activity.

Relations
.........

Grâce à cette technique d'héritage, on peut configurer des relations moins typées.

Par exemple, les fichiers peuvent être lié à des projets, des devis, des factures et des avoirs, mais ce sont des modèles différents.
Compte tenu qu'ils héritent tous de Node, on a configuré une relation générique de Node à Node, qui nous permet de lier les Nodes entre eux, indifféremment de leur type.
On peut donc lier un fichier à un projet, mais on pourrait, grâce à cette même relation, attacher un fichier à une activité.

Implémentation
..............

Aujourd'hui, plusieurs arbres polymorphiques sont implémentés dans Autonomie, celui-ci est le prinicipal :

                                                       Node

                                  /                     |                 \
                                 /                      |                  \
                                /                       |                   \
                             Task                       File                Event
                         /    |     \                                           \
                Estimation  Invoice  CancelInvoice                              Activity

Autres implémentations:

* Les types de frais (BaseExpenseType, ExpenseType, ExpenseTelType, ExpenseKmType)
* Les frais (BaseExpenseLine, ExpenseLine, ExpenseTelLine, ExpenseKmLine)

