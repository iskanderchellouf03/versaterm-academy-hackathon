import streamlit as st
from src.config import MAX_FILES


def get_documents():
    return st.session_state.get("uploaded_docs", [])


def get_active_documents():
    return [d for d in get_documents() if d.get("active", True)]


def add_document(filename, file_type, size, chunks):
    docs = get_documents()
    active_count = len([d for d in docs if d.get("active", True)])
    if active_count >= MAX_FILES:
        return f"Maximum of {MAX_FILES} files allowed. Remove a document first."
    docs.append({
        "filename": filename,
        "type": file_type,
        "size": size,
        "chunks": chunks,
        "active": True,
    })
    st.session_state["uploaded_docs"] = docs
    return None


def remove_document(filename):
    docs = get_documents()
    for doc in docs:
        if doc["filename"] == filename:
            doc["active"] = False
    st.session_state["uploaded_docs"] = docs
