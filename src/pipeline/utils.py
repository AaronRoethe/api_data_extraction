from datetime import date, timedelta
from pandas.tseries.holiday import AbstractHolidayCalendar, Holiday, nearest_workday, \
    USMartinLutherKingJr, USPresidentsDay, USMemorialDay, USLaborDay, USThanksgivingDay
import json, io

class CioxHoliday(AbstractHolidayCalendar):
    rules = [
        Holiday('NewYearsDay', month=1, day=1, observance=nearest_workday),
        USMartinLutherKingJr,
        USPresidentsDay,
        USMemorialDay,
        Holiday('USIndependenceDay', month=7, day=4, observance=nearest_workday),
        USLaborDay,
        USThanksgivingDay,
        Holiday('Christmas', month=12, day=25, observance=nearest_workday)
    ]

ciox_holidays = CioxHoliday()
today = date.today()
ONE_DAY = timedelta(days=1)

def next_business_day(start):
    next_day = start + ONE_DAY
    holidays = ciox_holidays.holidays(today, today + timedelta(days=30)).values
    while next_day.weekday() >= 5 or next_day in holidays:
        next_day += ONE_DAY
    return next_day

def last_business_day(start):
    next_day = start - ONE_DAY
    holidays = ciox_holidays.holidays(today, today + timedelta(days=30)).values
    while next_day.weekday() >= 5 or next_day in holidays:
        next_day -= ONE_DAY
    return next_day

def x_Bus_Day_ago(N):
    B10 = []
    seen = set(B10)
    i = today

    while len(B10) < N:
        item = last_business_day(i)
        if item not in seen:
            seen.add(item)
            B10.append(item)
        i -= timedelta(days=1)
    return B10[-1]

def class_inputs(api_object):
    inputs = dict(vars(api_object))
    del inputs['_key']
    del inputs['_secret']
    return inputs # json.dumps(inputs, indent=4)

def save_df_info(df):
    buffer = io.StringIO()
    df.info(buf=buffer)
    return buffer.getvalue()