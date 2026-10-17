# AGENTS.md

## Environment

- Python project at `backend/`
- Frontend at `frontend/` (Next.js, built with `npm run build`)
- Conda environment: `web-env` (activate with `conda activate web-env`)
- Working directory for tests: `backend/`
- PostgreSQL is NOT running; `DATABASE_URL` is unset for tests
- Qdrant cloud: `37832e36-65aa-4fc2-817c-35e534ab5ddb.sa-east-1-0.aws.cloud.qdrant.io`, collection `vr_coatings_knowledge`

## Test Commands

All commands are run from the `backend/` directory (except frontend build).

### Fast unit tests (no OCR, no Qdrant, no embeddings)
```bash
conda run -n web-env python -m pytest tests/test_conversation_validation.py tests/test_chat_greeting.py tests/test_chat_general.py tests/test_chat_api_no_db.py tests/test_rag_conversation_service.py tests/test_rag_evidence_guard.py tests/test_rag_generation.py tests/test_domain_guard.py -v --timeout=60
```

### Moderate RAG tests (Qdrant + embeddings, no OCR)
```bash
conda run -n web-env python -m pytest tests/test_rag_phase8_1_context.py tests/test_rag_phase8.py tests/test_rag_phase9a.py tests/test_rag_phase9b.py tests/test_rag_phase9b_recovery.py tests/test_rag_phase9c2_batch1.py tests/test_rag_phase9c3_batch2.py tests/test_rag_phase9c4_table_reconstruction.py tests/test_rag_phase7_2_regression.py tests/test_rag_chat_endpoint.py tests/test_rag_api_routes.py -v --timeout=120
```

### OCR-heavy tests (slow, run individually)
```bash
conda run -n web-env python -m pytest tests/test_rag_phase9c6_barrel_pump.py -v --timeout=300
```

### Phase 10 evaluation (slow, 10+ min, real Qdrant + mock generation)
```bash
conda run -n web-env python -m evals.run_phase10
```

### Full backend test suite (20+ min, includes OCR tests)
```bash
conda run -n web-env python -m pytest tests/ -v --timeout=600 --ignore=tests/test_phase10_evaluation.py
```

### Frontend build
```bash
cd frontend && npm run build
```

### Lint and typecheck
```bash
cd backend && ruff check app/
cd backend && mypy app/ --ignore-missing-imports --explicit-package-bases
```
