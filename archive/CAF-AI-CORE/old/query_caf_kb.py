#!/usr/bin/env python3
import argparse
import os
import re
import sys
from typing import Dict, List, Optional, Tuple, Union

import chromadb
from chromadb.utils import embedding_functions
from dotenv import load_dotenv


def preprocess_query(query: str) -> str:
    """Preprocess the query for better matching.

    Args:
        query: Raw query string

    Returns:
        Processed query string
    """
    # Normalize whitespace and case
    query = " ".join(query.lower().split())

    # Remove any special characters except alphanumeric and spaces
    query = re.sub(r"[^a-z0-9\s]", " ", query)

    # Normalize whitespace again after special char removal
    query = " ".join(query.split())

    return query


def calculate_relevance(doc: str, meta: Dict, dist: float) -> float:
    """Calculate combined relevance score using multiple factors.

    Args:
        doc: Document text
        meta: Document metadata
        dist: ChromaDB distance score

    Returns:
        Combined relevance score (lower is better)
    """
    # Start with the ChromaDB distance score
    score = dist

    # Boost by section type
    section_type = meta.get("section_type", "")
    section_boosts = {
        "intro": 0.9,     # Introductions are good context
        "procedure": 0.8, # Procedures are very relevant
        "faq": 0.85,     # FAQs are quite relevant
        "product": 0.95,  # Product info is somewhat relevant
    }
    score *= section_boosts.get(section_type, 1.0)

    # Boost if part of a guide
    parent_id = meta.get("parent_id", "")
    if "guide" in parent_id:
        score *= 0.9

    # Consider chunk order in guides
    chunk_idx = meta.get("chunk_idx", 999)
    if chunk_idx == 0:  # Intro chunks are important
        score *= 0.95

    return score


def process_results(
    docs: List[str], metas: List[Dict], dists: List[float]
) -> List[Tuple[str, Dict, float]]:
    """Process and sort search results by relevance.

    Args:
        docs: List of document texts
        metas: List of document metadata
        dists: List of ChromaDB distance scores

    Returns:
        List of (doc, meta, score) tuples, sorted by relevance
    """
    scored_results = [
        (doc, meta, calculate_relevance(doc, meta, dist))
        for doc, meta, dist in zip(docs, metas, dists)
    ]
    return sorted(scored_results, key=lambda x: x[2])


def format_result(doc: str, meta: Dict, score: float) -> str:
    """Format a single result for display.

    Args:
        doc: Document text
        meta: Document metadata
        score: Relevance score

    Returns:
        Formatted result string
    """
    # Get title if available, otherwise use doc_id
    title = meta.get("title", meta.get("doc_id", "Unknown"))

    # Clean and truncate the document text
    text = re.sub(r"\s+", " ", doc).strip()
    if len(text) > 300:
        text = text[:297] + "..."

    return f"[{title}]\n{text}\nScore: {score:.4f} | Doc ID: {meta.get('doc_id')}\n{'-' * 40}"


def load_env() -> Tuple[str, str, str]:
    """Load and validate required environment variables.

    Returns:
        Tuple of (api_key, db_path, collection_name)

    Raises:
        SystemExit: If required environment variables are missing
    """
    load_dotenv()
    try:
        api_key = os.environ["OPENAI_API_KEY"]
        db_path = os.environ["CHROMA_DB_PATH"]
        coll_name = os.environ["CHROMA_COLLECTION"]
    except KeyError as e:
        print(f"Missing environment variable: {e}")
        sys.exit(1)
    return api_key, db_path, coll_name


def get_collection():
    """Get the ChromaDB collection with OpenAI embeddings.

    Returns:
        ChromaDB collection object
    """
    embedder = embedding_functions.OpenAIEmbeddingFunction(
        api_key=os.environ["OPENAI_API_KEY"], model_name="text-embedding-ada-002"
    )
    client = chromadb.PersistentClient(path=os.environ["CHROMA_DB_PATH"])
    return client.get_collection(
        os.environ["CHROMA_COLLECTION"], embedding_function=embedder
    )


def main():
    """Main function to query the knowledge base."""
    # Load environment and get collection
    load_env()
    collection = get_collection()

    # Parse command line arguments
    parser = argparse.ArgumentParser(
        description="Query tool for the CAF knowledge base"
    )
    parser.add_argument("--query", required=True, help="Text to search for")
    parser.add_argument("--limit", type=int, default=3, help="Max number of results")
    parser.add_argument(
        "--metadata",
        help="Optional metadata filter in key:value format (e.g. section_type:faq)",
    )
    parser.add_argument(
        "--min-score",
        type=float,
        default=1.85,  # Most relevant results seem to be under 1.85
        help="Maximum distance score to include (lower is better)",
    )
    parser.add_argument(
        "--parent",
        help="Filter by parent_id (e.g. f24_guide)",
    )
    parser.add_argument(
        "--section",
        choices=["intro", "procedure", "product", "faq"],
        help="Filter by section type",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show detailed debug information",
    )
    args = parser.parse_args()

    # Preprocess the query
    processed_query = preprocess_query(args.query)

    # Build metadata filters
    where = {}
    filters = []
    if args.parent:
        filters.append({"parent_id": args.parent})
    if args.section:
        filters.append({"section_type": args.section})
    
    if filters:
        if len(filters) == 1:
            where = filters[0]
        else:
            where = {"$and": filters}

    # Perform the query
    query_args = {
        "query_texts": [processed_query],
        "n_results": args.limit * 2,  # Get more results for post-processing
        "include": ["documents", "metadatas", "distances"],
    }

    # Only add where filter if we have metadata filters
    if where:
        query_args["where"] = where

    results = collection.query(**query_args)

    # Extract results
    docs = results.get("documents", [[]])[0]
    metas = results.get("metadatas", [[]])[0]
    dists = results.get("distances", [[]])[0]

    if not docs:
        print("No results found.")
        return

    # Process and sort results
    scored_results = process_results(docs, metas, dists)

    print(f"🔍 Query: {args.query}")
    print(f"Processed query: {processed_query}\n")
    
    if args.debug:
        print("Raw results (showing first 5):")
        for doc, meta, score in scored_results[:5]:
            print(f"Score: {score:.4f} | Doc ID: {meta.get('doc_id')}")
            print(f"Title: {meta.get('title', 'No title')}")
            print("Content preview:")
            preview = re.sub(r'\s+', ' ', doc).strip()[:200]
            print(f"{preview}...")
            print("-" * 80)

    # Filter by score and limit
    final_results = [r for r in scored_results if r[2] <= args.min_score][: args.limit]

    print(f"\nResults after filtering (min_score={args.min_score}):\n")

    if not final_results:
        print("No results met the minimum score threshold.")
        return

    for doc, meta, score in final_results:
        print(format_result(doc, meta, score))


if __name__ == "__main__":
    main()
