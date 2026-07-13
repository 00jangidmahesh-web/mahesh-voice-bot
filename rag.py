"""
Builds (or loads) a persistent Chroma vectorstore over Mahesh's persona
knowledge base, so new sections/projects can be added later just by
editing data/mahesh_profile.txt and restarting the app — no code changes.
"""

import os

from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "data", "mahesh_profile.txt")
PERSIST_DIR = os.path.join(BASE_DIR, "chroma_db")

EMBEDDING_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL", "text-embedding-3-small")


def _build_vectorstore(embeddings: OpenAIEmbeddings) -> Chroma:
    loader = TextLoader(DATA_PATH, encoding="utf-8")
    docs = loader.load()

    # Headings ("## ...") mark natural topic boundaries in the profile doc,
    # so chunk generously and let overlap protect context at the edges.
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=900,
        chunk_overlap=150,
        separators=["\n## ", "\n### ", "\n\n", "\n", " "],
    )
    chunks = splitter.split_documents(docs)

    return Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        persist_directory=PERSIST_DIR,
        collection_name="mahesh_profile",
    )


def get_vectorstore() -> Chroma:
    """Load the persisted vectorstore if present, otherwise build it fresh.

    Rebuilding is triggered automatically whenever mahesh_profile.txt is
    newer than the persisted DB, so editing the profile and restarting the
    app is enough to pick up changes.
    """
    embeddings = OpenAIEmbeddings(model=EMBEDDING_MODEL)

    needs_rebuild = True
    if os.path.isdir(PERSIST_DIR) and os.listdir(PERSIST_DIR):
        db_mtime = os.path.getmtime(PERSIST_DIR)
        data_mtime = os.path.getmtime(DATA_PATH)
        needs_rebuild = data_mtime > db_mtime

    if needs_rebuild:
        return _build_vectorstore(embeddings)

    return Chroma(
        persist_directory=PERSIST_DIR,
        embedding_function=embeddings,
        collection_name="mahesh_profile",
    )
