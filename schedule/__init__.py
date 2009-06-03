from django.conf import settings

try:
    DATE_FILTER_FIELD = settings.SCHEDULE_DATE_FILTER_FIELD
except AttributeError:
    DATE_FILTER_FIELD = 'datefield'
try:
    DATE_FILTER_RANGE = settings.SCHEDULE_DATE_FILTER_RANGE
except AttributeError:
    DATE_FILTER_RANGE = 'daterange'
