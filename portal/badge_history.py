
import json, os
PATH="data/badge_history.json"
def timeline(agent=None):
    if os.path.exists(PATH): return json.load(open(PATH))
    return []
