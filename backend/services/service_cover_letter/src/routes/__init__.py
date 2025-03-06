# backend/services/service_cover_letter/src/routes/__init__.py

from fastapi import APIRouter
from src.routes.routes_corrections import router as corrections_router
from src.routes.routes_files import router as files_router
from src.routes.routes_joblistings import router as joblistings_router

router = APIRouter()

router.include_router(corrections_router, prefix="/corrections", tags=["Corrections"])
router.include_router(files_router, prefix="/files", tags=["Files"])
router.include_router(joblistings_router, prefix="/job_listings", tags=["Job Listings"])
