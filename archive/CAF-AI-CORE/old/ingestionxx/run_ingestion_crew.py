import json
import logging
import os
import sys
from datetime import datetime

import yaml
from chunker_agentic import agentic_chunk_document  # Make sure this is importable!
from enrich import enrich_yaml_fields
from push_to_chroma import push_chunks

# Directories
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_DIR = os.path.join(BASE_DIR, "..", "logs")  # Code/logs
CHUNKS_DIR = os.path.join(BASE_DIR, "..", "knowledge", "published", "chunks")
APPROVED_DIR = os.path.join(BASE_DIR, "..", "knowledge", "approved")


# Configure simple logging
def setup_logging():
    """
    Simple logging: log to Code/logs with timestamped filename and to console.
    """
    os.makedirs(LOG_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = os.path.join(LOG_DIR, f"ingestion_{timestamp}.log")

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s %(message)s",
        filename=log_file,
        filemode="a",
    )
    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setLevel(logging.INFO)
    console.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logging.getLogger().addHandler(console)

    logging.info(f"Logging started. File: {log_file}")
    return logging.getLogger(__name__)


logger = setup_logging()


def today():
    return datetime.now().strftime("%Y-%m-%d")


def parse_md_with_yaml(filepath):
    """
    Read a Markdown file and split into YAML front-matter and body.
    """
    logger.debug(f"Parsing markdown file with YAML: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    if content.startswith("---"):
        parts = content.split("---", 2)
        if len(parts) >= 3:
            meta = yaml.safe_load(parts[1]) or {}
            body = parts[2].lstrip()
            logger.debug(f"Parsed metadata keys: {list(meta.keys())}")
            return meta, body
    return {}, content


def build_yaml_block(meta):
    """
    Serialize a metadata dict to a YAML front-matter block.
    """
    logger.debug("Building YAML block from metadata")
    return (
        "---\n" + yaml.safe_dump(meta, sort_keys=False, allow_unicode=True) + "---\n\n"
    )


def approve_and_enrich(filepath):
    """
    Approve a file by parsing metadata, enriching it, and writing to published directory.
    """
    logger.info(f"[approve_and_enrich] Processing file: {filepath}")
    print(f"[approve_and_enrich] Processing: {filepath}")
    # Parse YAML and body
    meta, body = parse_md_with_yaml(filepath)
    # Enrich fields (meta + LLM, if needed)
    enriched_meta = enrich_yaml_fields(meta, body)
    # Update status and retrieved date
    enriched_meta["status"] = "published"
    enriched_meta["retrieved"] = today()
    # Write new .md to published/
    published_dir = "knowledge/published/"
    os.makedirs(published_dir, exist_ok=True)
    filename = os.path.basename(filepath)
    published_filepath = os.path.join(published_dir, filename)
    with open(published_filepath, "w", encoding="utf-8") as f:
        f.write(build_yaml_block(enriched_meta) + body)
    print(f"[approve_and_enrich] Saved: {published_filepath}")
    logger.info(f"[approve_and_enrich] Saved published file: {published_filepath}")
    return published_filepath


def chunk_document(published_filepath):
    """
    Chunk the published Markdown document using the agentic splitter.
    """
    logger.info(f"[chunk_document] Chunking file: {published_filepath}")
    print(f"[chunk_document] Chunking: {published_filepath}")
    # Load markdown (and meta if needed)
    with open(published_filepath, "r", encoding="utf-8") as f:
        md_text = f.read()
    # This should be your imported chunker (OpenAI agentic splitter)
    chunks = agentic_chunk_document(md_text, published_filepath)
    logger.info(f"[chunk_document] Generated {len(chunks)} chunks")
    return chunks


def write_chunks_json(chunk_list, output_path):
    """
    Write chunk list to a .json file for dev inspection.
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(chunk_list, f, ensure_ascii=False, indent=2)
    print(f"[write_chunks_json] Wrote {len(chunk_list)} chunks to: {output_path}")
    logger.info(f"[write_chunks_json] Wrote {len(chunk_list)} chunks to {output_path}")
    return output_path


def process_file(approved_filepath):
    """
    Full pipeline: approve/enrich, chunk, write JSON, and push to ChromaDB.
    """
    logger.info(f"[process_file] Starting processing: {approved_filepath}")
    try:
        published_filepath = approve_and_enrich(approved_filepath)
        chunk_list = chunk_document(published_filepath)
        base = os.path.splitext(os.path.basename(published_filepath))[0]
        chunk_json_path = os.path.join(CHUNKS_DIR, f"{base}.json")
        write_chunks_json(chunk_list, chunk_json_path)
        push_chunks(chunk_list)
        logger.info(
            f"[process_file] Successfully pushed {len(chunk_list)} chunks for {base}"
        )
        return {"filename": approved_filepath, "status": "ok"}
    except Exception as e:
        logger.error(
            f"[process_file] Error processing {approved_filepath}: {e}", exc_info=True
        )
        return {"filename": approved_filepath, "status": "error", "error": str(e)}


def main():
    """
    Entry point: process a single file or all approved files.
    """

    logger.info(f"[main] Args: {sys.argv}")
    if len(sys.argv) < 2:
        logger.error("Usage: python run_ingestion_crew.py <filename|--all>")
        print("Usage: python run_ingestion_crew.py <filename|--all>")
        return
    if sys.argv[1] == "--all":
        results = []
        os.makedirs(APPROVED_DIR, exist_ok=True)
        for fname in os.listdir(APPROVED_DIR):
            if fname.endswith(".md"):
                approved_filepath = os.path.join(APPROVED_DIR, fname)
                result = process_file(approved_filepath)
                results.append(result)
        # Print summary
        ok_count = sum(1 for r in results if r.get("status") == "ok")
        summary = f"Processed: {len(results)} files | Success: {ok_count}"
        logger.info(summary)
        print(summary)
    else:
        result = process_file(sys.argv[1])
        if result.get("status") != "ok":
            logger.error(f"Failed processing file: {result.get('filename')}")


if __name__ == "__main__":
    main()


# It will:
# Take a filename (or a folder for batch mode) from the approved
# check if verified: true and maybe other fields are correct in the yaml
# adds the retrieved date
# add more fields to the yaml
# add meta keywords
# add meta description

# Update the status: published
# Save to published/ with the same filename
# Log missing fields/issues

# python ingestion/run_process_inbox.py knowledge/inbox/imu_torino_sitepages.md
# python ingestion/run_process_inbox.py --all
