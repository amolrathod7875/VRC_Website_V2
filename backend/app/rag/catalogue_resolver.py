from __future__ import annotations

import logging
import os
from typing import Any
from urllib.parse import quote

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.rag_document import RagDocument
from app.rag.product_identity import resolve_product_identity, get_canonical_slug
from app.core.config import settings

logger = logging.getLogger(__name__)

# Fallback mapping for catalogue filenames without product_slug in rag_documents.
# Keys are lowercase filename stems; values are canonical product slugs.
_FILENAME_FALLBACK: dict[str, str] = {
    "tiger.pdf": "tiger",
    "tiger_mini.pdf": "tiger-mini",
    "rhino.pdf": "rhino",
    "lion_catalogue.pdf": "lion",
    "elephant.pdf": "elephant",
    "hippo.pdf": "hippo",
    "diaphragm pump.pdf": "hippo",
    "leopard.pdf": "leopard",
    "electric_pump.pdf": "leopard",
    "cheetah.pdf": "cheetah",
    "filters.pdf": "filters",
    "automatic_gun.pdf": "automatic-spray-guns",
    "conventional guns_f.pdf": "kingfisher",
    "manual_guns.pdf": "manual-spray-guns",
    "dragon.pdf": "dragon",
    "polyurea.pdf": "polyurea",
    "tube varnish coating system.pdf": "tube-varnish-coating-system",
    "vrc mix (low - medium) pressure.pdf": "vrc-mix-low-medium-pressure",
    "vrc - mix hp.pdf": "vrc-mix-hp",
}


class CatalogueResolver:
    def __init__(self, db: AsyncSession, media_root: str | None = None, media_base_url: str | None = None) -> None:
        self.db = db
        self.media_root = media_root or settings.MEDIA_ROOT
        self.media_base_url = (media_base_url or settings.MEDIA_BASE_URL).rstrip("/")

    def _catalogues_dir(self) -> str:
        return os.path.join(self.media_root, "catalogues")

    def _safe_url(self, filename: str) -> str:
        return f"{self.media_base_url}/catalogues/{quote(filename, safe='')}"

    def _physical_path(self, filename: str) -> str:
        return os.path.join(self._catalogues_dir(), filename)

    def _file_exists(self, filename: str) -> bool:
        path = self._physical_path(filename)
        if not os.path.isfile(path):
            logger.warning("Catalogue file missing on disk", extra={"filename": filename, "path": path})
            return False
        return True

    async def _db_catalogues(self, product_slug: str) -> list[RagDocument]:
        slug = (product_slug or "").strip().lower()
        if not slug:
            return []

        result = await self.db.execute(
            select(RagDocument)
            .where(
                RagDocument.source_type == "catalogue",
                RagDocument.status == "indexed",
            )
            .order_by(RagDocument.document_name.asc())
        )
        all_docs = list(result.scalars().all())

        matched: list[RagDocument] = []
        for doc in all_docs:
            doc_slug = (doc.product_slug or "").strip().lower()
            doc_slugs = doc.product_slugs or []
            if isinstance(doc_slugs, str):
                try:
                    import json
                    doc_slugs = json.loads(doc_slugs)
                except Exception:
                    doc_slugs = []
            if slug == doc_slug:
                matched.append(doc)
                continue
            if slug in [s.lower() for s in doc_slugs if isinstance(s, str)]:
                matched.append(doc)
                continue
        return matched

    async def resolve(self, product_slug: str) -> list[dict[str, Any]]:
        slug = (product_slug or "").strip().lower()
        if not slug:
            return []

        docs = await self._db_catalogues(slug)
        if not docs:
            logger.info("No catalogue documents found in DB", extra={"product_slug": slug})
            return []

        catalogues: list[dict[str, Any]] = []
        seen_documents: set[str] = set()

        for doc in docs:
            document_name = doc.document_name or ""
            if not document_name:
                continue

            if document_name in seen_documents:
                continue
            seen_documents.add(document_name)

            if not self._file_exists(document_name):
                logger.warning(
                    "Skipping missing catalogue file",
                    extra={"product_slug": slug, "document_name": document_name},
                )
                continue

            catalogues.append(
                {
                    "product_slug": slug,
                    "product_name": self._product_name(slug),
                    "document_name": document_name,
                    "url": self._safe_url(document_name),
                }
            )

        return catalogues

    def _product_name(self, slug: str) -> str:
        return slug.replace("-", " ").replace("_", " ").title()

    async def resolve_from_message(self, message: str) -> tuple[str | None, list[dict[str, Any]]]:
        resolved = resolve_product_identity(message)
        if not resolved:
            return None, []

        canonical_slug = resolved[0]
        catalogues = await self.resolve(canonical_slug)
        return canonical_slug, catalogues
