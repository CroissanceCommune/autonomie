# -*-coding:utf-8-*-
"""
Main classes for statistics computation
Allows to generate and combine queries

1- Build SQLAlchemy query objects
2- Combine the result of multiple query objects to merge them python-side (this
way we avoid conflict in group/having/join clauses)

Stats are composed of
Sheets which contains Entries which are composed with Criteria

For each entry, we build a main EntryQueryFactory, which contains a query_object
that is the root of our query tree

To be able to build queries

On doit pouvoir générer des query :
    1-
    db().query(
        distinct(models.user.UserDatas.id)
    ).filter(
        models.user.UserDatas.coordonnees_lastname.startswith('tje')
    ).count()

    2- Des relations M2o
    Les objets remotes existent déjà, c'est forcément par l'id qu'on match

    db().query(
        distinct(models.user.UserDatas.id)
    ).filter(
        models.user.UserDatas.parcours_status_id.in_((1,2,3))
    ).count()

    3- Des relations o2M
    On doit passer par les attributs des objets remotes pour filtrer
    filtre sur un attribut cible :

    db().query(
        distinct(models.user.UserDatas.id)
    ).outerjoin(
        models.user.UserDatas.parcours_date_diagnostic
    ).filter(
        models.user.DateDiagnosticDatas.date<datetime.datetime.now()
    ).count()


    filtre sur deux attributs cibles :

    db().query(
        distinct(models.user.UserDatas.id), models.user.UserDatas
        ).outerjoin(
        models.user.UserDatas.statut_external_activity
        ).filter(
        models.user.ExternalActivityDatas.brut_salary>100
        ).filter(models.user.ExternalActivityDatas.hours<8).count()

TODO :
    In [3]: query = db().query(UserDatas.id).outerjoin(UserDatas.parcours_convention_cape)

    In [4]: query = query.group_by(UserDatas.id)

    In [5]: query = query.having(func.max(DateConventionCAPEDatas.date) > datetime.date.today())

    In [6]: query.count()
"""
import datetime
from sqlalchemy import (
    not_,
    distinct,
    and_,
    or_,
    func,
)

from autonomie.models.base import DBSESSION


STRING_OPTIONS = (
    ("has", u"Contenant", ),
    ("sw", u"Commençant par", ),
    ("ew", u"Se terminant par", ),
    ("nhas", u"Ne contenant pas", ),
    ("neq", u"N'étant pas égal(e) à", ),
    ("eq", u"Étant égal(e) à", ),
    ("nll", u"N'étant pas renseigné(e)", ),
    ("nnll", u"Étant renseigné(e)", ),
)


BOOL_OPTIONS = (
    ('true', u"Étant coché(e)", ),
    ('false', u"N'étant pas coché(e)", ),
)


OPTREL_OPTIONS = (
    ("ioo", u"Faisant partie de", ),
    ("nioo", u"Ne faisant pas partie de", ),
    ("nll", u"N'étant pas renseigné(e)", ),
    ("nnll", u"Étant renseigné(e)", ),
)


NUMERIC_OPTIONS = (
    ("lte", u"Étant inférieur(e) ou égal(e)", ),
    ("gte", u"Étant supérieur(e) ou égal(e)", ),
    ("bw", u"Faisant partie de l'intervalle", ),
    ("nbw", u"Ne faisant pas partie de l'intervalle"),
    ("eq", u"Étant égal(e) à",),
    ("neq", u"N'étant pas égal(e) à", ),
    ("lt", u"Étant inférieur(e) à", ),
    ("gt", u"Étant supérieur(e) à", ),
    ("nll", u"N'étant pas renseigné(e)", ),
    ("nnll", u"Étant renseigné(e)", ),
)


