from datetime import datetime, timedelta
from time import sleep, time
from utilities.config import CHECK_SAFE_DATE_TIME, TIMEZONE, WEEK_RANGE
import pytz


def get_next_day(current_day):
    diff = timedelta(days=1)
    current_day += diff
    return current_day


def get_datetime_from_string(obj, time_string):

    set_time = datetime.strptime(time_string, '%H:%M')
    new_obj = obj.replace(hour=set_time.hour, minute=set_time.minute, second=0)

    return new_obj


def localize_datetime(obj):
    tz = pytz.timezone(TIMEZONE)
    return tz.localize(obj)


def get_prev_day(current_day):
    diff = timedelta(days=1)
    current_day -= diff
    return current_day


def get_now():
    return datetime.now()


def get_today():
    return datetime.today()


def get_safe_today():
    tod = get_today()
    temp = get_datetime_from_string(tod, CHECK_SAFE_DATE_TIME)
    if tod < temp:
        return get_prev_day(tod)
    else:
        return tod


def get_time():
    return datetime.now().time().strftime('%H:%M:%S')


def add_seconds_to_datetime(obj, seconds):
    return obj + timedelta(seconds=seconds)


def alarm(proc_name, set_time):
    print "Alarm set for '" + proc_name + "' at " + str(set_time)
    while True:
        if datetime.now() >= set_time:
            break
        remain = set_time - datetime.now()
        sleep(remain.seconds)
    print "Alarm Rings..."


def get_date_string(date_obj):
    date_string = date_obj.strftime('%d-%m-%Y')
    return date_string


def get_date_time_string(datetime_obj):
    return datetime_obj.strftime('%d-%m-%Y %H:%M')


def get_tweet_date_time_string(datetime_obj):
    return datetime_obj.strftime('%b %d %H:%M')


def get_week_start(obj):
    return obj - timedelta(days=(WEEK_RANGE - 1))


def convert_datetime_to_local(obj):
    tz = pytz.timezone(TIMEZONE)
    return obj.astimezone(tz)


def get_differenced_day(current_day, days_delta):
    diff = timedelta(days=days_delta)
    differenced_day = current_day + diff
    return differenced_day


# %%%%%%%%%%%%%%%%%%%%%%%%% EXECUTION TIME FUNCTIONS %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
# TODO this works only in series, implement process,thread independent timing

start_time = None
end_time = None


def time_taken():
    global start_time, end_time
    seconds = end_time - start_time
    minutes = seconds/60
    hours = int(minutes/60)
    minutes = int(minutes - hours*60)
    seconds = int(seconds - minutes*60 - hours*60*60)

    print 'Time to execute = ' + str(hours) + ':' + str(minutes) + ':' + str(seconds)


def start_timing():
    global start_time
    start_time = time()


def stop_timing():
    global end_time
    end_time = time()
    time_taken()
