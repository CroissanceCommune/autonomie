# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
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
    from pyramid.httpexceptions import HTTPFound
    assert isinstance(result, HTTPFound)


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
