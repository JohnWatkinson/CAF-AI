# enrich.py

import os
import re

from openai import OpenAI

# --- LLM helper functions ---


def llm_generate_keywords(text, n=8):
    """Generate meta keywords using OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[llm_generate_keywords] No OpenAI API key found.")
        return []
    client = OpenAI(api_key=api_key)
    prompt = f"Extract {n} highly relevant keywords (comma separated, no hashtags) for search and metadata from the following text:\n\n{text}\n\nKeywords:"
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",  # Use gpt-4o if you want
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        keywords = resp.choices[0].message.content.strip()
        return [k.strip() for k in keywords.split(",") if k.strip()]
    except Exception as e:
        print(f"[llm_generate_keywords] LLM error: {e}")
        return []


def llm_generate_description(text, maxlen=160):
    """Generate a meta description for SEO/summary using OpenAI."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[llm_generate_description] No OpenAI API key found.")
        return ""
    client = OpenAI(api_key=api_key)
    prompt = f"Write a concise meta description (max {maxlen} characters) for the following text, suitable for SEO and page summary:\n\n{text}\n\nDescription:"
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        desc = resp.choices[0].message.content.strip()
        if len(desc) > maxlen:
            desc = desc[: maxlen - 3].rsplit(" ", 1)[0] + "..."
        return desc
    except Exception as e:
        print(f"[llm_generate_description] LLM error: {e}")
        return ""


# --- Extraction helper ---


def extract_explicit_fields(content):
    """Extract **field**: value lines into dict."""
    meta = {}
    pattern = r"\*\*(.+?)\*\*:\s*(.+)"
    for line in content.splitlines():
        m = re.match(pattern, line)
        if m:
            field = m.group(1).strip().lower().replace(" ", "_")
            value = m.group(2).strip()
            meta[field] = value
    return meta


def llm_generate_tags(text, n=6):
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("[llm_generate_tags] No OpenAI API key found.")
        return []
    client = OpenAI(api_key=api_key)
    prompt = f"Suggest {n} simple, broad tags for this document (1–2 words each, comma-separated, lowercase):\n\n{text}\n\nTags:"
    try:
        resp = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
        )
        tags = resp.choices[0].message.content.strip()
        return [t.strip() for t in tags.split(",") if t.strip()]
    except Exception as e:
        print(f"[llm_generate_tags] LLM error: {e}")
        return []


# --- Main enrichment function ---


def enrich_yaml_fields(yaml_meta, doc_content):
    # 1. Explicit field extraction (existing code)
    extracted = extract_explicit_fields(doc_content)
    for k, v in extracted.items():
        if k not in yaml_meta or not yaml_meta[k]:
            yaml_meta[k] = v

    # 2. LLM for soft meta only (existing code)
    if not yaml_meta.get("meta_keywords"):
        yaml_meta["meta_keywords"] = llm_generate_keywords(doc_content)
    if not yaml_meta.get("meta_description"):
        yaml_meta["meta_description"] = llm_generate_description(doc_content)

    # 3. TAGS: keep existing, add LLM if needed
    tags = yaml_meta.get("tags", [])
    if isinstance(tags, str):
        tags = [t.strip() for t in tags.split(",") if t.strip()]
    if not tags:
        tags = []
    # LLM: supplement with new ones, but don't duplicate existing
    new_tags = llm_generate_tags(doc_content)
    tags += [t for t in new_tags if t not in tags]
    yaml_meta["tags"] = tags

    # 4. Never invent/guess hard fields

    return yaml_meta
