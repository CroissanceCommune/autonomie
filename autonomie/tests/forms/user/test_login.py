# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import pytest


def test_password_change_schema(login, pyramid_request):
    import colander
    from autonomie.forms.user.login import get_password_schema

    schema = get_password_schema()
    pyramid_request.context = login

    schema = schema.bind(request=pyramid_request)

    result = schema.deserialize(
        {'password': 'pwd', 'pwd_hash': u"New pass"}
    )

    assert result['pwd_hash'] == u'New pass'

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {'password': 'ooo', 'pwd_hash': u"New pass"}
        )


def test_add_schema(dbsession, pyramid_request, login, groups):
    import colander
    from autonomie.forms.user.login import get_add_edit_schema

    schema = get_add_edit_schema()
    schema = schema.bind(request=pyramid_request)
    result = schema.deserialize(
        {
            'login': 'test2',
            'pwd_hash': 'oo',
            'primary_group': 'contractor',
            'groups': ['trainer'],
            'user_id': 3
        }
    )

    assert 'pwd_hash' in result

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'test2',
                'pwd_hash': '',
                'primary_group': 'contractor',
                'groups': ['trainer'],
                'user_id': 3
            }
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'login',
                'pwd_hash': 'ooo',
                'primary_group': 'contractor',
                'groups': ['trainer'],
                'user_id': 3
            }
        )
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'test2',
                'pwd_hash': 'ooo',
                'primary_group': '',
                'groups': ['trainer'],
                'user_id': 3
            }
        )


def test_edit_schema_login_context(
    dbsession, pyramid_request, login, user, groups
):
    import colander
    from autonomie.forms.user.login import get_add_edit_schema
    from autonomie.models.user.login import Login
    from autonomie.models.user.user import User

    user2 = User(email='a@a.fr', lastname='lastname2', firstname='firstname2')
    dbsession.add(user2)
    dbsession.flush()

    item = Login(user_id=user2.id, login="test2")
    item.set_password('pwd2')
    dbsession.add(item)
    dbsession.flush()

    pyramid_request.context = item

    schema = get_add_edit_schema(edit=True)
    schema = schema.bind(request=pyramid_request)
    result = schema.deserialize(
        {
            'login': 'test2',
            'pwd_hash': '',
            'primary_group': "manager",
                'groups': ['trainer'],
            'user_id': user2.id,
        }
    )

    assert 'pwd_hash' not in result

    result = schema.deserialize(
        {
            'login': 'test2',
            'pwd_hash': 'notpwd2',
            'primary_group': "manager",
            'groups': ['trainer'],
            'user_id': user2.id,
        }
    )

    assert 'pwd_hash' in result

    # Login already used
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'login',
                'pwd_hash': '',
                'primary_group': "manager",
                'groups': ['trainer'],
                'user_id': user2.id,
            }
        )

    # User already linked to Login class
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'test2',
                'pwd_hash': 'ooo',
                'primary_group': "manager",
                'groups': ['trainer'],
                'user_id': user.id
            }
        )

    # wrong primary group
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'test2',
                'pwd_hash': 'ooo',
                "primary_group": "falseone",
                'groups': ['trainer'],
                'user_id': user2.id,
            }
        )
    # wrong group
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'test2',
                'pwd_hash': 'ooo',
                "primary_group": "contractor",
                'user_id': user2.id,
                "groups": ["falseone"],
            }
        )


def test_edit_schema_user_context(
    dbsession, pyramid_request, login, user, groups
):
    import colander
    from autonomie.forms.user.login import get_add_edit_schema
    from autonomie.models.user.login import Login
    from autonomie.models.user.user import User

    user2 = User(email='a@a.fr', lastname='lastname2', firstname='firstname2')
    dbsession.add(user2)
    dbsession.flush()

    item = Login(user_id=user2.id, login="test2")
    item.set_password('pwd2')
    dbsession.add(item)
    dbsession.flush()

    pyramid_request.context = user2

    schema = get_add_edit_schema(edit=True)
    schema = schema.bind(request=pyramid_request)
    result = schema.deserialize(
        {
            'login': 'test2',
            'pwd_hash': '',
            "primary_group": "contractor",
            'groups': ['trainer'],
            'user_id': user2.id,
        }
    )

    assert 'pwd_hash' not in result

    result = schema.deserialize(
        {
            'login': 'test2',
            'pwd_hash': 'notpwd2',
            "primary_group": "contractor",
            'groups': ['trainer'],
            'user_id': user2.id,
        }
    )

    assert 'pwd_hash' in result

    # Login already used
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': login.login,
                'pwd_hash': '',
                "primary_group": "contractor",
                'user_id': user2.id,
                'groups': ['trainer'],
            }
        )

    # User already linked to Login class
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'test2',
                'pwd_hash': '',
                "primary_group": "contractor",
                'user_id': user.id
            }
        )

    # wrong group
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'test2',
                'pwd_hash': '',
                'primary_group': 'unknown group',
                'groups': ['trainer'],
                'user_id': user2.id,
            }
        )

    # wrong group
    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {
                'login': 'test2',
                'pwd_hash': '',
                "primary_group": "contractor",
                'groups': ['unknown group'],
                'user_id': user2.id,
            }
        )


def test_auth_schema(dbsession, login):
    import colander
    from autonomie.forms.user.login import get_auth_schema

    schema = get_auth_schema()
    result = schema.deserialize(
        {'login': login.login, 'password': u'pwd'}
    )
    assert 'password' in result

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {'login': u'nottest', 'password': u'pwd'}
        )

    with pytest.raises(colander.Invalid):
        schema.deserialize(
            {'login': u'login', 'password': u'notpwd'}
        )
