
import json, os
class SemanticCache:
    def __init__(self, path="data/cache.json"):
        self.path = path
        self.db = []
        if os.path.exists(path):
            self.db = json.load(open(path))
    def find(self, v): return None
    def store(self, v, r): pass
