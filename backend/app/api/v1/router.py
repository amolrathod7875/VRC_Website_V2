from fastapi import APIRouter

from app.api.v1.endpoints import chat

api_router = APIRouter()

# NOTE: The PostgreSQL-backed website content APIs were removed in Phase 10R.3:
#   - /api/v1/products, /api/v1/applications, /api/v1/blogs, /api/v1/faqs,
#     /api/v1/clients, /api/v1/partners, /api/v1/industries,
#     database-backed /api/v1/media/{id}
#   - POST /api/v1/contact, GET /api/v1/jobs, POST /api/v1/jobs/{id}/apply
# Their content is served exclusively from static frontend data modules
# (frontend/src/lib/data.ts, faqs.ts, clients.ts, partnersData.ts,
# careerData.ts, contactData.ts). The /media/ static file mount in
# app/main.py remains intact for catalogues, images, videos and PDFs.
#
# Contact-form and career-application submission were removed from the
# backend because the frontend forms (InquiryForm) are already client-side
# stubs that do not call the backend. A PostgreSQL-free submission-storage
# solution is deferred to Phase 10R.4 - see the Phase 10R.3 final report.
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])