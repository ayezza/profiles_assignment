import logging
from fastapi import APIRouter, Query
from services.profile_service import ProfileService

router = APIRouter()
logger = logging.getLogger(__name__)

@router.get("/profiles/")
async def get_profiles(
    min_connections: int = Query(default=0, ge=0),
    min_recommendations: int = Query(default=0, ge=0),
    max_profiles: int = Query(default=100, ge=1)
):
    logger.info(f"Received parameters: min_connections={min_connections}, "
                f"min_recommendations={min_recommendations}, max_profiles={max_profiles}")
    
    service = ProfileService()
    results = await service.get_filtered_profiles(
        min_connections=min_connections,
        min_recommendations=min_recommendations,
        max_profiles=max_profiles
    )
    return results
