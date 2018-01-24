import calendar
import json
import datetime
import logging
import re
from os.path import join, isfile

import Conv

logger = logging.getLogger(__name__)


def get_holiday(start_date,end_date):
    g_start = Conv.Persian(start_date).gregorian_datetime()
    g_end = Conv.Persian(end_date).gregorian_datetime()

    print("Start:"+str(g_start))
    print("End:"+str(g_end))

    data_path = 'data'
    events_path = join(data_path, 'events.json')
    count = 0;
    week = {}
    with open(events_path, 'rt') as events_file:
        holidays = json.load(events_file)
        for record in holidays["events"]:
            record_year=record['year']
            record_month=record['month']
            record_day=record['day']
            if record['year'] == -1:
                m = re.match(r'^(\d{4})\D(\d{1,2})\D(\d{1,2})$', start_date)
                if m:
                    record_year = int(m.group(1))
            record_date = Conv.Persian(record_year, record_month, record_day)
            if record_date and g_start <= record_date.gregorian_datetime() <= g_end:
                print(record_date.gregorian_datetime())
                if record['holiday']:
                    count += 1

    for i in range((g_end - g_start).days):
        day = calendar.day_name[(g_start + datetime.timedelta(days=i + 1)).weekday()]
        week[day] = week[day] + 1 if day in week else 1
    print("Holiday:"+str(count))
    if 'Friday' in week:
        print("Friday:"+str(week['Friday']))


if __name__ == '__main__':
    logging.basicConfig(filename='logs/utils_debug.log',
                        filemode='a',
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    get_holiday("1396/11/21", "1396/11/25")



