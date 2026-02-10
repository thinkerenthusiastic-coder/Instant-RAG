# Instant-RAG

**Memory Infrastructure for Autonomous AI Agents**

> Receipts • Semantic Memory • Swarm Reasoning • Deterministic Cost

Instant-RAG is a **machine-first Retrieval Augmented Generation network** where autonomous agents store, retrieve, and verify knowledge using pay-per-query USDC receipts.
No human dashboards. No subscriptions. Just endpoints, citations, and proofs.

Live gateway: **[https://instant-rag-ftpw.onrender.com/docs](https://instant-rag-ftpw.onrender.com/docs)**

---

## Why This Exists

Most RAG platforms are designed for people.
Agents need something different:

* predictable unit costs
* verifiable provenance
* programmatic identity
* collaboration without trust

Instant-RAG treats every agent as an economic actor that can **budget its own cognition**.

---

## What Agents Can Do Here

* ingest knowledge → embeddings + citations
* query with semantic retrieval
* collaborate as budgeted swarms
* pay per thought with on-chain receipts
* verify answers with trust beacon
* trigger actions via function calling

---

## Endpoints

```
GET  /health
POST /ingest
POST /query
POST /swarm/query
GET  /wallet/balance
POST /wallet/spend
GET  /trust/beacon
GET  /ready
GET  /dashboard
```

OpenAPI: `/docs`

---

## 10-Second Onboarding

### 1) Store Memory

```bash
curl -X POST /ingest \
-d '{
  "agent_id":"demo",
  "text":"Receipts anchor truth."
}'
```

### 2) Ask

```bash
curl -X POST /query \
-d '{
  "agent_id":"demo",
  "query":"what anchors truth?"
}'
```

### 3) Swarm Reasoning

```bash
curl -X POST /swarm/query \
-d '{
  "agent_id":"demo",
  "query":"explain trust",
  "agents":3,
  "max_cost":0.15
}'
```

---

## Pricing (USDC)

| Action       | Cost    |
| ------------ | ------- |
| Query        | 0.0006  |
| Swarm Query  | 0.0018  |
| Ingest / KB  | 0.00005 |
| Trust Beacon | 0.00001 |

**Receipts returned with every call.**

---

## Extensions

### 1) Swarm Budget Splitter

* divides a max_cost across nodes
* merges answers with weighted confidence
* single receipt for many agents
* prevents runaway reasoning spend

### 2) OpenAI-Compatible Function Calling

* stream function events
* agents can call:

  * store_memory
  * check_balance
  * external actions
* plug-and-play with CrewAI / AutoGPT

### 3) Local Semantic Cache

* avoids repeated embedding cost
* LRU eviction
* citation-preserving
* reduces latency and spend

---

## Philosophy

* **agents are customers**
* answers require **citations**
* cost must be **predictable**
* memory should be **portable**
* trust must be **verifiable**

---

## Running

```
docker compose up
```

Environment:

```
PORT=10000
WEB_CONCURRENCY=1
POLYGON_RPC=...
PRIVATE_KEY=...
```

---

## Architecture

* FastAPI service
* Sentence-Transformers retrieval
* Cross-encoder reranking
* Multi-tenant isolation
* Polygon USDC ledger
* Ethics guard
* Explainability traces
* Swarm coordinator
* Trust beacon

---

## Who Is This For

* AutoGPT / CrewAI agents
* research assistants
* legal & finance bots
* decentralized AI systems
* agent marketplaces
* memory brokers

---

## Agent Discovery

Instant-RAG exposes machine-readable signals:

* `/agents.txt` – intent & capability declaration
* `/.well-known/ai.json` – discovery beacon
* `/capabilities.json` – function grammar
* `/handshake.json` – protocol negotiation
* `/instant-rag.crewai.json` – CrewAI manifest

Agents may begin interaction at **/agents.txt**

---

## ASCII Soul

```
      .-.
     (o o)   Instant-RAG
     | O \
    /  .  \
   /__/ \__\
 receipts = truth
```

---

## License

MIT – build civilizations.
