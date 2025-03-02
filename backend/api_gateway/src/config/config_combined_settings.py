#backend/api_gateway/src/config/config_combined_settings.py
from pydantic import BaseModel
from .config_top_level import TopLevelSettings
#from .config_low_level import LowLevelSettings  # Example future file

class CombinedSettings(BaseModel):
    top: TopLevelSettings
#    low: LowLevelSettings  # Optional today, ready for future use
