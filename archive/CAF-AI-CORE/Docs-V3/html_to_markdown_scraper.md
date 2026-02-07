## HTML-to-Markdown Scraper Pipeline

This document describes how to integrate a Markdown conversion step into your web scraping pipeline, ensuring that every crawled page outputs clean `.md` files with headings, lists, links, and more.

---

### 1. Dependencies

Install the following Python packages:

```bash
pip install scrapy markdownify pyyaml
```

* **Scrapy**: framework for scalable web crawling.
* **markdownify**: converts HTML to Markdown, preserving headings, lists, tables, and links.
* **PyYAML**: for writing YAML front-matter metadata.

---

### 2. Pipeline Implementation

Create or update your Scrapy item pipeline (`pipelines.py`) with the following class:

```python
# pipelines.py

from markdownify import markdownify as md
import os
import hashlib
import yaml
from datetime import datetime

class MarkdownPipeline:
    def process_item(self, item, spider):
        # Raw HTML from the spider
        html = item.get("html")

        # 1) Convert HTML to Markdown
        md_text = md(
            html,
            heading_style="ATX",      # Use '##' for <h2>, '###' for <h3>
            bullets="*",              # Use '*' for <ul> bullets
            strip=["script", "style"] # Remove scripts and styles
        )

        # 2) Add YAML front-matter
        fetched = datetime.utcnow().isoformat() + "Z"
        front = {
            "source_url": item.get("url"),
            "fetched_at": fetched,
        }
        full_md = f"---\n{yaml.dump(front)}---\n\n{md_text}"

        # 3) Write to knowledge/raw as .md
        slug = hashlib.sha1(item.get("url").encode()).hexdigest()[:8]
        os.makedirs("knowledge/raw", exist_ok=True)
        path = f"knowledge/raw/{slug}.md"
        with open(path, "w", encoding="utf-8") as f:
            f.write(full_md)

        return item
```

#### Usage in Scrapy Settings

In your `settings.py`, enable the pipeline:

```python
ITEM_PIPELINES = {
    'myproject.pipelines.MarkdownPipeline': 300,
}
```

Adjust the priority (`300`) as needed relative to other pipelines.

---

### 3. Workflow Overview

1. **Spider** crawls URLs and yields items with `html` and `url` fields.
2. **MarkdownPipeline** converts the HTML to Markdown, adds metadata, and saves a uniquely named `.md` file.
3. **knowledge/raw/** directory populates with ready-to-chunk Markdown files.

---

### 4. Customization Tips

* **Cleaning before conversion**: Use BeautifulSoup in `process_item` to remove unwanted sections (e.g., banners or ads) before `md()`.
* **Table handling**: If your pages include complex tables, consider exporting via `pandas.read_html()` and `.to_markdown()` for better formatting.
* **Image assets**: To embed images, extract `<img>` tags, download assets, and update Markdown links accordingly.

---

You can integrate this pipeline into your existing scraper and have it automatically produce high-quality Markdown files for downstream chunking and embedding. Let me know when you’re ready to test or need further enhancements!
