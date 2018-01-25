import calendar
import datetime
import json
import logging
import re
from os.path import join

from utils import jalali

logger = logging.getLogger(__name__)


def get_workday_count(start_date, end_date):
    """
    Returns the number of workdays in the given period
    :param start_date:
    :param end_date:
    :return: number of workdays
    """
    g_start = jalali.Persian(start_date).gregorian_datetime()
    g_end = jalali.Persian(end_date).gregorian_datetime()

    # print("Start:" + str(g_start))
    # print("End:" + str(g_end))

    data_path = '../data'
    events_path = join(data_path, 'events.json')
    holiday_count = 0
    week = {}
    with open(events_path, 'rt', encoding='utf-8') as events_file:
        holidays = json.load(events_file)
        for record in holidays["events"]:
            record_year = record['year']
            record_month = record['month']
            record_day = record['day']
            if record['year'] == -1:
                m = re.match(r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$', start_date)
                if m:
                    record_year = int(m.group(1))
            record_date = jalali.Persian(record_year, record_month, record_day)
            if record_date and g_start <= record_date.gregorian_datetime() <= g_end:
                # print(record_date.gregorian_datetime())
                if record['holiday']:
                    holiday_count += 1

    for i in range((g_end - g_start).days):
        day = calendar.day_name[(g_start + datetime.timedelta(days=i + 1)).weekday()]
        week[day] = week[day] + 1 if day in week else 1
    # print("Holiday:" + str(holiday_count))
    fridays = 0
    if 'Friday' in week:
        fridays = week['Friday']
        # print("Friday:" + str(week['Friday']))
    return (g_end - g_start).days + 1 - (holiday_count + fridays)


if __name__ == '__main__':
    logging.basicConfig(filename='../logs/utils_time.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    print(get_workday_count("1396/11/21", "1396/11/22"))
