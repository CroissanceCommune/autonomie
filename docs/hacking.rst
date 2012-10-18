Les gros hacks tout sales que l'on trouve dans Autonomie
========================================================

Gestion de la session Sqlalchemy dans les tests
-----------------------------------------------

Dans Autonomie, on utilise un session maker avec l'extension ZopeTransactionExtension.
L'extension permet de générer des sessions qui effectuent les commits vers la base Mysql et les rollbacks à chaque fin de requête (chaque transaction),
sans qu'on ait besoin de s'en soucier.

::

    DBSESSION = scoped_session(sessionmaker(extension=ZopeTransactionExtension()))

Dans le cadre des tests, on veut pouvoir manager les commits et les rollbacks (pour garder la même base d'un test à l'autre), on utilise donc un sessionmaker qui va binder avec une connection que l'on manage nous mêmes.
On écrase ainsi le session maker utilisé dans l'application avec celui utilisé pour nos tests

::

    cls.connection = cls.engine.connect()
    cls.DBSession = scoped_session(sessionmaker(bind=cls.connection))
    autonomie.models.DBSESSION = cls.DBSession

A la fin de chaque test, on revert les actions prévues (flusher ou commiter vers la bdd) pour avoir une bdd intacte pour la prochaine requête

::

    def setUp(self):
        self.trans = self.connection.begin()
        ...
    def tearDown(self):
        self.trans = self.trans.rollback()
        ...

.. note:: Compte tenu du fait que l'on utilise scoped_session pour wrapper le session maker, on est sûr que celui-ci nous renvoie une seule et même session au sein de chaque test.
