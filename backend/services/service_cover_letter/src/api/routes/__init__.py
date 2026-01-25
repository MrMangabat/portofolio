# backend/services/service_cover_letter/src/api/routes/__init__.py

from fastapi import APIRouter
from src.api.routes.routes_corrections import router as corrections_router
from src.api.routes.routes_files import router as files_router
from src.api.routes.routes_joblistings import router as joblistings_router
from src.api.routes.routes_embedding_file_service import router as embedding_router
from src.api.routes.routes_agent import router as agent_router

router = APIRouter()

router.include_router(corrections_router, prefix="/corrections", tags=["Corrections"])
router.include_router(files_router, prefix="/files", tags=["Files"])
router.include_router(joblistings_router, prefix="/job_listings", tags=["Job Listings"])
router.include_router(embedding_router, prefix="/cover_letter_embeddings", tags=["Embedding"])
router.include_router(agent_router, prefix="/agent", tags=["Agent"])
