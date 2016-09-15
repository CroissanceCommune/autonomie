#-*-coding:utf-8-*-
"""3.3.0 : fonctionnalites_9

Revision ID: 2b6ac7b172d3
Revises: 25a21d2410b7
Create Date: 2016-06-21 11:12:57.071400

"""

# revision identifiers, used by Alembic.
revision = '2b6ac7b172d3'
down_revision = '25a21d2410b7'

from alembic import op
import sqlalchemy as sa


def add_company_id(session, logger):
    logger.warn("Adding company_id to Task")
    from alembic.context import get_bind
    conn = get_bind()

    query = "select t.id, p.company_id from task t, project p where t.project_id = p.id"

    for id, company_id in conn.execute(query):
        req = "update task set company_id={0} where id={1}".format(company_id, id)
        session.execute(req)


def add_company_index(session, logger):
    logger.warn("Adding company_index to Task")
    from autonomie.models.company import Company
    from autonomie.models.task import Task
    for datas in session.query(Company.id):
        query = Task.query()
        query = query.options(
            sa.orm.load_only('id', 'company_id', "company_index", 'type_')
        )
        query = query.filter(Task.company_id == datas[0])
        for type_ in ('estimation', 'invoice', 'cancelinvoice'):
            index = 1
            typequery = query.filter(Task.type_ == type_)
            for task in typequery:
                task.company_index = index
                index += 1
                session.merge(task)


def add_internal_number(session, logger):
    logger.warn("Adding internal_number to Task")
    NUMBER_TMPLS = {
        'estimation': u"{s.project.code}_{s.customer.code}_D{s.project_index}\
        _{s.date:%m%y}",
        'invoice': u"{s.project.code}_{s.customer.code}_F{s.project_index}\
        _{s.date:%m%y}",
        'cancelinvoice': u"{s.project.code}_{s.customer.code}_A{s.project_index}\
        _{s.date:%m%y}"
    }
    from autonomie.models.task import Task
    from autonomie.models.customer import Customer
    from autonomie.models.project import Project
    from autonomie.models.project import Phase

    from sqlalchemy.orm import joinedload
    from sqlalchemy.orm import load_only

    query = Task.query().options(
        load_only("project_index", "company_index", "date", "phase_id", 'type_')
    )

    query = query.filter(
        Task.type_.in_(['invoice', 'estimation', 'cancelinvoice'])
    )
    query = query.options(joinedload(Task.customer).load_only(Customer.code))
    query = query.options(joinedload(Task.project).load_only(Project.code))

    for task in query:
        tmpl = NUMBER_TMPLS[task.type_]
        if Phase.get(task.phase_id) is None:
            session.delete(task)
        else:
            task.internal_number = tmpl.format(s=task).upper()
            session.merge(task)

def create_custom_treasury_modules(session, logger):
    logger.warn("Adding custom treasury modules")
    from autonomie.models.config import Config
    from autonomie.models.treasury import CustomInvoiceBookEntryModule

    organic_keys = (
        u"Contribution à l'organic",
        'compte_cg_organic',
        'compte_cg_debiteur_organic',
        'taux_contribution_organic',
        'sage_organic',
        u'Contribution Organic {client.name} {entreprise.name}'
    )

    cgscop_keys = (
        u"Contribution à la CGSCOP",
        'compte_cgscop',
        'compte_cg_debiteur',
        'taux_cgscop',
        'sage_cgscop',
        u'{client.name} {entreprise.name}'
    )

    assurance_keys = (
        u"Assurance",
        'compte_cg_assurance',
        'compte_cg_assurance',
        'taux_assurance',
        'sage_assurance',
        u'{client.name} {entreprise.name}',
    )

    for keys in (organic_keys, cgscop_keys, assurance_keys, ):
        (
            title,
            cg_debit,
            cg_credit,
            percentage_key,
            active_key,
            label_template
        ) = keys

        compte_cg_debit = Config.get(cg_debit)
        compte_cg_credit = Config.get(cg_credit)
        percentage = Config.get(percentage_key)
        enabled = Config.get(active_key, False)
        if compte_cg_debit and compte_cg_debit.value and compte_cg_credit and compte_cg_credit.value and percentage is not None:
            module = CustomInvoiceBookEntryModule(
                title=title,
                compte_cg_debit=compte_cg_debit.value,
                compte_cg_credit=compte_cg_credit.value,
                percentage=percentage.value,
                enabled=enabled.value,
                label_template=label_template,
            )
            session.add(module)


def upgrade():
    import logging
    logger = logging.getLogger('alembic.here')
    op.add_column(
        "user_datas",
        sa.Column(
            'statut_social_status_today_id',
            sa.Integer,
            sa.ForeignKey('social_status_option.id'),
        )
    )
    op.add_column(
        "user_datas",
        sa.Column(
            "parcours_employee_quality_id",
            sa.Integer,
            sa.ForeignKey('employee_quality_option.id'),
        )
    )
    op.add_column(
        "user_datas",
        sa.Column(
            "situation_antenne_id",
            sa.Integer,
            sa.ForeignKey('antenne_option.id')
        )
    )
    op.add_column(
        "task",
        sa.Column(
            "internal_number",
            sa.String(40),
        )
    )
    op.add_column(
        "task",
        sa.Column("company_index", sa.Integer)
    )
    op.execute("alter table task CHANGE sequence_number project_index int(11)")
    op.add_column(
        "task",
        sa.Column(
            "company_id",
            sa.Integer,
            sa.ForeignKey('company.id'),
        )
    )
    from autonomie.models.base import (
        DBSESSION,
    )
    session = DBSESSION()

    add_company_id(session, logger)
    add_company_index(session, logger)
    add_internal_number(session, logger)

    logger.warn("Adding Contract Histories")
    from autonomie.models.user import UserDatas, ContractHistory
    for id_, last_avenant in UserDatas.query('id', 'parcours_last_avenant'):
        if last_avenant:
            session.add(
                ContractHistory(
                    userdatas_id=id_,
                    date=last_avenant,
                    number=-1
                )
            )

    op.add_column(
        "date_convention_cape_datas",
        sa.Column('end_date', sa.Date(), nullable=True)
    )
    op.execute("alter table customer MODIFY code VARCHAR(4);")
    op.execute("alter table project MODIFY code VARCHAR(4);")

    create_custom_treasury_modules(session, logger)

    from zope.sqlalchemy import mark_changed
    mark_changed(session)


def downgrade():
    op.execute("SET FOREIGN_KEY_CHECKS=0;")
    op.drop_table('employee_quality_option')
    op.drop_column('user_datas', 'statut_social_today_id',)
    op.drop_column('user_datas', 'parcours_employee_quality_id',)
    op.execute("SET FOREIGN_KEY_CHECKS=1;")
