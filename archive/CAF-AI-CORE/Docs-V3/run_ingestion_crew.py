# run_ingestion_crew.py

import argparse
from pathlib import Path
from datetime import datetime
from chunker import chunk_text
from enrich import enrich_metadata
from metadata_classifier_agent import MetadataClassifierAgent
from push_to_chroma import push_chunks

def load_md(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def log(msg):
    print(f"[INGEST] {msg}")

def main():
    parser = argparse.ArgumentParser(
        description="CrewAI Markdown Ingestor: chunk/classify/enrich/push markdown knowledge files"
    )
    parser.add_argument("--file", required=True, help="Markdown file to ingest")
    parser.add_argument("--overwrite", action="store_true", help="Overwrite existing chunks in ChromaDB")
    parser.add_argument("--mode", default="sliding", choices=["sliding", "basic"], help="Chunking mode")
    parser.add_argument("--max-length", type=int, default=500, help="Max tokens/words per chunk")
    parser.add_argument("--overlap", type=int, default=50, help="Token overlap for sliding mode")
    args = parser.parse_args()

    path = Path(args.file)
    if not path.exists() or path.suffix.lower() != ".md":
        raise ValueError("File must exist and have .md extension")

    log(f"Loading {path.name}")
    text = load_md(path)
    retrieved_at = datetime.today().strftime("%Y-%m-%d")
    classifier = MetadataClassifierAgent()

    log(f"Chunking ({args.mode}) ...")
    chunks = chunk_text(text, max_length=args.max_length, mode=args.mode, overlap=args.overlap)
    log(f"Generated {len(chunks)} chunks")

    enriched_chunks = []
    topics = set()
    regions = set()
    doc_ids = []

    for idx, chunk in enumerate(chunks):
        doc_id = f"{path.stem}_c{idx}"

        try:
            meta = classifier.classify(chunk)
        except Exception as e:
            log(f"[!] LLM classify failed: {e}")
            meta = {"topic": "unknown", "region": "unknown", "year": "unknown", "type": "unknown"}

        topics.add(meta.get("topic", "unknown"))
        regions.add(meta.get("region", "unknown"))
        doc_ids.append(doc_id)

        enriched = enrich_metadata(
            chunk_text=chunk,
            topic=meta.get("topic", "unknown"),
            region=meta.get("region", "unknown"),
            doc_id=doc_id,
            retrieved_at=retrieved_at,
            source=str(path.name),
            created_by="crew_md_ingestor",
        )
        enriched_chunks.append(enriched)

    if args.overwrite:
        log("Overwrite enabled: Would remove existing chunks (not implemented yet)")
        # TODO: Implement ChromaDB delete logic for these doc_ids

    log("Pushing to ChromaDB...")
    push_chunks(enriched_chunks)

    log("Ingestion complete.")
    print("\n==== Summary ====")
    print(f"File: {path.name}")
    print(f"Chunks: {len(enriched_chunks)}")
    print(f"Topics: {', '.join(topics)}")
    print(f"Regions: {', '.join(regions)}")
    print("=================")

if __name__ == "__main__":
    main()
