
import json, os
PATH="data/hooks.json"
def register(url):
    d=[]
    if os.path.exists(PATH): d=json.load(open(PATH))
    d.append(url); json.dump(d, open(PATH,'w'))
