from langchain.retrievers import EnsembleRetriever
from langchain.retrievers import BM25Retriever, VectorStoreRetriever
# from langchain.vectorstores import Chroma # Example

def setup_hybrid_search(documents, embeddings, vector_store_cls):
    # Keyword retriever (BM25/TF-IDF)
    bm25 = BM25Retriever.from_documents(documents)
    bm25.k = 10

    # Semantic retriever (vector similarity)
    # vector_store = vector_store_cls.from_documents(documents, embeddings)
    # semantic = vector_store.as_retriever(search_kwargs={"k": 10})
    
    # Placeholder for actual vector store instance passed or created
    # semantic = ...

    # Combine with weights
    ensemble = EnsembleRetriever(
        retrievers=[bm25, semantic],
        weights=[0.3, 0.7]  # tune based on query type
    )

    return ensemble

# query_result = ensemble.get_relevant_documents(query)

# When to use:
# - Keyword search: Exact matches, names, codes, IDs
# - Semantic search: Conceptual similarity, paraphrasing
# - Hybrid: Most production use cases (best of both)
