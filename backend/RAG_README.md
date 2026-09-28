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
python -m app.rag.cli status
```

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

Retrieval performs dense vector search + sparse/BM25 search in Qdrant and fuses results.

## Troubleshooting

- Ensure `QDRANT_URL` and `QDRANT_API_KEY` are set.
- Ensure `GROQ_API_KEY` is set for generation.
- Ensure the company knowledge file exists at `backend/storage/knowledge/VR_Coatings_RAG_Monolithic_Knowledge_Base.txt`.
- Check backend logs for ingestion warnings such as OCR-needed pages.
