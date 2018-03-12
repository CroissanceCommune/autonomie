# -*- coding: utf-8 -*-
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;


def test_duplicate_task_line(task_line):
    newline = task_line.duplicate()
    for i in ('order', 'cost', 'tva', "description", "quantity", "unity"):
        assert getattr(newline, i) == getattr(task_line, i)


def test_gen_cancelinvoiceline(task_line):
    newline = task_line.gen_cancelinvoice_line()
    for i in ('order', 'tva', "description", "quantity", "unity"):
        assert getattr(newline, i) == getattr(task_line, i)
    assert newline.cost == -1 * task_line.cost


def test_duplicate_task_line_group(task_line_group, task_line):
    task_line_group.lines = [task_line]

    newgroup = task_line_group.duplicate()

    for i in ('order',  "description", "title"):
        assert getattr(newgroup, i) == getattr(task_line_group, i)

    assert newgroup.total_ht() == task_line_group.total_ht()


def test_task_line_from_sale_product(sale_product):
    from autonomie.models.task.task import TaskLine
    t = TaskLine.from_sale_product(sale_product)
    assert t.tva == sale_product.tva
    assert t.cost == 100000 * sale_product.value
    assert t.description == sale_product.description
    assert t.unity == sale_product.unity
