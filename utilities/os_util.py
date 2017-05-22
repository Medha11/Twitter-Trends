from os.path import isfile, dirname, realpath, join, splitext
from os import listdir


def get_dir(filename):
    return dirname(realpath(filename))


def get_files_in_dir(directory, ext=None):
    if ext:
        files = [f for f in listdir(directory) if splitext(f)[1] == ext and isfile(join(directory, f))]
    else:
        files = [f for f in listdir(directory) if isfile(join(directory, f))]

    return files


def kill_process_tree(pid):
    import psutil
    proc = psutil.Process(pid)
    for child in proc.children():
        child.kill()
    proc.kill()


