
import secrets
def create_agent(name, scopes=None):
    return {"client_id": secrets.token_hex(4), "client_secret": secrets.token_hex(8)}
def issue_token(cid, sec):
    return f"tok-{cid}"
def verify(t):
    return {"name":"demo"} if t else None
