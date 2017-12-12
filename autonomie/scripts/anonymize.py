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
import itertools
import logging
import pkg_resources

from autonomie_base.models.base import DBSESSION
from autonomie.utils.image import build_header
from autonomie.scripts.utils import (
    get_value,
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
        self.counter = itertools.count()

    def _zipcode(self):
        if hasattr(self.faker, 'zipcode'):
            return self.faker.zipcode()
        else:
            return self.faker.postcode()

    def _an_activity(self):
        from autonomie.models.activity import Activity, ActivityType
        for activity in self.session.query(Activity):
            for fieldname in (
                'point',
                'objectifs',
                'action',
                'documents',
                'notes'
            ):
                setattr(activity, fieldname, self.faker.text())

        type_labels = (
            u"RV conseil",
            u"RV suivi",
            u"RV Gestion",
            u"RV Admin",
            u"RV RH",
            u"RV Compta",
            u"RV hebdo",
            u"RV Mensuel",
        )

        for index, typ in enumerate(self.session.query(ActivityType).all()):
            typ.label = type_labels[index % 7]

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
            header = build_header(
                u"{0}\n {1} - {2}".format(comp.name, comp.phone, comp.email)
            )
            comp.header = {'name': 'header.png', 'data': header}

    def _an_competence(self):
        from autonomie.models.competence import (
            CompetenceGridItem,
            CompetenceGridSubItem,
        )
        for item in self.session.query(CompetenceGridItem):
            item.progress = self.faker.text()
        for item in self.session.query(CompetenceGridSubItem):
            item.comments = self.faker.text()

    def _an_config(self):
        from autonomie.models.config import Config, ConfigFiles

        Config.set('cae_admin_mail', self.faker.ascii_safe_email())
        Config.set('welcome', self.faker.sentence(nb_words=15))
        ConfigFiles.set(
            'logo.png',
            {
                'data': pkg_resources.resource_stream(
                    'autonomie',
                    'static/img/autonomie.jpg'
                ),
                'filename': 'logo.jpg',
            }
        )
        Config.set('coop_cgv', self.faker.paragraph(nb_sentences=40))
        Config.set('coop_pdffootertitle', u"""Une activité de ma CAE SARL SCOP à \
capital variable""")
        Config.set('coop_pdffootercourse', u"""Organisme de formation N° de déclaration \
d'activité au titre de la FPC : xx xx xxxxx. MA CAE est exonérée de TVA pour \
les activités s'inscrivant dans le cadre de la formation professionnelle \
conformément à l'art. L920-4 du Code du travail et de l'art. 202 C de \
l'annexe II du code général des impôts""")
        footer = u"""RCS XXXX 000 000 000 00000 - SIRET 000 \
000 000 000 00 - Code naf 0000Z TVA INTRACOM : FR0000000. Siège social : 10 \
rue vieille 23200 Aubusson"""
        Config.set('coop_pdffootercontent', footer)
        Config.set('coop_invoicepayment', u"""Par chèque libellé à l'ordre de : \
MA CAE/ %ENTREPRENEUR%
à envoyer à l'adresse suivante :
MA CAE/ %ENTREPRENEUR%
10 rue Vieille
23200 Aubusson

Ou par virement sur le compte de MA CAE/ %ENTREPRENEUR%
MA BANQUE
RIB : xxxxx xxxx xxxxxxxxxxxxx
IBAN : xxxx xxxx xxxx xxxx xxxx xxxx xxx
BIC : MABAFRMACAXX
Merci d'indiquer le numéro de facture sur le libellé de votre virement ou \
dos de votre chèque.
""")
        Config.set("coop_invoicelate", u"""Tout retard de paiement entraînera à titre de \
clause pénale, conformément à la loi 92.1442 du 31 décembre 1992, une \
pénalité égale à un taux d'intérêt équivalent à une fois et demi le taux \
d'intérêt légal en vigueur à cette échéance.
Une indemnité de 40 euros forfaitaire sera demandée en sus pour chaque \
facture payée après l’échéance fixée. Celle-ci n’est pas soumise à TVA.""")

        Config.set("activity_footer", footer)

        Config.set('workshop_footer', footer)

    def _an_customer(self):
        from autonomie.models.customer import Customer
        for cust in self.session.query(Customer):
            cust.name = self.faker.company()
            cust.address = self.faker.street_address()
            cust.zipcode = self._zipcode()
            cust.city = self.faker.city()
            cust.lastname = self.faker.last_name()
            cust.firstname = self.faker.first_name()
            cust.email = self.faker.ascii_safe_email()
            cust.phone = self.faker.phone_number()
            cust.fax = self.faker.phone_number()
            cust.tva_intracomm = ""
            cust.comments = self.faker.bs()

    def _an_expense(self):
        from autonomie.models.expense.sheet import (
            BaseExpenseLine,
            ExpenseKmLine,
            Communication,
        )
        for line in self.session.query(BaseExpenseLine):
            line.description = self.faker.text()
        for line in self.session.query(ExpenseKmLine):
            line.start = self.faker.city()
            line.end = self.faker.city()

        for com in self.session.query(Communication):
            com.content = self.faker.text()

    def _an_node(self):
        from autonomie.models.node import Node
        for node in self.session.query(Node):
            node.name = self.faker.sentence(nb_words=4, variable_nb_words=True)

    def _an_payment(self):
        from autonomie.models.payments import BankAccount
        for b in self.session.query(BankAccount):
            b.label = u"Banque : {0}".format(self.faker.company())

    def _an_project(self):
        from autonomie.models.project import Project, Phase
        for p in self.session.query(Project):
            p.definition = self.faker.text()

        for p in self.session.query(Phase):
            if p.name != u"Phase par défaut":
                p.name = self.faker.sentence(nb_words=3)

    def _an_sale_product(self):
        from autonomie.models.sale_product import (
            SaleProductCategory,
            SaleProduct,
            SaleProductGroup,
        )
        for cat in self.session.query(SaleProductCategory):
            cat.title = self.faker.sentence(nb_words=3)
            cat.description = self.faker.text()

        for prod in self.session.query(SaleProduct):
            prod.label = self.faker.sentence(nb_words=2)
            prod.description = self.faker.text()

        for group in self.session.query(SaleProductGroup):
            group.title = self.faker.sentence(nb_words=2)
            group.description = self.faker.text()

    def _an_statistic(self):
        from autonomie.models.statistics import (
            StatisticSheet
        )
        for s in self.session.query(StatisticSheet):
            s.title = self.faker.sentence(nb_words=4)

    def _an_task(self):
        from autonomie.models.task import (
            Task,
            DiscountLine,
            TaskLine,
            TaskLineGroup,
            Estimation,
            TaskStatus,
        )
        for task in self.session.query(Task):
            if task.status_comment:
                task.status_comment = self.faker.text()
            task.description = self.faker.text()
            task.address = task.customer.full_address
            task.workplace = self.faker.address()
        for line in self.session.query(DiscountLine):
            line.description = self.faker.text()

        for line in self.session.query(TaskLine):
            line.description = self.faker.text()

        for group in self.session.query(TaskLineGroup):
            if group.title:
                group.title = self.faker.sentence(nb_words=4)
            if group.description:
                group.description = self.faker.text()

        for status in self.session.query(TaskStatus):
            status.status_comment = self.faker.sentence(nb_words=6)

        for estimation in self.session.query(Estimation):
            if estimation.exclusions:
                estimation.exclusions = self.faker.text()

    def _an_user(self):
        from autonomie.models.user import (
            User,
            UserDatas,
            CompanyDatas,
            AntenneOption,
        )
        for u in self.session.query(User).filter_by(active=True):
            index = self.counter.next()
            if index == 1:
                u.login = u"admin1"
                u.groups = 'admin'

            elif index == 2:
                u.login = u"manager1"
                u.groups = "manager"

            elif index == 3:
                u.login = u"entrepreneur1"
                u.groups = u"contractor"

            u.lastname = self.faker.last_name()
            u.firstname = self.faker.first_name()
            u.email = self.faker.ascii_safe_email()
            u.set_password(u.login)
            if u.has_userdatas():
                u.userdatas.coordonnees_lastname = u.lastname
                u.userdatas.coordonnees_firstname = u.firstname
                u.userdatas.coordonnees_email1 = u.email

        for u in self.session.query(User).filter_by(active=False):
            index = self.counter.next()
            u.login = u"utilisateur_{0}".format(index)
            u.lastname = self.faker.last_name()
            u.firstname = self.faker.first_name()
            u.email = self.faker.ascii_safe_email()
            u.set_password(u.login)
            if u.has_userdatas():
                u.userdatas.coordonnees_lastname = u.lastname
                u.userdatas.coordonnees_firstname = u.firstname
                u.userdatas.coordonnees_email1 = u.email

        for u in self.session.query(UserDatas):
            if u.user_id is None:
                u.coordonnees_lastname = self.faker.last_name()
                u.coordonnees_firstname = self.faker.first_name()
                u.coordonnees_email1 = self.faker.ascii_safe_email()
            u.coordonnees_ladies_lastname = self.faker.last_name_female()
            u.coordonnees_email2 = self.faker.ascii_safe_email()
            u.coordonnees_tel = self.faker.phone_number()
            u.coordonnees_mobile = self.faker.phone_number()
            u.coordonnees_address = self.faker.street_address()
            u.coordonnees_zipcode = self._zipcode()
            u.coordonnees_city = self.faker.city()
            u.coordonnees_birthplace = self.faker.city()
            u.coordonnees_birthplace_zipcode = self._zipcode()
            u.coordonnees_secu = u"0 00 00 000 000 00"
            u.coordonnees_emergency_name = self.faker.name()
            u.coordonnees_emergency_phone = self.faker.phone_number()
            u.parcours_goals = self.faker.text()
        for datas in self.session.query(CompanyDatas):
            datas.title = self.faker.company()
            datas.name = self.faker.company()
            datas.website = self.faker.url()

        for a in AntenneOption.query():
            a.label = u"Antenne : {0}".format(self.faker.city())

    def run(self, module_key=None):
        if module_key is not None:
            if not module_key.startswith('_an_'):
                module_key = u"_an_%s" % module_key
            keys = [module_key]
            methods = {module_key: getattr(self, module_key)}
        else:
            methods = {}
            for method_name, method in inspect.getmembers(
                self,
                inspect.ismethod
            ):
                if method_name.startswith('_an_'):
                    methods[method_name] = method
            keys = methods.keys()
            keys.sort()
        for key in keys:
            print(key)
            methods[key]()


def anonymize_database(args, env):
    logger = logging.getLogger(__name__)
    method = get_value(args, "method", None)
    manager = Anonymizer(logger)
    manager.run(method)
