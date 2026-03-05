import math
import re
from collections import Counter

from src.config import TOP_K

STOPWORDS = {
    "a", "an", "the", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did", "will", "would", "shall",
    "should", "may", "might", "must", "can", "could", "to", "of", "in",
    "for", "on", "with", "at", "by", "from", "as", "into", "through",
    "and", "but", "or", "nor", "not", "so", "yet", "both", "either",
    "neither", "each", "every", "all", "any", "few", "more", "most",
    "other", "some", "such", "no", "only", "own", "same", "than", "too",
    "very", "just", "about", "above", "after", "again", "below", "between",
    "during", "before", "if", "it", "its", "this", "that", "these", "those",
    "what", "which", "who", "whom", "how", "when", "where", "why",
}


def _tokenize(text):
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in STOPWORDS and len(w) > 1]


def retrieve_top_k(query, documents, k=TOP_K):
    all_chunks = []
    for doc in documents:
        if not doc.get("active", True):
            continue
        for chunk in doc.get("chunks", []):
            all_chunks.append({
                "text": chunk["text"],
                "page": chunk.get("page"),
                "source": doc["filename"],
            })

    if not all_chunks:
        return []

    query_tokens = _tokenize(query)
    if not query_tokens:
        return []

    # Compute IDF for query tokens
    doc_freq = Counter()
    for chunk in all_chunks:
        chunk_tokens = set(_tokenize(chunk["text"]))
        for qt in query_tokens:
            if qt in chunk_tokens:
                doc_freq[qt] += 1

    n = len(all_chunks)
    idf = {}
    for token in query_tokens:
        df = doc_freq.get(token, 0)
        idf[token] = math.log((n + 1) / (df + 1)) + 1 if df > 0 else 0

    # Score each chunk
    scored = []
    for chunk in all_chunks:
        chunk_tokens = set(_tokenize(chunk["text"]))
        score = sum(idf.get(qt, 0) for qt in query_tokens if qt in chunk_tokens)
        if score > 0:
            scored.append({**chunk, "score": score})

    scored.sort(key=lambda x: x["score"], reverse=True)
    return scored[:k]
