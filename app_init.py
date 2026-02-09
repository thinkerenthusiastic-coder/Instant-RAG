
from core.semantic_cache import SemanticCache
from functions.retry_queue import start as start_queue
from identity.oauth import verify

cache = SemanticCache()

def boot(app):
    start_queue()
    app.state.cache = cache

def auth(req):
    t = req.headers.get("Authorization","").replace("Bearer ","")
    a = verify(t)
    if not a:
        from fastapi import HTTPException
        raise HTTPException(401,"invalid token")
    return a
