# backend/services/service_cover_letter/src/api/paths.py
"""
Route path constants for the cover letter service API.
"""

# Corrections endpoints
CORRECTIONS_PREFIX = "/corrections"

# Files endpoints
FILES_PREFIX = "/files"
FILES_UPLOAD = "/upload"

# Job listings endpoints
JOB_LISTINGS_PREFIX = "/job_listings"

# Embedding endpoints
EMBEDDING_PREFIX = "/cover_letter_embeddings"
EMBED_FILES = "/embed-files"

# Agent endpoints
AGENT_PREFIX = "/agent"
AGENT_GENERATE = "/generate"
AGENT_HEALTH = "/health"

# Research endpoints
RESEARCH_PREFIX = "/research"
RESEARCH_COMPANY_ALL = "/company/all"
RESEARCH_COMPANY_SINGLE = "/company/{officer}"
RESEARCH_COMPANY_CACHED = "/company/{company_name}/cached"
