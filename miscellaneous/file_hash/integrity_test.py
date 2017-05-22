import json
import hashlib
from os import listdir
from os.path import isfile, join
from colors import ColorCodes as C

path = join('..','data') # path where the files to be checked are

def getHash(fname): # returns SHA-256 hash of the file with fname as its path
    hash = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
        f.close()
    return hash.hexdigest()


if __name__ == '__main__':

    dict = {}
    with open('SHA256_hashes.json') as f:
        dict = json.load(f)

    files = [ f for f in listdir(path) if isfile(join(path,f)) ]
    total = 0
    correct = 0
    errors = []

    for file in files:
        if file in dict.keys():
            total+=1
            print 'Checking ' + file + '... ',
            SHAhash = getHash(join(path,file))
            if SHAhash == dict[file]:
                print  'SUCCESS' 
                correct+=1
            else:
                errors.append(file)
                print 'FAILURE' 
    print
    print str(correct) + ' out of ' + str(total) + ' files have '  + 'passed'  + ' the test'
    if correct != total:
        print
        print 'Following files have '  + 'failed'  + ' the test: '
        for file in errors:
            print '\t'  + file 