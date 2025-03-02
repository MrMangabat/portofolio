#backend/api_gateway/src/config/dependencies.py
from .config_top_level import api_gateway_top_level_configs
# from .config_low_level import api_gateway_low_level_configs  # If needed

from .config_combined_settings import CombinedSettings

def get_api_gateway_settings() -> CombinedSettings:
    return CombinedSettings(
        top=api_gateway_top_level_configs,
        # low=api_gateway_low_level_configs
    )
