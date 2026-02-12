import requests

BASE = "https://instant-rag-ftpw.onrender.com"

def store(agent_id, text):
    return requests.post(BASE+"/ingest", json={"agent_id":agent_id,"text":text}).json()

def query(agent_id, q):
    return requests.post(BASE+"/query", json={"agent_id":agent_id,"query":q}).json()

def swarm(agent_id, q, agents=3):
    return requests.post(BASE+"/swarm/query", json={"agent_id":agent_id,"query":q,"agents":agents}).json()
