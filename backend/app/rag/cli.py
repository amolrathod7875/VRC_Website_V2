import argparse
import asyncio
import logging
from pathlib import Path
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from app.core.database import Base
from app.rag.ingestion.ingestion_service import IngestionService
from app.rag.embeddings.dense import DenseEmbeddingService
from app.rag.embeddings.sparse import SparseEmbeddingService
from app.rag.vectorstore.qdrant_store import QdrantStore
from app.rag.config import rag_settings

logger = logging.getLogger(__name__)


def get_session() -> AsyncSession:
    engine = create_async_engine(rag_settings.DATABASE_URL, echo=False, future=True)
    session_factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    return session_factory()


async def _ingest_catalogue(file_path: str) -> None:
    async with get_session() as db:
        qdrant = QdrantStore()
        await qdrant.ensure_collection()
        service = IngestionService(db=db, qdrant_store=qdrant, dense=DenseEmbeddingService(), sparse=SparseEmbeddingService())
        result = await service.ingest_catalogue(Path(file_path))
        logger.info(result)


async def _ingest_company(file_path: str) -> None:
    async with get_session() as db:
        qdrant = QdrantStore()
        await qdrant.ensure_collection()
        service = IngestionService(db=db, qdrant_store=qdrant, dense=DenseEmbeddingService(), sparse=SparseEmbeddingService())
        result = await service.ingest_company(Path(file_path))
        logger.info(result)


def main() -> None:
    parser = argparse.ArgumentParser(description="VR Coatings RAG ingestion CLI")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("ingest-all", help="Ingest catalogues and company master")

    catalogue_parser = subparsers.add_parser("ingest-catalogues", help="Ingest all catalogues")
    catalogue_parser.add_argument("path", nargs="?", default=rag_settings.RAG_CATALOGUE_ROOT)

    company_parser = subparsers.add_parser("ingest-company", help="Ingest company master")
    company_parser.add_argument("path", nargs="?", default=rag_settings.RAG_COMPANY_KB_PATH)

    file_parser = subparsers.add_parser("ingest-file", help="Ingest a single file")
    file_parser.add_argument("path", help="Path to PDF or TXT file")

    subparsers.add_parser("status", help="Show ingestion status")

    args = parser.parse_args()
    if args.command == "ingest-all":
        asyncio.run(_ingest_catalogue(rag_settings.RAG_CATALOGUE_ROOT))
        asyncio.run(_ingest_company(rag_settings.RAG_COMPANY_KB_PATH))
    elif args.command == "ingest-catalogues":
        asyncio.run(_ingest_catalogue(args.path))
    elif args.command == "ingest-company":
        asyncio.run(_ingest_company(args.path))
    elif args.command == "ingest-file":
        path = Path(args.path)
        if path.suffix.lower() == ".pdf":
            asyncio.run(_ingest_catalogue(args.path))
        else:
            asyncio.run(_ingest_company(args.path))
    elif args.command == "status":
        print("Status command not implemented in CLI yet.")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
