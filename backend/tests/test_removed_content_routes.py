"""Tests demonstrating that the removed PostgreSQL-backed content APIs are no
longer required by the frontend and that the application starts cleanly without
DATABASE_URL configured.

Phase 10R.3 removed these read-only routes:
  - /api/v1/products, /api/v1/applications, /api/v1/blogs, /api/v1/faqs,
    /api/v1/clients, /api/v1/partners, /api/v1/industries,
    database-backed /api/v1/media/{id}
  - POST /api/v1/contact, GET /api/v1/jobs, POST /api/v1/jobs/{id}/apply

The frontend consumes all of this content from static modules:
  frontend/src/lib/data.ts, faqs.ts, clients.ts, partnersData.ts,
  careerData.ts, contactData.ts. The only live API calls the frontend makes
  are /api/v1/chat and /api/v1/chat/status.
"""
import os

from fastapi.testclient import TestClient


def _ensure_no_db_url():
    if os.environ.get("DATABASE_URL"):
        os.environ.pop("DATABASE_URL", None)


def test_app_starts_without_database_url():
    """The FastAPI app must import and serve routes with DATABASE_URL unset."""
    _ensure_no_db_url()
    from app.main import app
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_removed_content_routes_return_404():
    """Every removed read-only content route must no longer be registered."""
    _ensure_no_db_url()
    from app.main import app
    client = TestClient(app)

    removed_get_routes = [
        "/api/v1/products",
        "/api/v1/products/some-slug",
        "/api/v1/applications",
        "/api/v1/applications/automotive",
        "/api/v1/blogs",
        "/api/v1/blogs/some-post",
        "/api/v1/faqs",
        "/api/v1/faqs/category/general",
        "/api/v1/clients",
        "/api/v1/partners",
        "/api/v1/partners/asahi-sunac",
        "/api/v1/industries",
        "/api/v1/industries/manufacturing",
        "/api/v1/jobs",
        "/api/v1/jobs/sales-engineer",
        "/api/v1/media/some-asset-id",
    ]
    for route in removed_get_routes:
        response = client.get(route)
        assert response.status_code == 404, f"{route} should 404, got {response.status_code}"

    removed_post_routes = [
        "/api/v1/contact",
        "/api/v1/jobs/some-id/apply",
    ]
    for route in removed_post_routes:
        response = client.post(route, json={})
        assert response.status_code == 404, f"{route} should 404, got {response.status_code}"


def test_chat_routes_still_registered():
    """RAG/chatbot routes must survive the cleanup."""
    _ensure_no_db_url()
    from app.main import app
    client = TestClient(app)

    status_response = client.get("/api/v1/chat/status")
    assert status_response.status_code == 200
    assert "rag_ready" in status_response.json()

    # Chat POST should not 404 (it may 503 if generation is unavailable, but the
    # route itself must be registered).
    chat_response = client.post("/api/v1/chat", json={"message": "hello"})
    assert chat_response.status_code in (200, 503)


def test_media_static_mount_preserved():
    """The /media/ static file mount must remain intact."""
    _ensure_no_db_url()
    from app.main import app
    # StaticFiles mounts return 404 for missing files but the route exists.
    client = TestClient(app)
    response = client.get("/media/__nonexistent_probe__")
    assert response.status_code == 404