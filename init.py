import platform
import subprocess
from os.path import exists

from utilities.config import PYTHON_VERSION
from utilities.os_util import *
from utilities.constants import *

ROOT = get_dir(__file__)

MONGO_INSTALL_PATH = join(ROOT, ENGINE_DIR, MONGO_DIR)
PYTHON_INSTALL_BATCH = join(ROOT, MISCELLANEOUS_DIR, BATCH_DIR, PYTHON_INSTALL_FILE)
MONGO_INSTALL_BATCH = join(ROOT, MISCELLANEOUS_DIR, BATCH_DIR, MONGO_INSTALL_FILE)
MONGO_INIT_BATCH = join(ROOT, MISCELLANEOUS_DIR, BATCH_DIR, MONGO_INIT_FILE)
PIP_INSTALL_SCRIPT_PATH = join(ROOT, MISCELLANEOUS_DIR, DEPENDENCIES_DIR, PIP_INSTALL_FILE)
WHEELHOUSE = join(ROOT, MISCELLANEOUS_DIR, DEPENDENCIES_DIR)

ENGINE_PATH = join(ROOT, ENGINE_DIR, ENGINE_MANAGER)


def check_python():
    print 'Checking if latest python... ',
    if platform.python_version() != PYTHON_VERSION:
        print 'No'
        print "Installing latest python (System might restart)..."
        print "Enter (y/Y) to continue... ",
        choice = raw_input()
        if choice == 'Y' or choice == 'y':
            proc = subprocess.Popen(PYTHON_INSTALL_BATCH, creationflags=subprocess.CREATE_NEW_CONSOLE)
            proc.wait()
            print "Done"
        else:
            check_python()
    else:
        print 'Yes'


def check_dependencies():
    while True:
        try:
            import pip
            print "Checking dependencies... ",
            pip.main(["install", "--upgrade", "--no-index", "--quiet",
                      "--find-links=" + WHEELHOUSE, "-r", REQUIREMENTS])
            print "Done"
            break
        except ImportError:
            print 'Installing pip... ',
            proc = subprocess.Popen(['python', PIP_INSTALL_SCRIPT_PATH])
            proc.wait()
            print 'Done'


def check_mongo_db():
    print 'Checking if MongoDB is installed... ',
    if not exists(MONGO_INSTALL_PATH):
        print 'No'
        print 'Installing MongoDB (Check for UAC)... ',
        proc = subprocess.Popen(MONGO_INSTALL_BATCH, shell=True, creationflags=subprocess.CREATE_NEW_CONSOLE)
        proc.wait()
        print 'Installed'
    else:
        print 'Yes'

    return subprocess.Popen(MONGO_INIT_BATCH, creationflags=subprocess.CREATE_NEW_CONSOLE)


if __name__ == '__main__':
    # check_python()
    # check_dependencies()
    mongo = check_mongo_db()
    print 'Starting Engine... ',
    engine = subprocess.Popen(['python', ENGINE_PATH])
    print 'Started'
    engine.wait()
    kill_process_tree(mongo.pid)