DATE_OPTIONS = (
    ('dr', u"Dans l'intervalle", ),
    ('this_year', u"Depuis le début de l'année", ),
    ('this_month', u"Ce mois-ci", ),
    ("previous_year", u"L'année dernière", ),
    ("previous_month", u"Le mois dernier", ),
    ("nll", u"N'étant pas renseigné(e)", ),
    ("nnll", u"Étant renseigné(e)", ),
)


MULTIDATE_OPTIONS = (
    ('first_dr', u"Le premier dans l'intervalle", ),
    ('first_this_year', u"Le premier depuis le début de l'année", ),
    ('first_this_month', u"Le premier ce mois-ci", ),
    ("first_previous_year", u"Le premier l'année dernière", ),
    ("first_previous_month", u"Le premier le mois dernier", ),
    ('last_dr', u"Le dernier dans l'intervalle", ),
    ('last_this_year', u"Le dernier depuis le début de l'année", ),
    ('last_this_month', u"Le dernier ce mois-ci", ),
    ("last_previous_year", u"Le dernier l'année dernière", ),
    ("last_previous_month", u"Le dernier le mois dernier", ),
    ("nll", u"N'étant pas renseigné(e)", ),
    ("nnll", u"Étant renseigné(e)", ),
)


class MissingDatasError(Exception):
    """
    Custom exception raised when some datas is missing for filtering
    """
    pass


class SheetQueryFactory(object):
    """
    Statistics sheet

    Compound of :
        a list of entries

    Rendering:

            A sheet should be rendered as a csv file, the headers :
                ('label', 'count', 'description')
            each row matches an entry

    :param obj model: The model we're building stats on (UserDatas)
    :param obj sheet: The StatisticSheet instance we're mapping
    :param obj inspector: The model's sqlalchemy inspector used to retrieve
    database related informations
    """
    entries = []

    def __init__(self, model, sheet, inspector):
        self.model = model
        self.sheet = sheet
        self.inspector = inspector

        self.entries = []
        for entry in self.sheet.entries:
            self.entries.append(
                EntryQueryFactory(
                    self.model,
                    entry,
                    self.inspector,
                )
            )

    @property
    def headers(self):
        return (
            {'name': u'label', 'label': u"Libellé"},
            {'name': u'description', 'label': u'Description'},
            {'name': u'count', 'label': u"Nombre"},
        )

    @property
    def rows(self):
        """
        Return the rows of our sheet output
        """
        result = []
        for entry in self.entries:
            result.append(entry.render_row())

        return result


class EntryQueryFactory(object):
    """
    Statistic entry

    Compound of :
        a label
        a description
        a list of criteria

    :param obj model: The model we're building stats on (UserDatas)
    :param obj entry_model: The StatisticEntry model instance
    :param obj inspector: The model's sqlalchemy inspector used to retrieve
    database related informations

    Return a unique sqlalchemy query object
    If needed, we make independant queries that we group in the main query
    filtering on the resulting ids
    """
    model = None
    related_joins = None
    criteria = []

    def __init__(self, model, entry_model, inspector):
        self.model = model
        self.entry = entry_model
        self.stat_model = inspector

        self.query_object = QueryFactory(
            self.model,
            self.entry.criteria,
            self.stat_model,
        )

    def query(self):
        """
        :returns: A sqla query matching the selected criteria in the form
        [(model.id, model_instance)...]
        :rtype: A query object
        """
        return self.query_object.query()

    def render_row(self):
        """
        Returns the datas expected for statistics rendering
        """
        return {
            "label": self.entry.title,
            "count": self.query_object.count(),
            "description": self.entry.description,
        }


