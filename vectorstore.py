import os
from typing import Optional, Dict, Any, List
from config import CHROMA_PERSIST_DIR, EMBEDDING_MODEL
import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

# Setup Chroma client
def get_chroma_client():
    # using duckdb+parquet local store (default)
    settings = Settings(persist_directory=CHROMA_PERSIST_DIR)
    return chromadb.Client(settings)

def get_collection(name: str = "style_memory"):
    client = get_chroma_client()
    ef = embedding_functions.SentenceTransformerEmbeddingFunction(model_name=EMBEDDING_MODEL)
    # create or get collection with embedding function
    try:
        collection = client.get_collection(name)
    except Exception:
        collection = client.create_collection(name, embedding_function=ef)
    return collection

def store_style(prompt_text: str, metadata: Optional[Dict[str, Any]] = None, id: Optional[str] = None):
    col = get_collection()
    if metadata is None:
        metadata = {}
    doc_id = id or f"style_{int(os.times()[4]*1000)}"
    col.add(documents=[prompt_text], metadatas=[metadata], ids=[doc_id])
    # Persist
    client = get_chroma_client()
    client.persist()
    return doc_id

def query_similar(prompt_text: str, n_results: int = 3) -> List[Dict[str, Any]]:
    col = get_collection()
    results = col.query(query_texts=[prompt_text], n_results=n_results)
    # results schema: {"ids":[[...] ], "distances":[[...] ], "metadatas":[[...] ], "documents":[[...] ]}
    res = []
    if results and results.get("ids"):
        for i in range(len(results["ids"][0])):
            res.append({
                "id": results["ids"][0][i],
                "doc": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "distance": results["distances"][0][i] if results.get("distances") else None
            })
    return res
