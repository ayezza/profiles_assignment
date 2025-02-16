import logging
from typing import List
from models.profile import Profile

logger = logging.getLogger(__name__)

class ProfileService:
    def __init__(self):
        # ...existing code...

    async def get_filtered_profiles(
        self,
        min_connections: int,
        min_recommendations: int,
        max_profiles: int
    ) -> List[Profile]:
        logger.debug(f"Filtering profiles with parameters: min_connections={min_connections}, "
                    f"min_recommendations={min_recommendations}, max_profiles={max_profiles}")
        
        filtered_profiles = [
            profile for profile in self.profiles
            if profile.number_of_connections >= min_connections
            and profile.number_of_recommendations >= min_recommendations
        ]

        # Trier et limiter le nombre de profils
        filtered_profiles.sort(key=lambda p: (-p.number_of_connections, -p.number_of_recommendations))
        return filtered_profiles[:max_profiles]