def get_query_helper(model, criterion_model, inspector):
    """
    Return the appropriate helper class used to filter on a given criterion
    :param model: The model we are building stats on (e.g: UserDatas)
    :param criterion_model: The criterion we want to build a helper from
    :param inspector: A SQLAlchemy inspection class

    :returns: A CriterionQueryHelper instance
    """
    if criterion_model.type == 'string':
        factory = StrCriterionQueryHelper
    elif criterion_model.type == 'number':
        factory = NumericCriterionQueryHelper
    elif criterion_model.type == 'optrel':
        factory = OptRelCriterionQueryHelper
    elif criterion_model.type == 'static_opt':
        factory = OptRelCriterionQueryHelper
    elif criterion_model.type in ('date', 'multidate'):
        factory = DateCriterionQueryHelper
    elif criterion_model.type == 'bool':
        factory = BoolCriterionQueryHelper
    elif criterion_model.type == 'or':
        factory = OrCriterionQueryHelper
    elif criterion_model.type == 'and':
        factory = AndCriterionQueryHelper
    else:
        raise Exception(u"Unknown Criterion model type : %s" % (
            criterion_model.type,
        ))
    return factory(model, criterion_model, inspector)


def get_query_factory(model, criterion_model, inspector, parent=None):
    """
    Return a query factory for the given criterion_model

    :param model: The model we are building stats on (e.g: UserDatas)
    :param criterion_model: The criterion we want to build a helper from
    :param inspector: A SQLAlchemy inspection class

    :returns: A QueryFactory instance
    """
    if criterion_model.type == 'or':
        factory = OrQueryFactory

    elif criterion_model.type == 'and':
        factory = AndQueryFactory

    else:
        factory = QueryFactory
    return factory(model, criterion_model, inspector, parent)


class CriterionQueryHelper(object):
    """
    Statistic criterion

    Compound of :
        a model we query on
        a field name
        a condition key
        conditions values
        a type
    """
    model = None
    key = None
    search1 = None
    type = 'str'
    # 0 can't be a none value since it can be a valid one (0 children)
    none_values = (None, '')

    def __init__(self, model, criterion_model, inspector):
        self.model = model
        self.criterion_model = criterion_model

        self.key = criterion_model.key
        self.method = criterion_model.method

        self.sqla_datas = inspector.get_datas(self.key)
        self.column = self.sqla_datas['column']

    def get_join_class(self):
        """
        Return a related class if this criterion used one
        """
        return self.sqla_datas.get('join_class')

    def gen_filter(self):
        result = None
        if self.key:
            filter_method = getattr(self, "filter_%s" % self.method, None)
            if filter_method is not None:
                result = filter_method(self.column)
        return result

    def gen_having_clause(self):
        """
        Generate a 'having' clause and its associated group_by clause
        """
        result = None
        if self.key:
            having_method = getattr(self, "having_%s" % self.method, None)
            if having_method is not None:
                result = having_method(self.column)
        return result

    def filter_nll(self, attr):
        """ null """
        return attr.in_(self.none_values)

    def filter_nnll(self, attr):
        """ not null """
        return not_(attr.in_(self.none_values))

    def filter_eq(self, attr):
        """ equal """
        if self.search1:
            return attr == self.search1

    def filter_neq(self, attr):
        """ not equal """
        if self.search1:
            return attr != self.search1


class StrCriterionQueryHelper(CriterionQueryHelper):
    """
    Statistic criterion related to strings
    """
    def __init__(self, model, criterion_model, inspector):
        CriterionQueryHelper.__init__(self, model, criterion_model, inspector)
        self.search1 = criterion_model.search1
        self.search2 = criterion_model.search2

    def filter_has(self, attr):
        """ contains """
        if self.search1:
            like_str = u"%" + self.search1 + u"%"
            return attr.like(like_str)

    def filter_sw(self, attr):
        """ startswith """
        if self.search1:
            like_str = self.search1 + u"%"
            return attr.like(like_str)

    def filter_ew(self, attr):
        """ endswith """
        if self.search1:
            like_str = self.search1 + u"%"
            return attr.like(like_str)

    def filter_nhas(self, attr):
        """ not contains """
        f = self.filter_has(attr)
        if f is not None:
            return not_(f)


class BoolCriterionQueryHelper(CriterionQueryHelper):
    def filter_true(self, attr):
        return attr == True

    def filter_false(self, attr):
        return attr == False


