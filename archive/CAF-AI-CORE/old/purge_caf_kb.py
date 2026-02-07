# Code/tools/purge_full_page_docs.py

import chromadb


def purge_full_page_docs(chroma_path="kb/caf-kb/chromadb"):
    client = chromadb.PersistentClient(path=chroma_path)
    collection = client.get_collection("caf_kb")

    print("🧹 Scanning for doc_ids ending in '_full_page'...")
    all_ids = collection.get()["ids"]
    to_delete = [doc_id for doc_id in all_ids if doc_id.endswith("_full_page")]

    print(f"⚠️ Found {len(to_delete)} documents to delete.")
    if not to_delete:
        return

    confirm = input("Type 'yes' to confirm deletion: ")
    if confirm.lower() == "yes":
        collection.delete(ids=to_delete)
        print("✅ Deleted.")
    else:
        print("❌ Cancelled.")


if __name__ == "__main__":
    purge_full_page_docs()
