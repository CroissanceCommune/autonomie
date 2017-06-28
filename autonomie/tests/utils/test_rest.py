# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
from autonomie.utils.rest import (
    RestJsonRepr,
    RestError,
)


class DummyModel(dict):
    def appstruct(self):
        return self


class DummySchema:
    def serialize(self, datadict):
        return {'schemakey': datadict['schemakey']*2}

    def bind(self, **params):
        self.bind_params = params
        return self


class DummyJsonRepr(RestJsonRepr):
    schema = DummySchema()


def test_json():
    datas = DummyModel(schemakey=10, otherkey="dummy")
    jsonrepr = DummyJsonRepr(datas)
    assert(set(jsonrepr.__json__('request').keys())
           .difference(datas.keys()) == set([]))


def test_bind_params():
    jsonrepr = DummyJsonRepr({}, bind_params=dict(test=5))
    schema = jsonrepr.get_schema("request")
    assert(schema.bind_params.keys() == ['test'])
    jsonrepr = DummyJsonRepr({})
    schema = jsonrepr.get_schema("request")
    assert(schema.bind_params.keys() == ['request'])


def test_it(config):
    err = RestError({}, 151)
    assert(err.status == u"151 Continue")
    assert(err.content_type == 'application/json')


def test_script_utils():
    from autonomie.scripts.utils import get_value
    args = {'--test': 'toto', '--': 'titi'}
    assert get_value(args, 'test', '') == 'toto'
    assert get_value(args, 'test1', 'test') == 'test'
