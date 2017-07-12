# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import datetime
import pytest


def test_status_change_view_invalid_error(
    config, get_csrf_request_with_db, estimation, user
):
    config.add_route('project', '/{id}')
    from autonomie.utils.rest import RestError
    from autonomie.views.estimations.rest_api import EstimationStatusView

    request = get_csrf_request_with_db(
        post={'submit': 'valid'}
    )
    request.context = estimation
    request.user = user
    request.is_xhr = True

    view = EstimationStatusView(request)

    with pytest.raises(RestError) as invalid_exc:
        view.__call__()
        assert invalid_exc.code == 400
    assert estimation.status == 'draft'


def test_status_change_view_forbidden_error(
    config, get_csrf_request_with_db, full_estimation, user
):
    config.add_route('project', '/{id}')
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=False
    )
    from autonomie.utils.rest import RestError
    from autonomie.views.estimations.rest_api import EstimationStatusView

    request = get_csrf_request_with_db(
        post={'submit': 'valid'}
    )
    request.context = full_estimation
    request.user = user
    request.is_xhr = True

    view = EstimationStatusView(request)

    with pytest.raises(RestError) as forbidden_exc:
        view.__call__()
        assert forbidden_exc.code == 403
    assert full_estimation.status == 'draft'


def test_status_change_view(
    config, get_csrf_request_with_db, full_estimation, user
):
    config.add_route('project', '/{id}')
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import EstimationStatusView

    request = get_csrf_request_with_db(
        post={'submit': 'valid'}
    )
    request.context = full_estimation
    request.user = user
    request.is_xhr = True

    view = EstimationStatusView(request)
    result = view.__call__()
    assert result == {'redirect': '/%s' % full_estimation.project_id}
    assert full_estimation.status == 'valid'


