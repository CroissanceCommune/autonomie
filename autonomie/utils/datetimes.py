import datetime


class UnicodeDate(datetime.date):
    """Tweaked class formatting as unicode rather than str

    Because original class behaviour (outputing bytes) causes that kind of call
    to fail if non-ascii char is present in month name ::

        u'{:%B}'.format(date(2018, 12, 12))

    NB: Using Python3 will make this un-necessary (date.__format__ natively
    outputs unicode).

    """
    def __format__(self, *args, **kwargs):
        ret = super(UnicodeDate, self).__format__(*args, **kwargs)
        return ret.decode('utf-8')
