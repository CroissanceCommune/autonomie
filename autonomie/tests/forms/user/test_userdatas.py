# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


def test_add_edit_schema(content, dbsession, pyramid_request):
    import colander
    from autonomie.forms.user.userdatas import get_add_edit_schema
    schema = get_add_edit_schema()
    schema.bind(request=pyramid_request)

    result = schema.deserialize(
        {
            'situation_situation_id': 1,
            'coordonnees_firstname': u"firstname",
            "coordonnees_lastname": u"lastname",
            "coordonnees_email1": u"email1@email.fr",
        }
    )
    assert 'coordonnees_firstname' in result

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'situation_situation_id': 1,
                'coordonnees_firstname': u"firstname",
                'coordonnees_lastname': u"lastname",
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'situation_situation_id': 1,
                'coordonnees_lastname': u"lastname",
                "coordonnees_email1": u"email1@email.fr",
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'situation_situation_id': 1,
                'coordonnees_firstname': u"firstname",
                "coordonnees_email1": u"email1@email.fr",
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'coordonnees_firstname': u"firstname",
                'coordonnees_lastname': u"lastname",
                "coordonnees_email1": u"email1@email.fr",
            }
        )
