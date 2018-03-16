import datetime
import decimal
import gettext
import logging

_ = gettext.gettext

log = logging.getLogger(__name__)

def calc_pace(distance, seconds):
    """
    >>> calc_pace(distance=10, seconds=1*60*60)
    6.0
    """
    log.info("calculate_pace(): distance %r time %r", distance, seconds)
    pace = (seconds/ decimal.Decimal(60)) / distance
    return pace


def human_duration(t):
    """
    Converts a time duration into a friendly text representation.

    >>> human_duration("type error")
    Traceback (most recent call last):
        ...
    TypeError: human_duration() argument must be timedelta, integer or float)


    >>> human_duration(datetime.timedelta(microseconds=1000))
    u'1.0 ms'
    >>> human_duration(0.01)
    u'10.0 ms'
    >>> human_duration(0.9)
    u'900.0 ms'
    >>> human_duration(datetime.timedelta(seconds=1))
    u'1.0 sec'
    >>> human_duration(65.5)
    u'1.1 min'
    >>> human_duration((60 * 60)-1)
    u'59.0 min'
    >>> human_duration(60*60)
    u'1.0 hours'
    >>> human_duration(1.05*60*60)
    u'1.1 hours'
    >>> human_duration(datetime.timedelta(hours=24))
    u'1.0 days'
    >>> human_duration(2.54 * 60 * 60 * 24 * 365)
    u'2.5 years'
    """
    assert isinstance(t, decimal.Decimal)

    chunks = (
      (decimal.Decimal(60 * 60 * 24 * 365), _('years')),
      (decimal.Decimal(60 * 60 * 24 * 30), _('months')),
      (decimal.Decimal(60 * 60 * 24 * 7), _('weeks')),
      (decimal.Decimal(60 * 60 * 24), _('days')),
      (decimal.Decimal(60 * 60), _('hours')),
    )

    if t < 1:
        return _("%.1f ms") % round(t * 1000, 1)
    if t < 60:
        return _("%.1f sec") % round(t, 1)
    if t < 60 * 60:
        return _("%.1f min") % round(t / 60, 1)

    for seconds, name in chunks:
        count = t / seconds
        if count >= 1:
            count = round(count, 1)
            break
    return "%(number).1f %(type)s" % {'number': count, 'type': name}


def human_distance(km):
    if km < 1:
        return "%.1f m" % round(km * 1000, 1)

    if km == int(km):
        return "%.0f km" % km

    # FIXME:
    txt = "%.4f" % km
    txt = txt.rstrip("0")
    return "%s km" % txt