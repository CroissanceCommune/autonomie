Les services dans Autonomie
============================

Les services ont vocation à regrouper un ensemble cohérent de fonctionnalités.
Ils fournissent les avantages suivant :

1- Facile à tester;
2- En spécifiant les méthodes publiques via des interfaces, on peut avoir des
services différents en fonction des objets auxquels ils sont associés.

Plusieurs niveaux :

1- Les services branchés à l'aide de pyramid_services : configurables dans le
fichier .ini
2- Les services rattachés directement aux modèles


pyramid_services
-----------------

https://github.com/mmerickel/pyramid_services

Permet de rendre configurable les services utilisés.

On référence les services dans le fichier autonomie/__init__.py

.. code-block:: python

   AUTONOMIE_SERVICE_FACTORIES = (
      (
         "cle_dans_le_fichier_settings",
         "path_vers_l_instance_par_defaut_du_service",
         "interface_pour_le_service",
      ),
      ...
   )

Ensuite on utilise le service configuré

.. code-block:: python

   current_service = self.request.find_service(IInterfacePourMonService)
   # Si mon service spécifie ne méthode "process"
   current_service.process(datas)


Services rattachés aux modèles
-------------------------------

Les services rattachés aux modèles permettent de regrouper des méthodes sous
une même classe.

Un service peut être privé, comme les services rattachés au travers l'attribut
_autonomie_service, le modèle va alors forwarder certains appels au service en
question

Exemple dans autonomie/models/customer.py

.. code-block:: python

   class Customer(DBBASE):
      ...
      @property
      def full_address(self):
          """
          :returns: the customer address formatted in french format
          """
          return self._autonomie_service.get_address(self)


Un service peut être public dans ce cas il doit respecter une interface
déclarée dans autonomie/interfaces.py. Il sera appelé par du code extérieur au
modèle.

Exemple dans autonomie/events/files.py

.. code-block:: python

   def on_file_change(event):
       if hasattr(event.parent, "file_requirement_service"):
           event.parent.file_requirement_service.register(
               event.parent, event.file_object, action=event.action
           )
           if hasattr(event.parent, "status_service"):
               event.parent.status_service.update_status(
                   event.parent,
               )