class OptRelCriterionQueryHelper(CriterionQueryHelper):
    """
    Statistic criterion related to related options
    """
    def __init__(self, model, criterion_model, inspector):
        CriterionQueryHelper.__init__(self, model, criterion_model, inspector)
        self.searches = criterion_model.searches

    def filter_ioo(self, attr):
        """ is one of """
        if self.searches:
            return attr.in_(self.searches)

    def filter_nioo(self, attr):
        """ is not one of """
        if self.searches:
            return not_(attr.in_(self.searches))


class NumericCriterionQueryHelper(CriterionQueryHelper):
    """
    Statistic criterion for filtering numeric datas
    """
    def __init__(self, model, criterion_model, inspector):
        CriterionQueryHelper.__init__(self, model, criterion_model, inspector)
        self.search1 = criterion_model.search1
        self.search2 = criterion_model.search2

    def filter_lte(self, attr):
        if self.search1:
            return attr <= self.search1
        return

    def filter_gte(self, attr):
        if self.search1:
            return attr >= self.search1
        return

    def filter_lt(self, attr):
        if self.search1:
            return attr < self.search1
        return

    def filter_gt(self, attr):
        if self.search1:
            return attr > self.search1
        return

    def bw(self, attr):
        if self.search1 and self.search2:
            return and_(attr > self.search1, attr < self.search2)

    def nbw(self, attr):
        if self.search1 and self.search2:
            return or_(attr <= self.search1, attr >= self.search2)


class DateCriterionQueryHelper(CriterionQueryHelper):
    """
    Statistic criterion related to Dates
    """
    def __init__(self, model, criterion_model, inspector):
        CriterionQueryHelper.__init__(self, model, criterion_model, inspector)
        self.search1 = criterion_model.search1
        self.search2 = criterion_model.search2

    def filter_dr(self, attr):
        if self.search1 and self.search2:
            return and_(
                attr >= self.search1,
                attr <= self.search2,
            )
        raise MissingDatasError(
            u"Il manque des informations pour générer la requête statistique",
            key=self.key,
            method=self.method,
        )

    def filter_this_year(self, attr):
        """
        This year
        """
        current_year = datetime.date.today().year
        first_day = datetime.date(current_year, 1, 1)
        return attr >= first_day

    def filter_previous_year(self, attr):
        """
        Last year
        """
        previous_year = datetime.date.today().year - 1
        first_day = datetime.date(previous_year, 1, 1)
        last_day = datetime.date(previous_year, 12, 31)
        return and_(
            attr >= first_day,
            attr <= last_day,
        )

    def filter_this_month(self, attr):
        """
        This month
        """
        today = datetime.date.today()
        first_day = datetime.date(today.year, today.month, 1)
        return attr >= first_day

    def get_first_day_of_previous_month(self, today, nb_months=1):
        """
        Return the first day of this month - nb_months
        Handle year switch

        :param int nb_months: the number of months to go back
        """
        month = today.month - 1 - nb_months
        year = today.year + month / 12
        month = month % 12 + 1
        return datetime.date(year, month, 1)

    def filter_previous_month(self, attr):
        """
        Last month
        """
        today = datetime.date.today()
        first_day = self.get_first_day_of_previous_month(today)
        last_day = datetime.date(today.year, today.month, 1)
        return and_(
            attr >= first_day,
            attr < last_day
        )

    def having_first_dr(self, attr):
        return self.filter_dr(func.min(attr))

    def having_first_this_year(self, attr):
        return self.filter_this_year(func.min(attr))

    def having_first_this_month(self, attr):
        return self.filter_this_month(func.min(attr))

    def having_first_previous_year(self, attr):
        return self.filter_previous_year(func.min(attr))

    def having_first_previous_month(self, attr):
        return self.filter_previous_month(func.min(attr))

    def having_last_dr(self, attr):
        return self.filter_dr(func.max(attr))

    def having_last_this_year(self, attr):
        return self.filter_this_year(func.max(attr))

    def having_last_this_month(self, attr):
        return self.filter_this_month(func.max(attr))

    def having_last_previous_year(self, attr):
        return self.filter_previous_year(func.max(attr))

    def having_last_previous_month(self, attr):
        return self.filter_previous_month(func.max(attr))


