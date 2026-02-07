import json
import os
import re
import sys

from openai import OpenAI

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


import json
import re


def clean_and_extract_json(content: str) -> str:
    """
    Extract the JSON array from the raw model output and clean common issues.
    """
    # Keep only the content between the first '[' and last ']'
    try:
        start = content.find("[")
        end = content.rfind("]")
        if start == -1 or end == -1 or end <= start:
            print("No valid JSON array found in content")
            return None
        content = content[start : end + 1]

        # Fix missing commas between objects: '}{' -> '}, {'
        content = re.sub(r"\}\s*\{", r"}, {", content)

        # Remove trailing commas before closing brackets
        content = re.sub(r",\s*\](?!,)", "]", content)

        # Remove any non-JSON safe control chars
        content = content.replace("\u0000", " ")

        # Basic validation - try to parse it
        json.loads(content)
        return content
    except Exception as e:
        print(f"Failed to clean/validate JSON: {str(e)}")
        return None


def agentic_chunk_markdown(md_text, model="gpt-3.5-turbo", max_chunk_words=250):
    prompt = f"""
You are a reliable document chunker for an AI knowledge system.

TASK:
1. Read the Markdown below.
2. Break it into self-contained chunks (≤ {max_chunk_words} words each).
3. For each chunk, output an object with exactly these string fields:
   • "chunk"        – the chunk text
   • "title"        – a concise section heading
   • "summary"      – 1–2-sentence overview
   • "keywords"     – comma-separated terms, including ALL high-level topics/entities of the parent document (e.g. always include “F24”, “IMU” if the doc is about those)
   • "section_type" – one of: intro, faq, procedure, product, legal, story, etc.

OUTPUT FORMAT (must follow *exactly*):
- A single JSON array:  
  [
    {{ …object1… }},
    {{ …object2… }},
    …
  ]
- No code fences, no Markdown, no comments.
- No trailing commas.
- All values quoted; the array must start with `[` and end with `]`.

MARKDOWN INPUT:
---
{md_text}
---

END. Return ONLY the JSON array. Nothing else.
"""

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.1,
        max_tokens=4096,
    )

    raw = response.choices[0].message.content
    cleaned = clean_and_extract_json(raw)
    try:
        data = json.loads(cleaned)
        if isinstance(data, list):
            return data
        else:
            # If model returned single object, wrap it
            return [data]
    except json.JSONDecodeError as e:
        print(f"JSON parse failed: {e}")
        print("Cleaned content:\n", cleaned)
        return None


def agentic_chunk_document(md_text, published_filepath):
    """
    Takes markdown text and the path to the published file.
    Returns a list of chunk dicts, each with doc_id, parent_id, and chunk_idx.
    Returns None if chunking fails.
    """
    chunks = agentic_chunk_markdown(md_text)
    if chunks is None:
        print(f"Failed to chunk document {published_filepath}")
        return None

    base = os.path.splitext(os.path.basename(published_filepath))[0]
    for idx, chunk in enumerate(chunks):
        chunk["doc_id"] = f"{base}_c{idx}"
        chunk["parent_id"] = base
        chunk["chunk_idx"] = idx
    return chunks
