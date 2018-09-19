SQLAlchemy
==========

Requête et optimisation des chargements
------------------------------------------

Filtrage sur une relation
...........................

Pour filtrer sur les relations d'un objet on va utiliser

    - join ou outerjoin (selon le type de relation)
    - filter()

ManyToOne relationship

.. code-block:: python

   >>> query = db().query(Project).outerjoin(Project.company).filter(Company.name.like('%a%'))

OneToMany relationship

.. code-block:: python

   >>> query = db().query(Project).outerjoin(Project.customers).filter(Project.customers.any(Customer.name.like('%a%')))


Optimisation du chargement
...........................

Pour optimiser le chargement de données, on va utiliser load_only, qui va
permettre de limiter les colonnes à requérir :

.. code-block:: python

   >>> from sqlalchemy.orm import load_only
   >>> query = Project.query().options(load_only('id', 'name'))


Note : Pour les relations les join ne chargent pas de données. Lorsque l'on va accéder à project.customers[0].name, on va faire une nouvelle requête sur la table customer.


Donc pour faire la même chose sur des relations que l'on charge simultanément, on va utiliser

   - selectinload
   - load_only

.. code-block:: python


   >>> query = db().query(Project).options(selectinload(Project.customers).load_only('id', 'label'))

Si on veut cumuler le filtrage et le chargement des informations, on utilisera la requête suivante.

.. code-block:: python

   >>> query = db().query(Project).options(selectinload(Project.customers).load_only('id', 'label')).outerjoin(Project.customers).filter(Customer.name.like('%a%'))
