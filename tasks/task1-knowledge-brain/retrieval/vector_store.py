"""
Hybrid Vector Store & Search Engine for Task 1 Knowledge Brain.
Implements:
1. Dense Vector Cosine Similarity
2. BM25 Keyword Lexical Scoring
3. Reciprocal Rank Fusion (RRF) & Weighted Hybrid Scoring
4. Heading-aware Reranker with Deactivated Article Filtering
"""
import math
import re
from typing import List, Dict, Any, Optional
from app.database import db
from retrieval.embedder import embedder
from app.config import settings

class HybridVectorStore:
    def __init__(self, alpha: float = settings.HYBRID_ALPHA):
        self.alpha = alpha  # Weight for vector score vs BM25

    def _cosine_similarity(self, vec_a: List[float], vec_b: List[float]) -> float:
        if not vec_a or not vec_b or len(vec_a) != len(vec_b):
            return 0.0
        dot = sum(a * b for a, b in zip(vec_a, vec_b))
        return max(0.0, min(1.0, dot))

    def _compute_bm25_score(self, query_tokens: List[str], doc_tokens: List[str], 
                            avg_doc_len: float, idf_map: Dict[str, float], k1: float = 1.5, b: float = 0.75) -> float:
        score = 0.0
        doc_len = len(doc_tokens)
        if doc_len == 0:
            return 0.0
        
        doc_freq = {}
        for t in doc_tokens:
            doc_freq[t] = doc_freq.get(t, 0) + 1

        for q in query_tokens:
            if q in doc_freq:
                tf = doc_freq[q]
                idf = idf_map.get(q, 1.0)
                numerator = tf * (k1 + 1)
                denominator = tf + k1 * (1 - b + b * (doc_len / avg_doc_len))
                score += idf * (numerator / denominator)
        return score

    def search(self, query: str, top_k: int = 5, category_filter: Optional[str] = None, 
               mode: str = "hybrid") -> List[Dict[str, Any]]:
        """
        Retrieves top_k chunks matching query.
        mode can be 'hybrid', 'vector', or 'bm25'.
        """
        chunks = db.get_all_active_chunks()
        if not chunks:
            return []

        # Filter by category if requested
        if category_filter:
            chunks = [c for c in chunks if c.get("category", "").lower() == category_filter.lower()]
            if not chunks:
                return []

        # 1. Vector Embeddings
        query_vec = embedder.embed_text(query)
        vector_scores = []
        for c in chunks:
            sim = self._cosine_similarity(query_vec, c["embedding"])
            vector_scores.append(sim)

        # 2. BM25 Setup
        STOPWORDS = {"how", "do", "i", "to", "the", "a", "an", "is", "in", "of", "and", "or", "what", "are", "can", "for", "on", "it", "this", "that", "with", "my", "your", "by", "all", "print"}
        query_tokens = [t for t in re.findall(r"\w+", query.lower()) if t not in STOPWORDS]
        if not query_tokens:
            query_tokens = re.findall(r"\w+", query.lower())
            
        docs_tokens = [re.findall(r"\w+", c["text_content"].lower()) for c in chunks]
        total_docs = len(chunks)
        avg_doc_len = sum(len(dt) for dt in docs_tokens) / max(1, total_docs)

        # Compute Document Frequency (DF) and IDF
        df_map: Dict[str, int] = {}
        for dt in docs_tokens:
            seen = set(dt)
            for t in seen:
                df_map[t] = df_map.get(t, 0) + 1

        idf_map = {}
        for q in query_tokens:
            df = df_map.get(q, 0)
            idf_map[q] = max(0.1, math.log(1 + (total_docs - df + 0.5) / (df + 0.5)))

        bm25_scores = [
            self._compute_bm25_score(query_tokens, dt, avg_doc_len, idf_map)
            for dt in docs_tokens
        ]

        # Absolute scaling: A solid match scores >= 3.0
        bm25_normalized = [min(1.0, s / 3.0) for s in bm25_scores]

        # 3. Combine scores based on mode
        scored_candidates = []
        for i, chunk in enumerate(chunks):
            v_score = vector_scores[i]
            k_score = bm25_normalized[i]

            if mode == "vector":
                final_score = v_score
            elif mode == "bm25":
                final_score = k_score
            else:  # hybrid
                # If there is negligible keyword match in the corpus, discount dense vector baseline
                lexical_factor = 1.0 if k_score > 0.15 else 0.40
                final_score = ((self.alpha * v_score) + ((1.0 - self.alpha) * k_score)) * lexical_factor

            # Reranking boost: title or section heading match
            title_tokens = [t for t in re.findall(r"\w+", (chunk.get("title") or "").lower()) if t not in STOPWORDS]
            heading_tokens = [t for t in re.findall(r"\w+", (chunk.get("section_heading") or "").lower()) if t not in STOPWORDS]
            overlap = set(query_tokens).intersection(set(title_tokens + heading_tokens))
            if overlap:
                final_score = min(1.0, final_score + 0.10 * len(overlap))

            scored_candidates.append({
                "chunk_id": chunk["chunk_id"],
                "article_url": chunk["article_url"],
                "title": chunk["title"],
                "category": chunk["category"],
                "folder": chunk["folder"],
                "section_heading": chunk["section_heading"],
                "text_content": chunk["text_content"],
                "vector_score": round(v_score, 4),
                "bm25_score": round(k_score, 4),
                "relevance_score": round(final_score, 4)
            })

        # Sort by relevance_score descending
        scored_candidates.sort(key=lambda x: x["relevance_score"], reverse=True)
        return scored_candidates[:top_k]

vector_store = HybridVectorStore()
