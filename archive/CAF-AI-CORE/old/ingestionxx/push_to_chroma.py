# push_to_chroma.py
import datetime
import os

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv

load_dotenv()


def get_collection():
    embedder = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"], model_name="text-embedding-3-small"
    )
    client = chromadb.PersistentClient(path=os.environ["CHROMA_DB_PATH"])
    return client.get_or_create_collection(
        os.environ["CHROMA_COLLECTION"],
        embedding_function=embedder,
    )


def delete_doc_ids(doc_ids: list[str]):
    collection = get_collection()
    print(f"[🗑️] Deleting {len(doc_ids)} doc_ids from ChromaDB...")
    try:
        collection.delete(ids=doc_ids)
        print(f"[✓] Deleted {len(doc_ids)} doc_ids.")
    except Exception as e:
        print(f"[!] Error deleting doc_ids: {e}")


def flatten_metadata(meta):
    flat = {}
    for k, v in meta.items():
        if isinstance(v, list):
            flat[k] = ", ".join(str(x) for x in v)
        elif isinstance(v, dict):
            flat[k] = str(v)
        elif isinstance(v, (datetime.date, datetime.datetime)):
            flat[k] = v.isoformat()
        elif not isinstance(v, (str, int, float, bool)) and v is not None:
            flat[k] = str(v)
        else:
            flat[k] = v
    return flat


def push_chunks(chunk_list):
    collection = get_collection()
    docs = []
    metadatas = []
    ids = []
    for chunk in chunk_list:
        docs.append(chunk["chunk"])
        meta = {k: v for k, v in chunk.items() if k != "chunk"}
        metadatas.append(meta)
        ids.append(meta["doc_id"])
    collection.add(documents=docs, metadatas=metadatas, ids=ids)
    print(f"[push_chunks] Pushed {len(docs)} chunks to ChromaDB.")
