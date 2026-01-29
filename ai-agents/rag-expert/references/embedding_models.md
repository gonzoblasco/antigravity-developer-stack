# Embedding Model Selection

Different models are optimized for different use cases. Benchmarking on your specific data is crucial.

| Category         | Model                    | Description                         | Use Case                  |
| :--------------- | :----------------------- | :---------------------------------- | :------------------------ |
| **General**      | `text-embedding-3-small` | Fast, good quality, cost-effective  | Standard RAG, high volume |
| **High Quality** | `text-embedding-3-large` | Best semantic understanding         | Complex reasoning, nuance |
| **Multilingual** | `multilingual-e5-large`  | Strong cross-language performance   | International support     |
| **Code**         | `code-search-ada-002`    | Optimized for code syntax/semantics | Codebases, technical docs |

## Selection Strategy

```python
# Different models for different use cases
models = {
    "general": "text-embedding-3-small",      # Fast, good quality
    "high_quality": "text-embedding-3-large", # Best quality
    "multilingual": "multilingual-e5-large",  # Cross-language
    "code": "code-search-ada-002"             # Code-specific
}

# Benchmark on your data
# evaluate_embeddings(models, test_queries, test_docs)
```

## Key Considerations

- **Dimension Size**: Larger dimensions = better quality but higher storage/latency costs.
- **Context Length**: Ensure the model supports your chunk size.
- **Language Support**: Don't use English-only models for multilingual data.
