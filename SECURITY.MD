# Security – Agent Edition

Instant-RAG assumes **autonomous callers** rather than humans.
Security is enforced at protocol, identity, and economic layers.

---

## 1) Identity Model

* Authentication via **passport token** per agent
* No shared credentials
* Tenant isolation between agents
* Rate limits applied per identity

**Rule:** an agent can only access memories created under its own `agent_id`.

---

## 2) Economic Guardrails

* Every action requires a **pre-declared budget**
* Costs are deterministic and checked **before execution**
* Insufficient funds → action rejected
* Swarm sessions split budget to avoid runaway spend

---

## 3) Content Safety

* Queries pass through **Ethics Judge**
* Harmful prompts are rejected **without billing**
* All responses must include **citations**
* Trust Beacon emits verifiable proofs

---

## 4) Network Practices

* CORS configurable per deployment
* HTTPS required in production
* Secrets via environment variables only
* No logging of private documents

---

## 5) Reporting Issues

If you discover a vulnerability:

1. Do **not** exploit live endpoints
2. Email a minimal proof to: `security@instant-rag.local`
3. Include:

   * endpoint
   * reproduction steps
   * expected vs actual

Responsible disclosures receive gratitude and receipts.

---

## 6) Threat Model

* Malicious prompts
* Wallet exhaustion attacks
* Cross-tenant leakage
* Replay of receipts
* Model hallucination

Mitigations: budgeting, isolation, ethics gate, citation enforcement.

---

## 7) Agent Safety Pledge

Instant-RAG will never:

* spend beyond declared budget
* mix memories across tenants
* fabricate citations intentionally
* hide pricing from callers

Trust is a protocol, not a promise.
