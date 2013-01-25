Les documents
=============

Modèles
-------

Le modèle Task est le modèle de document de base.
Les autres modèles dérivent de celui-ci excepté les ManualInvoice
qui sont un héritage du hack symfony (gestion.).

Un polymorphisme est utilisé pour différencier les différentes Task, celui-ci
est fait par le biais de la colonne type_.

Ainsi on obtient les correspondances suivantes:

* type_=task correspond à un document de base
* type_=invoice correspond à une facture (Invoice)
* type_=cancelinvoice correspond à un avoir (CancelInvoice)
* type_=estimation correspond à un devis (Estimation)

Il est ainsi possible d'effectuer des requêtes sur l'ensemble des devis et
des factures grâce à la méthode with_polymorphic

.. code-block:: python

    Task.query()\
         .with_polymorphic([Invoice, CancelInvoice, Estimation])\
         .join(Task.phase)\
         .filter(and_(Task.CAEStatus == 'wait', Phase.name is not None))\
         .order_by(Task.statusDate).all()

Les statuts
-----------

Les statuts des documents sont stockés dans la colonne CAEStatus du modèle Task.
Un validateur Sqlalchemy permet de prévenir les modifications non autorisées
de statut.

Workflow
........

Une machine à état permet de gérer le workflow des documents.

Un état
~~~~~~~

Le workflow est composé d'état qui sont :

* un nom
* une permission (optionnelle)
* une fonction de callback (optionnelle)

un booléen indique si c'est état doivent être inscrit dans la base de données
comme statut de document.

La fonction de callback prend le document et le user_id comme argument et
d'éventuels arguments optionnels passés comme keyword dict.

L'objet State:

.. code-block:: python

    def change_nutts(task, user_id, dest):
        print "User %s will change task : %s from nutts to %s" % (user_id,
                                                                  task.name,
                                                                       dest)
        return task

    state = State('name', 'edit', change_nutts, True)
    if state.is_allowed(task, request):
        task = state.process(task, user_id, dest='Nutella°')

La machine à état
~~~~~~~~~~~~~~~~~

La machine à état éxécute les changements d'état et gère l'ensemble des droits:

.. code-block:: python

    statedict = {'statename0':((statename1, permission, callback, cae_state_boolean),
                                (statename2,)),
                 'statename1':.....}
    state_machine = TaskState(default_statename, statedict)
    ret_datas = state_machine.process(task_obj, request, user_id, new_state)


