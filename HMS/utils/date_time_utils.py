import json
from datetime import datetime, time


def parse_schedule(schedule_str):
    schedule = json.loads(schedule_str)
    parsed_schedule = {}

    for day, periods in schedule.items():
        parsed_periods = []
        for period in periods:
            start_str, end_str = period.split("-")
            start_time = datetime.strptime(start_str, "%H:%M").time()
            end_time = datetime.strptime(end_str, "%H:%M").time()
            parsed_periods.append((start_time, end_time))
        parsed_schedule[day] = parsed_periods

    return parsed_schedule
