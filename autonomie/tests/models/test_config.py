# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
def test_load_value(dbsession):
    from autonomie.models.config import get_config, Config
    dbsession.add(Config(name="name", value="value"))
    dbsession.flush()
    all_ = get_config()
    assert "name" in all_.keys()
    assert all_["name"] == "value"
