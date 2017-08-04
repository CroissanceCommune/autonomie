# coding: utf-8


def id_func(value):
    return value


def task_formatter(task):
    from autonomie.utils.strings import format_amount
    res = {
        'official_number': task.official_number,
        'date': task.date,
        'ht': format_amount(task.ht, grouping=False, precision=5),
        'tva': format_amount(task.tva, grouping=False, precision=5),
        'ttc': format_amount(task.ttc, grouping=False, precision=5),
        'company': task.project.company.name,
        'code': task.project.company.code_compta,
        'quantity': sum([line.quantity for line in task.all_lines]),
        'customer': task.customer.name,
        'description': task.description,
        'payment': '',
    }
    if task.payments:
        res['payment'] = task.payments[0].mode
    return res


def get_tasks(financial_year, from_number):
    from autonomie.models.task import Task, Invoice, CancelInvoice
    from autonomie.models.project import Project
    from sqlalchemy import or_
    query = Task.query()
    query = query.with_polymorphic([Invoice, CancelInvoice])
    query = query.outerjoin(Task.project)
    query = query.outerjoin(Project.company)
    query = query.outerjoin(Task.customer)
    query = query.filter(Task.status == 'valid')
    query = query.filter(
        or_(
            Invoice.financial_year == financial_year,
            CancelInvoice.financial_year == financial_year,
        )
    )
    query = query.filter(Task.official_number >= from_number)
    return query


def write_xls(year, from_number, filepath, force=False):
    from sqla_inspect import excel
    xls = excel.XlsWriter()
    xls.headers = (
        {'label': 'Identifiant', 'name': 'official_number',
         '__col__': {},
         },
        {'label': 'Date', 'name': 'date', 'format': "dd/mm/yyyy",
         '__col__': {},
         },
        {'label': 'Quantité', 'name': 'quantity', '__col__': {},},
        {'label': 'Objet', 'name': 'description', '__col__': {},},
        {'label': "Compte analytique entrepreneur", 'name': "code",
         '__col__': {},
         },
        {'label': 'Entrepreneur', 'name': 'company', '__col__': {}, },
        {'label': 'Client', 'name': 'customer', '__col__': {}},
        {'label': 'HT', 'name': 'ht',
         '__col__': {},
         },
        {'label': 'TVA', 'name': 'tva',
         '__col__': {},
         },
        {'label': 'TTC', 'name': 'ttc',
         '__col__': {},
         },
        {'label': 'Mode de paiement', 'name': 'payment', '__col__': {},},
    )
    xls._datas = []
    for task in get_tasks(year, from_number):
        task_dict = task_formatter(task)
        xls._datas.append(xls.format_row(task_dict))
    import os
    if os.path.exists(filepath) and not force:
        print("File exists add force=True to your command")
        return False

    with file(filepath, 'w') as f_buf:
        xls.render(f_buf)
    return True