class OrCriterionQueryHelper(object):

    def __init__(self, model, composite, inspector):
        self.model = model
        self.composite_model = composite
        self.criteria = []
        for criterion in composite.criteria:
            self.criteria.append(
                get_query_helper(model, criterion, inspector)
            )

    def gen_filter(self):
        filters = []
        for criterion in self.criteria:
            filters.append(criterion.gen_filter())
        return or_(*filters)

    def get_keys_and_join_classes(self):
        for criterion in self.criteria:
            if hasattr(criterion, 'get_keys_and_join_classes'):
                # It's a composite subcriterion
                for key, value in criterion.get_keys_and_join_classes():
                    yield key, value
            else:
                # it's a simple criterion
                yield criterion.key, criterion.get_join_class()


class AndCriterionQueryHelper(OrCriterionQueryHelper):
    def gen_filter(self):
        # NOTE : this method cannot be factorized easily since sqla is doing
        # strange object attachment when the and_ and or_ function are used in a
        # query
        filters = []
        for criterion in self.criteria:
            filters.append(criterion.gen_filter())
        return and_(*filters)


class QuerySet(object):
    """
    A set of independant queries
    """
    children = []

    def add(self, query_object):
        """
        Add a child to the QuerySet
        """
        self.children.append(query_object)

    def get_ids(self):
        """
        Return the ids matching all the queries
        """
        ids = None
        for query in self.children:
            if ids is None:
                ids = query.get_ids()
            else:
                ids = ids.intersection(query.get_ids())
        return ids


