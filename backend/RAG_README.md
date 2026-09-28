# VR Coatings Backend RAG

## Architecture

- FastAPI backend serves `POST /api/v1/chat`.
- RAG pipeline uses Qdrant Cloud for hybrid dense + BM25 retrieval.
- PDF catalogues are parsed fresh using PyMuPDF.
- Company master knowledge is parsed from `backend/storage/knowledge/VR_Coatings_RAG_Monolithic_Knowledge_Base.txt`.
- Generation uses a provider abstraction; default provider is Groq.

## Source hierarchy

- Catalogue PDF = highest authority for product technical info.
- Company master TXT = primary for company info.
- Existing website/database content = secondary.

## Environment variables

```env
QDRANT_URL=
QDRANT_API_KEY=
QDRANT_COLLECTION_NAME=vr_coatings_knowledge
RAG_DENSE_MODEL=BAAI/bge-small-en-v1.5
RAG_SPARSE_MODEL=Qdrant/bm25
RAG_DENSE_TOP_K=20
RAG_SPARSE_TOP_K=20
RAG_FINAL_TOP_K=8
RAG_RERANK_ENABLED=false
RAG_CATALOGUE_ROOT=/app/storage/catalogues
RAG_COMPANY_KB_PATH=/app/storage/knowledge/VR_Coatings_RAG_Monolithic_Knowledge_Base.txt
LLM_PROVIDER=groq
GROQ_API_KEY=
GROQ_MODEL=
```

## Qdrant setup

Use Qdrant Cloud. Do not add Qdrant to docker-compose.

## Groq setup

Set `GROQ_API_KEY` and `GROQ_MODEL` in the backend `.env`.

## Ingestion commands

```bash
python -m app.rag.cli ingest-all
python -m app.rag.cli ingest-catalogues
python -m app.rag.cli ingest-company
python -m app.rag.cli ingest-file "storage/catalogues/Panther.pdf"
python -m app.rag.cli inspect-file "storage/catalogues/Panther.pdf"
python -m app.rag.cli search "What is Tiger used for?"
python -m app.rag.cli status
```

## OCR ingestion

Scanned/image-only PDFs require OCR. Install ingestion dependencies:

**Linux/macOS (conda web-env recommended):**

```bash
conda run -n web-env python -m pip install -r backend/requirements-rag-ingestion.txt
```

**Windows PowerShell (conda web-env):**

```powershell
conda run -n web-env python -m pip install -r backend\requirements-rag-ingestion.txt
```

**Windows PowerShell (manual venv):**

```powershell
python -m venv backend\.venv-rag-ingestion
backend\.venv-rag-ingestion\Scripts\Activate.ps1
python -m pip install --upgrade pip setuptools wheel
python -m pip install -r backend\requirements-rag-ingestion.txt
python -m pip check
```

The production web API does NOT need OCR packages if catalogue ingestion is performed separately.

## OCR model cache

PaddleOCR downloads pretrained models on first use. Models are cached at:

- Linux/macOS: `~/.paddlex/official_models/`
- Windows: `%USERPROFILE%\.paddlex\official_models\`

Models downloaded:
- `PP-LCNet_x1_0_doc_ori` — document orientation
- `UVDoc` — document unwarping
- `PP-LCNet_x1_0_textline_ori` — textline detection
- `PP-OCRv6_medium_det` — text detection
- `PP-OCRv6_medium_rec` — text recognition

Delete the cache directory to force re-download.

## OCR confidence

OCR results include two confidence metrics:
- `text_confidence`: average over all recognized text blocks
- `table_confidence`: average over numeric blocks only

A paragraph with imperfect OCR may still be usable. A technical numeric table requires stricter validation. If `table_confidence` drops below `0.9`, a `TABLE_CONFIDENCE_WARNING` is added to the page result.

## OCR performance

First-run initialization downloads models and may take 1-2 minutes. Subsequent runs are faster. Typical per-page processing time on CPU is 30-60 seconds depending on image resolution.

## Scanned PDF handling

If a PDF page has insufficient extractable text, the system falls back to OCR using PaddleOCR/PP-Structure. OCR results are cached under `backend/.rag_cache/ocr/` keyed by document SHA-256.

## Installing ingestion dependencies

```bash
pip install -r backend/requirements-rag-ingestion.txt
```

## OCR cache

OCR results are cached locally to avoid repeated computation. The cache key uses the document SHA-256 and page number. Add `backend/.rag_cache/` to `.gitignore`.

## Table confidence

Technical tables are parsed with strict column alignment. If row length does not match the number of models, the table is not silently parsed. Model-level chunks are generated only when table reconstruction is confident.

## BM25 sparse vectors

Sparse embeddings use FastEmbed `SparseTextEmbedding` with `Qdrant/bm25`. This enables exact matching for technical identifiers such as model numbers and pressure values.

## Hybrid RRF verification

Hybrid retrieval uses Qdrant's `Prefetch` + `Fusion.RRF` query API. Dense and sparse results are fused server-side, not manually concatenated.

## Incremental update behavior

Ingestion calculates SHA-256 for every source document. If the hash matches the existing `rag_documents` record, the document is skipped. If the hash changes, only that document is reindexed.

## How to add a new catalogue

Place the PDF in `backend/storage/catalogues/` and run:

```bash
python -m app.rag.cli ingest-file "storage/catalogues/NewProduct.pdf"
```

## How to update an existing catalogue

Replace the PDF and run:

```bash
python -m app.rag.cli ingest-all
```

Only the changed catalogue will be reindexed.

## Company TXT ingestion

```bash
python -m app.rag.cli ingest-company
```

## Hybrid retrieval

Retrieval performs dense vector search + sparse/BM25 search in Qdrant and fuses results using RRF.

## Troubleshooting

- Ensure `QDRANT_URL` and `QDRANT_API_KEY` are set.
- Ensure `GROQ_API_KEY` is set for generation.
- Ensure the company knowledge file exists at `backend/storage/knowledge/VR_Coatings_RAG_Monolithic_Knowledge_Base.txt`.
- For scanned PDFs, install `backend/requirements-rag-ingestion.txt`.
- Check backend logs for ingestion warnings such as OCR-needed pages.
