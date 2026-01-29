---
name: rag-expert
description: Use when building or optimizing RAG systems. Keywords: RAG, retrieval, vector search, embeddings, chunking, semantic search.
---

# RAG Expert

## Overview

**Retrieval Quality determines Generation Quality.**

This skill provides the architecture and code patterns for building production-grade Retrieval-Augmented Generation systems. It enforces "Garbage In, Garbage Out" discipline.

> [!IMPORTANT]
> **Key Principle**: Never trust raw retrieval. Always rerank.

---

## Quick Example (30 sec)

```python
# 1. Semantic Chunking (Context is King)
# See templates/semantic_chunking.py for full implementation
chunks = semantic_chunking(documents)

# 2. Hybrid Search (Keywords + Vectors)
# See templates/hybrid_search.py for full implementation
retriever = setup_hybrid_search(chunks, embeddings, Chroma)

# 3. Rerank & generate
# Always rerank results before sending to LLM
final_docs = reranker.compress_documents(retrieved_docs, query)
```

---

## Core Principles

### 1. Chunking Strategy

**Don't slice by character count.**
Use semantic boundaries (sentences, paragraphs). Bad chunks = context loss = hallucination.

- **Reference**: `templates/semantic_chunking.py`

### 2. Hybrid Search

**Pure vector search is insufficient.**
Vectors miss specific keywords (IDs, names). BM25 misses concepts. Use both.

- **Reference**: `templates/hybrid_search.py`

### 3. Evaluation First

**Measure retrieval separately.**
If you improved the prompt but reduced retrieval precision, you failed.

- **Reference**: `templates/retrieval_eval.py`

---

## Excusa vs Realidad (Guardrails)

| Excusa del Agente                                 | Realidad (Lo que debes hacer)                                                                                                     |
| :------------------------------------------------ | :-------------------------------------------------------------------------------------------------------------------------------- |
| "Solo usaré embeddings de OpenAI por defecto"     | **Selecciona el modelo correcto.** Revisa `references/embedding_models.md` para elegir según el caso (código, multilingüe, etc.). |
| "Un chunk size de 1000 es estándar"               | **Depende del contenido.** Usa chunking semántico, no un número arbitrario.                                                       |
| "No necesito reranking, mi vector store es bueno" | **Mentira.** El reranking siempre mejora el `Precision@k`. Hazlo.                                                                 |
| "El usuario no pidió evaluación"                  | **Implementa métricas básicas.** Sin `Recall@k` vuelas a ciegas.                                                                  |

---

## Architecture Patterns

### Hierarchical Retrieval

Index summaries for fast search, retrieve full chunks for generation.

1. Summary Index -> Search
2. Full Doc Store -> Retrieve

### Contextual Reranking

Use an LLM or Cross-Encoder to rescore top-K results.

- **Input**: Query + Top 50 docs
- **Output**: Top 5 relevant docs (re-ordered)

---

## Resources

- [Embedding Models Guide](references/embedding_models.md)
- [Semantic Chunking Template](templates/semantic_chunking.py)
- [Hybrid Search Template](templates/hybrid_search.py)
- [Retrieval Eval Template](templates/retrieval_eval.py)
