# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
import time
import pytest
from hashlib import md5
from autonomie.tests.tools import Dummy


@pytest.fixture
def settings():
    return {}


@pytest.fixture
def request(settings):
    registry = Dummy(settings=settings)
    req = Dummy(registry=registry, headers={})
    return req


def test_settings_has_value(request, settings):
    from autonomie.utils.predicates import SettingHasValuePredicate

    predicate = SettingHasValuePredicate(('key', True), None)
    assert predicate(None, request) is False
    predicate = SettingHasValuePredicate(('key', False), None)
    assert predicate(None, request) is True

    settings['key'] = "Test value"
    predicate = SettingHasValuePredicate(('key', True), None)
    assert predicate(None, request) is True
    predicate = SettingHasValuePredicate(('key', False), None)
    assert predicate(None, request) is False


def test_get_timestamp_from_request(request):
    from autonomie.utils.predicates import get_timestamp_from_request

    with pytest.raises(KeyError):
        get_timestamp_from_request(request)

    request.headers = {'timestamp': "124545.152"}
    assert get_timestamp_from_request(request) == "124545.152"

    request.headers = {'Timestamp': "124545.152"}
    assert get_timestamp_from_request(request) == "124545.152"


def test_check_timestamp():
    from autonomie.utils.predicates import check_timestamp
    assert check_timestamp(time.time(), tolerance=2)
    assert not check_timestamp(time.time() - 3, tolerance=2)


def test_get_clientsecret_from_request(request):
    from autonomie.utils.predicates import get_clientsecret_from_request

    with pytest.raises(KeyError):
        get_clientsecret_from_request(request)

    with pytest.raises(ValueError):
        request.headers = {'Authorization': "HMAC-OTHER secret"}
        get_clientsecret_from_request(request)

    with pytest.raises(KeyError):
        request.headers = {'Authorization': "nospacesecret"}
        get_clientsecret_from_request(request)

    request.headers = {'Authorization': "HMAC-MD5 secret"}
    assert get_clientsecret_from_request(request) == "secret"

    request.headers = {'authorization': "HMAC-MD5 secret"}
    assert get_clientsecret_from_request(request) == "secret"


def test_check_secret():
    from autonomie.utils.predicates import check_secret

    # In [8]: md5('123456-secret').hexdigest()
    # Out[8]: '06dda91136f6ad4688cdf6c8fd991696'
    assert check_secret("06dda91136f6ad4688cdf6c8fd991696", 123456, "secret")


def test_api_key_authentication(request, settings):
    from autonomie.utils.predicates import ApiKeyAuthenticationPredicate

    settings['key'] = 'secret'
    timestamp = request.headers['timestamp'] = time.time()
    request.headers['Authorization'] = "HMAC-MD5 " + \
        md5(u"%s-secret" % timestamp).hexdigest()

    api = ApiKeyAuthenticationPredicate('key', None)
    assert api(None, request)

    api = ApiKeyAuthenticationPredicate('wrongkey', None)
    assert not api(None, request)
