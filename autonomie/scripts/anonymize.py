# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
"""
Script used to anonymize the content of the current database (
remove names,
customer personnal infos,
personnal datas ...)
"""
import inspect
import logging

from autonomie_base.models.base import DBSESSION
from autonomie.scripts.utils import (
    command,
)


try:
    from faker import Faker
except ImportError:
    raise Exception(
        u"You should install faker nefore being able to anonymize "
        u"datas : "
        u"pip install faker"
    )


class Anonymizer(object):
    def __init__(self, logger):
        self.us_faker = Faker()
        self.faker = Faker('fr_FR')
        self.logger = logger
        self.session = DBSESSION()
        self.count = 1

    def _an_activity(self):
        from autonomie.models.activity import Activity
        for activity in self.session.query(Activity):
            for fieldname in (
                'point',
                'objectifs',
                'action',
                'documents',
                'notes'
            ):
                setattr(activity, fieldname, self.faker.text())

    def _an_commercial(self):
        from autonomie.models.commercial import TurnoverProjection
        for t in self.session.query(TurnoverProjection):
            t.comment = self.faker.text()

    def _an_company(self):
        from autonomie.models.company import Company
        for comp in self.session.query(Company):
            comp.name = self.faker.company()
            comp.goal = self.faker.bs()
            comp.comments = self.faker.catch_phrase()
            comp.phone = self.faker.phone_number()
            comp.mobile = self.faker.phone_number()
            comp.email = self.faker.ascii_safe_email()

    def _an_customer(self):
        from autonomie.models.customer import Customer
        for cust in self.session.query(Customer):
            cust.name = self.faker.company()
            cust.address = self.faker.street_address()
            if hasattr(self.faker, 'zipcode'):
                cust.zipcode = self.faker.zipcode()
            else:
                cust.zipcode = self.faker.postcode()
            cust.city = self.faker.city()
            cust.lastname = self.faker.last_name()
            cust.firstname = self.faker.first_name()
            cust.email = self.faker.ascii_safe_email()
            cust.phone = self.faker.phone_number()
            cust.fax = self.faker.phone_number()
            cust.tva_intracomm = ""
            cust.comments = self.faker.bs()

    def run(self):
        for method_name, method in inspect.getmembers(self, inspect.ismethod):
            if method_name.startswith('_an_'):
                method()


def anonymize_database(args, env):
    logger = logging.getLogger(__name__)
    manager = Anonymizer(logger)
    manager.run()


def autonomie_sample_datas_cmd():
    """Autonomie datas manipulation tool (fake datas, anonymization ...)
    Usage:
        autonomie-sample-datas <config_uri> anonymize

    o anonymize : Anonymize datas
    """
    def callback(arguments, env):
        if arguments['anonymize']:
            func = anonymize_database
        return func(arguments, env)
    try:
        return command(callback, autonomie_sample_datas_cmd.__doc__)
    finally:
        pass
