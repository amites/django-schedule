import datetime
from schedule import DATE_FILTER_FIELD, DATE_FILTER_RANGE
from schedule import periods
    
DATE_RANGE_ALIASES = {
    'all': None,
    'fromtoday': lambda d: periods.Period(None, datetime.datetime.combine(d.date(), datetime.time.min), None),
    'today': lambda d: periods.Day(None, date = d),
    'thisweek': lambda d: periods.Week(None, date = d),
    'thismonth': lambda d: periods.Month(None, date = d),
}
        
def apply_date_filter(query, request):
    """
    Returns QuerySet with date filters applied
    """
    field = request.GET.get(DATE_FILTER_FIELD, None)
    if field is None:
        return query
    
    date_range = request.GET.get(DATE_FILTER_RANGE, 'today')
    creator = DATE_RANGE_ALIASES[date_range]
    if creator is None:
        return query
    
    period = creator(datetime.datetime.now())
    
    if period.start is not None and period.end is not None:
        kwargs = {'%s__range' % str(field): (period.start, period.end)}
        return query.filter(**kwargs)
    elif period.start is not None:
        kwargs = {'%s__gte' % str(field): period.start}
        return query.filter(**kwargs)
    elif period.end is not None:
        kwargs = {'%s__lte' % str(field): period.end}
        return query.filter(**kwargs)
        
    return query
    

