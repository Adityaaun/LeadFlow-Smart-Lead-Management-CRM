from fastapi import APIRouter
from backend.app.api.leads import router as leads_router

api_router = APIRouter()
api_router.include_router(leads_router)
