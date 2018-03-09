Les fixtures pytest permettent de fournir des variables facilement
intégrables dans les tests

si dans un fichier chargé pour les tests (idéalement un fichier
contest.py) on a :

.. code-block:: python

    import pytest

    @pytest.fixture
    def model(dbsession):
        item = Model(param1=param1, param2=param2)
        item = dbsession.add(item)
        dbsession.flush()
        return item


On peut alors utiliser cette fixture dans tous les tests en l'intégrant
comme paramètre dans la signature de la fonctione


.. code-block:: python

    def test_fonctionnalite(model):
        assert model.method() == resultat_attendu


La fixture nommée model la plus proche en terme d'arborescence du
fichier de test est utilisée.
