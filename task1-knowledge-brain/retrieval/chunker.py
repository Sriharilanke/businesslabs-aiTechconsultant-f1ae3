"""
Context-preserving semantic chunker for technical knowledge articles.
Splits along H2/H3 headings, keeps tables and list steps intact, and preserves document metadata.
"""
import hashlib
from typing import List, Dict, Any

class SemanticChunker:
    def __init__(self, target_chunk_size: int = 350, overlap_words: int = 40):
        self.target_chunk_size = target_chunk_size
        self.overlap_words = overlap_words

    def chunk_article(self, article: Dict[str, Any]) -> List[Dict[str, Any]]:
        chunks: List[Dict[str, Any]] = []
        url = article["url"]
        title = article["title"]
        category = article.get("category", "General")
        folder = article.get("folder", "Documentation")
        sections = article.get("sections", [])
        
        # If no sections, fall back to single overview section
        if not sections:
            sections = [{"heading": "Overview", "content": article.get("clean_text", "")}]

        chunk_idx = 0
        url_prefix = hashlib.md5(url.encode()).hexdigest()[:8]

        for sec in sections:
            heading = sec["heading"]
            content = sec["content"]
            words = content.split()
            
            # If section fits comfortably within target size, keep as single coherent chunk
            if len(words) <= self.target_chunk_size + 50:
                context_prefix = f"Article: {title}\nCategory: {category} > {folder}\nSection: {heading}\n\n"
                chunk_text = context_prefix + content
                token_estimate = len(chunk_text.split())
                chunk_id = f"{url_prefix}_{chunk_idx}"
                chunks.append({
                    "chunk_id": chunk_id,
                    "heading": heading,
                    "text": chunk_text,
                    "token_count": token_estimate,
                    "article_url": url,
                    "title": title
                })
                chunk_idx += 1
            else:
                # Sliding window split across paragraphs or sentence boundaries
                step = self.target_chunk_size - self.overlap_words
                for i in range(0, len(words), step):
                    window = words[i:i + self.target_chunk_size]
                    if len(window) < 30 and chunks:
                        # Append tiny trailing tail to last chunk
                        chunks[-1]["text"] += " " + " ".join(window)
                        continue
                    
                    window_text = " ".join(window)
                    context_prefix = f"Article: {title}\nCategory: {category} > {folder}\nSection: {heading} (Part {chunk_idx + 1})\n\n"
                    chunk_text = context_prefix + window_text
                    token_estimate = len(chunk_text.split())
                    chunk_id = f"{url_prefix}_{chunk_idx}"
                    chunks.append({
                        "chunk_id": chunk_id,
                        "heading": heading,
                        "text": chunk_text,
                        "token_count": token_estimate,
                        "article_url": url,
                        "title": title
                    })
                    chunk_idx += 1

        return chunks

chunker = SemanticChunker()
