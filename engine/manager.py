import subprocess
from multiprocessing import Process, Value
from os import remove

from utilities.config import *
from utilities.os_util import *
from utilities.time_management import *
from utilities.constants import *


TODAY = get_today()
TOMORROW = get_next_day(TODAY)
STOP_TIME = None
RESTART_TIME = None

ROOT = get_dir(__file__)
PROJECT_ROOT = dirname(ROOT)

EXTRACTOR_SCRIPT_PATH = join(ROOT, EXTRACTOR_DIR, EXTRACTOR)
EXTRACTOR_DATA_PATH = join(ROOT, EXTRACTOR_DIR, DATA_DIR)
PROCESS_SCRIPT_PATH = join(ROOT, PROCESSOR_DIR, PROCESSOR)
MODELLER_PROCESS_SCRIPT_PATH = join(ROOT, TOPIC_MODELLER_DIR, MODELLER)
PORTAL_PROCESS_SCRIPT_PATH = join(PROJECT_ROOT, WEBSITE_DIR, DJANGO_MANAGER)


def cleanup():

    print 'Cleaning up breadcrumbs... ',
    deleted = False
    while not deleted:
        try:
            data_files = get_files_in_dir(EXTRACTOR_DATA_PATH, JSON)

            for data_file in data_files:
                remove(join(EXTRACTOR_DATA_PATH, data_file))
            deleted = True

        except: None

    print 'Cleaned'


def data_extraction():
    print 'Starting Extractor... ',
    extractor = subprocess.Popen(['python', EXTRACTOR_SCRIPT_PATH], creationflags=subprocess.CREATE_NEW_CONSOLE)
    print 'Started with PID ' + str(extractor.pid)
    return extractor


def data_processing(stop_bool, stop_time):

    next_stop = get_now()
    while stop_bool.value == 0:
        next_stop = min(add_seconds_to_datetime(next_stop, PROCESSOR_SLEEP_TIME), stop_time)
        print 'Processor started sleeping at ' + get_time()
        alarm(PROCESSOR_PROCESS, next_stop)
        print 'Processor Woke Up!!!'
        print 'Starting Processor... ',
        processor = subprocess.Popen(['python', PROCESS_SCRIPT_PATH])
        print 'Started with PID ' + str(processor.pid)
        processor.wait()


def lda_process():
    print 'Starting Topic Modeller... ',
    topic_modeller = subprocess.Popen(['python', MODELLER_PROCESS_SCRIPT_PATH])
    print 'Started with PID ' + str(topic_modeller.pid)
    return topic_modeller


def start_portal():
    print 'Starting Django Manager... ',
    django_manager = subprocess.Popen(['python', PORTAL_PROCESS_SCRIPT_PATH, RUNSERVER_COMMAND], creationflags=subprocess.CREATE_NEW_CONSOLE)
    print 'Started with PID ' + str(django_manager.pid)
    return django_manager


if __name__ == '__main__':

    lda_subprocess = None
    portal_subprocess = None

    while True:  # run everyday
        STOP_TIME = get_datetime_from_string(TODAY, STOP_DATA_EXTRACTION_TIME)
        RESTART_TIME = get_datetime_from_string(TOMORROW, RESTART_DATA_EXTRACTION_TIME)

        stop_processor = Value('i', 0)
        extractor_pid = Value('i', 0)

        extractor = data_extraction()
        processor = Process(target=data_processing, args=(stop_processor, STOP_TIME,))

        processor.start()

        if lda_subprocess:
            lda_subprocess.wait()

        portal_subprocess = start_portal()

        alarm(MANAGER_PROCESS, STOP_TIME)

        kill_process_tree(extractor.pid)
        cleanup()

        stop_processor.value = 1
        processor.join()
        print 'Processor exiting...'

        print 'Stopping portal... ',
        kill_process_tree(portal_subprocess.pid)
        print 'Stopped'
        lda_subprocess = lda_process()

        if DEBUG:
            lda_subprocess.wait()
            break

        alarm(MANAGER_PROCESS, RESTART_TIME)
        print 'Restarting scripts!!! '
        TODAY = TOMORROW
        TOMORROW = get_next_day(TODAY)

