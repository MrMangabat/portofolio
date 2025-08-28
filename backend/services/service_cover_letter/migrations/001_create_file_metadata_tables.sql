-- File: migrations/001_create_file_metadata_tables.sql
/*
WHY: Extends existing PostgreSQL schema with structured file metadata following service architecture patterns
CONTRIBUTION: Establishes single source of truth for file data within service_cover_letter domain boundaries
HOW: Creates normalized tables with foreign key relationships following existing corrections table patterns
*/

-- Enable UUID extension (likely already exists from existing schema)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Core file metadata table following existing PostgreSQL model patterns
CREATE TABLE file_metadata (
    /*
    WHY: Centralizes common file attributes while supporting type-specific extensions, following service domain modeling
    CONTRIBUTION: Provides single source of truth for file data that integrates with existing MinIO UUID-based storage
    HOW: Uses CHECK constraints and indexes optimized for the existing FileUploads.vue → fileStore.js → API workflow
    */
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    filename VARCHAR(255) NOT NULL, -- Original filename from FileUploads.vue
    file_type VARCHAR(20) NOT NULL CHECK (file_type IN ('template', 'cv', 'application')),
    language VARCHAR(10) NOT NULL CHECK (language IN ('english', 'danish')),
    schema_version VARCHAR(10) DEFAULT '1.0' NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    -- Integration fields for existing MinIO workflow
    minio_bucket VARCHAR(50) NOT NULL, -- Links to existing cover-letters/cv/images buckets
    minio_filename VARCHAR(255) NOT NULL, -- UUID-based filename used in MinIO
    original_content_type VARCHAR(100), -- From FastAPI UploadFile.content_type
    file_size INTEGER, -- From existing FileItem structure
    
    -- Qdrant integration field
    qdrant_point_id UUID, -- Links to embedded_cover_letters collection point ID
    
    UNIQUE(minio_bucket, minio_filename) -- Prevent MinIO storage conflicts
);

-- Template-specific metadata extending file_metadata
CREATE TABLE template_metadata (
    /*
    WHY: Isolates template business logic from base file data, enabling jobtype-based filtering for LLM context
    CONTRIBUTION: Supports semantic search enhancement and template recommendation engine for cover letter generation
    HOW: Uses foreign key cascade to maintain consistency with MinIO file lifecycle managed by fileStore.js
    */
    file_id UUID PRIMARY KEY REFERENCES file_metadata(id) ON DELETE CASCADE,
    jobtype VARCHAR(100) NOT NULL, -- User-selected from dropdown populated by jobtypes table
    industry_sectors JSONB DEFAULT '[]'::jsonb, -- Multi-select industry tags
    template_subtype VARCHAR(50) DEFAULT 'cover_letter' CHECK (template_subtype IN ('cover_letter', 'application')),
    company_size_target VARCHAR(20) DEFAULT 'any' CHECK (company_size_target IN ('startup', 'mid', 'enterprise', 'any')),
    
    -- Semantic search optimization fields
    last_used_at TIMESTAMP, -- For usage-based ranking
    effectiveness_score FLOAT DEFAULT 0.0 -- Future ML feature
);

-- CV-specific metadata extending file_metadata
CREATE TABLE cv_metadata (
    /*
    WHY: Captures CV-specific attributes needed for role matching and experience filtering in cover letter context
    CONTRIBUTION: Enables future CV section extraction and drag-drop CV builder integration with template workflow
    HOW: Uses JSONB for flexible skill/role arrays while maintaining structured experience data for LLM prompts
    */
    file_id UUID PRIMARY KEY REFERENCES file_metadata(id) ON DELETE CASCADE,
    primary_roles JSONB DEFAULT '[]'::jsonb, -- Extracted or user-defined roles
    experience_years INTEGER CHECK (experience_years >= 0 AND experience_years <= 50),
    industries_mentioned JSONB DEFAULT '[]'::jsonb, -- Auto-extracted industry references
    skills_extracted JSONB DEFAULT '[]'::jsonb, -- Text extraction results for LLM context
    is_current_cv BOOLEAN DEFAULT FALSE, -- Primary CV flag for user workflow
    sections_extracted JSONB DEFAULT '{}'::jsonb, -- Future drag-drop CV builder data
    
    -- Processing status tracking
    extraction_completed BOOLEAN DEFAULT FALSE,
    extraction_error TEXT -- Error logging for failed text processing
);

