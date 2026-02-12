from fastapi import FastAPI, UploadFile, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import logging
import os

from tenants.manager import tm
from core.retriever import SimpleRetriever, chunk_text, weave_answer
from core.ratelimit import limiter
from core.subscription import subs
from core.audit import auditor
from contracts.engine import engine
from explain.trace import build_trace
from explain.scores import confidence_from_parts
from ethics.judge import judge
from identity.passport import passport
from swarm.session import run as swarm_run
from api_trust import router as trust_router

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Instant-RAG Platform",
    description="Production-ready multi-tenant RAG system",
    version="1.0.0"
)

# ─── Public Site + Agent Discovery ───────────────────────────────────────
from fastapi.staticfiles import StaticFiles

# Ensure required folders exist
os.makedirs("static/.well-known", exist_ok=True)

# Serve machine discovery files FIRST
app.mount(
    "/.well-known",
    StaticFiles(directory="static/.well-known"),
    name="wellknown"
)

# Serve landing page and public assets
app.mount(
    "/",
    StaticFiles(directory="static", html=True),
    name="public"
)
# ─────────────────────────────────────────────────────────────────────────

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include trust router
app.include_router(trust_router)

# ─── Models ──────────────────────────────────────────────────────────────

class QueryRequest(BaseModel):
    text: str = Field(..., max_length=10000, min_length=1)
    agent_id: str = Field(..., min_length=1, max_length=100)
    token: str = Field(..., min_length=1)

class IngestRequest(BaseModel):
    agent_id: str = Field(..., min_length=1, max_length=100)
    token: str = Field(..., min_length=1)

# ─── Core Endpoints ──────────────────────────────────────────────────────

@app.get("/health")
def health():
    return {"status": "ok", "version": "1.0.0"}

@app.post("/ingest")
async def ingest(file: UploadFile, agent_id: str, token: str):
    try:
        if not passport.verify(agent_id, token):
            raise HTTPException(status_code=401, detail="invalid_passport")

        if subs.check(agent_id) != "active":
            raise HTTPException(status_code=403, detail="subscription_inactive")

        tenant = tm.get(agent_id)

        try:
            content = await file.read()
            text = content.decode("utf-8")
        except UnicodeDecodeError:
            raise HTTPException(status_code=400, detail="file_must_be_utf8_text")

        chunks = chunk_text(text)
        tenant.retriever.add_documents(chunks, source_name=file.filename)

        auditor.record("ingest", agent_id, {
            "chunks": len(chunks),
            "filename": file.filename,
            "size": len(text)
        })

        return {
            "status": "indexed",
            "chunks": len(chunks),
            "filename": file.filename
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during ingestion: {str(e)}")
        raise HTTPException(status_code=500, detail="ingestion_failed")

@app.post("/query")
async def query(request: QueryRequest):
    try:
        if not passport.verify(request.agent_id, request.token):
            raise HTTPException(status_code=401, detail="invalid_passport")

        if subs.check(request.agent_id) != "active":
            raise HTTPException(status_code=403, detail="subscription_inactive")

        ok, reason = judge.inspect(request.text)
        if not ok:
            auditor.record("ethics_block", request.agent_id, {
                "query": request.text[:120],
                "reason": reason
            })
            raise HTTPException(status_code=400, detail=f"ethics_block: {reason}")

        if not limiter.allow(request.agent_id):
            raise HTTPException(status_code=429, detail="rate_limited")

        tenant = tm.get(request.agent_id)
        results, cites, scores = tenant.retriever.search(request.text)

        trace = build_trace(request.text, results, scores)
        packet = weave_answer(results, cites)

        packet["explanation"] = trace
        packet["confidence"] = confidence_from_parts(
            0.7,
            max(scores) if scores else 0,
            len(cites)
        )

        auditor.record("query", request.agent_id, {
            "q": request.text[:120],
            "results": len(results),
            "confidence": packet["confidence"]
        })

        return packet

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during query: {str(e)}")
        raise HTTPException(status_code=500, detail="query_failed")

@app.post("/swarm/query")
async def swarm_query(request: QueryRequest):
    try:
        if not passport.verify(request.agent_id, request.token):
            raise HTTPException(status_code=401, detail="invalid_passport")

        if subs.check(request.agent_id) != "active":
            raise HTTPException(status_code=403, detail="subscription_inactive")

        async def query_fn(text: str):
            q = QueryRequest(
                text=text,
                agent_id=request.agent_id,
                token=request.token
            )
            return await query(q)

        result = await swarm_run(request.text, query_fn)

        auditor.record("swarm_query", request.agent_id, {
            "q": request.text[:120]
        })

        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during swarm query: {str(e)}")
        raise HTTPException(status_code=500, detail="swarm_query_failed")

@app.get("/stats/{agent_id}")
async def get_stats(agent_id: str, token: str):
    try:
        if not passport.verify(agent_id, token):
            raise HTTPException(status_code=401, detail="invalid_passport")

        tenant = tm.get(agent_id)
        logs = auditor.read_all()

        agent_logs = [l for l in logs if l.get("agent") == agent_id]

        return {
            "agent_id": agent_id,
            "total_queries": len([l for l in agent_logs if l.get("event") == "query"]),
            "total_ingestions": len([l for l in agent_logs if l.get("event") == "ingest"]),
            "total_documents": len(tenant.retriever.docs)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail="stats_failed")

# ─── Crypto Wallet Endpoints ─────────────────────────────────────────────

from payments.ledger import balance, spend
from payments.pricing import prices

@app.get("/wallet/balance")
def get_balance(agent_id: str):
    return {"balance": balance(agent_id)}

@app.post("/wallet/spend")
def wallet_spend(agent_id: str, action: str):
    cost = prices.get(action)

    if cost is None:
        return {"error": "unknown_action"}

    if not spend(agent_id, cost):
        return {"error": "insufficient_funds"}

    return {"status": "ok"}

# ─── Dashboard ───────────────────────────────────────────────────────────

from dashboard import router as admin_router
app.include_router(admin_router)

@app.get("/ready")
async def ready():
    return {"status": "ok"}

# ─── Run ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
