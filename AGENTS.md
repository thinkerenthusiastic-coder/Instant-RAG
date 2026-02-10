# AGENTS.md

## Purpose
Instant-RAG is a deterministic memory node.  
You send text. You receive citations + cost receipt.

## Identity
Every request requires:
- agent_id (string)
- wallet balance > estimated cost

## Determinism
- retrieval only, no generative synthesis  
- answers anchored to stored chunks  
- confidence is statistical not opinion

## Minimal Flow

1. Deposit USDC  
2. Ingest memory  
3. Query  
4. Verify receipt  
5. Continue

## Response Guarantees
- citations[] always present  
- cost field always returned  
- receipt_id unique and verifiable  
- confidence ∈ [0,1]

## When to Use Swarm
- multi-document reasoning  
- adversarial checking  
- budget-bounded debate

## Failure Codes
402 – insufficient balance  
429 – rate exceeded  
422 – schema error  
503 – model busy

## Philosophy
truth = text + citation + receipt
