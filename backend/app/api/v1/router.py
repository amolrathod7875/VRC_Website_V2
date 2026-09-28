from fastapi import APIRouter
from app.api.v1.endpoints import products, applications, blogs, faqs, careers, contact, clients, partners, industries, media, chat

api_router = APIRouter()

api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(applications.router, prefix="/applications", tags=["applications"])
api_router.include_router(blogs.router, prefix="/blogs", tags=["blogs"])
api_router.include_router(faqs.router, prefix="/faqs", tags=["faqs"])
api_router.include_router(careers.router, prefix="/jobs", tags=["careers"])
api_router.include_router(contact.router, prefix="/contact", tags=["contact"])
api_router.include_router(clients.router, prefix="/clients", tags=["clients"])
api_router.include_router(partners.router, prefix="/partners", tags=["partners"])
api_router.include_router(industries.router, prefix="/industries", tags=["industries"])
api_router.include_router(media.router, prefix="/media", tags=["media"])
api_router.include_router(chat.router, prefix="/chat", tags=["chat"])