def test_signed_status_change_wrong(
    config, get_csrf_request_with_db, full_estimation, user
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.utils.rest import RestError
    from autonomie.views.estimations.rest_api import EstimationSignedStatusView

    request = get_csrf_request_with_db(
        post={'submit': 'wrong'}
    )
    request.context = full_estimation
    request.user = user
    request.is_xhr = True

    view = EstimationSignedStatusView(request)
    with pytest.raises(RestError) as invalid_exc:
        view.__call__()
        assert invalid_exc.code == 400


def test_signed_status_change_forbidden(
    config, get_csrf_request_with_db, full_estimation, user
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=False
    )
    from autonomie.utils.rest import RestError
    from autonomie.views.estimations.rest_api import EstimationSignedStatusView

    request = get_csrf_request_with_db(
        post={'submit': 'signed'}
    )
    request.context = full_estimation
    request.user = user
    request.is_xhr = True

    view = EstimationSignedStatusView(request)
    with pytest.raises(RestError) as forbidden_exc:
        view.__call__()
        assert forbidden_exc.code == 403


def test_signed_status_change(
    config, get_csrf_request_with_db, full_estimation, user
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import EstimationSignedStatusView

    request = get_csrf_request_with_db(
        post={'submit': 'aborted'}
    )
    request.context = full_estimation
    request.user = user
    request.is_xhr = True

    view = EstimationSignedStatusView(request)
    result = view.__call__()
    assert result['datas'] == {'signed_status': 'aborted'}


def test_add_task_group(
    dbsession, config, get_csrf_request_with_db, full_estimation, user
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import TaskLineGroupRestView

    request = get_csrf_request_with_db(
        post={'title': u"Title", 'description': u"Description"}
    )
    request.context = full_estimation
    request.user = user
    request.is_xhr = True

    view = TaskLineGroupRestView(request)
    result = view.post()
    assert result.task_id == full_estimation.id
    assert result.title == u"Title"
    assert result.description == u"Description"


def test_edit_task_group(
    dbsession, config, get_csrf_request_with_db, user,
    task_line_group
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import TaskLineGroupRestView

    request = get_csrf_request_with_db(
        post={'title': u"New Title"}
    )
    request.context = task_line_group
    request.user = user
    request.is_xhr = True

    view = TaskLineGroupRestView(request)
    result = view.put()
    assert result.title == u"New Title"
    assert result.description == u"Group description"


def test_add_task_line(
    dbsession, config, get_csrf_request_with_db, task_line_group, user,
    unity, tva
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import TaskLineRestView

    request = get_csrf_request_with_db(
        post={
            'description': u"Description",
            "cost": "150.12345",
            "tva": str(tva.value / 100),
            "quantity": 2,
            "unity": unity.label
        }
    )
    request.context = task_line_group
    request.user = user
    request.is_xhr = True

    view = TaskLineRestView(request)
    result = view.post()
    assert result.group_id == task_line_group.id
    assert result.description == u"Description"
    assert result.cost == 15012345
    assert result.tva == tva.value
    assert result.quantity == 2
    assert result.unity == unity.label

    # test invalid entry
    from autonomie.utils.rest import RestError
    request = get_csrf_request_with_db(
        post={
            'description': u"Description",
            "tva": str(tva.value / 100),
            "quantity": 2,
        }
    )
    request.context = task_line_group
    request.user = user
    request.is_xhr = True

    view = TaskLineRestView(request)

    with pytest.raises(RestError):
        view.post()


def test_edit_task_line(
    dbsession, config, get_csrf_request_with_db, user, task_line,
    unity, product,
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import TaskLineRestView

    request = get_csrf_request_with_db(
        post={'cost': "160"}
    )
    request.context = task_line
    request.user = user
    request.is_xhr = True

    view = TaskLineRestView(request)
    result = view.put()
    assert result.cost == 16000000
    assert result.description == u"Task Line description"
    assert result.quantity == 1
    assert result.unity == unity.label
    assert result.product_id == product.id


def test_add_discount_line(
    dbsession, config, get_csrf_request_with_db, full_estimation, user,
    unity, tva
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import DiscountLineRestView

    request = get_csrf_request_with_db(
        post={
            'description': u"Description",
            "amount": "150.12345",
            "tva": str(tva.value / 100),
        }
    )
    request.context = full_estimation
    request.user = user
    request.is_xhr = True

    view = DiscountLineRestView(request)
    result = view.post()
    assert result.task_id == full_estimation.id
    assert result.description == u"Description"
    assert result.amount == 15012345
    assert result.tva == tva.value


def test_edit_discount_line(
    dbsession, config, get_csrf_request_with_db, user, discount_line,
    unity, product,
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import DiscountLineRestView

    request = get_csrf_request_with_db(
        post={'amount': "160"}
    )
    request.context = discount_line
    request.user = user
    request.is_xhr = True

    view = DiscountLineRestView(request)
    result = view.put()
    assert result.amount == 16000000
    assert result.description == u"Discount"


def test_add_payment_line(
    dbsession, config, get_csrf_request_with_db, full_estimation, user,
    unity, tva
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import PaymentLineRestView

    request = get_csrf_request_with_db(
        post={
            'description': u"Description",
            "amount": "150.12345",
            "date": "2017-06-01",
        }
    )
    request.context = full_estimation
    request.user = user
    request.is_xhr = True

    view = PaymentLineRestView(request)
    result = view.post()
    assert result.task_id == full_estimation.id
    assert result.description == u"Description"
    assert result.amount == 15012345
    assert result.date == datetime.date(2017, 06, 01)


def test_edit_payment_line(
    dbsession, config, get_csrf_request_with_db, user, payment_line,
    unity, product,
):
    config.testing_securitypolicy(
        userid="test",
        groupids=('admin',),
        permissive=True
    )
    from autonomie.views.estimations.rest_api import PaymentLineRestView

    request = get_csrf_request_with_db(
        post={'amount': "160"}
    )
    request.context = payment_line
    request.user = user
    request.is_xhr = True

    view = PaymentLineRestView(request)
    result = view.put()
    assert result.amount == 16000000
    assert result.description == "Payment Line"
