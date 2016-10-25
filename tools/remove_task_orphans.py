# -*- coding: utf-8 -*-
# * Copyright (C) 2012-2016 Croissance Commune
# * Authors:
#       * TJEBBES Gaston <g.t@majerti.fr>
#       * Arezki Feth <f.a@majerti.fr>;
#       * Miotte Julien <j.m@majerti.fr>;
#
# This file is part of Autonomie : Progiciel de gestion de CAE.
#
#    Autonomie is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Autonomie is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Autonomie.  If not, see <http://www.gnu.org/licenses/>.
from autonomie.models.base import DBSESSION as db
from autonomie.models.task import *

model_dict = {
    'estimation': Estimation,
    'invoice': Invoice,
    'cancelinvoice': CancelInvoice,
}

def main():
    task_ids = {}
    for key in model_dict.keys():
        task_ids[key] = set([
            item[0] for item in db().query(Task.id).filter(Task.type_==key)]
        )

    model_ids = {}
    for key, model in model_dict.items():
        model_ids[key] = set([item[0] for item in db().query(model.id)])

    for key in model_dict.keys():
        print(task_ids[key].difference(model_ids[key]))


if __name__ == '__main__':
    main()