class QueryFactory(object):
    """
    A query factory that produce a sqlalchemy query, can combine multiple query
    factories or query helpers

    :attr list criteria: The list of StatisticCriterion handled by this object
    :attr obj model: The Sqlalchemy model we're talking about
    :attr obj inspector: The Statistic SQLA inspector used to collect columns ..
    :attr bool root: Is this object at the top level of our entry
    """
    def __init__(self, model, criteria, inspector, parent=None):
        self.model = model
        self.inspector = inspector
        self.parent = parent
        self.root = parent is None

        if not hasattr(criteria, '__iter__'):
            criteria = [criteria]
        self.criteria = criteria
        self.single = len(self.criteria) == 1

        # When building queries we should ensure we limit the joins
        self.already_joined = []

        self.query_factories = []
        self.query_helpers = []
        self._wrap_criteria()

    def _wrap_criteria(self):
        """
        Wrap criteria with adapted wrappers

            What goes in the main_query will be wrapped as Stat
            CriterionQueryHelper

            What should be queried independantly should be wrapped with a Query
            Factory object
        """
        for criterion in self.criteria:
            if (self.root and not criterion.has_parent()) or \
                    (criterion.parent == self.parent):
                if not self.single:
                    self.query_factories.append(
                        get_query_factory(self.model, criterion, self.inspector)
                    )
                else:
                    self.query_helpers.append(
                        get_query_helper(self.model, criterion, self.inspector)
                    )

    def _get_ids_from_factories(self):
        """
        Return the ids of matching entries retrieved through the query_factories
        """
        ids = None
        for factory in self.query_factories:
            if ids is None:
                ids = factory.get_ids()
            else:
                # AND CLAUSE
                ids = ids.intersection(ids)
        return ids


    def query(self):
        """
        Return the main query used to find objects

        e.g:

            query = DBSESSION().query(distinct(UserDatas.id), UserDatas)
            query = query.filter(UserDatas.name.startswith('test'))
            query = query.outerjoin(UserDatas.conseiller)
            query = query.filter(User.lastname=='A manager')
            query = query.filter(
                UserDatas.id.in_(
                    [list of ids retrieved from independant queries]
                )
            )

        """
        self.already_joined = []
        if self.root:
            main_query = DBSESSION().query(distinct(self.model.id), self.model)
        else:
            main_query = DBSESSION().query(distinct(self.model.id))

        # Pour chaque critère sur lesquels on va ajouter des filtres, on a
        # besoin d'être sûr que la classe concernée est bien requêtée, il faut
        # donc ajouter des outerjoins pour chaque classe liée.

        # NOTE: on ne gère pas les alias (les joins sur deux tables identiques
        # pour deux relations différentes)
        for criterion in self.query_helpers:
            # On génère le filtre
            filter_ = criterion.gen_filter()
            having = criterion.gen_having_clause()

            # si il y a un filtre ...
            if filter_ is not None:
                main_query = self.join(main_query, criterion)
                main_query = main_query.filter(filter_)

            elif having is not None:
                main_query = self.join(main_query, criterion)
                main_query = main_query.group_by(self.model.id)
                main_query = main_query.having(having)

        if self.query_factories:
            ids = list(self._get_ids_from_factories())
            main_query = main_query.filter(self.model.id.in_(ids))

        return main_query

    def join(self, query, criterion):
        """
        add outerjoin calls to the query regarding the stat criterion

        :param query: The query to join on
        :param criterion: The criterion query helper which needs a join
        """
        if hasattr(criterion, "get_join_class"):
            # critère 'simple'
            # On récupère l'objet lié
            join_class = criterion.get_join_class()
            query = self.add_join_to_query(query, criterion.key, join_class)
        else:
            # Critère composé
            for key, join_class in criterion.get_keys_and_join_classes():
                query = self.add_join_to_query(query, key, join_class)
        return query

    def add_join_to_query(self, query, key, join_class):
        """
        Add an outerjoin to a query if it's not already in
        :param query: The query to join on
        :param key: The inspector's column key (used to collect already joined
        tables)
        :param join_class: The class to outerjoin in our query
        """
        # Si il y a un outerjoin à faire (le critère se fait sur un
        # attribut de l'objet lié)
        if join_class is not None:
            # on ne va pas outerjoiné deux fois la classe pour le même
            # critère
            if key not in self.already_joined:
                query = query.outerjoin(join_class)
                self.already_joined.append(key)
        return query

    def get_ids(self):
        """
        Return the ids matched by the current query
        """
        return set([item[0] for item in self.query()])


class OrQueryFactory(QueryFactory):
    """
    An independant OR query factory
    All children of the or query are requested indepedantly
    Or clause is done Python side
    """
    def _wrap_criteria(self):
        """
        Wrap criteria with adapted wrappers

            What goes in the main_query will be wrapped as Stat
            CriterionQueryHelper

            What should be queried independantly should be wrapped with a Query
            Factory object
        """
        parent_criterion = self.criteria[0]
        for criterion in parent_criterion.criteria:
            self.query_factories.append(
                get_query_factory(
                    self.model,
                    criterion,
                    self.inspector,
                    parent=parent_criterion)
            )

    def get_ids(self):
        """
        Compute the or clause on the independant query factories resulting ids
        list
        """
        ids = None
        for factory in self.query_factories:
            if ids is None:
                ids = factory.get_ids()
            else:
                # OR CLAUSE
                ids = ids.union(factory.get_ids())
        return ids


class AndQueryFactory(OrQueryFactory):
    """
    An independant AND query factory

    All children of the or query are requested indepedantly
    End clause is done Python side
    """
    def get_ids(self):
        """
        Compute the and clause on the independant query factories resulting ids
        list
        """
        ids = None
        for factory in self.query_factories:
            if ids is None:
                ids = factory.get_ids()
            else:
                # AND CLAUSE
                ids = ids.intersection(factory.get_ids())
        return ids

