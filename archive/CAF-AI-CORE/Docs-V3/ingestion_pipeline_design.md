## Ingestion Pipeline: File-to-Markdown Workflow

This document outlines a robust ingestion pipeline for converting diverse source files into clean Markdown (MD) files, preparing them for downstream chunking and embedding in your CAF-AI system.

---

### 1. Supported Source Formats

* **Office Documents**: `.docx`, `.pptx`, `.xlsx`
* **PDFs**: Text-based and scanned (OCR)
* **HTML/Markdown**: Existing `.html`, `.md` files
* **Plain Text**: `.txt` logs, transcripts, code files

### 2. Conversion Tools & Libraries

| Format   | Tool/Library                    | Notes                                         |
| -------- | ------------------------------- | --------------------------------------------- |
| DOCX     | `mammoth` (Python)              | Preserves headings, lists, tables             |
| PPTX     | `python-pptx` + custom exporter | Slide text + alt-text for images              |
| XLSX     | `openpyxl` / `pandas`           | Export sheets as tables or CSV → to MD tables |
| PDF text | `pdfminer.six`                  | Extracts text layout, requires cleanup        |
| PDF OCR  | `Tesseract` + `pytesseract`     | For scanned PDFs                              |
| HTML     | `BeautifulSoup` → `markdownify` | Converts tags to MD syntax                    |

### 3. File-normalization Workflow

```plaintext
[Source Files]
     |
     v
[Format Detector] -> identifies file type
     |
     v
[Converter Module]
     |
     v
[Pre-processor]
     |
     v
[Markdown Output] -> saved to `knowledge/published/*.md`

```

#### 3.1 Format Detector

* Inspect file extension and MIME type.
* For ambiguous extensions, read header bytes.

#### 3.2 Converter Module

* **DOCX**: Use `mammoth.convert_to_markdown()` → cleans paragraphs, headings, lists.
* **PPTX**: Iterate slides, extract `.text_frame.text` → prefix with `## Slide <n>`; extract image alt-text or annotate.
* **XLSX**: Read each sheet into DataFrame → `.to_markdown()` for simple tables.
* **PDF**: Try `pdfminer` for text; if empty, route through `pytesseract` OCR on rendered images.
* **HTML**: Strip scripts/styles → `markdownify.markdownify(html)`.

#### 3.3 Pre-processor

* **Clean Markdown**:

  * Remove duplicate blank lines.
  * Normalize headings to `##`/`###` levels.
  * Escape unsupported characters.
* **Front-matter** (optional): Add YAML metadata at the top:

  ```yaml
  ---
  source: original_filename.pdf
  ingested_at: 2025-05-26T02:00:00Z
  ---
  ```
* **Chunk hints**: Insert HTML comments to guide chunker, e.g.:

  ```markdown
  <!-- chunk-start: faq-question -->
  **Q:** What is TASI?
  <!-- chunk-end -->
  ```

### 4. Directory & Naming Conventions

* **Staging directory**: `knowledge/raw/` mirrors original paths.
* **Published MD**: `knowledge/published/{category}/{filename}.md`
* Use lowercase, hyphens for filenames.

### 5. Automation & Scheduling

* Implement as a Python script or Airflow DAG:

  1. **Watch** `knowledge/raw/` for new files.
  2. **Trigger** conversion task per file.
  3. **Validate** Markdown (lint and spellcheck).
  4. **Move** to `knowledge/published/` on success, or to `knowledge/errors/` on failure.
* Schedule hourly or event-driven via filesystem notifications.

### 6. Testing & Validation

* **Unit tests**: sample files for each format → compare against known MD outputs.
* **Integration tests**: end-to-end ingestion → chunking → embedding → retrieval sanity checks.
* **Linting**: use `remark` or `markdownlint` to enforce style.

### 7. Next Steps

1. Write converter functions per format with clear interfaces.
2. Build and test pre-processor cleanup routines.
3. Integrate into your ingestion pipeline and verify with sample datasets.

This workflow ensures reliable, consistent Markdown ingestion—setting you up for effective chunking and embedding downstream.
