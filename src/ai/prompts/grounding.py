import streamlit as st
from src.docs.store import get_active_documents
from src.docs.retriever import retrieve_top_k


def build_grounding_context(user_input):
    documents = get_active_documents()
    if not documents:
        return ""

    chunks = retrieve_top_k(user_input, documents)
    if not chunks:
        return ""

    sources = set(c["source"] for c in chunks)
    st.info(f"Using {len(chunks)} reference(s) from: {', '.join(sources)}")

    formatted = []
    for chunk in chunks:
        source = chunk["source"]
        page = chunk.get("page")
        header = f"--- Reference: {source}, p.{page} ---" if page else f"--- Reference: {source} ---"
        formatted.append(f"{header}\n{chunk['text']}\n")

    refs = "\n".join(formatted)
    return (
        f"\n\nReference Context (from uploaded documents):\n{refs}\n"
        "When you use information from the reference context above, "
        "cite the source as [Source: filename.ext] or [Source: filename.ext, p.N] "
        "if page information is available. If the reference context is not relevant "
        "to the query, ignore it and do not force citations."
    )
