import json
import hashlib
from os import listdir
from os.path import isfile, join

path = join('..','data') #folder containing files

def getHash(fname):
    hash = hashlib.sha256()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash.update(chunk)
        f.close()
    return hash.hexdigest()

if __name__ == '__main__':


    dict = {}

    try:
        with open('SHA256_hashes.json') as f:
            dict = json.load(f)
    except: None

    files = [ f for f in listdir(path) if isfile(join(path,f)) ] #getting all file names

    l = len(files) - len(dict)
    c=0
    per = 10
    if l>0:
        for file in files:
            
            try:
                dict[file]
            except:
                c+=1
                dict[file] = getHash(join(path,file))
            if (c*100)/l >= per:            
                print str(per) + '% done'
                per+=10

            
    with open('SHA256_hashes.json', 'w') as f:
        json.dump(dict, f)