-- Jobtype lookup table following existing corrections pattern
CREATE TABLE jobtypes (
    /*
    WHY: Maintains controlled vocabulary for jobtype dropdown in FileUploads.vue interface, similar to corrections management
    CONTRIBUTION: Ensures data consistency for template categorization and enables jobtype-based analytics
    HOW: Follows same pattern as existing corrections table with active lifecycle management
    */
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    category VARCHAR(50), -- Grouping for future UI organization
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT -- Human-readable description for UI
);

-- Industry lookup table for consistent categorization
CREATE TABLE industries (
    /*
    WHY: Provides standardized industry vocabulary for template and CV categorization
    CONTRIBUTION: Enables industry-based filtering in semantic search and market analysis capabilities
    HOW: Mirrors jobtypes structure for consistency with existing lookup table patterns
    */
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) UNIQUE NOT NULL,
    sector VARCHAR(50), -- Higher-level grouping
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    description TEXT
);

-- Performance indexes aligned with expected query patterns
CREATE INDEX idx_file_metadata_type_language ON file_metadata(file_type, language);
CREATE INDEX idx_file_metadata_created_at ON file_metadata(created_at DESC);
CREATE INDEX idx_file_metadata_minio_lookup ON file_metadata(minio_bucket, minio_filename);
CREATE INDEX idx_template_metadata_jobtype ON template_metadata(jobtype);
CREATE INDEX idx_template_metadata_subtype ON template_metadata(template_subtype);
CREATE INDEX idx_template_metadata_last_used ON template_metadata(last_used_at DESC);
CREATE INDEX idx_cv_metadata_current ON cv_metadata(is_current_cv) WHERE is_current_cv = TRUE;
CREATE INDEX idx_jobtypes_active_name ON jobtypes(is_active, name) WHERE is_active = TRUE;
CREATE INDEX idx_industries_active_name ON industries(is_active, name) WHERE is_active = TRUE;

-- Updated timestamp trigger for file_metadata
CREATE OR REPLACE FUNCTION update_file_metadata_timestamp()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

CREATE TRIGGER trigger_update_file_metadata_timestamp
    BEFORE UPDATE ON file_metadata
    FOR EACH ROW
    EXECUTE FUNCTION update_file_metadata_timestamp();

-- Seed data aligned with existing cover letter use cases
INSERT INTO jobtypes (name, category, is_active, description) VALUES
    ('data_scientist', 'analytics', TRUE, 'Data science and machine learning roles'),
    ('data_engineer', 'engineering', TRUE, 'Data engineering and pipeline development'),
    ('project_leader', 'management', TRUE, 'Project management and team leadership'),
    ('analyst', 'analytics', TRUE, 'Business and data analysis roles'),
    ('software_engineer', 'engineering', TRUE, 'Software development and engineering'),
    ('product_manager', 'management', TRUE, 'Product management and strategy'),
    ('consultant', 'advisory', TRUE, 'Consulting and advisory positions'),
    ('researcher', 'academic', TRUE, 'Research and academic positions');

INSERT INTO industries (name, sector, is_active, description) VALUES
    ('technology', 'tech', TRUE, 'Software, hardware, and technology companies'),
    ('finance', 'financial_services', TRUE, 'Banking, investment, and financial services'),
    ('healthcare', 'health', TRUE, 'Healthcare, pharmaceuticals, and medical devices'),
    ('consulting', 'professional_services', TRUE, 'Management and strategy consulting'),
    ('education', 'public_sector', TRUE, 'Educational institutions and training'),
    ('manufacturing', 'industrial', TRUE, 'Manufacturing and industrial companies'),
    ('retail', 'consumer', TRUE, 'Retail and consumer goods'),
    ('energy', 'utilities', TRUE, 'Energy, utilities, and environmental services');