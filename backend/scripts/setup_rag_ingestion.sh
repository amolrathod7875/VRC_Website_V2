#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BACKEND_DIR="$(dirname "$SCRIPT_DIR")"

echo "============================================================"
echo "RAG OCR Ingestion Environment Setup (web-env)"
echo "============================================================"
echo ""

echo "[1/3] Installing OCR dependencies into conda web-env"
conda run -n web-env python -m pip install --upgrade pip setuptools wheel
conda run -n web-env python -m pip install -r "$BACKEND_DIR/requirements-rag-ingestion.txt"

echo ""
echo "[2/3] Verifying environment"
conda run -n web-env python -m pip check

echo ""
echo "[3/3] Running OCR diagnostics"
cd "$BACKEND_DIR"
conda run -n web-env python -m app.rag.cli ocr-status

echo ""
echo "============================================================"
echo "Setup complete"
echo "============================================================"
echo ""
