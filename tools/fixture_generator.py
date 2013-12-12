from itertools import count, islice
from random import choice
#import datetime
import json


def random_projects():
    company = 'Company1'
    counter = count()
    for num in counter:
        project_name = 'project_%d' % num
        project_code = 'PC%2d' % num

        project = dict(name=project_name, code=project_code, 
            customers=[], phases=[], estimations=[], company=company)
        
        for time in xrange(3): 
            customer = {}

            customer['name'] = 'cust_%d_%s' % (time, project_name)
            project['customers'].append(customer)

        for time in xrange(3):
            phase = dict(name='phase_%d' % time)
            project['phases'].append(phase)

    # setup the part that is to be tested
        for time in xrange(4):
            phase = choice(project['phases'])
            customer = choice(project['customers'])

            # tasks will be ordered according to dates.
            
            # randomize dates
            year = choice((2012, 2013))
            month = choice(xrange(1, 13))
            day = choice(xrange(1, 29))
            # not easy to json-serialize
            # estimation_date = datetime.date(2013, 01, 01)
            estimation_date = (year, month, day)

            estimation = dict(
                phase=phase, 
                customer=customer,
                taskDate=estimation_date
                )
            project['estimations'].append(estimation)
        yield project

projectnb = 12
projects = islice(random_projects(), 12)
print json.dumps(list(projects))
