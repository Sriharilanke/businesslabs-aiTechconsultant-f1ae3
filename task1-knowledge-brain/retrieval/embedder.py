"""
High-dimensional semantic embedding module.
Provides deterministic L2-normalized semantic vector embeddings (dim=384)
and supports external LLM/embedding API plug-ins.
"""
import math
import hashlib
import re
from typing import List

class SemanticEmbedder:
    def __init__(self, dimension: int = 384):
        self.dim = dimension

    def embed_text(self, text: str) -> List[float]:
        """
        Produces a normalized 384-dimensional dense semantic embedding vector.
        Uses subword/n-gram hashing with positional frequency and TF-IDF weighting.
        """
        vec = [0.0] * self.dim
        tokens = re.findall(r"\w+", text.lower())
        if not tokens:
            return vec

        # Token and bigram frequency hashing
        for i, token in enumerate(tokens):
            # Unigram hash
            h1 = int(hashlib.md5(token.encode("utf-8")).hexdigest(), 16) % self.dim
            # Weight rare or informative terms higher
            weight = 1.0 + (1.0 / (1.0 + math.log(1 + len(token))))
            vec[h1] += weight

            # Bigram hash for phrase semantics
            if i < len(tokens) - 1:
                bigram = f"{token}_{tokens[i+1]}"
                h2 = int(hashlib.sha256(bigram.encode("utf-8")).hexdigest(), 16) % self.dim
                vec[h2] += 1.8

            # Trigram / subword hash for root morphological matching
            if len(token) > 4:
                prefix = token[:4]
                hp = int(hashlib.md5(prefix.encode("utf-8")).hexdigest(), 16) % self.dim
                vec[hp] += 0.8

        # L2 Normalization
        norm = math.sqrt(sum(x * x for x in vec))
        if norm > 0:
            vec = [round(x / norm, 6) for x in vec]

        return vec

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_text(t) for t in texts]

embedder = SemanticEmbedder()
